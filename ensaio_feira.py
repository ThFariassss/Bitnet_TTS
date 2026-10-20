"""
ensaio_feira.py
Bateria automática de perguntas de feira, SEM microfone e SEM voz.
Serve para achar problemas no repertório antes do evento:

  1. perguntas que não têm resposta local (iriam para a IA);
  2. respostas longas demais para ouvir (limite padrão: 35 palavras);
  3. textos que a voz costuma ler mal (dígitos, siglas, parênteses, símbolos);
  4. gatilhos duplicados dentro do repertório (a resposta antiga vence a nova).

Uso:
    python3 ensaio_feira.py                 # roda tudo
    python3 ensaio_feira.py --palavras 25   # limite de palavras mais rígido
    python3 ensaio_feira.py --so-estatico   # só as verificações 2, 3 e 4 (não roda perguntas)

Para acrescentar perguntas de teste, edite PERGUNTAS_FEIRA abaixo.
"""
import re
import sys

import brain
import pronuncia
import repertorio

LIMITE_PALAVRAS = 35
if "--palavras" in sys.argv:
    LIMITE_PALAVRAS = int(sys.argv[sys.argv.index("--palavras") + 1])

# Perguntas que o público costuma fazer (escritas como o Vosk transcreve: sem pontuação)
PERGUNTAS_FEIRA = [
    # sobre o robô
    "qual o seu nome", "quem criou voce", "como voce funciona", "voce funciona sem internet",
    "voce usa inteligencia artificial", "voce aprende sozinho", "voce tem sentimentos",
    "voce vai dominar o mundo", "voce vai roubar meu emprego", "quanto voce custa",
    "voce e melhor que o chat gpt", "voce dorme", "voce tem amigos", "voce anda",
    "o que voce sabe fazer", "que camera voce usa", "voce me ve", "voce e de verdade",
    "voce mente", "isso e uma gravacao",
    # laboratório e universidade
    "o que e o lsa", "onde fica o laboratorio", "o que voces fazem aqui", "quem coordena o laboratorio",
    "quais projetos o laboratorio tem", "como entrar no laboratorio", "que cursos tem na pucrs",
    "qual curso fazer para trabalhar com robos", "o que e um sistema autonomo",
    # entretenimento
    "conta uma piada", "outra piada", "conta uma curiosidade", "me conta uma charada",
    "verdade ou mito", "quiz", "o que voce prefere", "canta parabens", "me conta uma historia",
    "joga um dado", "faz uma rima", "me motiva", "conta ate dez",
    # ciência, tecnologia e carreira
    "o que e inteligencia artificial", "o que e robotica", "o que e um algoritmo",
    "como funciona um motor eletrico", "o que e machine learning", "o que e um sensor",
    "como aprender a programar", "como aprender robotica", "que profissao escolher",
    "o que e o enem", "o que e energia solar", "o que e impressao 3d",
    # geral
    "qual a capital da franca", "quanto e sete vezes oito", "que horas sao", "que dia e hoje",
    "quantos planetas tem o sistema solar", "quem descobriu o brasil", "o que e o grenal",
    "me fale sobre porto alegre", "o que e chimarrao",
    # falhas e interação
    "nao entendi", "muito barulho", "tira uma foto", "tchau", "obrigado", "voce e burro",
]

# o que a voz costuma ler mal; \d = dígitos, siglas em maiúsculas, símbolos
_PROBLEMAS = [
    (re.compile(r"\d"), "dígito (a voz pode ler errado; escreva por extenso)"),
    (re.compile(r"\b[A-Z]{2,}\b"), "sigla em maiúsculas (pode ser soletrada ou lida como palavra)"),
    (re.compile(r"[()\[\]{}/%&@#*_=+<>]"), "símbolo que a voz lê ou ignora"),
    (re.compile(r"\bhttps?://|www\."), "endereço de internet"),
]


def _palavras(t):
    return len(t.split())


def verificar_perguntas():
    print("== 1. perguntas de feira ==")
    sem, longas = [], []
    for q in PERGUNTAS_FEIRA:
        n = brain.corrigir_texto(q)
        r = (brain.resposta_matematica(n) or brain.resposta_geografia(n)
             or brain.resposta_hora_data(n) or brain._buscar_em_frases(n))
        if not r and brain.e_despedida(n):
            continue  # despedida é tratada pelo servidor, não pelo repertório
        if not r:
            sem.append(q)
        elif _palavras(r) > LIMITE_PALAVRAS:
            longas.append((q, _palavras(r)))
    print(f"{len(PERGUNTAS_FEIRA)} perguntas; {len(sem)} sem resposta local (iriam para a IA)")
    for q in sem:
        print(f"   SEM RESPOSTA: {q}")
    if longas:
        print(f"   {len(longas)} com resposta acima de {LIMITE_PALAVRAS} palavras (primeira resposta sorteada):")
        for q, n in longas:
            print(f"   LONGA ({n} palavras): {q}")


def verificar_respostas():
    print("\n== 2. respostas longas demais (qualquer variação) ==")
    longas = []
    for gs, rs in repertorio.FRASES:
        for r in rs:
            if _palavras(r) > LIMITE_PALAVRAS:
                longas.append((_palavras(r), gs[0], r))
    longas.sort(reverse=True)
    print(f"{len(longas)} respostas acima de {LIMITE_PALAVRAS} palavras (as {min(15, len(longas))} maiores):")
    for n, g, r in longas[:15]:
        print(f"   {n:3d} palavras  [{g}]  {r[:70]}...")

    print("\n== 3. textos que a voz lê mal ==")
    achados = {}
    for gs, rs in repertorio.FRASES:
        for r in rs:
            falado = pronuncia.para_fala(r)  # já com as trocas do pronuncia.py
            for padrao, motivo in _PROBLEMAS:
                m = padrao.search(falado)
                if m:
                    achados.setdefault(motivo, []).append((gs[0], m.group(0), r))
    if not achados:
        print("nenhum")
    for motivo, itens in achados.items():
        print(f"{len(itens)} com {motivo}:")
        for g, trecho, r in itens[:8]:
            print(f"   [{g}] '{trecho}' em: {r[:60]}...")
        if len(itens) > 8:
            print(f"   ... e mais {len(itens) - 8}")


def verificar_duplicados():
    print("\n== 4. gatilhos que aparecem em mais de uma entrada ==")
    vistos = {}
    dup = []
    for i, (gs, rs) in enumerate(repertorio.FRASES):
        for g in gs:
            if g in vistos and vistos[g] != i:
                dup.append((g, vistos[g], i))
            vistos.setdefault(g, i)
    print(f"{len(dup)} gatilhos repetidos (vale a entrada que vem primeiro em FRASES)")
    for g, a, b in dup[:20]:
        print(f"   '{g}': entrada {a} vence a entrada {b}")
    if len(dup) > 20:
        print(f"   ... e mais {len(dup) - 20}")


if __name__ == "__main__":
    if "--so-estatico" not in sys.argv:
        verificar_perguntas()
    verificar_respostas()
    verificar_duplicados()
