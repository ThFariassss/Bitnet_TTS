from collections import Counter
from ultralytics import YOLO
import time

MODEL_NAME = "/home/th/Downloads/Bitnet_TTS/yolo11n.pt"

CONF_THRESHOLD = 0.50

# 160 = mais rápido
IMG_SIZE = 160

_model = None


def get_model():
    global _model

    if _model is None:
        print(f"[YOLO] carregando {MODEL_NAME}...")
        _model = YOLO(MODEL_NAME)
        print("[YOLO] modelo carregado!")

    return _model


def detect_objects(frame):

    model = get_model()

    inicio = time.time()

    results = model.predict(
        frame,
        conf=CONF_THRESHOLD,
        imgsz=IMG_SIZE,
        verbose=False,
        device="cpu"
    )

    tempo = time.time() - inicio

    result = results[0]

    names = result.names

    objects = Counter()

    for box in result.boxes:

        class_id = int(box.cls[0])

        nome = names[class_id]

        objects[nome] += 1

    # Bounding boxes
    annotated_frame = result.plot()

    print(
        f"[YOLO] {tempo:.2f}s -> {objects}"
    )

    return objects, annotated_frame


def objects_to_description(objects):

    if not objects:
        return "nada de reconhecível"

    partes = []

    for nome, quantidade in objects.items():

        if quantidade == 1:

            partes.append(
                f"1 {_traduzir(nome, False)}"
            )

        else:

            partes.append(
                f"{quantidade} {_traduzir(nome, True)}"
            )

    return ", ".join(partes)


_TRADUCOES = {

    "person": ("pessoa", "pessoas"),

    "cell phone": ("celular", "celulares"),

    "cup": ("xícara", "xícaras"),

    "bottle": ("garrafa", "garrafas"),

    "chair": ("cadeira", "cadeiras"),

    "dining table": ("mesa", "mesas"),

    "laptop": ("notebook", "notebooks"),

    "keyboard": ("teclado", "teclados"),

    "mouse": ("mouse", "mouses"),

    "book": ("livro", "livros"),

    "backpack": ("mochila", "mochilas"),

    "tv": ("televisão", "televisões"),

    "clock": ("relógio", "relógios"),

    "dog": ("cachorro", "cachorros"),

    "cat": ("gato", "gatos"),

    "bowl": ("tigela", "tigelas"),

    "remote": ("controle remoto", "controles remotos"),

    "scissors": ("tesoura", "tesouras"),
}


def _traduzir(nome, plural):

    traducao = _TRADUCOES.get(nome)

    if traducao is None:

        return nome + ("s" if plural else "")

    return traducao[1] if plural else traducao[0]