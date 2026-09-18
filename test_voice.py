"""
test_voice.py
Testa SÓ o TTS: fala uma frase fixa em voz alta. Não usa câmera nem BitNet.

Rode no ambiente que tem pyttsx3 (e opcionalmente piper-tts) instalado.
"""

from voice import falar, esperar_todas_falas_terminarem

print("Falando frase de teste... (verifique se saiu som pelo alto-falante)")
falar("Se você está ouvindo isso, o Pedro sangali vai ser deportado pra ISRAEL")
esperar_todas_falas_terminarem()
print("Terminou.")


"""
main.py
Loop principal: webcam -> YOLOv8 (visão) -> BitNet (frase) -> TTS (fala).

A detecção do YOLO roda em uma THREAD SEPARADA da captura/exibição do vídeo.
Isso é o que evita a câmera travar: a exibição sempre roda na velocidade da
webcam, e a detecção (mais lenta, em CPU) só atualiza a anotação na tela
quando terminar de processar o frame mais recente disponível, sem bloquear
o que é mostrado.
"""

import os
import time
import threading

import cv2

# Limita quantos núcleos o PyTorch usa para o YOLO, deixando folga de CPU
# para a thread que captura/exibe o vídeo não ficar competindo por ciclos.
# Ajuste conforme os núcleos da sua máquina (ex.: metade dos núcleos).
try:
    import torch
    torch.set_num_threads(max(1, (os.cpu_count() or 4) // 2))
except ImportError:
    pass

from vision import detect_objects, objects_to_description
from brain import gerar_resposta
from voice import falar

CAMERA_INDEX = 0
LARGURA_CAPTURA = 640           # resolução da captura da webcam (menor = mais fluido)
ALTURA_CAPTURA = 480
INTERVALO_SEGUNDOS = 4          # a cada quantos segundos dispara a narração
JANELA_TITULO = "Camera - pressione 'q' para sair"

# --- estado compartilhado entre a thread de detecção e o loop principal ---
_lock = threading.Lock()
_frame_mais_recente = None       # último frame capturado, pra thread de detecção consumir
_frame_anotado = None            # último resultado (com caixas) pra exibir na tela
_descricao_atual = "nada de reconhecível"
_parar = False


def thread_deteccao():
    """Roda em loop, sempre pegando o frame mais recente disponível e
    rodando o YOLO nele. Como o YOLO é mais lento que a captura, ela vai
    naturalmente processar menos frames por segundo que a exibição --
    e está tudo bem, é exatamente esse o desacoplamento que queremos."""
    global _frame_anotado, _descricao_atual

    while not _parar:
        with _lock:
            frame = _frame_mais_recente.copy() if _frame_mais_recente is not None else None

        if frame is None:
            time.sleep(0.01)
            continue

        objetos, anotado = detect_objects(frame)
        descricao = objects_to_description(objetos)

        with _lock:
            _frame_anotado = anotado
            _descricao_atual = descricao


def narrar_em_thread(descricao: str) -> None:
    """Gera a frase e fala em uma thread separada, para não travar o vídeo."""
    def tarefa():
        print(f"[cérebro] gerando resposta para: {descricao} ...")
        try:
            frase = gerar_resposta(descricao)
            print(f"[assistente] {frase}")
            falar(frase)
        except Exception as erro:
            print(f"[ERRO] falha ao gerar/falar a resposta: {erro!r}")
            import traceback
            traceback.print_exc()

    threading.Thread(target=tarefa, daemon=True).start()


def main():
    global _frame_mais_recente, _parar

    captura = cv2.VideoCapture(CAMERA_INDEX)
    if not captura.isOpened():
        raise RuntimeError("Não consegui abrir a câmera. Verifique CAMERA_INDEX.")
    captura.set(cv2.CAP_PROP_FRAME_WIDTH, LARGURA_CAPTURA)
    captura.set(cv2.CAP_PROP_FRAME_HEIGHT, ALTURA_CAPTURA)
    captura.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # evita acumular frames antigos

    worker = threading.Thread(target=thread_deteccao, daemon=True)
    worker.start()

    ultima_descricao_narrada = None
    ultimo_disparo = 0.0

    print("Iniciando... pressione 'q' na janela de vídeo para sair.")

    try:
        while True:
            ok, frame = captura.read()
            if not ok:
                print("Falha ao capturar frame; tentando de novo.")
                continue

            with _lock:
                _frame_mais_recente = frame
                frame_para_exibir = _frame_anotado if _frame_anotado is not None else frame
                descricao = _descricao_atual

            agora = time.time()
            tempo_passou = (agora - ultimo_disparo) >= INTERVALO_SEGUNDOS
            mudou = descricao != ultima_descricao_narrada

            if tempo_passou and mudou:
                narrar_em_thread(descricao)
                ultima_descricao_narrada = descricao
                ultimo_disparo = agora

            cv2.imshow(JANELA_TITULO, frame_para_exibir)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        _parar = True
        captura.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()