import os
import re
import subprocess
import unicodedata
from difflib import SequenceMatcher
import random
USE_BITNET = False

BITNET_REPO = "/home/th/Downloads/BitNet"
BITNET_MODEL_REL = "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"
BITNET_CONDA_ENV = "bitnet"
MAX_TOKENS = 20
TIMEOUT_SEGUNDOS = 15
LIMIAR_FUZZY = 0.72

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
    """Normaliza e corrige erros comuns de transcrição. Esse é o texto que
    deve ser usado em TODAS as comparações -- nunca compare com o texto
    bruto do microfone."""
    texto = normalizar(texto)
    for errado, correto in _CORRECOES.items():
        texto = re.sub(rf"\b{re.escape(errado)}\b", correto, texto)
    return texto


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


FRASES_NAO_ENTENDI = [
    "Não entendi bem. Pode repetir de outro jeito?",
    "Desculpa, não consegui entender. Pode falar de novo?",
    "Hmm, não captei essa. Pode repetir?",
]


def gerar_resposta(pergunta_bruta: str) -> str:
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

    resposta = _buscar_em_frases(texto)
    if resposta:
        print("[BRAIN] -> base de frases")
        return resposta

    if USE_BITNET:
        print("[BRAIN] -> BitNet (nada local encontrado)")
        resposta = _executar_bitnet(pergunta_bruta)
        if resposta:
            return resposta

    print("[BRAIN] -> não encontrado, pedindo pra repetir")
    return random.choice(FRASES_NAO_ENTENDI)