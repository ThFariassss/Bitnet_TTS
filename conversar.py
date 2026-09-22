import time
import memoria
from brain import gerar_resposta, e_despedida, corrigir_texto, FRASES_NAO_ENTENDI
from mic import escutar_uma_frase
from voice import falar, esperar_todas_falas_terminarem
NOME = "C-2GELSA"
FRASE_INICIAL = (
    "Olá! Eu sou o C-2GELSA, robô do Laboratório de Sistemas Autônomos, "
)
FRASE_FINAL = "Até mais! Foi um prazer conversar com você."
def conversar():
    print()
    print("=" * 60)
    print(f"{NOME:^60}")
    print("=" * 60)
    print("Laboratório de Sistemas Autônomos - LSA - PUCRS")
    print()
    print("Modo de conversa por voz. Diga 'tchau' para encerrar.")
    print()
    memoria.criar_banco()
    print("[ROBÔ]", FRASE_INICIAL)
    falar(FRASE_INICIAL)
    esperar_todas_falas_terminarem()  
    while True:
        try:
            print()
            print(f"[{NOME}] Ouvindo...")

            inicio_escuta = time.time()
            pergunta = escutar_uma_frase()
            tempo_escuta = time.time() - inicio_escuta

            print(f"[VOCÊ] {pergunta}")
            print(f"[MIC] reconhecimento levou {tempo_escuta:.2f}s")

            texto_corrigido = corrigir_texto(pergunta)

            if e_despedida(texto_corrigido):
                print(f"[{NOME}] {FRASE_FINAL}")
                falar(FRASE_FINAL)
                esperar_todas_falas_terminarem()
                memoria.salvar_conversa(pergunta, FRASE_FINAL)
                break

            inicio_brain = time.time()
            resposta = gerar_resposta(pergunta)
            tempo_brain = time.time() - inicio_brain

            print(f"[BRAIN] resposta em {tempo_brain:.2f}s")
            print(f"[{NOME}] {resposta}")

            falar(resposta)
            memoria.salvar_conversa(pergunta, resposta)

            if resposta in FRASES_NAO_ENTENDI:
                memoria.registrar_nao_respondida(pergunta, texto_corrigido)

        except KeyboardInterrupt:
            print()
            print("[MAIN] encerrando...")
            break

        except Exception as erro:
            print()
            print("[ERRO]", repr(erro))
            import traceback
            traceback.print_exc()
            time.sleep(0.2)

    print()
    print("=" * 60)
    print(f"{NOME} encerrado.")
    print("=" * 60)


if __name__ == "__main__":
    conversar()