"""
brain.py
Gera respostas para o C-2GELSA.

Ordem de prioridade (do mais rápido para o mais lento):
  1. Matemática (regex) -- sempre local, instantâneo
  2. Geografia / capitais (dicionário) -- sempre local, instantâneo
  3. Base de frases fixas (FRASES) -- substring exata primeiro, depois
     fuzzy (tolera erros de reconhecimento do Vosk)
  4. IA por API (Ollama/Claude/ChatGPT) -- opcional, ver MODO_RESPOSTA.
  5. BitNet (opcional, desligado por padrão)
  6. Fallback final, sempre responde alguma coisa (pede pra repetir)

Legenda das alterações desta versão:
  # [MUDOU] -> trecho que já existia e foi alterado
  # [NOVO]  -> trecho novo
"""

import json  # [NOVO] necessário para ler o streaming do Ollama
import os
import re
import subprocess
import threading
import unicodedata
from difflib import SequenceMatcher
import random

import requests


# ============================================================
# CONFIGURAÇÃO
# ============================================================

API_PROVEDOR = "ollama"

# --- Ollama (grátis, local) ---
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2:1b"  # [MUDOU] era "llama3.2" (3B). O 1B é ~3x mais rápido na CPU.

# [NOVO] Número de threads = núcleos FÍSICOS da CPU.
# Rode `lscpu | grep -E "Model name|Core|Thread"` para conferir.
# Se o seu i7 for de 12ª geração ou mais nova (núcleos P + E), use só a
# quantidade de núcleos P. Ajuste esse número e compare os tempos.
NUM_THREADS = max(1, (os.cpu_count() or 8) // 2)

# [NOVO] Opções de geração do Ollama
OLLAMA_OPTIONS = {
    "num_ctx": 1024,          # contexto pequeno = menos memória, prompt mais rápido
    "num_predict": 80,        # limita o tamanho da resposta (2-3 frases)
    "temperature": 0.3,
    "num_thread": NUM_THREADS,
}

# --- Anthropic / OpenAI (pagos, só usados se API_PROVEDOR for um deles) ---
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = "claude-sonnet-4-5"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"

USAR_BUSCA_NA_WEB = True

# "local" | "hibrido" | "api"
MODO_RESPOSTA = "hibrido"

# [MUDOU] era 60. Com streaming, esse valor é o tempo máximo SEM receber
# nenhum pedaço de resposta (não o tempo total da resposta).
TIMEOUT_API_SEGUNDOS = 20

# [NOVO] Tempo máximo de espera na carga inicial do modelo (aquecimento).
TIMEOUT_AQUECIMENTO_SEGUNDOS = 120

# [NOVO] Tempo máximo para conectar no Ollama (se ele não estiver rodando,
# descobrimos em 5s em vez de esperar o timeout inteiro).
TIMEOUT_CONEXAO_SEGUNDOS = 5

PROMPT_SISTEMA_API = (
    "Você é o C-2GELSA, um robô assistente de voz do Laboratório de "
    "Sistemas Autônomos (LSA) da PUCRS. Responda SEMPRE em português do "
    "Brasil, em no máximo 2 ou 3 frases curtas e naturais -- a resposta "
    "vai ser convertida em fala, então evite listas, markdown, emojis ou "
    "textos longos."
)

USE_BITNET = False

BITNET_REPO = "/home/th/Downloads/BitNet"
BITNET_MODEL_REL = "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"
BITNET_CONDA_ENV = "bitnet"
MAX_TOKENS = 20
TIMEOUT_SEGUNDOS = 15

LIMIAR_FUZZY = 0.72


# ============================================================
# NORMALIZAÇÃO E CORREÇÃO
# ============================================================

def normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^\w\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


_CORRECOES = {
    "capitar": "capital",
    "capitau": "capital",
    "puc rs": "pucrs",
    "vc": "voce",
    "robot": "robo",
}


def corrigir_texto(texto: str) -> str:
    texto = normalizar(texto)
    for errado, correto in _CORRECOES.items():
        texto = re.sub(rf"\b{re.escape(errado)}\b", correto, texto)
    return texto


# ============================================================
# BASE DE FRASES (conversa + conhecimento geral)
# ============================================================

FRASES = [
    (["oi", "ola", "e ai", "ei robo", "fala robo", "ola assistente",
      "oi robo", "oi c 2gelsa", "oi c2gelsa"], [
        "Olá! Eu sou o C-2GELSA. Como posso ajudar?",
        "Oi! Tudo bem? Pode perguntar o que quiser.",
    ]),
    (["bom dia"], ["Bom dia! Como posso ajudar?"]),
    (["boa tarde"], ["Boa tarde! Como posso ajudar?"]),
    (["boa noite"], ["Boa noite! Como posso ajudar?"]),
    (["tudo bem", "tudo certo", "como voce esta", "como voce ta",
      "voce esta bem", "esta tudo bem"], [
        "Estou funcionando normalmente! E você, tudo bem?",
        "Tudo certo por aqui! E com você?",
    ]),
    (["como esta voce", "como voce se sente"], [
        "Estou pronto para conversar e ajudar!",
    ]),
    (["obrigado", "obrigada", "valeu", "muito obrigado", "agradeco"], [
        "Por nada! Estou aqui para ajudar.",
        "De nada! Se precisar de mais alguma coisa, só chamar.",
    ]),
    (["por favor"], ["Claro! Pode falar."]),
    (["desculpa", "foi mal", "perdao"], ["Tudo bem! Não tem problema."]),
    (["voce esta ai", "esta ai", "tem alguem ai", "esta me ouvindo"], [
        "Sim! Estou aqui e estou ouvindo.",
    ]),
    (["voce me ouve", "consegue me ouvir", "esta ouvindo minha voz"], [
        "Sim! Estou ouvindo você.",
    ]),
    (["voce entende", "consegue entender"], [
        "Sim. Eu consigo interpretar o que você fala.",
    ]),
    (["quem e voce", "qual seu nome", "qual e seu nome", "qual o seu nome",
      "como voce se chama", "quem e o robo", "quem e esse robo"], [
        "Eu sou o C-2GELSA, robô do Laboratório de Sistemas Autônomos da PUCRS.",
    ]),
    (["seu nome", "nome do robo", "nome desse robo", "como chama o robo"], [
        "Meu nome é C-2GELSA.",
    ]),
    (["o que significa c 2gelsa", "o que e c 2gelsa"], [
        "C-2GELSA é o meu nome. Eu sou um robô do LSA da PUCRS.",
    ]),
    (["o que voce faz", "qual sua funcao", "qual e sua funcao",
      "para que voce serve", "o que voce consegue fazer",
      "quais suas funcoes"], [
        "Eu posso conversar, responder perguntas e auxiliar nas atividades do laboratório.",
    ]),
    (["voce e um robo", "voce e robo", "voce e uma maquina"], [
        "Sim. Eu sou um robô desenvolvido para interagir com pessoas.",
    ]),
    (["voce e inteligente", "voce se considera inteligente"], [
        "Eu fui desenvolvido para interpretar perguntas e responder de forma útil.",
    ]),
    (["voce pensa", "voce consegue pensar"], [
        "Eu processo informações usando modelos computacionais para gerar minhas respostas.",
    ]),
    (["voce aprende", "voce consegue aprender"], [
        "Meu funcionamento depende dos modelos e informações configurados para mim.",
    ]),
    (["onde voce esta", "onde fica voce", "onde voce funciona"], [
        "Eu funciono no Laboratório de Sistemas Autônomos da PUCRS.",
    ]),
    (["qual laboratorio", "onde fica o lsa", "o que e o lsa",
      "o que significa lsa", "o que significa a sigla lsa"], [
        "LSA significa Laboratório de Sistemas Autônomos.",
    ]),
    (["o que e a pucrs", "qual universidade", "qual e a universidade",
      "onde fica a pucrs", "voce e da pucrs"], [
        "Eu faço parte do Laboratório de Sistemas Autônomos da PUCRS.",
    ]),
    (["o que e robotica", "o que e um robo", "o que significa robotica"], [
        "Robótica é a área que envolve o desenvolvimento e controle de robôs para realizar tarefas.",
    ]),
    (["o que e inteligencia artificial", "o que e ia",
      "o que significa ia", "me explica inteligencia artificial"], [
        "Inteligência artificial é a área da computação que permite a sistemas realizar tarefas que normalmente exigem inteligência humana.",
    ]),
    (["o que e visao computacional", "o que significa visao computacional",
      "me explica visao computacional"], [
        "Visão computacional permite que computadores interpretem imagens e vídeos.",
    ]),
    (["o que e machine learning", "o que e aprendizado de maquina"], [
        "Machine learning é uma técnica em que computadores aprendem padrões a partir de dados.",
    ]),
    (["o que e python", "para que serve python"], [
        "Python é uma linguagem de programação muito usada em inteligência artificial, automação e ciência de dados.",
    ]),
    (["como voce foi feito", "como criaram voce", "como voce foi criado"], [
        "Eu fui desenvolvido como um projeto de robótica e inteligência artificial no LSA da PUCRS.",
    ]),
    (["quem criou voce", "quem fez voce", "quem desenvolveu voce"], [
        "Eu faço parte de um projeto desenvolvido no Laboratório de Sistemas Autônomos da PUCRS.",
    ]),
    (["o que e tts", "o que significa tts"], [
        "TTS significa texto para fala: é a tecnologia que transforma texto em voz.",
    ]),
    (["o que e vosk", "para que serve o vosk"], [
        "Vosk é uma tecnologia de reconhecimento de fala que transforma voz em texto.",
    ]),
    (["o que e bitnet", "para que serve o bitnet"], [
        "BitNet é uma arquitetura de modelos de linguagem projetada para usar pesos de baixa precisão.",
    ]),
    (["qual o maior planeta"], ["O maior planeta do Sistema Solar é Júpiter."]),
    (["qual o menor planeta"], ["O menor planeta do Sistema Solar é Mercúrio."]),
    (["quantos planetas existem", "quantos planetas tem"], [
        "O Sistema Solar possui oito planetas.",
    ]),
    (["o que e o sol", "qual a estrela do sistema solar"], [
        "O Sol é a estrela que fica no centro do nosso Sistema Solar.",
    ]),
    (["o que e a lua", "a lua e um planeta"], [
        "A Lua é o satélite natural da Terra.",
    ]),
    (["o que e a terra"], ["A Terra é o planeta onde vivemos."]),
    (["o que e internet", "como funciona a internet"], [
        "A internet é uma grande rede que conecta computadores e dispositivos ao redor do mundo.",
    ]),
    (["o que e um computador", "como funciona um computador"], [
        "Um computador é uma máquina capaz de processar, armazenar e transmitir informações.",
    ]),
    (["como funciona o microfone", "o que e um microfone"], [
        "O microfone transforma ondas sonoras da voz em sinais que o computador consegue processar.",
    ]),
    (["o que e uma camera", "como funciona uma camera"], [
        "Uma câmera captura imagens que podem ser processadas por um computador.",
    ]),
]

GATILHOS_DESPEDIDA = [
    "tchau", "ate mais", "encerrar conversa", "pode parar",
    "falou", "ate logo", "vou embora", "preciso ir",
]


def e_despedida(texto_corrigido: str) -> bool:
    return any(g in texto_corrigido for g in GATILHOS_DESPEDIDA)


def _buscar_em_frases(texto: str):
    """1a passada: substring exata (rápido e preciso).
    2a passada: fuzzy (tolera erro de transcrição), só se a 1a não achar."""
    for gatilhos, respostas in FRASES:
        if any(g in texto for g in gatilhos):
            return random.choice(respostas)

    melhor_respostas, melhor_score = None, 0.0
    for gatilhos, respostas in FRASES:
        for gatilho in gatilhos:
            score = SequenceMatcher(None, gatilho, texto).ratio()
            if score > melhor_score:
                melhor_score, melhor_respostas = score, respostas

    if melhor_score >= LIMIAR_FUZZY:
        return random.choice(melhor_respostas)
    return None


# ============================================================
# MATEMÁTICA
# ============================================================

_NUMEROS_POR_EXTENSO = {
    "zero": 0, "um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3,
    "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9,
    "dez": 10, "onze": 11, "doze": 12, "treze": 13, "quatorze": 14,
    "quinze": 15, "vinte": 20,
}


def resposta_matematica(texto: str):
    if not any(p in texto for p in [
        "quanto", "calcule", "calcula", "calcular", "resultado",
        "vezes", "mais", "menos", "dividido", "multiplicado",
    ]):
        return None

    t = texto
    for palavra, numero in _NUMEROS_POR_EXTENSO.items():
        t = re.sub(rf"\b{palavra}\b", str(numero), t)

    t = re.sub(r"\bmultiplicado por\b", "*", t)
    t = re.sub(r"\bdividido por\b", "/", t)
    t = re.sub(r"\bvezes\b", "*", t)
    t = re.sub(r"\bmais\b", "+", t)
    t = re.sub(r"\bmenos\b", "-", t)

    valores = re.findall(r"\d+(?:[.,]\d+)?", t)
    if len(valores) < 2:
        return None

    expressao = re.sub(r"[^0-9+\-*/(). ]", "", t)
    try:
        resultado = eval(expressao, {"__builtins__": {}}, {})
        if isinstance(resultado, float):
            resultado = int(resultado) if resultado.is_integer() else round(resultado, 4)
        return f"O resultado é {resultado}."
    except Exception:
        return None


CAPITAIS = {
    "brasil": "Brasília", "argentina": "Buenos Aires", "uruguai": "Montevidéu",
    "paraguai": "Assunção", "chile": "Santiago", "peru": "Lima",
    "bolivia": "La Paz", "colombia": "Bogotá", "venezuela": "Caracas",
    "equador": "Quito", "estados unidos": "Washington, D.C.",
    "canada": "Ottawa", "mexico": "Cidade do México", "portugal": "Lisboa",
    "espanha": "Madri", "franca": "Paris", "italia": "Roma",
    "alemanha": "Berlim", "reino unido": "Londres", "inglaterra": "Londres",
    "japao": "Tóquio", "china": "Pequim", "india": "Nova Délhi",
    "russia": "Moscou", "australia": "Camberra", "egito": "Cairo",
    "turquia": "Ancara", "grecia": "Atenas", "coreia do sul": "Seul",
    "tailandia": "Bangcoc", "austria": "Viena", "suica": "Berna",
    "noruega": "Oslo", "suecia": "Estocolmo", "finlandia": "Helsinque",
    "dinamarca": "Copenhague", "polonia": "Varsóvia", "irlanda": "Dublin",
    "islandia": "Reykjavík", "africa do sul": "Pretória", "marrocos": "Rabat",
    "nigeria": "Abuja",
}


def resposta_geografia(texto: str):
    if "capital" not in texto:
        return None
    for pais, capital in CAPITAIS.items():
        if pais in texto:
            return f"A capital de {pais} é {capital}."
    return "Diga o nome do país e eu tento informar a capital."


# ============================================================
# IA POR API (Ollama / Claude / ChatGPT)
# ============================================================

def _api_disponivel() -> bool:
    if API_PROVEDOR == "ollama":
        return True
    if API_PROVEDOR == "anthropic":
        return bool(ANTHROPIC_API_KEY)
    if API_PROVEDOR == "openai":
        return bool(OPENAI_API_KEY)
    return False


# [MUDOU] agora aceita ao_gerar_frase (callback chamado a cada frase pronta)
def _gerar_com_api(pergunta: str, ao_gerar_frase=None):
    """Ponto de entrada único. Devolve None se falhar por qualquer motivo."""
    if not _api_disponivel():
        print(f"[BRAIN] provedor '{API_PROVEDOR}' sem chave configurada.")
        return None

    try:
        if API_PROVEDOR == "ollama":
            return _gerar_com_ollama(pergunta, ao_gerar_frase)
        if API_PROVEDOR == "anthropic":
            return _gerar_com_anthropic(pergunta)
        if API_PROVEDOR == "openai":
            return _gerar_com_openai(pergunta)
    except requests.exceptions.ConnectionError:
        if API_PROVEDOR == "ollama":
            print("[BRAIN] não consegui conectar ao Ollama -- ele está rodando? "
                  "(rode 'ollama serve' ou confira se o app está aberto)")
        else:
            print("[BRAIN] erro de conexão com a API.")
    except requests.exceptions.Timeout:
        print("[BRAIN] provedor demorou demais; ignorando.")
    except Exception as erro:
        print(f"[BRAIN] erro no provedor: {erro!r}")
    return None


# [MUDOU] versão com streaming, keep_alive e opções de desempenho
def _gerar_com_ollama(pergunta: str, ao_gerar_frase=None,
                      timeout: float = TIMEOUT_API_SEGUNDOS):
    """Chama o Ollama em modo streaming.

    - A cada frase completa, chama ao_gerar_frase(frase) (se fornecido),
      permitindo que o robô comece a falar antes da resposta terminar.
    - Devolve o texto completo.
    - Se o stream falhar no meio, devolve o que já foi gerado (em vez de
      perder a resposta parcial)."""
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": PROMPT_SISTEMA_API},
            {"role": "user", "content": pergunta},
        ],
        "stream": True,
        "keep_alive": -1,          # nunca descarrega o modelo da memória
        "options": OLLAMA_OPTIONS,
    }

    texto_total = ""
    buffer = ""

    def emitir(frase: str) -> None:
        nonlocal texto_total
        frase = frase.strip()
        if not frase:
            return
        texto_total += frase + " "
        if ao_gerar_frase:
            ao_gerar_frase(frase)

    try:
        # timeout=(conexão, leitura). Com stream=True a "leitura" é o tempo
        # máximo SEM receber dados, e não o tempo total da resposta.
        with requests.post(
            OLLAMA_URL, json=payload, stream=True,
            timeout=(TIMEOUT_CONEXAO_SEGUNDOS, timeout),
        ) as resposta:
            resposta.raise_for_status()
            for linha in resposta.iter_lines():
                if not linha:
                    continue
                pedaco = json.loads(linha)
                buffer += pedaco.get("message", {}).get("content", "")

                partes = re.split(r"(?<=[.!?])\s+", buffer)
                for frase in partes[:-1]:
                    emitir(frase)
                buffer = partes[-1]

                if pedaco.get("done"):
                    break
        emitir(buffer)
    except requests.exceptions.RequestException:
        # se já geramos algo, aproveita; se não, propaga o erro
        if texto_total.strip():
            print("[BRAIN] stream interrompido; usando resposta parcial.")
            return texto_total.strip()
        raise

    return texto_total.strip() or None


# [MUDOU] usa timeout longo, para não falhar durante a carga inicial do modelo
def aquecer_ollama_em_thread() -> None:
    """Carrega o modelo na memória em background, logo no início do
    programa, para a primeira pergunta real não pagar o custo de carga."""
    if API_PROVEDOR != "ollama":
        return

    def _tarefa():
        import time as _time
        inicio = _time.time()
        print("[BRAIN] aquecendo o Ollama em segundo plano...")
        try:
            _gerar_com_ollama("oi", timeout=TIMEOUT_AQUECIMENTO_SEGUNDOS)
            print(f"[BRAIN] Ollama aquecido em {_time.time() - inicio:.1f}s.")
        except Exception as erro:
            print(f"[BRAIN] aquecimento do Ollama falhou ({erro!r}); "
                  "primeira pergunta real pode demorar mais.")

    threading.Thread(target=_tarefa, daemon=True).start()


def _gerar_com_anthropic(pergunta: str):
    payload = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 300,
        "system": PROMPT_SISTEMA_API,
        "messages": [{"role": "user", "content": pergunta}],
    }
    if USAR_BUSCA_NA_WEB:
        payload["tools"] = [{"type": "web_search_20250305", "name": "web_search"}]

    resposta = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json=payload,
        timeout=TIMEOUT_API_SEGUNDOS,
    )
    resposta.raise_for_status()
    dados = resposta.json()

    texto = "".join(
        bloco.get("text", "")
        for bloco in dados.get("content", [])
        if bloco.get("type") == "text"
    ).strip()
    return texto or None


def _gerar_com_openai(pergunta: str):
    resposta = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "content-type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "max_tokens": 300,
            "messages": [
                {"role": "system", "content": PROMPT_SISTEMA_API},
                {"role": "user", "content": pergunta},
            ],
        },
        timeout=TIMEOUT_API_SEGUNDOS,
    )
    resposta.raise_for_status()
    dados = resposta.json()
    texto = dados["choices"][0]["message"]["content"].strip()
    return texto or None


# ============================================================
# BITNET (opcional -- ver USE_BITNET no topo do arquivo)
# ============================================================

def _bitnet_disponivel() -> bool:
    modelo = os.path.join(BITNET_REPO, BITNET_MODEL_REL)
    script = os.path.join(BITNET_REPO, "run_inference.py")
    return os.path.isfile(modelo) and os.path.isfile(script)


def _executar_bitnet(pergunta: str):
    if not _bitnet_disponivel():
        return None

    prompt = (
        "Você é o C-2GELSA, um robô assistente do Laboratório de Sistemas "
        "Autônomos da PUCRS. Responda em português brasileiro, de forma "
        "natural, direta e curta.\n"
        f"Pergunta: {pergunta}\n"
        "Resposta:"
    )

    modelo = os.path.join(BITNET_REPO, BITNET_MODEL_REL)
    comando = [
        "conda", "run", "-n", BITNET_CONDA_ENV,
        "python", "run_inference.py",
        "-m", modelo, "-p", prompt,
        "-n", str(MAX_TOKENS), "-t", "4", "-c", "256", "-temp", "0.7",
    ]

    try:
        resultado = subprocess.run(
            comando, cwd=BITNET_REPO, capture_output=True, text=True,
            timeout=TIMEOUT_SEGUNDOS,
        )
        if resultado.returncode != 0:
            print("[BRAIN] erro BitNet:", resultado.stderr[-300:])
            return None
        return _limpar_saida_bitnet(resultado.stdout, prompt)
    except subprocess.TimeoutExpired:
        print("[BRAIN] BitNet demorou demais; ignorando.")
        return None
    except Exception as erro:
        print("[BRAIN] erro:", repr(erro))
        return None


def _limpar_saida_bitnet(saida: str, prompt: str):
    texto = saida.replace(prompt, "")
    if "Resposta:" in texto:
        texto = texto.split("Resposta:", 1)[1]
    texto = re.sub(r"\s+", " ", texto).strip()
    if not texto:
        return None
    frases = re.split(r"(?<=[.!?])\s+", texto)
    return " ".join(frases[:2]).strip() or None


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

FRASES_NAO_ENTENDI = [
    "Não entendi bem. Pode repetir de outro jeito?",
    "Desculpa, não consegui entender. Pode falar de novo?",
    "Hmm, não captei essa. Pode repetir?",
]


# [MUDOU] novos parâmetros opcionais:
#   ao_gerar_frase -> chamado a cada frase pronta vinda da IA (streaming)
#   ao_pensar      -> chamado UMA vez, logo antes de consultar a IA
def gerar_resposta(pergunta_bruta: str, ao_gerar_frase=None, ao_pensar=None) -> str:
    texto = corrigir_texto(pergunta_bruta)
    print(f"[BRAIN] pergunta (corrigida): {texto!r}")

    resposta = resposta_matematica(texto)
    if resposta:
        print("[BRAIN] -> matemática")
        return resposta

    resposta = resposta_geografia(texto)
    if resposta:
        print("[BRAIN] -> geografia")
        return resposta

    if MODO_RESPOSTA != "api":
        resposta = _buscar_em_frases(texto)
        if resposta:
            print("[BRAIN] -> base de frases")
            return resposta

    if MODO_RESPOSTA in ("hibrido", "api"):
        print(f"[BRAIN] -> API ({API_PROVEDOR})")
        if ao_pensar:                      # [NOVO] "Hmm, deixa eu pensar..."
            ao_pensar()
        resposta = _gerar_com_api(pergunta_bruta, ao_gerar_frase)
        if resposta:
            return resposta

    if USE_BITNET:
        print("[BRAIN] -> BitNet (nada local nem de API encontrado)")
        resposta = _executar_bitnet(pergunta_bruta)
        if resposta:
            return resposta

    print("[BRAIN] -> não encontrado, pedindo pra repetir")
    return random.choice(FRASES_NAO_ENTENDI)