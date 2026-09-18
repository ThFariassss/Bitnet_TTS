"""
voice.py
Converte texto em fala.

Tenta usar Piper TTS (melhor qualidade, voz pt-BR) se estiver instalado e
configurado; caso contrário, cai para pyttsx3 (100% offline, sem downloads,
voz mais robótica mas funciona em qualquer máquina).

IMPORTANTE: o pyttsx3 tem um bug conhecido quando o mesmo "engine" é usado
a partir de threads diferentes -- o runAndWait() pode simplesmente não
tocar nada, sem erro nenhum. Por isso aqui existe UMA ÚNICA thread
dedicada só para falar, criada uma vez; qualquer outra parte do programa
(mesmo rodando em suas próprias threads) só empurra o texto para uma fila,
e é essa thread dedicada que efetivamente chama o pyttsx3, sempre a partir
do mesmo lugar.
"""

import os
import queue
import subprocess
import tempfile
import threading

# ------------------------------------------------------------------
# Se for usar Piper, ajuste o caminho do modelo de voz .onnx baixado.
# Deixe None para usar direto o pyttsx3.
# ------------------------------------------------------------------
PIPER_VOICE_MODEL = None  # ex.: "/caminho/para/pt_BR-faber-medium.onnx"

_fila_falas = queue.Queue()
_thread_falante_iniciada = False
_lock_thread = threading.Lock()


def falar(texto: str) -> None:
    """Ponto de entrada público: enfileira o texto para ser falado.
    Pode ser chamado de qualquer thread com segurança."""
    if not texto:
        return

    if PIPER_VOICE_MODEL and os.path.isfile(PIPER_VOICE_MODEL):
        try:
            _falar_com_piper(texto)
            return
        except Exception as erro:
            print(f"[voice] Piper falhou ({erro}); usando pyttsx3.")

    _garantir_thread_falante()
    _fila_falas.put(texto)


def _garantir_thread_falante() -> None:
    global _thread_falante_iniciada
    with _lock_thread:
        if not _thread_falante_iniciada:
            threading.Thread(target=_loop_falante_pyttsx3, daemon=True).start()
            _thread_falante_iniciada = True


def _loop_falante_pyttsx3() -> None:
    """Roda para sempre em UMA thread dedicada: cria o engine uma vez e
    consome a fila, falando cada frase na ordem em que chegou."""
    import pyttsx3

    engine = pyttsx3.init()
    engine.setProperty("rate", 175)

    # tenta escolher uma voz em português, se existir no sistema
    for voz in engine.getProperty("voices"):
        idioma = ""
        if voz.languages:
            bruto = voz.languages[0]
            idioma = bruto.decode(errors="ignore") if isinstance(bruto, bytes) else str(bruto)
        if "pt" in idioma.lower() or "portug" in voz.name.lower() or "brazil" in voz.name.lower():
            engine.setProperty("voice", voz.id)
            break

    while True:
        texto = _fila_falas.get()
        try:
            engine.say(texto)
            engine.runAndWait()
        except Exception as erro:
            print(f"[voice] Erro ao falar com pyttsx3: {erro}")
        finally:
            _fila_falas.task_done()


def esperar_todas_falas_terminarem() -> None:
    """Bloqueia até que todas as frases enfileiradas tenham sido faladas.
    Não é necessário no main.py (que fica rodando indefinidamente), mas é
    útil em scripts de teste curtos, que sem isso terminariam antes da
    thread de voz conseguir falar."""
    _fila_falas.join()


def _falar_com_piper(texto: str) -> None:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        caminho_wav = tmp_wav.name

    comando_piper = [
        "piper",
        "--model", PIPER_VOICE_MODEL,
        "--output_file", caminho_wav,
    ]
    subprocess.run(comando_piper, input=texto, text=True, check=True)

    if os.name == "posix":
        player = "afplay" if _existe_comando("afplay") else "aplay"
        subprocess.run([player, caminho_wav], check=True)
    else:
        import winsound
        winsound.PlaySound(caminho_wav, winsound.SND_FILENAME)

    os.remove(caminho_wav)


def _existe_comando(nome: str) -> bool:
    from shutil import which
    return which(nome) is not None

# Adicione isso no final do seu arquivo voice.py
def falar_e_esperar(texto: str) -> None:
    """Fala o texto usando pyttsx3 de forma síncrona, bloqueando a thread atual 
    até terminar o áudio, garantindo que o tempo de narração seja respeitado."""
    if not texto:
        return
        
    import pyttsx3
    try:
        # Inicializa um engine temporário dedicado a esta thread de narração
        engine_local = pyttsx3.init()
        engine_local.say(texto)
        engine_local.runAndWait()
    except Exception as e:
        print(f"[voice] Erro na narração síncrona: {e}")
