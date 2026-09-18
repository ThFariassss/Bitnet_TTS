import os
import time
import threading
import cv2

try:
    import torch
    # CORREÇÃO: Deixe um limite um pouco mais restrito se sua CPU for de 4 núcleos, 
    # ou garanta que ele use menos se o BitNet/TTS também rodarem em CPU.
    torch.set_num_threads(max(1, (os.cpu_count() or 4) // 2))
except ImportError:
    pass

from vision import detect_objects, objects_to_description
from brain import gerar_resposta
from voice import falar

CAMERA_INDEX = 0
LARGURA_CAPTURA = 640           
ALTURA_CAPTURA = 480
INTERVALO_SEGUNDOS = 4          
JANELA_TITULO = "Camera - pressione 'q' para sair"

# --- estado compartilhado ---
_lock = threading.Lock()
_frame_mais_recente = None       
_frame_anotado = None            
_descricao_atual = "nada de reconhecível"
_parar = False
_novo_frame_disponivel = False  # CORREÇÃO: Flag para avisar que há um frame inédito
_narrador_ocupado = False       # CORREÇÃO: Evita acumular threads de voz/LLM

def thread_deteccao():
    global _frame_anotado, _descricao_atual, _novo_frame_disponivel

    while not _parar:
        frame = None
        with _lock:
            # CORREÇÃO: Só processa se a câmera de fato entregou um frame NOVO
            if _novo_frame_disponivel and _frame_mais_recente is not None:
                frame = _frame_mais_recente.copy()
                _novo_frame_disponivel = False # Consome o frame

        if frame is None:
            time.sleep(0.01) # CORREÇÃO: Dorme 10ms se não há frame novo (alivia a CPU)
            continue

        objetos, anotado = detect_objects(frame)
        descricao = objects_to_description(objetos)

        with _lock:
            _frame_anotado = anotado
            _descricao_atual = descricao
        
        # CORREÇÃO: Uma pequena folga mecânica após o YOLO processar ajuda 
        # a thread principal do OpenCV a respirar e atualizar a tela sem lag.
        time.sleep(0.01) 


# Altere APENAS esta função dentro do seu main.py

from voice import falar_e_esperar  # <-- Certifique-se de importar a nova função

def narrar_em_thread(descricao: str) -> None:
    """Gera a frase e fala em uma thread separada, protegida contra acúmulo."""
    global _narrador_ocupado
    
    def tarefa():
        global _narrador_ocupado
        print(f"[cérebro] gerando resposta para: {descricao} ...")
        try:
            # 1. Roda o BitNet na CPU (isso pode levar de 1 a 3 segundos)
            frase = gerar_resposta(descricao)
            print(f"[assistente] {frase}")
            
            # 2. Narra e ESPERA o áudio terminar fisicamente de tocar
            falar_e_esperar(frase)
            
        except Exception as erro:
            print(f"[ERRO] falha ao gerar/falar a resposta: {erro!r}")
        finally:
            # 3. Só agora libera o sistema para aceitar novas falas
            _narrador_ocupado = False 

    _narrador_ocupado = True # Bloqueia novos disparos no loop do main.py
    threading.Thread(target=tarefa, daemon=True).start()



def main():
    global _frame_mais_recente, _parar, _novo_frame_disponivel

    captura = cv2.VideoCapture(CAMERA_INDEX)
    if not captura.isOpened():
        raise RuntimeError("Não consegui abrir a câmera. Verifique CAMERA_INDEX.")
    
    captura.set(cv2.CAP_PROP_FRAME_WIDTH, LARGURA_CAPTURA)
    captura.set(cv2.CAP_PROP_FRAME_HEIGHT, ALTURA_CAPTURA)
    captura.set(cv2.CAP_PROP_BUFFERSIZE, 1)  

    worker = threading.Thread(target=thread_deteccao, daemon=True)
    worker.start()

    ultima_descricao_narrada = None
    ultimo_disparo = 0.0

    print("Iniciando... pressione 'q' na janela de vídeo para sair.")

    try:
        while True:
            # CORREÇÃO: Limpeza dupla de buffer antes da leitura (essencial para webcams USB)
            captura.grab()
            ok, frame = captura.read()
            if not ok:
                print("Falha ao capturar frame; tentando de novo.")
                continue

            with _lock:
                _frame_mais_recente = frame
                _novo_frame_disponivel = True # Avisa a thread do YOLO que há novidade
                frame_para_exibir = _frame_anotado if _frame_anotado is not None else frame
                descricao = _descricao_atual

            agora = time.time()
            tempo_passou = (agora - ultimo_disparo) >= INTERVALO_SEGUNDOS
            mudou = descricao != ultima_descricao_narrada

            # CORREÇÃO: Incluído o check 'not _narrador_ocupado'
            if tempo_passou and mudou and not _narrador_ocupado:
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
