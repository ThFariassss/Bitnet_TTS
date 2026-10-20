"""
gatilhos_gramatica.py
Imprime (em JSON) todas as frases que o reconhecedor de voz precisa aceitar: os
gatilhos do repertório, as capitais, as contas e as frases de contexto. É a entrada
do gerar_gramatica.py:

    cd ~/Bitnet_TTS && python3 gatilhos_gramatica.py > /tmp/gatilhos.json
    cd ~/dev/LSA_robot/src && python3 jetson/gerar_gramatica.py /tmp/gatilhos.json

(use o python do venv do projeto; com o do sistema também funciona se o brain.py importar)
"""
import json

import brain
import repertorio
import repertorio_contexto

g = [t for gs, _ in repertorio.FRASES for t in gs]
g += repertorio_contexto.gatilhos_para_gramatica()
g += ["qual a capital %s %s" % (p, k) for k in brain.CAPITAIS for p in ("de", "do", "da", "dos", "das")]
g += ["qual a capital " + c for cs, _, _ in brain.CAPITAIS_ESTADOS for c in cs]
n = list(brain._NUMEROS_POR_EXTENSO)
g += ["quanto e %s %s %s" % (a, op, b) for a in n for b in n for op in ("mais", "menos", "vezes", "dividido por")]
print(json.dumps(g))
