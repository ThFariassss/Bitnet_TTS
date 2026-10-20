"""Ajusta o texto antes de ir pro TTS (o Piper nao sabe ler siglas/nomes proprios)."""
import re

# "C-2GELSA" sai fluido, "cê dois jélsa", sem pausas (antes soletrava o final)
_NOME_ROBO = re.compile(r"\bc[\s-]*2[\s-]*gelsa\b", re.IGNORECASE)
_NOME_SOLETRADO = "cê dois jélsa"

# apelido "C-2" (sozinho): cê, dois
_APELIDO = re.compile(r"\bc[\s-]*2\b", re.IGNORECASE)
_APELIDO_SOLETRADO = "cê dois"

# "PUCRS": "puc" junto e "RS" soletrado, sem pausas
_PUCRS = re.compile(r"\bpucrs\b", re.IGNORECASE)
_PUCRS_SOLETRADO = "puc érre ésse"


# "LSA" tambem sai soletrado: éle, ésse, á
_LSA = re.compile(r"\blsa\b", re.IGNORECASE)
_LSA_SOLETRADO = "éle, ésse, á"

# "Intel Core i7" (e i3/i5/i9): o Piper nao le "i7"; vira "i sete"
_INTEL_I = re.compile(r"\bi([3579])\b", re.IGNORECASE)


_UNID = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "onze",
         "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"]
_DEZ = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
_CENT = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos",
         "oitocentos", "novecentos"]


def _ate_999(n: int) -> str:
    if n < 20:
        return _UNID[n]
    if n < 100:
        d, u = divmod(n, 10)
        return _DEZ[d] + (" e " + _UNID[u] if u else "")
    if n == 100:
        return "cem"
    c, resto = divmod(n, 100)
    return _CENT[c] + (" e " + _ate_999(resto) if resto else "")


def por_extenso(n: int) -> str:
    """0 a 999999 em português; acima disso devolve os próprios dígitos."""
    if n >= 1_000_000:
        return str(n)
    if n < 1000:
        return _ate_999(n)
    mil, resto = divmod(n, 1000)
    inicio = "mil" if mil == 1 else _ate_999(mil) + " mil"
    if resto == 0:
        return inicio
    # "mil e cem", "dois mil e dois"; sem "e" quando sobra centena com dezena ("mil novecentos e sessenta")
    ligacao = " e " if resto < 100 or resto % 100 == 0 else " "
    return inicio + ligacao + _ate_999(resto)


# "3D" e "5G" antes dos dígitos soltos
_TRES_D = re.compile(r"\b3\s?d\b", re.IGNORECASE)
_CINCO_G = re.compile(r"\b5\s?g\b", re.IGNORECASE)
_NUMERO = re.compile(r"(?<![\w.,])\d+(?![\w.,]*\d)(?!,\d)")


# Siglas em MAIÚSCULAS que a voz não lê bem (só casa maiúscula, para não pegar palavras comuns)
_SIGLAS_FALADAS = {
    "GPS": "gê pê ésse", "TTS": "tê tê ésse", "DNA": "dê ene á", "CPU": "cê pê ú",
    "TV": "tê vê", "VAR": "vê á érre", "ROS": "rós", "ENIAC": "êniaque", "NVIDIA": "envídia",
}
_SIGLAS_RE = re.compile(r"\b(" + "|".join(_SIGLAS_FALADAS) + r")\b")


def para_fala(texto: str) -> str:
    texto = _NOME_ROBO.sub(_NOME_SOLETRADO, texto)
    texto = _APELIDO.sub(_APELIDO_SOLETRADO, texto)
    texto = _PUCRS.sub(_PUCRS_SOLETRADO, texto)
    texto = _INTEL_I.sub(lambda m: "i " + {"3": "três", "5": "cinco", "7": "sete", "9": "nove"}[m.group(1)], texto)
    texto = _SIGLAS_RE.sub(lambda m: _SIGLAS_FALADAS[m.group(1)], texto)
    texto = _TRES_D.sub("três dê", texto)
    texto = _CINCO_G.sub("cinco gê", texto)
    texto = _NUMERO.sub(lambda m: por_extenso(int(m.group(0))), texto)
    return _LSA.sub(_LSA_SOLETRADO, texto)
