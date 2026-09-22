import os
import queue
import subprocess
import tempfile
import threading

PIPER_PYTHON = "/home/th/Downloads/yes/envs/bitnet/bin/python"


#PIPER_VOICE_MODEL = None
PIPER_VOICE_MODEL = (
    "/home/th/Downloads/Bitnet_TTS/"
    "vozes_faber/pt/pt_BR/faber/medium/"
    "pt_BR-faber-medium.onnx"
)

_fila_falas = queue.Queue()

_thread_falante_iniciada = False

_lock_thread = threading.Lock()

def falar(texto: str) -> None:

    if not texto:
        return

    texto = str(texto).strip()

    if not texto:
        return

    _garantir_thread_falante()

    _fila_falas.put(texto)

def _garantir_thread_falante():

    global _thread_falante_iniciada

    with _lock_thread:

        if not _thread_falante_iniciada:

            thread = threading.Thread(
                target=_loop_falante,
                daemon=True
            )

            thread.start()

            _thread_falante_iniciada = True


def _loop_falante():

    while True:

        texto = _fila_falas.get()

        try:

            _falar_com_piper(texto)

        except Exception as erro:

            print(
                f"[VOICE] Erro ao falar: {erro}"
            )

        finally:

            _fila_falas.task_done()


def _falar_com_piper(texto):

    if not os.path.isfile(PIPER_VOICE_MODEL):

        raise FileNotFoundError(
            f"Modelo Piper não encontrado:\n"
            f"{PIPER_VOICE_MODEL}"
        )

    if not os.path.isfile(PIPER_PYTHON):

        raise FileNotFoundError(
            f"Python do ambiente não encontrado:\n"
            f"{PIPER_PYTHON}"
        )

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as tmp:

        caminho_wav = tmp.name

    try:

        comando = [

            PIPER_PYTHON,

            "-m",
            "piper",

            "--model",
            PIPER_VOICE_MODEL,

            "--output_file",
            caminho_wav,
        ]

        print(
            f"[VOICE] falando: {texto}"
        )

        resultado = subprocess.run(

            comando,

            input=texto,

            text=True,

            capture_output=True,

            check=False
        )

        if resultado.returncode != 0:

            print(
                "[VOICE] Piper retornou erro:"
            )

            print(
                resultado.stderr
            )

            raise RuntimeError(
                "Piper não conseguiu gerar o áudio."
            )

        if os.name == "posix":

            subprocess.run(
                [
                    "aplay",
                    caminho_wav
                ],
                check=True
            )

        else:

            import winsound

            winsound.PlaySound(
                caminho_wav,
                winsound.SND_FILENAME
            )

    finally:
        try:

            os.remove(
                caminho_wav
            )

        except OSError:

            pass

def esperar_todas_falas_terminarem():

    _fila_falas.join()