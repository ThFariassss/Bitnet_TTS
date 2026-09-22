import json
import queue
import time

import sounddevice as sd
import vosk


VOSK_MODEL_PATH = (
    "/home/th/Downloads/Bitnet_TTS/"
    "vosk-model-small-pt-0.3"
)

SAMPLE_RATE = 44100
CHANNELS = 1
BLOCKSIZE = 2048
PULSE_DEVICE_NAME = "pulse"


_modelo = None
_device_index = None
_audio_queue = queue.Queue()



def encontrar_dispositivo_entrada():
    """Procura o dispositivo 'pulse'. Se não achar, cai para o dispositivo
    de entrada padrão do sistema em vez de travar o programa -- assim o
    microfone continua funcionando mesmo em máquinas onde o Pulse/PipeWire
    aparece com outro nome."""
    dispositivos = sd.query_devices()

    print()
    print("Procurando entrada Pulse/PipeWire...")

    for dispositivo in dispositivos:
        nome = dispositivo["name"].lower()
        if PULSE_DEVICE_NAME in nome and dispositivo["max_input_channels"] > 0:
            print()
            print("Entrada encontrada:")
            print(f"  Nome: {dispositivo['name']}")
            print(f"  Índice: {dispositivo['index']}")
            print(f"  Sample rate: {dispositivo['default_samplerate']}")
            return dispositivo["index"]

    print("[MIC] Dispositivo 'pulse' não encontrado; usando o padrão do sistema.")
    padrao = sd.default.device[0]
    if padrao is None or padrao < 0:
        raise RuntimeError(
            "Nenhum dispositivo de entrada de áudio disponível. "
            "Confira se o microfone está conectado (rode: python -m sounddevice)."
        )
    return padrao



def carregar_modelo():
    global _modelo
    if _modelo is None:
        print()
        print("Carregando modelo Vosk...")
        inicio = time.time()
        vosk.SetLogLevel(-1)
        _modelo = vosk.Model(VOSK_MODEL_PATH)
        tempo = time.time() - inicio
        print(f"Modelo Vosk carregado em {tempo:.2f}s.")
    return _modelo




def _callback_audio(indata, frames, time_info, status):
    if status:
        print("[MIC]", status)
    _audio_queue.put(bytes(indata))


def _limpar_fila():
    while True:
        try:
            _audio_queue.get_nowait()
        except queue.Empty:
            break


def escutar_uma_frase() -> str:
    """Bloqueia até detectar uma frase completa (uma pausa natural marca
    o fim) e devolve o texto reconhecido."""
    global _device_index

    if _device_index is None:
        _device_index = encontrar_dispositivo_entrada()

    modelo = carregar_modelo()
    _limpar_fila()

    reconhecedor = vosk.KaldiRecognizer(modelo, SAMPLE_RATE)

    print()
    print("[MIC] Escutando...")

    with sd.RawInputStream(
        device=_device_index,
        samplerate=SAMPLE_RATE,
        blocksize=BLOCKSIZE,
        dtype="int16",
        channels=CHANNELS,
        callback=_callback_audio,
    ):
        while True:
            dados = _audio_queue.get()
            if reconhecedor.AcceptWaveform(dados):
                resultado = json.loads(reconhecedor.Result())
                texto = resultado.get("text", "").strip()
                if texto:
                    return texto
             