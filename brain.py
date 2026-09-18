"""
brain.py
Gera uma frase em português a partir da lista de objetos detectados,
usando o BitNet.cpp (LLM de 1 bit rodando em CPU) via subprocess.

Se o BitNet não estiver configurado (repositório/modelo ausentes), usa
uma resposta de template (fallback_response) para o pipeline continuar
funcionando enquanto você configura o modelo.
"""

import os
import re
import subprocess

# ------------------------------------------------------------------
# AJUSTE ESTES DOIS CAMINHOS depois de clonar e preparar o BitNet.cpp
# (veja o README, seção 3).
# ------------------------------------------------------------------
BITNET_REPO = "/home/th/Downloads/BitNet"
BITNET_MODEL_REL = "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"

MAX_TOKENS = 40
TIMEOUT_SEGUNDOS = 60


def _bitnet_disponivel() -> bool:
    modelo = os.path.join(BITNET_REPO, BITNET_MODEL_REL)
    script = os.path.join(BITNET_REPO, "run_inference.py")
    return os.path.isfile(modelo) and os.path.isfile(script)


def _montar_prompt(descricao_objetos: str) -> str:
    return (
        "Você é um assistente que narra o que uma câmera está vendo, em "
        "português, em uma única frase curta, natural e amigável, sem "
        "listar tecnicamente os itens.\n"
        f"Objetos detectados: {descricao_objetos}.\n"
        "Frase:"
    )


#def gerar_resposta(descricao_objetos: str) -> str:
#    """Ponto de entrada principal: recebe a descrição dos objetos e devolve
#    uma frase falável em português."""
#    if _bitnet_disponivel():
 #       try:
  #          return _gerar_com_bitnet(descricao_objetos)
   #     except Exception as erro:
    #        print(f"[brain] BitNet falhou ({erro}); usando fallback.")
    #return fallback_response(descricao_objetos)
# Altere apenas esta função no seu brain.py

def gerar_resposta(descricao_objetos: str) -> str:
    """Ponto de entrada principal: recebe a descrição dos objetos e devolve
    uma frase falável de forma instantânea, sem carregar arquivos pesados."""
    
    # IGNORAR o BitNet temporariamente se quiser velocidade máxima em tempo real:
    return fallback_response(descricao_objetos)



def _gerar_com_bitnet(descricao_objetos: str) -> str:
    prompt = _montar_prompt(descricao_objetos)
    modelo = os.path.join(BITNET_REPO, BITNET_MODEL_REL)

    comando = [
        "python", "run_inference.py",
        "-m", modelo,
        "-p", prompt,
        "-n", str(MAX_TOKENS),
        "-temp", "0.7",
    ]

    resultado = subprocess.run(
        comando,
        cwd=BITNET_REPO,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SEGUNDOS,
    )

    if resultado.returncode != 0:
        raise RuntimeError(resultado.stderr.strip() or "erro desconhecido")

    return _limpar_saida(resultado.stdout, prompt)


def _limpar_saida(saida_bruta: str, prompt: str) -> str:
    """run_inference.py ecoa o prompt antes da geração; removemos isso e
    cortamos na primeira quebra de linha/ponto final para pegar só a frase."""
    texto = saida_bruta.replace(prompt, "").strip()
    texto = re.sub(r"\s+", " ", texto)
    # corta no primeiro ponto final para não trazer lixo de geração continuada
    match = re.search(r"[.!?]", texto)
    if match:
        texto = texto[: match.end()]
    return texto.strip() or fallback_response("")


def fallback_response(descricao_objetos: str) -> str:
    """Resposta de template, usada quando o BitNet não está configurado.
    Permite testar câmera -> texto -> voz sem precisar compilar nada."""
    if not descricao_objetos or descricao_objetos == "nada de reconhecível":
        return "Não estou vendo nada reconhecível agora."
    return f"Estou vendo o seguinte: {descricao_objetos}."
