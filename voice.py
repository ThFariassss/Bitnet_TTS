import queue
import subprocess
import threading

from piper_residente import Piper

_piper = None
_fila_falas = queue.Queue()
_thread_falante_iniciada = False
_lock_thread = threading.Lock()


def falar(texto: str) -> None:
    """Ponto de entrada público: enfileira o texto para ser falado.
    Pode ser chamado de qualquer thread com segurança."""
    if not texto:
        return

    texto = str(texto).strip()
    if not texto:
        return

    _garantir_thread_falante()
    _fila_falas.put(texto)


def _garantir_thread_falante() -> None:
    global _thread_falante_iniciada
    with _lock_thread:
        if not _thread_falante_iniciada:
            thread = threading.Thread(target=_loop_falante, daemon=True)
            thread.start()
            _thread_falante_iniciada = True


def _loop_falante() -> None:
    while True:
        texto = _fila_falas.get()
        try:
            _falar_com_piper(texto)
        except Exception as erro:
            print(f"[VOICE] Erro ao falar: {erro}")
        finally:
            _fila_falas.task_done()


def _falar_com_piper(texto: str) -> None:
    global _piper
    if _piper is None:
        # caminhos por LSA_PIPER_DIR / LSA_PIPER_VOICE (padrão: ~/piper)
        _piper = Piper()

    print(f"[VOICE] falando: {texto}")
    wav = _piper.sintetizar(texto)
    subprocess.run(["aplay", "-q", "-"], input=wav, check=True)


def esperar_todas_falas_terminarem() -> None:
    """Bloqueia até que todas as frases enfileiradas tenham sido faladas.
    Útil em scripts de teste curtos, que sem isso terminariam antes da
    thread de voz conseguir falar."""
    _fila_falas.join()
