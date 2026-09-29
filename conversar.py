import time
import memoria
import brain
from brain import gerar_resposta, e_despedida, corrigir_texto, FRASES_NAO_ENTENDI
from mic import escutar_uma_frase
from voice import falar, esperar_todas_falas_terminarem

NOME = "C-2GELSA"

FRASE_INICIAL = (
    "Olá! Eu sou o C-2GELSA, robô do Laboratório de Sistemas Autônomos, "
    "Estou pronto para conversar com você."
)

FRASE_FINAL = "Até mais! Foi um prazer conversar com você."
FRASE_PENSANDO = "deixa eu pensar..."
def conversar():
    print()
    print("=" * 60)
    print(f"{NOME:^60}")
    print("=" * 60)
    print("Laboratório de Sistemas Autônomos - LSA - PUCRS")
    print()
    print("Modo de conversa por voz. Diga 'tchau' para encerrar.")
    print()

    memoria.criar_banco()
    brain.aquecer_ollama_em_thread()

    print("[ROBÔ]", FRASE_INICIAL)
    falar(FRASE_INICIAL)
    esperar_todas_falas_terminarem()

    while True:
        try:
            print()
            print(f"[{NOME}] Ouvindo...")

            inicio_escuta = time.time()
            pergunta = escutar_uma_frase()
            tempo_escuta = time.time() - inicio_escuta

            print(f"[VOCÊ] {pergunta}")
            print(f"[MIC] reconhecimento levou {tempo_escuta:.2f}s")

            texto_corrigido = corrigir_texto(pergunta)

            if e_despedida(texto_corrigido):
                print(f"[{NOME}] {FRASE_FINAL}")
                falar(FRASE_FINAL)
                esperar_todas_falas_terminarem()
                memoria.salvar_conversa(pergunta, FRASE_FINAL)
                break
            frases_faladas = []

            def _ao_gerar_frase(frase):
                frases_faladas.append(frase)
                print(f"[{NOME}] {frase}")
                falar(frase)

            def _ao_pensar():
                print(f"[{NOME}] {FRASE_PENSANDO}")
                falar(FRASE_PENSANDO)

            inicio_brain = time.time()
            resposta = gerar_resposta(
                pergunta,
                ao_gerar_frase=_ao_gerar_frase,
                ao_pensar=_ao_pensar,
            )
            tempo_brain = time.time() - inicio_brain

            print(f"[BRAIN] resposta completa em {tempo_brain:.2f}s")
            if not frases_faladas:
                print(f"[{NOME}] {resposta}")
                falar(resposta)

            memoria.salvar_conversa(pergunta, resposta)

            if resposta in FRASES_NAO_ENTENDI:
                memoria.registrar_nao_respondida(pergunta, texto_corrigido)

            esperar_todas_falas_terminarem()

        except KeyboardInterrupt:
            print()
            print("[MAIN] encerrando...")
            break

        except Exception as erro:
            print()
            print("[ERRO]", repr(erro))
            import traceback
            traceback.print_exc()
            time.sleep(0.2)

    print()
    print(f"{NOME} encerrado.")

if __name__ == "__main__":
    conversar()