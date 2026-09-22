"""
C-2GELSA
Sistema de conversa exclusivamente por voz.

MICROFONE
   ↓
VOSK
   ↓
BRAIN
   ↓
TTS
   ↓
ALTO-FALANTE

Não usa câmera.
Não usa YOLO.
Não usa BitNet por padrão.

A prioridade é velocidade de conversa.
"""

import time

from brain import gerar_resposta
from mic import escutar_uma_frase
from voice import falar


# ============================================================
# CONFIGURAÇÃO
# ============================================================

NOME = "C-2GELSA"

FRASE_INICIAL = (
    "Olá! Eu sou o C-2GELSA, "
    "robô do Laboratório de Sistemas Autônomos, "
    "o LSA, da PUCRS. "
    "Estou pronto para conversar com você."
)


# ============================================================
# CONVERSA
# ============================================================

def conversa():

    print()
    print("=" * 60)
    print("                 C-2GELSA")
    print("=" * 60)
    print()
    print("Laboratório de Sistemas Autônomos - LSA")
    print("PUCRS")
    print()
    print("Modo de conversa por voz.")
    print("Não é necessário usar o teclado.")
    print()
    print("Diga 'tchau' para encerrar.")
    print()

    # --------------------------------------------------------
    # APRESENTAÇÃO
    # --------------------------------------------------------

    print("[ROBÔ]")
    print(FRASE_INICIAL)
    print()

    falar(FRASE_INICIAL)

    # --------------------------------------------------------
    # LOOP
    # --------------------------------------------------------

    while True:

        try:

            print()
            print("[C-2GELSA] Estou ouvindo...")

            inicio_escuta = time.time()

            pergunta = escutar_uma_frase()

            if not pergunta:
                continue

            tempo_escuta = time.time() - inicio_escuta

            print()
            print(
                f"[VOCÊ] {pergunta}"
            )

            print(
                f"[MIC] reconhecimento: "
                f"{tempo_escuta:.2f}s"
            )

            texto = pergunta.lower()

            # ------------------------------------------------
            # SAÍDA
            # ------------------------------------------------

            if (
                "tchau" in texto
                or "até mais" in texto
                or "ate mais" in texto
                or "encerrar conversa" in texto
                or "pode parar" in texto
            ):

                resposta = (
                    "Até mais! "
                    "Foi um prazer conversar com você."
                )

                print()
                print("[C-2GELSA]")
                print(resposta)

                falar(resposta)

                break

            print("[BRAIN] processando...")

            inicio_brain = time.time()

            resposta = gerar_resposta(
                pergunta
            )

            tempo_brain = (
                time.time() - inicio_brain
            )

            print(
                f"[BRAIN] resposta em "
                f"{tempo_brain:.2f}s"
            )


            print()
            print("[C-2GELSA]")
            print(resposta)


            falar(resposta)

        except KeyboardInterrupt:

            print()
            print("[MAIN] encerrando...")
            break

        except Exception as erro:

            print()
            print(
                "[ERRO]",
                repr(erro)
            )
            time.sleep(0.2)

    print()
    print("=" * 60)
    print("C-2GELSA encerrado.")
    print("=" * 60)




if __name__ == "__main__":
    conversa()