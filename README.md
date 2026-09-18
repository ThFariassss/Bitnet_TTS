# Câmera + YOLO + BitNet + TTS

Robozinho de bolso: a câmera vê algo com **YOLOv8 pré-treinado (COCO)**, o
**BitNet b1.58** (LLM de 1 bit, roda em CPU) gera uma frase falada sobre o que
foi visto, e um mecanismo de **TTS** fala essa frase em voz alta.

```
 webcam --> [YOLOv8n] --> lista de objetos --> [BitNet] --> frase --> [TTS] --> alto-falante
             (visão)                            (cérebro)             (voz)
```

Nenhuma etapa exige treinamento. YOLO usa os pesos oficiais treinados em
COCO (80 classes: pessoa, cachorro, celular, garrafa, cadeira, ...). BitNet
usa um modelo pronto baixado do Hugging Face.

## Estrutura

```
yolo-bitnet-tts/
├── README.md
├── requirements.txt
├── vision.py     # detecção de objetos com YOLOv8
├── brain.py      # chama o BitNet e gera a frase
├── voice.py      # transforma a frase em áudio (TTS) e reproduz
└── main.py       # loop principal: junta tudo
```

## 1. Ambiente Python

```bash
python -m venv venv
source venv/bin/activate      # no Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. YOLO (visão) — nada a instalar além do pip acima

O `vision.py` usa `ultralytics`, que baixa automaticamente o checkpoint
`yolov8n.pt` (o menor e mais rápido, ~6MB) na primeira execução. Ele já vem
treinado nas 80 classes do COCO, então não precisa treinar nada.

Se quiser mais precisão (e tiver GPU/CPU mais forte), troque `yolov8n.pt` por
`yolov8s.pt` ou `yolov8m.pt` em `vision.py`.

## 3. BitNet (cérebro) — precisa ser clonado e compilado uma vez

O BitNet.cpp é a implementação oficial da Microsoft para rodar LLMs de 1 bit
em CPU. Ele fica em um repositório separado (não é um pacote pip):

```bash
# fora da pasta do projeto, ou em uma subpasta "engines/"
git clone --recursive https://github.com/microsoft/BitNet.git
cd BitNet
pip install -r requirements.txt

# baixa o modelo oficial de 2B parâmetros e prepara os pesos quantizados
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
```

Isso cria `models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf`, que é o arquivo
que `brain.py` vai chamar via `run_inference.py`.

Depois, edite as duas variáveis no topo de `brain.py`:

```python
BITNET_REPO = "/caminho/absoluto/para/BitNet"
BITNET_MODEL = "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"
```

> Alternativa mais simples para testar o pipeline sem compilar nada: em
> `brain.py` há uma função `fallback_response()` baseada em template, usada
> automaticamente se o BitNet não estiver configurado — assim você já pode
> rodar câmera → texto → voz e trocar o "cérebro" depois.

## 4. TTS (voz)

Duas opções, já implementadas em `voice.py` com fallback automático:

- **Piper TTS** (offline, boa qualidade, tem voz em pt-BR) — recomendado.
  ```bash
  pip install piper-tts
  # baixe uma voz pt-BR, ex.: pt_BR-faber-medium
  # https://github.com/rhasspy/piper/blob/master/VOICES.md
  ```
- **pyttsx3** (offline, 100% local, roda no motor de voz do sistema
  operacional — SAPI5 no Windows, NSSpeech no Mac, espeak no Linux). Não
  precisa baixar nada, mas a voz é mais robótica.
  ```bash
  pip install pyttsx3
  ```

Se o Piper não estiver configurado, `voice.py` cai automaticamente no
pyttsx3.

## 5. Rodar tudo

```bash
python main.py
```

O script:
1. Abre a webcam (índice `0`; troque em `main.py` se tiver mais de uma).
2. A cada `INTERVALO_SEGUNDOS`, roda o YOLO num frame.
3. Se a lista de objetos detectados mudou desde a última vez, manda para o
   BitNet gerar uma frase curta e natural sobre o que está vendo.
4. Fala a frase com o TTS.
5. Continua o loop (pressione `q` na janela da câmera para sair).

## Ideias de evolução

- Trocar o "vendo objeto X" por eventos (ex.: só falar quando uma *pessoa*
  aparece pela primeira vez, tipo campainha inteligente).
- Adicionar reconhecimento de fala (STT) para virar um assistente que
  responde perguntas sobre o que está vendo ("o que tem na mesa?").
- Rodar em Raspberry Pi: YOLOv8n + BitNet 1-bit foram feitos para isso — é
  o combo mais leve possível de visão + LLM em CPU.
