"""
cantar.py
Faz o C-2GELSA "cantar" Parabéns pra Você e a Marcha Imperial (Star Wars).

O Piper só fala, então a canção é montada sílaba por sílaba: cada sílaba da letra é
sintetizada pelo Piper, tem o tom (altura) ajustado para a nota da melodia e a duração
esticada para o tempo da nota. Por cima vai um acompanhamento suave com a mesma melodia,
que ajuda o ouvido a achar a música. O resultado é robótico, de propósito.

Uso (o servidor_conversa.py já faz isso):
    cantar.qual_musica(texto_corrigido)    -> "parabens", "marcha" ou None
    cantar.eh_pedido(texto_corrigido)      -> True se pediram alguma música
    cantar.cantar(tts, chave)              -> bytes de um WAV (usa cache em disco)
    cantar.parabens(tts)                   -> atalho para cantar(tts, "parabens")

Para testar sem o robô:
    python3 cantar.py [parabens|marcha]    -> grava /tmp/<musica>.wav
Para mudar uma música, edite a letra dela (sílaba, nota, tempos) ou o andamento.
Para acrescentar outra, crie a letra e uma entrada em MUSICAS.
Precisa de numpy e scipy (o venv do projeto tem).
"""
import hashlib
import io
import os
import wave

GATILHOS_PARABENS = [
    "canta parabens", "cante parabens", "canta o parabens", "cante o parabens",
    "canta parabens pra voce", "canta parabens para mim", "canta parabens pra mim",
    "canta parabens para ele", "canta parabens para ela", "canta parabens pra ele", "canta parabens pra ela",
    "canta parabens para ele", "voce canta parabens", "voce sabe cantar parabens",
    "canta feliz aniversario", "cante feliz aniversario", "canta o feliz aniversario",
    "canta a musica de aniversario", "canta a musica do aniversario", "cante a musica de aniversario",
    "canta musica de aniversario", "canta a cancao de aniversario", "canta o parabens pra voce",
    "canta parabens a voce", "canta parabens a todos", "canta o parabens para todos",
    "canta parabens para todo mundo", "canta uma musica de aniversario", "canta parabens a voce",
    "canta parabens pra todos", "canta parabens pra todo mundo",
    # variações de pedido ("consegue cantar...", "cantar...", "cante um...")
    "cantar feliz aniversario", "cantar parabens", "cantar o parabens", "cantar o feliz aniversario",
    "cantar a musica de aniversario", "cantar a musica do aniversario", "cantar musica de aniversario",
    "cante um feliz aniversario", "canta um feliz aniversario", "cante um parabens", "canta um parabens",
    "consegue cantar feliz aniversario", "consegue cantar parabens", "consegue cantar o parabens",
    "sabe cantar feliz aniversario", "sabe cantar parabens", "sabe cantar o parabens",
    "voce sabe cantar feliz aniversario", "voce consegue cantar feliz aniversario",
    "voce consegue cantar parabens", "pode cantar feliz aniversario", "pode cantar parabens",
    "pode cantar o parabens", "pode cantar o feliz aniversario", "quero ouvir feliz aniversario",
    "quero ouvir parabens pra voce", "canta pra mim feliz aniversario", "canta pra ele feliz aniversario",
    "canta pra ela feliz aniversario", "cante pra mim feliz aniversario", "cante pra ele feliz aniversario",
    "cante pra ela feliz aniversario", "cante parabens pra voce", "cante parabens para ele",
    "cante parabens para ela", "cante parabens pra ele", "cante parabens pra ela", "cante parabens para mim",
    "cante parabens pra mim", "cante parabens para todos", "cante parabens pra todos",
]

# Semitons acima da nota-base ("sol" da melodia). Parabéns em maior: sol sol lá sol dó' si ...
_G, _A, _B, _C, _D, _E, _F, _G2 = 0, 2, 4, 5, 7, 9, 10, 12

# (sílaba como o Piper deve falar, nota em semitons, duração em tempos)
LETRA = [
    ("pa", _G, .75), ("ra", _G, .25), ("béns", _A, 1), ("pra", _G, 1), ("vo", _C, 1), ("cê", _B, 2),
    ("nes", _G, .75), ("ta", _G, .25), ("da", _A, 1), ("ta", _G, 1), ("quê", _D, 1), ("ri", _C, 1), ("da", _C, 2),
    ("mui", _G, .75), ("tas", _G, .25), ("fe", _G2, 1), ("li", _E, 1), ("ci", _C, 1), ("da", _B, 1), ("des", _A, 2),
    ("mui", _F, .75), ("tos", _F, .25), ("a", _E, 1), ("nos", _C, 1), ("de", _D, 1), ("vi", _C, 1), ("da", _C, 2),
]
# Fim de cada verso: pausa curtinha depois da sílaba de índice (para respirar)
_PAUSAS_APOS = {5: 0.5, 12: 0.5, 19: 0.5}

ANDAMENTO_BPM = 92           # tempos por minuto
NOTA_BASE_HZ = 130.8         # a nota "sol" da melodia (aqui, dó: cabe na voz grave do Faber)
ACOMPANHAMENTO = 0.22        # volume da melodia de fundo (0 desliga)
VERSAO = "2"                 # mude para invalidar o cache em disco


# Marcha Imperial (tema do Darth Vader), em sol menor, sem letra: o robô "canta" tan-ta-ran.
# Notas em semitons a partir do sol: mi bemol = -4, si bemol = 3, ré' = 7, mi bemol' = 8, fá sustenido = -1.
_Mb, _Sb, _R2, _Mb2, _Fs = -4, 3, 7, 8, -1
_MARCHA_A = [("tan", _G, 1), ("tan", _G, 1), ("tan", _G, 1), ("ta", _Mb, .75), ("ran", _Sb, .25),
             ("tan", _G, 1), ("ta", _Mb, .75), ("ran", _Sb, .25), ("tan", _G, 2)]
_MARCHA_B = [("tan", _R2, 1), ("tan", _R2, 1), ("tan", _R2, 1), ("ta", _Mb2, .75), ("ran", _Sb, .25),
             ("tan", _Fs, 1), ("ta", _Mb, .75), ("ran", _Sb, .25), ("tan", _G, 2)]
LETRA_MARCHA = _MARCHA_A + _MARCHA_B + _MARCHA_A
_PAUSAS_MARCHA = {8: 0.5, 17: 0.5}

_TAXA = 22050
_CACHE_DIR = os.path.expanduser("~/.cache/lsa-cantar")


GATILHOS_MARCHA = []   # só com verbo ("canta ..."): "o que é a marcha imperial" é pergunta, não pedido
for _v in ("canta", "cante", "cantar", "toca", "toque", "tocar", "voce canta", "voce toca", "voce sabe cantar",
           "voce consegue cantar", "voce sabe tocar", "sabe cantar", "consegue cantar", "pode cantar", "pode tocar",
           "quero ouvir", "canta pra mim", "cante pra mim"):
    for _o in ("a marcha imperial", "a marcha imperial do star wars", "o tema do darth vader",
               "a musica do darth vader", "a musica do star wars", "o tema do star wars", "a musica do imperio"):
        GATILHOS_MARCHA.append("%s %s" % (_v, _o))

MUSICAS = {
    "parabens": dict(letra=LETRA, pausas=_PAUSAS_APOS, bpm=ANDAMENTO_BPM, base=NOTA_BASE_HZ,
                     acomp=ACOMPANHAMENTO, gatilhos=GATILHOS_PARABENS,
                     falada="Parabéns pra você, nesta data querida, muitas felicidades, muitos anos de vida!"),
    "marcha": dict(letra=LETRA_MARCHA, pausas=_PAUSAS_MARCHA, bpm=100, base=146.8,
                   acomp=0.28, gatilhos=GATILHOS_MARCHA,
                   falada="Tan, tan, tan, tan ta ran, tan ta ran, tan!"),
}

def qual_musica(texto_corrigido: str):
    """Chave da música pedida em MUSICAS ("parabens", "marcha") ou None. A mais específica ganha."""
    import re
    for chave in ("marcha", "parabens"):
        if any(re.search(r"\b%s\b" % re.escape(g), texto_corrigido) for g in MUSICAS[chave]["gatilhos"]):
            return chave
    return None


def eh_pedido(texto_corrigido: str) -> bool:
    return qual_musica(texto_corrigido) is not None


# ---------------------------------------------------------------- áudio básico

def _ler_wav(dados):
    import numpy as np
    w = wave.open(io.BytesIO(dados))
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    if w.getnchannels() > 1:
        x = x.reshape(-1, w.getnchannels()).mean(axis=1)
    return x, w.getframerate()


def _gravar_wav(x, taxa=_TAXA):
    import numpy as np
    buf = io.BytesIO()
    w = wave.open(buf, "wb")
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(taxa)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    w.close()
    return buf.getvalue()


def _aparar(x, limiar=0.02):
    """Tira o silêncio do começo e do fim."""
    import numpy as np
    ativo = np.where(np.abs(x) > limiar * max(1e-9, np.abs(x).max()))[0]
    if len(ativo) == 0:
        return x
    return x[max(0, ativo[0] - 40): ativo[-1] + 40]


def _analise_tom(x, taxa=_TAXA, passo=128, janela=1024):
    """(centros, periodos): período (em amostras) em cada quadro; NaN onde não há voz.
    Autocorrelação simples; serve para a voz grave e falada do Piper."""
    import numpy as np
    lag_min, lag_max = int(taxa / 400), int(taxa / 70)
    centros, periodos = [], []
    for ini in range(0, max(1, len(x) - janela), passo):
        q = x[ini: ini + janela]
        centros.append(ini + len(q) // 2)
        if len(q) < janela or np.abs(q).max() < 0.03:
            periodos.append(np.nan)
            continue
        q = q - q.mean()
        ac = np.correlate(q, q, mode="full")[len(q) - 1:]
        if ac[0] <= 0:
            periodos.append(np.nan)
            continue
        ac = ac / ac[0]
        lag = lag_min + int(np.argmax(ac[lag_min:lag_max]))
        periodos.append(float(lag) if ac[lag] > 0.45 else np.nan)
    return np.array(centros, dtype=float), np.array(periodos, dtype=float)


def _marcas_de_tom(x, ini, fim, periodo_em):
    """Posições (amostras) de um pico por período dentro de x[ini:fim]."""
    import numpy as np
    t0 = int(periodo_em(ini))
    s0 = ini + int(np.argmax(x[ini: ini + max(2, t0)]))
    marcas = [s0]
    while True:
        t = periodo_em(marcas[-1])
        prox = marcas[-1] + t
        if prox + t > fim:
            break
        lo, hi = int(prox - 0.25 * t), int(prox + 0.25 * t) + 1
        marcas.append(lo + int(np.argmax(x[lo:hi])))
    return np.array(marcas)


def _psola(x, ini, fim, marcas, periodo_em, nota_hz, n_saida, vibrato=0.0):
    """Reconstrói x[ini:fim] com `n_saida` amostras e tom `nota_hz`, repetindo/pulando períodos
    da própria voz (TD-PSOLA): o timbre e as vogais se mantêm, só muda o tom e a duração."""
    import numpy as np
    saida = np.zeros(n_saida + 4096)
    peso = np.zeros_like(saida)
    t_alvo = _TAXA / nota_hz
    pos = t_alvo
    rng = np.random.RandomState(7)
    while pos < n_saida - t_alvo / 2:
        fracao = pos / max(1, n_saida)
        alvo_src = ini + fracao * (fim - ini)
        k = int(np.argmin(np.abs(marcas - alvo_src)))
        k = min(max(k + rng.randint(-1, 2), 0), len(marcas) - 1)   # variação mínima: evita zumbido
        m = int(marcas[k])
        ts = max(8, int(periodo_em(m)))
        a, b = max(0, m - ts), min(len(x), m + ts)
        grao = np.zeros(2 * ts)
        grao[ts - (m - a): ts + (b - m)] = x[a:b]
        grao *= np.hanning(2 * ts)
        c = int(pos)
        saida[c - ts: c + ts] += grao if c - ts >= 0 else 0
        peso[c - ts: c + ts] += np.hanning(2 * ts) if c - ts >= 0 else 0
        t = pos / _TAXA
        passo = t_alvo * (1 + vibrato * np.sin(2 * np.pi * 5.5 * t) * min(1.0, max(0.0, (t - 0.25) / 0.3)))
        pos += passo
    return saida[:n_saida] / np.maximum(peso[:n_saida], 0.35)


def _silaba_cantada(x, nota_hz, duracao_s):
    """Pega a sílaba falada `x` e devolve ela cantada na nota e duração pedidas."""
    import numpy as np
    x = _aparar(x)
    centros, periodos = _analise_tom(x)
    voz = np.where(~np.isnan(periodos))[0]
    alvo = int(duracao_s * _TAXA)
    if len(voz) < 3:                       # sem trecho com voz: toca como falou, no tamanho certo
        return np.interp(np.linspace(0, len(x) - 1, alvo), np.arange(len(x)), x)
    mediano = float(np.median(periodos[voz]))
    periodo_em = lambda s: float(np.interp(s, centros[voz], periodos[voz]))
    passo = int(centros[1] - centros[0])
    n_ini = int(max(0, centros[voz[0]] - passo))
    n_fim = int(min(len(x), centros[voz[-1]] + passo))
    inicio, nucleo, coda = x[:n_ini], (n_ini, n_fim), x[n_fim:]
    marcas = _marcas_de_tom(x, n_ini, n_fim, periodo_em)
    n_nucleo = max(int(0.08 * _TAXA), alvo - len(inicio) - len(coda))
    if len(marcas) < 3:
        return np.interp(np.linspace(0, len(x) - 1, alvo), np.arange(len(x)), x)
    cantada = _psola(x, n_ini, n_fim, marcas, periodo_em, nota_hz, n_nucleo,
                     vibrato=0.012 if duracao_s > 0.8 else 0.0)
    # o nível do núcleo acompanha o da sílaba original
    ref = np.sqrt(np.mean(x[n_ini:n_fim] ** 2)) + 1e-9
    cantada *= ref / (np.sqrt(np.mean(cantada ** 2)) + 1e-9)
    saida = np.concatenate([inicio, cantada, coda])
    rampa = min(len(saida) // 4, int(0.012 * _TAXA))
    if rampa > 1:
        saida[:rampa] *= np.linspace(0, 1, rampa)
        saida[-rampa:] *= np.linspace(1, 0, rampa)
    return saida


def _nota_hz(semitons, base=NOTA_BASE_HZ):
    return base * 2 ** (semitons / 12.0)


def _tom_suave(freq, duracao_s):
    """Nota de fundo: onda quase triangular com decaimento (soa como um carrilhão)."""
    import numpy as np
    n = int(duracao_s * _TAXA)
    t = np.arange(n) / _TAXA
    onda = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t) + 0.1 * np.sin(6 * np.pi * freq * t)
    env = np.minimum(1, t / 0.01) * np.exp(-1.6 * t)
    return onda * env


def _montar(tts, m=None):
    import numpy as np
    m = m or MUSICAS["parabens"]
    tempo = 60.0 / m["bpm"]
    pedacos, fundo, t_atual = [], [], 0.0
    for i, (silaba, semitons, tempos) in enumerate(m["letra"]):
        fala, taxa = _ler_wav(tts.sintetizar(silaba))
        if taxa != _TAXA:
            fala = np.interp(np.linspace(0, len(fala) - 1, int(len(fala) * _TAXA / taxa)), np.arange(len(fala)), fala)
        dur = tempos * tempo
        canto = _silaba_cantada(fala, _nota_hz(semitons, m["base"]), dur)
        pedacos.append(canto)
        # a melodia de fundo toca uma oitava acima, começando junto com a sílaba
        if m["acomp"]:
            fundo.append((int(t_atual * _TAXA), _tom_suave(_nota_hz(semitons + 12, m["base"]), min(dur * 1.1, 1.2))))
        silencio = m["pausas"].get(i, 0.0) * tempo
        t_atual += dur + silencio
        if silencio:
            pedacos.append(np.zeros(int(silencio * _TAXA)))
        # cada pedaço de voz tem a duração da nota, então a soma já bate com t_atual
    voz = np.concatenate(pedacos)
    voz = voz / max(1e-9, np.abs(voz).max()) * 0.85
    mix = voz.copy()
    for ini, nota in fundo:
        fim = min(len(mix), ini + len(nota))
        if ini < len(mix):
            mix[ini:fim] += nota[: fim - ini] * m["acomp"]
    mix = np.concatenate([np.zeros(int(0.15 * _TAXA)), mix, np.zeros(int(0.4 * _TAXA))])
    return _gravar_wav(mix / max(1.0, np.abs(mix).max() / 0.95))


def cantar(tts, chave="parabens"):
    """WAV da canção. Monta uma vez (uns segundos) e guarda em ~/.cache/lsa-cantar."""
    m = MUSICAS[chave]
    h = hashlib.sha1(("%s|%s|%s|%s|%s" % (VERSAO, m["letra"], m["bpm"], m["base"], m["acomp"])).encode()).hexdigest()[:12]
    caminho = os.path.join(_CACHE_DIR, "%s-%s.wav" % (chave, h))
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return f.read()
    wav = _montar(tts, m)
    try:
        os.makedirs(_CACHE_DIR, exist_ok=True)
        with open(caminho, "wb") as f:
            f.write(wav)
    except OSError:
        pass
    return wav


def parabens(tts):
    return cantar(tts, "parabens")


if __name__ == "__main__":
    import sys
    from piper_residente import Piper
    chave = sys.argv[1] if len(sys.argv) > 1 else "parabens"
    destino = "/tmp/%s.wav" % chave
    with open(destino, "wb") as f:
        f.write(_montar(Piper(), MUSICAS[chave]))
    print("gravado em", destino)
