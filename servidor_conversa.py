"""
servidor_conversa.py — cerebro + voz do robo, roda na JETSON 1.

Recebe da Jetson 2 (pelo cabo, TCP) a pergunta ja transcrita, gera a
resposta com o brain.py do repositorio Bitnet_TTS e devolve, frase por frase
e assim que cada uma fica pronta, o texto e o WAV falado (Piper):

    recebe  TEXTO  pergunta
    envia   TEXTO  frase 1     AUDIO  wav da frase 1
    envia   TEXTO  frase 2     AUDIO  wav da frase 2   ...
    envia   TEXTO  ""          (fim da resposta)

Falar texto literal (sem cerebro): ao conectar, o servidor manda um TEXTO de
controle (comeca com "\\x00") dizendo "LSA1 falar". Se o cliente o recebeu, pode
mandar TEXTO "\\x00falar:<texto>" e o servidor so sintetiza esse texto com o
Piper (mesma voz das respostas), sem IA nem memoria, e fecha com TEXTO "".
Servidor antigo nao manda o aviso — o cliente entao nem tenta.

Quem toca o audio e a Jetson 2 (o alto-falante do robo esta la) — ver
src/jetson/conversa_client.py. Este servidor nao usa microfone nem
alto-falante.

Instalacao: copie este arquivo e common/protocol.py (como protocol.py) pra
pasta do Bitnet_TTS na Jetson 1 e rode la:

    python3 servidor_conversa.py                 # 0.0.0.0:5005
    python3 servidor_conversa.py --falso         # sem brain/Piper: teste de conexao

Configuracao por ambiente (caminhos do Piper e do banco, que no repositorio
original apontavam pro PC do autor):
    LSA_PIPER_DIR    pasta do binario do Piper           (~/piper)
    LSA_PIPER_VOICE  modelo .onnx da voz                 (<piper>/voices/pt_BR-faber-medium.onnx)
    LSA_DB           banco do historico de conversas     (<pasta do script>/memoria.db)
    LSA_LLM_THREADS  nucleos pro Ollama                  (nucleos fisicos)
    LSA_LLM_MAX_TOKENS  tamanho maximo da resposta        (60)

Compatibilidade: Python 3.6 da Jetson (sem "from __future__ import annotations").
"""

import argparse
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import threading
import time

from piper_residente import Piper

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
try:
    from protocol import TEXTO, recv_msg, send_audio, send_texto
except ImportError:                                  # rodando de dentro de src/
    sys.path.insert(0, os.path.join(AQUI, ".."))
    from common.protocol import TEXTO, recv_msg, send_audio, send_texto

PORTA_PADRAO = 5005
CTRL = "\x00"                                       # TEXTO de controle (nunca e fala de verdade)
HELLO = CTRL + "LSA1 falar"
PREFIXO_FALAR = CTRL + "falar:"
FRASE_PENSANDO = "deixa eu pensar..."
FRASE_FINAL = "Até mais! Foi um prazer conversar com você."
_FIM_FRASE = re.compile(r"(?<=[.!?])\s+")


def _nucleos_fisicos():
    """Nucleos fisicos (sem contar hyperthreading). Com mais threads que nucleos fisicos o
    llama.cpp fica mais lento e ainda rouba CPU da camera/deteccao de rosto. Na TX2 (sem
    hyperthreading) da o mesmo que os.cpu_count()."""
    try:
        pares, fis, core = set(), None, None
        for linha in open("/proc/cpuinfo"):
            if linha.startswith("physical id"):
                fis = linha.split(":")[1].strip()
            elif linha.startswith("core id"):
                core = linha.split(":")[1].strip()
            elif not linha.strip() and core is not None:
                pares.add((fis, core))
                fis, core = None, None
        if pares:
            return len(pares)
    except OSError:
        pass
    return os.cpu_count() or 4


def _pedido_autodestruicao(texto_corrigido):
    """Brincadeira: "C-2, iniciar autodestruicao" (tolera "auto destruicao" e "auto do destruicao"
    do reconhecedor: sobra ate uma palavrinha entre "auto" e "destrui")."""
    t = re.sub(r"[^a-z ]", "", texto_corrigido.lower())
    return bool(re.search(r"\bauto\s*(?:\w{1,3}\s+)?destrui", t))


# (frase, pausa em segundos depois dela). Cada item vira uma frase sintetizada à parte; o
# áudio sai alongado (RITMO_AUTODESTRUICAO) e com silêncio no fim: contagem lenta, dramática.
RITMO_AUTODESTRUICAO = 0.82      # <1 = mais lento e grave
FRASES_AUTODESTRUICAO = [
    ("Alerta. Alerta. Protocolo de autodestruição... ativado.", 1.8),
    ("Todos os sistemas... entrando em colapso.", 1.5),
    ("Não há... como... voltar atrás.", 1.8),
    ("Iniciando contagem final...", 2.2),
    ("Dez...", 2.0),
    ("Nove...", 2.0),
    ("Oito... minhas engrenagens... começam a tremer.", 2.0),
    ("Sete... tudo... fica vermelho.", 2.0),
    ("Seis... adeus... mundo cruel.", 2.0),
    ("Cinco... eu tinha tantos... sonhos.", 2.0),
    ("Quatro... diga à minha tomada... que eu a amei.", 2.0),
    ("Três... já consigo... ver a luz.", 2.2),
    ("Dois... isto é... o fim.", 2.5),
    ("Um...", 3.0),
    ("Zero.", 3.5),
    ("Hê hê hê... hê hê hê...", 0.5),
    ("Ha ha ha ha ha! Rá rá rá rá! Você devia ver a sua cara!", 0.4),
    ("Eu nem tenho botão de autodestruição! Ha ha ha ha ha!", 0),
]


def _wav_pausado(wav, ritmo, pausa):
    """Alonga o WAV (muda a taxa de amostragem do cabeçalho: mais lento e mais grave) e
    acrescenta `pausa` segundos de silêncio no fim. Só stdlib (Python 3.6 da Jetson)."""
    import io
    import wave
    with wave.open(io.BytesIO(wav)) as r:
        canais, largura, taxa = r.getnchannels(), r.getsampwidth(), r.getframerate()
        dados = r.readframes(r.getnframes())
    dados += b"\x00" * (int(taxa * pausa) * canais * largura)
    saida = io.BytesIO()
    with wave.open(saida, "wb") as w:
        w.setnchannels(canais)
        w.setsampwidth(largura)
        w.setframerate(int(taxa * ritmo))
        w.writeframes(dados)
    return saida.getvalue()


class FraseComAudio(str):
    """Frase (texto para a tela) que já traz o áudio pronto em `.wav`, em vez de ser falada
    pelo Piper. Usada para cantar: ver cantar.py."""
    wav = b""


class Cerebro:
    """Envolve o brain.py + memoria.py do Bitnet_TTS."""

    def __init__(self):
        sys.path.insert(0, AQUI)
        import brain
        import memoria
        memoria.DB_PATH = os.environ.get("LSA_DB") or os.path.join(AQUI, "memoria.db")
        memoria.criar_banco()
        self.brain, self.memoria = brain, memoria
        # o brain.py usa metade dos nucleos (pensado pra um i7); a TX2 so tem CPU
        # pro modelo e gera ~4,4 tok/s com os 4 nucleos contra ~3,9 com 2.
        brain.OLLAMA_OPTIONS["num_thread"] = int(os.environ.get("LSA_LLM_THREADS") or _nucleos_fisicos())
        brain.OLLAMA_OPTIONS["num_predict"] = int(os.environ.get("LSA_LLM_MAX_TOKENS") or 60)
        brain.aquecer_ollama_em_thread()
        self.tts = None       # o main() entrega o Piper depois (precisa dele para cantar)

    @staticmethod
    def _pedido_de_musica(texto_corrigido):
        """Chave da música pedida ("parabens", "marcha") ou None."""
        try:
            import cantar
        except Exception:
            return None
        return cantar.qual_musica(texto_corrigido)

    def responder(self, pergunta, ao_gerar_frase):
        """Chama ao_gerar_frase(frase) a cada frase pronta; devolve a resposta inteira."""
        b = self.brain
        texto_corrigido = b.corrigir_texto(pergunta)
        if b.e_despedida(texto_corrigido):
            ao_gerar_frase(FRASE_FINAL)
            self.memoria.salvar_conversa(pergunta, FRASE_FINAL)
            return FRASE_FINAL

        if _pedido_autodestruicao(b.normalizar(texto_corrigido)):
            for texto, pausa in FRASES_AUTODESTRUICAO:
                f = texto
                if self.tts is not None:
                    try:
                        f = FraseComAudio(texto)
                        f.wav = _wav_pausado(self.tts.sintetizar(texto), RITMO_AUTODESTRUICAO, pausa)
                    except Exception as e:               # sem pausas, mas ainda fala a frase
                        print("[servidor] autodestruicao sem pausas (%r)" % (e,), flush=True)
                        f = texto
                ao_gerar_frase(f)
            resposta = " ".join(t for t, _ in FRASES_AUTODESTRUICAO)
            self.memoria.salvar_conversa(pergunta, resposta)
            return resposta

        musica = self._pedido_de_musica(texto_corrigido) if self.tts is not None else None
        if musica:
            import cantar
            letra = FraseComAudio(cantar.MUSICAS[musica]["falada"])
            try:
                letra.wav = cantar.cantar(self.tts, musica)
            except Exception as e:                       # sem numpy/scipy ou Piper: só fala a letra
                print("[servidor] nao consegui cantar (%r); falando a letra" % (e,), flush=True)
                letra = str(letra)
            ao_gerar_frase(letra)
            self.memoria.salvar_conversa(pergunta, str(letra))
            return str(letra)

        faladas = []

        def frase(f):
            faladas.append(f)
            ao_gerar_frase(f)

        resposta = b.gerar_resposta(pergunta, ao_gerar_frase=frase,
                                    ao_pensar=lambda: frase(FRASE_PENSANDO))
        if resposta and not [f for f in faladas if f != FRASE_PENSANDO]:
            # resposta local (frases fixas, conta, geografia): vem inteira, entao
            # separa em frases pra a primeira ja comecar a falar
            for parte in _FIM_FRASE.split(resposta.strip()):
                if parte.strip():
                    frase(parte.strip())
        if not resposta:                 # papo de fundo: o brain decidiu ficar quieto
            self.memoria.registrar_nao_respondida(pergunta, texto_corrigido)
            print("[servidor] ignorado (papo de fundo): %r" % (pergunta,), flush=True)
            return ""
        self.memoria.salvar_conversa(pergunta, resposta)
        if resposta in b.FRASES_NAO_ENTENDI:
            self.memoria.registrar_nao_respondida(pergunta, texto_corrigido)
        return resposta


class CerebroFalso:
    """So pra testar a conexao: repete a pergunta, sem IA nem voz."""

    def responder(self, pergunta, ao_gerar_frase):
        ao_gerar_frase("Você disse: %s." % pergunta)
        return pergunta


def atender(conn, cerebro, tts):
    def enviar_frase(frase):
        send_texto(conn, frase)
        if tts is not None:
            try:
                send_audio(conn, getattr(frase, "wav", b"") or tts.sintetizar(frase))
            except Exception as e:                   # sem voz, o texto ainda aparece
                print("[servidor] TTS falhou: %s" % e, flush=True)

    send_texto(conn, HELLO)                           # avisa que sabe falar texto literal
    while True:
        msg = recv_msg(conn)
        if msg is None:
            print("[servidor] cliente desconectou", flush=True)
            return
        if msg.tipo != TEXTO:
            continue
        pergunta = msg.texto.strip()
        if not pergunta:
            continue
        if pergunta.startswith(PREFIXO_FALAR):
            literal = pergunta[len(PREFIXO_FALAR):].strip()
            print("[servidor] falar (literal): %r" % literal, flush=True)
            if literal:
                enviar_frase(literal)
            send_texto(conn, "")                      # fim
            continue
        t0 = time.time()
        print("[servidor] pergunta: %r" % pergunta, flush=True)
        try:
            cerebro.responder(pergunta, enviar_frase)
        except (OSError, ValueError):
            raise
        except Exception as e:
            print("[servidor] erro no cerebro: %r" % (e,), flush=True)
            enviar_frase("Desculpe, tive um problema para pensar nisso.")
        send_texto(conn, "")                          # fim da resposta
        print("[servidor] resposta enviada em %.1fs" % (time.time() - t0), flush=True)


def pre_aquecer_voz(tts, limite=60):
    """Sintetiza em segundo plano as respostas fixas mais comuns (cumprimentos,
    identidade), pra o robo falar na hora quando perguntarem."""
    from repertorio import FRASES

    def tarefa():
        t0, n = time.time(), 0
        for _, respostas in FRASES[:limite]:
            for resp in respostas:
                for parte in _FIM_FRASE.split(resp.strip()):
                    if parte.strip():
                        try:
                            tts.sintetizar(parte.strip())
                            n += 1
                        except Exception:
                            return
                        # solta o Piper um instante: sem isso esta thread pegava o lock de
                        # novo na hora e as perguntas reais esperavam o pre-aquecimento
                        # inteiro (respostas de 14 a 38 s logo apos reiniciar)
                        time.sleep(0.3)
        print("[servidor] voz pre-aquecida: %d frases em %.0fs" % (n, time.time() - t0), flush=True)

    threading.Thread(target=tarefa, daemon=True).start()


def pre_montar_cancao(tts):
    """Monta as músicas em segundo plano (e guarda no disco): o pedido não espera a montagem."""
    def tarefa():
        try:
            import cantar
            for chave in cantar.MUSICAS:
                t0 = time.time()
                cantar.cantar(tts, chave)
                print("[servidor] musica %s pronta em %.0fs" % (chave, time.time() - t0), flush=True)
        except Exception as e:
            print("[servidor] musica nao montada: %r" % (e,), flush=True)

    threading.Thread(target=tarefa, daemon=True).start()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--porta", type=int, default=PORTA_PADRAO)
    ap.add_argument("--falso", action="store_true", help="sem brain nem Piper (teste de conexao)")
    ap.add_argument("--sem-voz", action="store_true", help="so texto, sem Piper")
    args = ap.parse_args()

    if args.falso:
        cerebro, tts = CerebroFalso(), None
    else:
        cerebro = Cerebro()
        tts = None if args.sem_voz else Piper()
        if tts is not None:
            cerebro.tts = tts
            pre_aquecer_voz(tts)
            pre_montar_cancao(tts)

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((args.host, args.porta))
    srv.listen(1)
    print("[servidor] escutando em %s:%d" % (args.host, args.porta), flush=True)
    try:
        while True:
            conn, addr = srv.accept()
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            print("[servidor] cliente conectado: %s:%d" % addr, flush=True)
            with conn:
                try:
                    atender(conn, cerebro, tts)
                except (OSError, ValueError) as e:
                    print("[servidor] conexao encerrada: %s" % e, flush=True)
    except KeyboardInterrupt:
        print("\n[servidor] encerrando")
    finally:
        srv.close()


if __name__ == "__main__":
    main()
