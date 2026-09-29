# C-2GELSA — conversa por voz

Robô de conversa por voz do LSA/PUCRS. Sem câmera, só ouvido, cérebro e
voz:

```
microfone -> Vosk (mic.py) -> brain.py -> voice.py (Piper) -> alto-falante
                                  |
                                  v
                          memoria.py (histórico +
                          perguntas não respondidas)
```

## Instalação em uma máquina nova (depois de `git clone`)

O repositório só tem o **código**. Os arquivos pesados (modelos de IA,
voz, banco de dados local) ficam de fora do Git (veja `.gitignore`) e
precisam ser baixados/gerados de novo em cada máquina. Siga em ordem:

**1. Dependências Python:**
```bash
pip install -r requirements.txt
```

**2. Dependências de sistema (Linux):**
```bash
sudo apt install -y libportaudio2 alsa-utils
```

**3. Ollama (o "cérebro" para perguntas fora do escrito localmente) --
grátis, sem chave de API:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:1b
```
> Se sua máquina não tiver GPU dedicada (NVIDIA/AMD), use o modelo `1b`
> mesmo -- é o que roda em tempo razoável só na CPU. Com GPU, modelos
> maiores (`llama3.2`, `llama3.1`) ficam melhores e ainda rápidos.

**4. Vosk (reconhecimento de fala) -- baixe o modelo separadamente:**
```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip
unzip vosk-model-small-pt-0.3.zip
```
Depois, ajuste o caminho em `mic.py`:
```python
VOSK_MODEL_PATH = "/caminho/absoluto/para/vosk-model-small-pt-0.3"
```

**5. Piper (voz) -- baixe a voz separadamente:**
Baixe uma voz pt-BR em https://github.com/rhasspy/piper/blob/master/VOICES.md
(o projeto foi testado com a voz "Faber"). Depois, ajuste em `voice.py`:
```python
PIPER_PYTHON = "/caminho/para/o/python/do/ambiente/com/piper/instalado"
PIPER_VOICE_MODEL = "/caminho/para/pt_BR-faber-medium.onnx"
```
Se `piper` não estiver instalado nesse Python: `pip install piper-tts`.

**6. Caminho do banco de histórico**, em `memoria.py`:
```python
DB_PATH = "/caminho/absoluto/para/memoria.db"
```
(o arquivo é criado automaticamente na primeira execução, não precisa
existir antes.)

**7. Teste, na ordem:**
```bash
python test_texto.py     # testa o cérebro digitando, sem mic/voz
python conversar.py      # conversa de verdade, por voz
```

## IA por API/local: Ollama (grátis) ou Claude/ChatGPT (pago)

O `brain.py` tem três modos, controlados por `MODO_RESPOSTA`:

- **`"local"`** — só a base de frases fixas (`FRASES`) + matemática +
  geografia. Rápido, de graça, sem internet.
- **`"hibrido"`** *(recomendado, é o padrão)* — tenta local primeiro; se
  não achar nada, chama o provedor de IA configurado em `API_PROVEDOR`.
- **`"api"`** — pula a base local e manda toda pergunta pro provedor.

### `API_PROVEDOR = "ollama"` (padrão, GRÁTIS)

O [Ollama](https://ollama.com) roda modelos abertos (Llama, Gemma, Phi...)
**localmente na sua máquina** — sem internet, sem chave de API, sem
custo nenhum. Diferente do BitNet, ele mantém o modelo carregado em
memória, então (depois do primeiro "aquecimento") as respostas saem sem
precisar recarregar do zero a cada pergunta.

**Sem GPU dedicada, a velocidade é limitada pela CPU.** Testamos em um
notebook Intel Core i7 com gráficos integrados (Intel Iris Xe, sem GPU
NVIDIA/AMD) e o modelo `llama3.2` padrão (3B parâmetros) levava
~15-30s por resposta curta -- inviável para conversa fluida. Trocando
para `llama3.2:1b` (modelo bem menor), caiu para ~6-7s. Esse é o
trade-off real de rodar IA generativa sem GPU: modelos menores respondem
rápido mas são menos capazes; modelos maiores são melhores mas mais
lentos. Ajuste `OLLAMA_MODEL` em `brain.py` conforme seu hardware:

```python
OLLAMA_MODEL = "llama3.2:1b"   # rápido, recomendado sem GPU
# OLLAMA_MODEL = "llama3.2"    # melhor qualidade, precisa de mais CPU/GPU
```

O `brain.py` já "aquece" o Ollama em segundo plano assim que o programa
inicia (`aquecer_ollama_em_thread()`), pra esconder a demora do primeiro
carregamento do modelo.

> Sem busca na web nesse modo -- o Ollama é local, não tem acesso à
> internet embutido. Ele responde com o conhecimento que já tem
> "memorizado" do treinamento, sem buscar nada atualizado.

### `API_PROVEDOR = "anthropic"` ou `"openai"` (PAGO)

Só use se quiser respostas de um dos modelos comerciais grandes,
com busca na web real (só a Anthropic tem essa ferramenta integrada
aqui). Tem custo por pergunta, cobrado na sua conta.

1. Crie uma conta e gere uma chave em
   [console.anthropic.com](https://console.anthropic.com) (ou
   [platform.openai.com](https://platform.openai.com)).
2. Configure a chave como variável de ambiente:
   ```bash
   export ANTHROPIC_API_KEY="sua-chave-aqui"
   ```
3. Em `brain.py`: `API_PROVEDOR = "anthropic"`.

Se a chave não estiver configurada, a API falha silenciosamente (aviso
no terminal) e o fluxo cai pro próximo fallback -- não trava a conversa.

## O que mudou / foi corrigido em relação à versão original

1. **`corrigir_texto()` agora é chamado de fato.** Antes existia mas
   nunca era usado -- o texto do Vosk ia direto pra comparação sem
   correção.
2. **Busca aproximada (fuzzy)** na base de frases: se a comparação exata
   não achar nada, tenta por similaridade antes de desistir -- tolera
   pequenos erros de transcrição do Vosk.
3. **BitNet desligado por padrão** (`USE_BITNET = False`) -- substituído
   pelo Ollama, que é mais rápido de configurar e mantém o modelo
   carregado em memória (o BitNet recarregava do zero em toda chamada).
4. **`memoria.py` simplificado**: histórico da conversa + log de
   perguntas não respondidas, sem a busca exata em banco que quase nunca
   batia com fala transcrita.
5. **Bug de regex na matemática corrigido** (`"demais"` não vira mais
   `"de+"`).
6. **Voz trocada para Piper** (voz "Faber", mais natural que o
   `pyttsx3`), mantendo o padrão de thread dedicada + fila para a fala
   sair sempre na ordem certa.

## Estrutura

```
Bitnet_TTS/
├── README.md
├── requirements.txt
├── .gitignore
├── mic.py           # microfone + Vosk (reconhecimento de fala)
├── brain.py         # gera as respostas (local, híbrido ou API)
├── voice.py         # texto -> fala (Piper TTS)
├── memoria.py       # histórico + log de perguntas não respondidas
├── conversar.py     # script principal (fala de verdade)
└── test_texto.py    # testa o brain.py digitando, sem falar nem ouvir
```

## Como testar

**1. Cérebro sozinho, digitando (mais rápido pra ajustar frases, sem
esperar o mic/voz):**
```bash
python test_texto.py
```

**2. Conversa de verdade, por voz:**
```bash
python conversar.py
```
Fale perto do microfone. Diga "tchau" (ou "até mais", "pode parar") para
encerrar.

## Como adicionar mais conhecimento local

Depois de uma sessão de testes, veja o que caiu no fallback (ou, no modo
híbrido, o que precisou ir pro Ollama por não estar na base local):
```bash
python -c "import memoria; memoria.listar_nao_respondidas()"
```
Adicione uma nova entrada em `FRASES`, no `brain.py`:
```python
(["gatilho 1", "gatilho 2"], ["resposta 1", "resposta 2 (opcional, varia)"]),
```
Quanto mais isso estiver preenchido, menos a conversa depende do Ollama
(mais rápido, já que é tudo instantâneo em memória).