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

import collections
import json  # [NOVO] necessário para ler o streaming do Ollama
import os
import re
import subprocess
import threading
import time
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
    "textos longos.\n"
    "Sobre você: seu nome é C-2GELSA; você é um robô que conversa por voz, "
    "roda em um computador e foi desenvolvido pela equipe do LSA "
    "da PUCRS, em Porto Alegre. Você não tem gênero nem sentimentos humanos.\n"
    "A pergunta vem de um reconhecedor de voz e pode chegar cortada ou com "
    "palavras erradas. Se ela não fizer sentido, diga que não entendeu e peça "
    "para a pessoa repetir, em vez de adivinhar. Se não souber a resposta, diga "
    "que não sabe; nunca invente fatos.\n"
    "Regras: não invente nomes, cargos, datas nem números; para pessoas ou "
    "fatos específicos que você não conhece, diga \"não tenho certeza\". Não dê "
    "opinião sobre política, religião nem times; seja neutro e simpático. "
    "Nunca peça desculpas em excesso nem explique que é uma IA em detalhes: "
    "responda direto, em no máximo duas frases."
)

USE_BITNET = False

BITNET_REPO = "/home/th/Downloads/BitNet"
BITNET_MODEL_REL = "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"
BITNET_CONDA_ENV = "bitnet"
MAX_TOKENS = 20
TIMEOUT_SEGUNDOS = 15

PALAVRAS_FRASE_LONGA = 8   # a partir daqui, gatilho de 1-2 palavras sozinho nao basta (ver _buscar_entrada)
PALAVRAS_RUIDO_MUDO = 4    # frase assim longa, sem cara de pergunta e fora do repertorio: o robo fica quieto

LIMIAR_FUZZY = 0.82  # 0.72 confundia "o que e pouco mao" com "o que e um computador"


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
# Para aumentar o repertório, edite o arquivo repertorio.py.
# ============================================================

from repertorio import FRASES, GATILHOS_DESPEDIDA, GATILHOS_FUZZY_ESTRITOS
import repertorio_contexto as rc


_REGEX_GATILHO = {}


def _contem(texto: str, gatilho: str) -> bool:
    """True se o gatilho aparece no texto como palavras inteiras
    (evita que "oi" case dentro de "foi" ou "coisa")."""
    if gatilho not in texto:               # barato e descarta quase todos
        return False
    rx = _REGEX_GATILHO.get(gatilho)
    if rx is None:
        rx = _REGEX_GATILHO[gatilho] = re.compile(rf"\b{re.escape(gatilho)}\b")
    return rx.search(texto) is not None


def e_despedida(texto_corrigido: str) -> bool:
    return any(_contem(texto_corrigido, g) for g in GATILHOS_DESPEDIDA)


def _buscar_entrada(texto: str):
    """Lista de respostas da entrada que casa com `texto` (ou None).
    1a passada: substring exata (rápido e preciso).
    2a passada: fuzzy (tolera erro de transcrição), só se a 1a não achar."""
    # Conversa de fundo: numa frase longa, um gatilho curto ("e ai", "repetir") casa por acaso
    # com um trecho que ninguem dirigiu ao robo. Gatilho de 1-2 palavras so vale em frase curta.
    n_palavras = len(texto.split())
    for gatilhos, respostas in FRASES:
        if any(_contem(texto, g) and not (n_palavras >= PALAVRAS_FRASE_LONGA and g.count(" ") < 2)
               for g in gatilhos):
            return respostas

    # Mesmo resultado de comparar tudo com ratio(), mas pula quem não tem como
    # ganhar: ratio() <= quick_ratio() <= real_quick_ratio(), então só calcula
    # o ratio completo se o limite superior passa do LIMIAR e do melhor atual.
    melhor_respostas, melhor_score = None, 0.0
    sm = SequenceMatcher(None)
    sm.set_seq2(texto)                     # seq2 é indexada uma vez só
    ultima_palavra = texto.rsplit(" ", 1)[-1]
    for gatilhos, respostas in FRASES:
        for gatilho in gatilhos:
            sm.set_seq1(gatilho)
            corte = max(melhor_score, LIMIAR_FUZZY - 1e-9)
            if sm.real_quick_ratio() < corte or sm.quick_ratio() < corte:
                continue
            # Gatilhos "prefixo + nome curto" (repertorio_cultura): sem isto, "fala sobre a mae"
            # casava com "fala sobre marte" só pelo prefixo. A última palavra tem que ser parecida.
            if gatilho in GATILHOS_FUZZY_ESTRITOS and \
                    SequenceMatcher(None, ultima_palavra, gatilho.rsplit(" ", 1)[-1]).ratio() < 0.8:
                continue
            score = sm.ratio()
            if score > melhor_score:
                melhor_score, melhor_respostas = score, respostas

    if melhor_score >= LIMIAR_FUZZY:
        return melhor_respostas
    return None


def _buscar_em_frases(texto: str):
    respostas = _buscar_entrada(texto)
    return _escolher(respostas) if respostas else None


# ============================================================
# CONTEXTO DA CONVERSA
# ============================================================
# O robô guarda a última resposta por alguns minutos para (1) não repetir a mesma
# frase em sequência quando a entrada tem várias respostas, e (2) atender pedidos
# que dependem do que ele acabou de dizer: "outra", "repete", "conta mais".
# O estado é global: o robô conversa com uma pessoa por vez.

CONTEXTO_VALIDADE_SEGUNDOS = 60
_RECENTES = collections.deque(maxlen=12)   # últimas respostas dadas (para não repetir)
_ESTADO = {"entrada": None, "pergunta": None, "resposta": None, "quando": 0.0}


def _expirar_contexto() -> None:
    """Esquece tudo (última resposta e respostas recentes) se passou
    CONTEXTO_VALIDADE_SEGUNDOS sem conversa. Contado desde a última atividade,
    para não apagar a memória no meio de uma conversa."""
    if _ESTADO["quando"] and time.time() - _ESTADO["quando"] >= CONTEXTO_VALIDADE_SEGUNDOS:
        esquecer_contexto()


def _escolher(respostas):
    """Sorteia uma resposta, evitando as dadas há pouco (e nunca a última, se houver outra)."""
    _expirar_contexto()
    if len(respostas) == 1:
        escolhida = respostas[0]
    else:
        opcoes = ([r for r in respostas if r not in _RECENTES]
                  or [r for r in respostas if r != _ESTADO["resposta"]]
                  or respostas)
        escolhida = random.choice(opcoes)
    _RECENTES.append(escolhida)
    return escolhida


def _contexto_valido():
    if _ESTADO["resposta"] and time.time() - _ESTADO["quando"] < CONTEXTO_VALIDADE_SEGUNDOS:
        return _ESTADO
    return None


def esquecer_contexto() -> None:
    """Zera a memória da conversa (para testes ou quando chega uma pessoa nova)."""
    _RECENTES.clear()
    _ESTADO.update(entrada=None, pergunta=None, resposta=None, quando=0.0)


def _guardar_contexto(pergunta, resposta, entrada) -> None:
    _ESTADO.update(entrada=entrada, pergunta=pergunta, resposta=resposta, quando=time.time())


def _resposta_contextual(texto: str, ao_gerar_frase=None, ao_pensar=None):
    """Atende "outra", "repete" e "conta mais" usando a última resposta.
    Devolve None se a fala não é desse tipo (segue o fluxo normal)."""
    exato_outra = texto in rc.GATILHOS_OUTRA_EXATO
    exato_mais = texto in rc.GATILHOS_MAIS_EXATO
    ultimo = _contexto_valido()

    if not ultimo:
        # "outra" solta, sem nada antes: melhor perguntar do que mandar pra IA
        if exato_outra or exato_mais:
            return random.choice(rc.SEM_CONTEXTO_OUTRA)
        return None

    if any(_contem(texto, g) for g in rc.GATILHOS_REPETIR_CONTEM):
        print("[BRAIN] -> contexto: repetindo a última resposta")
        return "Claro! " + ultimo["resposta"]

    if exato_outra or exato_mais:
        entrada = ultimo["entrada"]
        if entrada and len(entrada) > 1:
            print("[BRAIN] -> contexto: outra resposta da mesma entrada")
            resposta = _escolher(entrada)
            _guardar_contexto(ultimo["pergunta"], resposta, entrada)
            return resposta
        if exato_mais and MODO_RESPOSTA in ("hibrido", "api") and _api_disponivel():
            print("[BRAIN] -> contexto: IA continua o assunto")
            if ao_pensar:
                ao_pensar()
            pedido = (f"Antes a pessoa perguntou: {ultimo['pergunta']}. "
                      f"Você respondeu: {ultimo['resposta']} "
                      f"Agora ela pediu: {texto}. Continue o assunto com informação nova, "
                      f"em até duas frases curtas, sem repetir o que já disse.")
            resposta = _gerar_com_api(pedido, ao_gerar_frase)
            if resposta:
                _guardar_contexto(ultimo["pergunta"], resposta, None)
                return resposta
        return random.choice(rc.OUTRA_UNICA)
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


# chave (sem acento, como chega do reconhecedor) -> (nome falado com artigo, capital)
CAPITAIS = {
    "brasil": ("do Brasil", "Brasília"), "argentina": ("da Argentina", "Buenos Aires"),
    "uruguai": ("do Uruguai", "Montevidéu"), "paraguai": ("do Paraguai", "Assunção"),
    "chile": ("do Chile", "Santiago"), "peru": ("do Peru", "Lima"),
    "bolivia": ("da Bolívia", "La Paz"), "colombia": ("da Colômbia", "Bogotá"),
    "venezuela": ("da Venezuela", "Caracas"), "equador": ("do Equador", "Quito"),
    "estados unidos": ("dos Estados Unidos", "Washington"), "canada": ("do Canadá", "Ottawa"),
    "mexico": ("do México", "Cidade do México"), "cuba": ("de Cuba", "Havana"),
    "costa rica": ("da Costa Rica", "San José"), "panama": ("do Panamá", "Cidade do Panamá"),
    "guatemala": ("da Guatemala", "Cidade da Guatemala"),
    "portugal": ("de Portugal", "Lisboa"), "espanha": ("da Espanha", "Madri"),
    "franca": ("da França", "Paris"), "italia": ("da Itália", "Roma"),
    "alemanha": ("da Alemanha", "Berlim"), "reino unido": ("do Reino Unido", "Londres"),
    "inglaterra": ("da Inglaterra", "Londres"), "irlanda": ("da Irlanda", "Dublin"),
    "holanda": ("da Holanda", "Amsterdã"), "paises baixos": ("dos Países Baixos", "Amsterdã"),
    "belgica": ("da Bélgica", "Bruxelas"), "suica": ("da Suíça", "Berna"),
    "austria": ("da Áustria", "Viena"), "grecia": ("da Grécia", "Atenas"),
    "noruega": ("da Noruega", "Oslo"), "suecia": ("da Suécia", "Estocolmo"),
    "finlandia": ("da Finlândia", "Helsinque"), "dinamarca": ("da Dinamarca", "Copenhague"),
    "islandia": ("da Islândia", "Reykjavík"), "polonia": ("da Polônia", "Varsóvia"),
    "hungria": ("da Hungria", "Budapeste"), "republica tcheca": ("da República Tcheca", "Praga"),
    "ucrania": ("da Ucrânia", "Kiev"), "russia": ("da Rússia", "Moscou"),
    "turquia": ("da Turquia", "Ancara"), "israel": ("de Israel", "Jerusalém"),
    "ira": ("do Irã", "Teerã"), "iraque": ("do Iraque", "Bagdá"),
    "arabia saudita": ("da Arábia Saudita", "Riad"), "egito": ("do Egito", "Cairo"),
    "marrocos": ("do Marrocos", "Rabat"), "nigeria": ("da Nigéria", "Abuja"),
    "quenia": ("do Quênia", "Nairóbi"), "africa do sul": ("da África do Sul", "Pretória"),
    "angola": ("de Angola", "Luanda"), "mocambique": ("de Moçambique", "Maputo"),
    "cabo verde": ("de Cabo Verde", "Praia"), "china": ("da China", "Pequim"),
    "japao": ("do Japão", "Tóquio"), "coreia do sul": ("da Coreia do Sul", "Seul"),
    "coreia do norte": ("da Coreia do Norte", "Pyongyang"), "india": ("da Índia", "Nova Délhi"),
    "tailandia": ("da Tailândia", "Bangcoc"), "vietna": ("do Vietnã", "Hanói"),
    "filipinas": ("das Filipinas", "Manila"), "indonesia": ("da Indonésia", "Jacarta"),
    "australia": ("da Austrália", "Camberra"), "nova zelandia": ("da Nova Zelândia", "Wellington"),
}

CAPITAIS.update({
    "mongolia": ("da Mongólia", "Ulan Bator"), "cazaquistao": ("do Cazaquistão", "Astana"),
    "afeganistao": ("do Afeganistão", "Cabul"), "paquistao": ("do Paquistão", "Islamabad"),
    "bangladesh": ("de Bangladesh", "Daca"), "nepal": ("do Nepal", "Katmandu"),
    "malasia": ("da Malásia", "Kuala Lumpur"), "singapura": ("de Singapura", "Singapura"),
    "camboja": ("do Camboja", "Nom Pen"), "laos": ("do Laos", "Vienciana"),
    "taiwan": ("de Taiwan", "Taipé"), "siria": ("da Síria", "Damasco"),
    "jordania": ("da Jordânia", "Amã"), "libano": ("do Líbano", "Beirute"),
    "kuwait": ("do Kuwait", "Cidade do Kuwait"), "catar": ("do Catar", "Doha"),
    "emirados arabes unidos": ("dos Emirados Árabes Unidos", "Abu Dabi"),
    "emirados arabes": ("dos Emirados Árabes Unidos", "Abu Dabi"),
    "oma": ("de Omã", "Mascate"), "iemen": ("do Iêmen", "Sanaa"),
    "etiopia": ("da Etiópia", "Adis Abeba"), "gana": ("de Gana", "Acra"),
    "senegal": ("do Senegal", "Dacar"), "argelia": ("da Argélia", "Argel"),
    "tunisia": ("da Tunísia", "Túnis"), "libia": ("da Líbia", "Trípoli"),
    "sudao": ("do Sudão", "Cartum"), "tanzania": ("da Tanzânia", "Dodoma"),
    "uganda": ("de Uganda", "Campala"), "camaroes": ("de Camarões", "Iaundé"),
    "zimbabue": ("do Zimbábue", "Harare"), "zambia": ("da Zâmbia", "Lusaka"),
    "namibia": ("da Namíbia", "Vinduque"), "botsuana": ("de Botsuana", "Gaborone"),
    "madagascar": ("de Madagascar", "Antananarivo"), "guine bissau": ("da Guiné-Bissau", "Bissau"),
    "romenia": ("da Romênia", "Bucareste"), "bulgaria": ("da Bulgária", "Sófia"),
    "servia": ("da Sérvia", "Belgrado"), "croacia": ("da Croácia", "Zagreb"),
    "eslovenia": ("da Eslovênia", "Liubliana"), "eslovaquia": ("da Eslováquia", "Bratislava"),
    "lituania": ("da Lituânia", "Vilnius"), "letonia": ("da Letônia", "Riga"),
    "estonia": ("da Estônia", "Tallinn"), "bielorrussia": ("da Bielorrússia", "Minsk"),
    "luxemburgo": ("de Luxemburgo", "Luxemburgo"), "malta": ("de Malta", "Valeta"),
    "chipre": ("do Chipre", "Nicósia"), "albania": ("da Albânia", "Tirana"),
    "georgia": ("da Geórgia", "Tbilisi"), "armenia": ("da Armênia", "Erevan"),
    "azerbaijao": ("do Azerbaijão", "Baku"), "haiti": ("do Haiti", "Porto Príncipe"),
    "republica dominicana": ("da República Dominicana", "Santo Domingo"),
    "jamaica": ("da Jamaica", "Kingston"), "honduras": ("de Honduras", "Tegucigalpa"),
    "nicaragua": ("da Nicarágua", "Manágua"), "el salvador": ("de El Salvador", "San Salvador"),
    "guiana": ("da Guiana", "Georgetown"), "suriname": ("do Suriname", "Paramaribo"),
    "bahamas": ("das Bahamas", "Nassau"), "fiji": ("de Fiji", "Suva"),
    "papua nova guine": ("da Papua-Nova Guiné", "Port Moresby"),
})

# capitais dos estados brasileiros. As chaves incluem a preposição ("do", "de")
# quando o nome sozinho seria ambíguo ("para" é estado e também preposição), e
# os nomes mais longos vêm antes ("mato grosso do sul" antes de "mato grosso").
CAPITAIS_ESTADOS = [
    (["rio grande do sul", "do rs"], "do Rio Grande do Sul", "Porto Alegre"),
    (["rio grande do norte"], "do Rio Grande do Norte", "Natal"),
    (["mato grosso do sul"], "de Mato Grosso do Sul", "Campo Grande"),
    (["mato grosso"], "de Mato Grosso", "Cuiabá"),
    (["santa catarina"], "de Santa Catarina", "Florianópolis"),
    (["parana"], "do Paraná", "Curitiba"),
    (["estado de sao paulo", "de sao paulo"], "do estado de São Paulo", "São Paulo"),
    (["estado do rio de janeiro", "do rio de janeiro", "do rio"], "do estado do Rio de Janeiro", "Rio de Janeiro"),
    (["minas gerais", "de minas"], "de Minas Gerais", "Belo Horizonte"),
    (["espirito santo"], "do Espírito Santo", "Vitória"),
    (["bahia"], "da Bahia", "Salvador"),
    (["sergipe"], "de Sergipe", "Aracaju"),
    (["alagoas"], "de Alagoas", "Maceió"),
    (["pernambuco"], "de Pernambuco", "Recife"),
    (["paraiba"], "da Paraíba", "João Pessoa"),
    (["ceara"], "do Ceará", "Fortaleza"),
    (["piaui"], "do Piauí", "Teresina"),
    (["maranhao"], "do Maranhão", "São Luís"),
    (["do para", "estado do para"], "do Pará", "Belém"),
    (["amapa"], "do Amapá", "Macapá"),
    (["amazonas"], "do Amazonas", "Manaus"),
    (["roraima"], "de Roraima", "Boa Vista"),
    (["rondonia"], "de Rondônia", "Porto Velho"),
    (["acre"], "do Acre", "Rio Branco"),
    (["tocantins"], "do Tocantins", "Palmas"),
    (["goias"], "de Goiás", "Goiânia"),
    (["distrito federal"], "do Distrito Federal", "Brasília"),
]


def resposta_geografia(texto: str):
    if "capital" not in texto:
        return None
    for chaves, estado, capital in CAPITAIS_ESTADOS:
        if any(_contem(texto, c) for c in chaves):
            return f"A capital {estado} é {capital}."
    for chave, (pais, capital) in CAPITAIS.items():
        if _contem(texto, chave):
            return f"A capital {pais} é {capital}."
    # país fora do dicionário (ou capital de estado): deixa a base de frases
    # ou a IA responderem
    return None


# ============================================================
# HORA E DATA
# ============================================================

_DIAS_SEMANA = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
                "sexta-feira", "sábado", "domingo"]
_MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
          "agosto", "setembro", "outubro", "novembro", "dezembro"]


def resposta_hora_data(texto: str):
    from datetime import datetime
    from zoneinfo import ZoneInfo
    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))  # horario de Brasilia (o sistema esta em UTC)
    if any(_contem(texto, g) for g in ["que horas sao", "que hora e", "que horas e", "horas sao", "me fala as horas",
                                        "me diz as horas", "me diga as horas", "que horas",
                                        "qual a hora", "qual e a hora", "me diz a hora",
                                        "sabe que horas"]):
        if agora.minute == 0:
            return f"Agora são {agora.hour} horas em ponto."
        minutos = "1 minuto" if agora.minute == 1 else f"{agora.minute} minutos"
        horas = "1 hora" if agora.hour == 1 else f"{agora.hour} horas"
        return f"Agora são {horas} e {minutos}."
    if any(_contem(texto, g) for g in ["que dia e hoje", "qual o dia de hoje",
                                        "qual e o dia de hoje", "que dia da semana",
                                        "qual a data", "qual e a data", "data de hoje",
                                        "dia e hoje", "hoje que dia", "que dia e", "que dia estamos",
                                        "em que dia estamos", "hoje e que dia"]):
        return (f"Hoje é {_DIAS_SEMANA[agora.weekday()]}, {agora.day} de "
                f"{_MESES[agora.month - 1]} de {agora.year}.")
    if any(_contem(texto, g) for g in ["que ano e", "em que ano estamos", "qual o ano"]):
        return f"Estamos em {agora.year}."
    if any(_contem(texto, g) for g in ["que mes e", "em que mes estamos", "qual o mes"]):
        return f"Estamos em {_MESES[agora.month - 1]}."
    return None



# ============================================================
# FILTRO DE RUIDO DO RECONHECEDOR
# ============================================================
# O Vosk pequeno as vezes entrega "frases" sem sentido ("uma duas cinquenta
# pele", "serie legal"). Mandar isso pro LLM de 1B so gera respostas inventadas
# ("voce quer que eu diga que nao entendi?"). Uma fala dirigida ao robo quase
# sempre tem uma palavra de pergunta, um verbo de pedido ou se dirige a ele.
_PALAVRAS_PERGUNTA = frozenset("""
    que quem qual quais quanto quantos quanta quantas como onde quando porque por cade
    fale fala diga conte conta explique explica mostre mostra cante canta ensine ensina
    descreva responda me pode poderia sabe consegue quer gosta tem existe faz
    voce tu seu sua robo
""".split())
_NUMEROS_SOLTOS = frozenset(_NUMEROS_POR_EXTENSO) | {"trinta", "quarenta", "cinquenta", "sessenta",
                                                      "setenta", "oitenta", "noventa", "cem", "mil"}


_INICIO_PERGUNTA = frozenset("""qual quais quem quando onde aonde como quanto quantos quantas quanta porque por
    que o a me voce tu fale fala conte conta diga diz explique explica cante canta toque toca mostre mostra
    descreva responda pode poderia sabe consegue""".split())
_ENDERECO = frozenset("voce tu robo c2 c2gelsa".split())


def parece_dirigida(texto: str) -> bool:
    """Frases longas: so conta como dirigida ao robo se chama por ele (voce, robo...) ou se
    comeca como pergunta/pedido. Conversa de fundo tem "que", "como", "tem" no meio e passava
    pelo filtro de palavras de pergunta."""
    palavras = texto.split()
    if _ENDERECO.intersection(palavras):
        return True
    return bool(_INICIO_PERGUNTA.intersection(palavras[:2])) and any(p in _PALAVRAS_PERGUNTA for p in palavras)


def pergunta_plausivel(texto: str) -> bool:
    """True se `texto` (ja corrigido/normalizado) parece uma fala dirigida ao robo."""
    palavras = texto.split()
    if len(palavras) < 2:
        return False
    if sum(p in _NUMEROS_SOLTOS for p in palavras) * 2 >= len(palavras):
        return False       # "uma duas cinquenta ..." = ruido
    if not any(p in _PALAVRAS_PERGUNTA for p in palavras):
        return False
    return len(palavras) < PALAVRAS_FRASE_LONGA - 2 or parece_dirigida(texto)


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
    cortou = False  # o Ollama parou por num_predict (resposta cortada no meio)

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
                    cortou = pedaco.get("done_reason") == "length"
                    break
        # resposta cortada pelo limite de tokens: descarta a frase incompleta
        # (a não ser que seja tudo o que temos)
        if not (cortou and texto_total.strip()
                and not buffer.rstrip().endswith((".", "!", "?"))):
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

    _expirar_contexto()
    resposta = _resposta_contextual(texto, ao_gerar_frase, ao_pensar)
    if resposta:
        return resposta

    _entrada_da_vez[0] = None
    resposta = _gerar_resposta_normal(pergunta_bruta, texto, ao_gerar_frase, ao_pensar)
    if resposta and resposta not in FRASES_NAO_ENTENDI:
        _guardar_contexto(texto, resposta, _entrada_da_vez[0])
    return resposta


_entrada_da_vez = [None]   # entrada do repertório usada na resposta atual (para "outra")


def _gerar_resposta_normal(pergunta_bruta: str, texto: str, ao_gerar_frase=None, ao_pensar=None) -> str:

    resposta = resposta_matematica(texto)
    if resposta:
        print("[BRAIN] -> matemática")
        return resposta

    resposta = resposta_geografia(texto)
    if resposta:
        print("[BRAIN] -> geografia")
        return resposta

    resposta = resposta_hora_data(texto)
    if resposta:
        print("[BRAIN] -> hora/data")
        return resposta

    if MODO_RESPOSTA != "api":
        entrada = _buscar_entrada(texto)
        if entrada:
            print("[BRAIN] -> base de frases")
            _entrada_da_vez[0] = entrada
            return _escolher(entrada)

    if not pergunta_plausivel(texto):
        if len(texto.split()) >= PALAVRAS_RUIDO_MUDO:
            # papo de fundo captado pelo microfone: responder ("nao entendi") so atrapalha
            print("[BRAIN] -> papo de fundo, ficando quieto (sem LLM)")
            return ""
        print("[BRAIN] -> ruido do reconhecedor, pedindo pra repetir (sem LLM)")
        return random.choice(FRASES_NAO_ENTENDI)

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