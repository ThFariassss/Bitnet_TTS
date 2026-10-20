"""
relatorio_perguntas.py
Mostra o que as pessoas perguntaram ao C-2GELSA e NÃO tinha resposta local
(ou seja, foi para a IA, que é mais lenta e às vezes inventa).

Uso:
    python3 relatorio_perguntas.py            # todas as conversas do memoria.db
    python3 relatorio_perguntas.py 50         # só as últimas 50 conversas
    python3 relatorio_perguntas.py --ruido    # inclui as frases que parecem ruído do Vosk

Cada pergunta é testada de novo contra o repertório ATUAL, então o que você já
cadastrou depois da conversa não aparece mais. As mais repetidas vêm primeiro:
são as que mais valem uma resposta nova no repertório (repertorio_feira.py).
"""
import collections
import os
import sqlite3
import sys

import brain

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memoria.db")


def tem_resposta_local(texto: str) -> bool:
    return bool(
        brain.resposta_matematica(texto)
        or brain.resposta_geografia(texto)
        or brain.resposta_hora_data(texto)
        or brain._buscar_em_frases(texto)
    )


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    com_ruido = "--ruido" in sys.argv
    limite = int(args[0]) if args else None

    con = sqlite3.connect(DB)
    sql = "select pergunta from conversa order by id desc"
    if limite:
        sql += f" limit {limite}"
    perguntas = [p for (p,) in con.execute(sql)]
    total = len(perguntas)

    sem_resposta = collections.Counter()
    ruido = 0
    exemplo = {}
    for p in perguntas:
        t = brain.corrigir_texto(p)
        if tem_resposta_local(t):
            continue
        if not brain.pergunta_plausivel(t):
            ruido += 1
            if not com_ruido:
                continue
        sem_resposta[t] += 1
        exemplo.setdefault(t, p)

    print(f"{total} perguntas analisadas.")
    print(f"{total - sum(sem_resposta.values()) - (0 if com_ruido else ruido)} têm resposta local; "
          f"{ruido} parecem ruído do reconhecedor{' (incluídas abaixo)' if com_ruido else ' (ocultas, use --ruido)'}; "
          f"{sum(sem_resposta.values())} vão para a IA.\n")
    if not sem_resposta:
        print("Nada sem resposta local. 🎉")
        return
    print("Perguntas que foram para a IA (mais repetidas primeiro):")
    for t, n in sem_resposta.most_common():
        print(f"  {n:3d}x  {exemplo[t]}")
    print("\nPara cada uma que fizer sentido, acrescente um item em repertorio_feira.py "
          "(lista FRASES_FEIRA), reinicie o servidor e rode o gerar_gramatica.py.")


if __name__ == "__main__":
    main()
