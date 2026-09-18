"""
vision.py
Detecção de objetos com YOLOv8 pré-treinado (sem treinar nada).
"""

from collections import Counter
from ultralytics import YOLO

# yolov8n.pt = versão "nano", mais rápida, ideal para webcam em tempo real.
# Troque por "yolov8s.pt" ou "yolov8m.pt" se quiser mais precisão.
MODEL_NAME = "yolo11n.pt"
CONF_THRESHOLD = 0.5
# Reduz a resolução interna que o YOLO processa (não afeta a imagem exibida
# na tela). Menor = mais rápido, mas pode perder objetos pequenos/distantes.
# Valores comuns: 320 (rápido), 480, 640 (padrão, mais lento em CPU).
IMG_SIZE = 256

_model = None


def get_model():
    """Carrega o modelo uma única vez (lazy load)."""
    global _model
    if _model is None:
        _model = YOLO(MODEL_NAME)
    return _model


def detect_objects(frame):
    """
    Roda a detecção em um frame (array numpy, formato BGR do OpenCV).

    Retorna:
        objects: Counter com a contagem de cada classe detectada,
                 ex.: Counter({'person': 1, 'cup': 2})
        annotated_frame: frame com as caixas desenhadas, para exibir na tela
    """
    model = get_model()
    results = model.predict(frame, conf=CONF_THRESHOLD, imgsz=IMG_SIZE, verbose=False)
    result = results[0]

    names = result.names
    objects = Counter()
    for box in result.boxes:
        class_id = int(box.cls[0])
        objects[names[class_id]] += 1

    annotated_frame = result.plot()
    return objects, annotated_frame


def objects_to_description(objects: Counter) -> str:
    """Transforma a contagem de objetos em uma descrição curta em português."""
    if not objects:
        return "nada de reconhecível"

    partes = []
    for nome, qtd in objects.items():
        if qtd == 1:
            partes.append(f"1 {_traduzir(nome, plural=False)}")
        else:
            partes.append(f"{qtd} {_traduzir(nome, plural=True)}")
    return ", ".join(partes)


_TRADUCOES = {
    "person": ("pessoa", "pessoas"),
    "cell phone": ("celular", "celulares"),
    "cup": ("xícara", "xícaras"),
    "bottle": ("garrafa", "garrafas"),
    "chair": ("cadeira", "cadeiras"),
    "laptop": ("notebook", "notebooks"),
    "keyboard": ("teclado", "teclados"),
    "mouse": ("mouse", "mouses"),
    "book": ("livro", "livros"),
    "dog": ("cachorro", "cachorros"),
    "cat": ("gato", "gatos"),
    "tv": ("televisão", "televisões"),
    "clock": ("relógio", "relógios"),
    "backpack": ("mochila", "mochilas"),
}


def _traduzir(nome_en: str, plural: bool) -> str:
    par = _TRADUCOES.get(nome_en)
    if par is None:
        return nome_en + ("s" if plural else "")
    return par[1] if plural else par[0]