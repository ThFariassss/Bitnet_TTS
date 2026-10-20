"""
repertorio_contexto.py
Frases que só fazem sentido DEPOIS de uma resposta do robô ("outra", "repete",
"conta mais"). O brain.py usa a última resposta (guardada por poucos minutos)
para atendê-las; ver a seção "CONTEXTO DA CONVERSA" do brain.py.

Dois tipos de gatilho:
  - EXATO: a fala inteira tem que ser igual (evita pegar "fala mais alto" por
    causa de "fala mais").
  - CONTEM: basta a expressão aparecer na fala, como palavras inteiras.

Tudo aqui também entra na gramática do reconhecedor de voz (ver
gatilhos_gramatica.py), por isso os gatilhos vão sem acento e minúsculos.
"""

# "outra piada" sem dizer o assunto: sorteia outra resposta da mesma entrada
GATILHOS_OUTRA_EXATO = {
    "outra", "outro", "mais uma", "mais um", "outra por favor", "outro por favor",
    "mais uma por favor", "quero outra", "quero outro", "tem outra", "tem outro",
    "e outra", "e outro", "outra vez", "me da outra", "me de outra", "conta outra",
    "conte outra", "de novo", "mais outra", "mais outro",
}

# "conta mais", "continua": outra resposta da mesma entrada, ou a IA continua o assunto
GATILHOS_MAIS_EXATO = {
    "conta mais", "conte mais", "fala mais", "fale mais", "me conta mais", "me fale mais",
    "continua", "continue", "pode continuar", "e depois", "e entao", "quero saber mais",
    "mais detalhes", "me explica melhor", "explica melhor", "explique melhor",
}

# "repete": repete a última resposta, palavra por palavra
GATILHOS_REPETIR_CONTEM = [
    "repete", "repita", "pode repetir", "repete a resposta", "pode repetir a resposta",
    "repete isso", "o que voce disse", "o que voce falou", "fale de novo", "fala de novo",
    "nao entendi", "nao entendi a resposta", "nao entendi nada", "explica de novo", "explique de novo",
]

SEM_CONTEXTO_OUTRA = [
    "Outra o quê? Me pergunte alguma coisa, por exemplo uma piada ou uma curiosidade!",
    "Ainda não falamos de nada! Peça uma piada, uma curiosidade ou faça uma pergunta.",
]
OUTRA_UNICA = [
    "Essa eu só sei de um jeito! Pergunte outra coisa, que eu tento ajudar.",
    "Sobre isso eu só sei essa resposta. Quer perguntar outra coisa?",
]


def gatilhos_para_gramatica():
    """Todas as expressões, para o gerar_gramatica.py incluir no reconhecedor de voz."""
    return sorted(GATILHOS_OUTRA_EXATO | GATILHOS_MAIS_EXATO | set(GATILHOS_REPETIR_CONTEM))
