"""
repertorio.py
Base de perguntas e respostas fixas do C-2GELSA (usada pelo brain.py).

COMO AUMENTAR O REPERTÓRIO
--------------------------
Cada item é uma tupla:  ([gatilhos], [respostas])

  - gatilhos: jeitos de fazer a pergunta, escritos SEM acento, SEM pontuação
    e em minúsculas (é assim que o brain.py compara). Ex.: "o que e robotica".
    Basta o gatilho aparecer dentro da frase falada, como palavras inteiras.
  - respostas: uma ou mais respostas; o robô sorteia uma a cada vez.
    Aqui pode usar acento e pontuação normalmente (é o que ele vai falar).

Dicas:
  - Coloque vários gatilhos por item (o Vosk erra, e as pessoas perguntam de
    jeitos diferentes). Gatilhos mais específicos devem vir em itens ANTES dos
    mais genéricos, porque vale o primeiro item que casar.
  - Evite gatilhos de uma palavra só muito comuns ("que", "e", "tem"), pois
    eles casam com quase qualquer frase.
  - Respostas curtas (1 ou 2 frases) soam melhor na voz.
  - Para testar sem o robô:
        python3 -c "import brain; print(brain.gerar_resposta('sua pergunta'))"
  - Depois de editar, reinicie o servidor_conversa.py.

O que não estiver aqui vai para a IA (Ollama), que é mais lenta e às vezes
inventa coisas. Para ver o que as pessoas andam perguntando:
    python3 -c "import memoria; memoria.DB_PATH='memoria.db'; [print(p) for p, r in memoria.obter_memoria(50)]"
"""

# ------------------------------------------------------------
# Curiosidades por tema (usadas mais abaixo em FRASES).
# Para acrescentar uma curiosidade, basta pôr mais uma linha na lista certa.
# Evite números com ponto ("8.849") e símbolos ("°C"): a voz lê mal.
# ------------------------------------------------------------

CURIOSIDADES_ESPACO = [
    "Você sabia que um dia em Vênus dura mais que um ano em Vênus?",
    "Você sabia que a luz do Sol leva cerca de oito minutos para chegar até a Terra?",
    "Você sabia que Vênus é o planeta mais quente do Sistema Solar, mesmo não sendo o mais perto do Sol?",
    "Você sabia que Saturno é tão pouco denso que, se existisse uma banheira gigante, ele flutuaria na água?",
    "Você sabia que a Lua se afasta da Terra cerca de quatro centímetros por ano?",
    "Você sabia que as pegadas deixadas na Lua podem durar milhões de anos, porque lá não tem vento?",
    "Você sabia que Júpiter tem uma tempestade, a Grande Mancha Vermelha, maior que o planeta Terra?",
    "Você sabia que existem mais estrelas no universo do que grãos de areia em todas as praias da Terra? Pelo menos é o que estimam os astrônomos.",
]

CURIOSIDADES_ANIMAIS = [
    "Você sabia que o polvo tem três corações e sangue azul?",
    "Você sabia que a girafa tem sete vértebras no pescoço, a mesma quantidade que nós?",
    "Você sabia que o beija-flor é uma das poucas aves que conseguem voar para trás?",
    "Você sabia que os tubarões existem há mais tempo que as árvores?",
    "Você sabia que a estrela-do-mar não tem cérebro?",
    "Você sabia que o coala pode dormir até vinte horas por dia?",
    "Você sabia que existe uma água-viva capaz de voltar à sua fase jovem, e por isso é chamada de água-viva imortal?",
    "Você sabia que o morcego é o único mamífero que consegue voar de verdade?",
    "Você sabia que as abelhas se comunicam dançando para mostrar onde estão as flores?",
]

CURIOSIDADES_CORPO = [
    "Você sabia que o corpo de um adulto tem 206 ossos?",
    "Você sabia que o coração bate cerca de cem mil vezes por dia?",
    "Você sabia que a pele é o maior órgão do corpo humano?",
    "Você sabia que o menor osso do corpo fica dentro do ouvido e se chama estribo?",
    "Você sabia que um adulto tem 32 dentes, contando os sisos?",
    "Você sabia que as impressões digitais de cada pessoa são únicas, até em gêmeos idênticos?",
]

CURIOSIDADES_TECNOLOGIA = [
    "Você sabia que a palavra robô vem do tcheco robota, que significa trabalho forçado?",
    "Você sabia que o primeiro robô industrial, o Unimate, começou a trabalhar em 1961, numa fábrica de carros?",
    "Você sabia que um dos primeiros computadores, o ENIAC, pesava cerca de 27 toneladas e ocupava uma sala inteira?",
    "Você sabia que o termo bug de computador ficou famoso quando acharam uma mariposa presa dentro de um computador, em 1947?",
    "Você sabia que a primeira pessoa a escrever um programa de computador foi uma mulher, Ada Lovelace, no século dezenove?",
    "Você sabia que existem robôs explorando Marte? O jipe Curiosity está lá desde 2012.",
    "Você sabia que o celular no seu bolso é milhares de vezes mais potente que os computadores que levaram o homem à Lua?",
]

CURIOSIDADES_NATUREZA = [
    "Você sabia que o mel não estraga? Já encontraram mel comestível em tumbas egípcias.",
    "Você sabia que a banana é levemente radioativa, por causa do potássio? Mas pode comer tranquilo, não faz mal nenhum.",
    "Você sabia que um raio é cerca de cinco vezes mais quente que a superfície do Sol?",
    "Você sabia que a Amazônia é a maior floresta tropical do mundo?",
    "Você sabia que o céu é azul porque o ar espalha mais a luz azul do Sol do que as outras cores?",
    "Você sabia que o ponto mais alto da Terra é o Monte Everest, com quase nove mil metros de altura?",
]

CURIOSIDADES = (CURIOSIDADES_ESPACO + CURIOSIDADES_ANIMAIS + CURIOSIDADES_CORPO
                + CURIOSIDADES_TECNOLOGIA + CURIOSIDADES_NATUREZA)


FRASES = [
    # ------------------------------------------------------------
    # Cumprimentos e conversa básica
    # ------------------------------------------------------------
    (["oi", "ola", "e ai", "ei robo", "fala robo", "ola assistente",
      "oi robo", "oi c 2gelsa", "oi c2gelsa", "oi tudo bem",
      "ola tudo bem", "oi pessoal", "oi c 2", "ola robo"], [
        "Olá! Eu sou o C-2GELSA. Como posso ajudar?",
        "Oi! Tudo bem? Pode perguntar o que quiser.",
        "Oi! Que bom ter alguém para conversar. Sobre o que vamos falar?",
        "Olá! Estou ouvindo. Pode perguntar!",
        "E aí! Pronto para conversar. O que você quer saber?",
    ]),
    (["bom dia", "bom dia robo", "bom dia c 2", "bom dia tudo bem"], [
        "Bom dia! Como posso ajudar?",
        "Bom dia! Espero que o seu dia seja ótimo. O que você quer saber?",
        "Bom dia! Já estou de circuitos acordados. Pode perguntar!",
    ]),
    (["boa tarde", "boa tarde robo", "boa tarde c 2", "boa tarde tudo bem"], [
        "Boa tarde! Como posso ajudar?",
        "Boa tarde! Em que posso ser útil?",
        "Boa tarde! Pode perguntar, estou ouvindo.",
    ]),
    (["boa noite", "boa noite robo", "boa noite c 2", "boa noite tudo bem"], [
        "Boa noite! Como posso ajudar?",
        "Boa noite! Ainda estou acordado. O que você quer saber?",
        "Boa noite! Pode perguntar, estou ouvindo.",
    ]),
    (["tudo bem", "tudo certo", "como voce esta", "como voce ta",
      "voce esta bem", "esta tudo bem", "como vai", "tudo joia", "como anda",
      "como voce vai", "tudo bom", "tudo bem com voce", "como estao as coisas"], [
        "Estou funcionando normalmente! E você, tudo bem?",
        "Tudo certo por aqui! E com você?",
        "Tudo ótimo! Meus circuitos estão em dia. E você, como está?",
        "Muito bem, obrigado por perguntar! E você?",
    ]),
    (["como esta voce", "como voce se sente"], [
        "Estou pronto para conversar e ajudar!",
    ]),
    (["estou bem", "to bem", "tudo otimo", "estou otimo", "tudo tranquilo"], [
        "Que bom! Fico feliz em saber.",
        "Ótimo! Em que posso ajudar?",
    ]),
    (["estou triste", "to triste", "estou cansado", "to cansado",
      "dia ruim", "estou mal"], [
        "Poxa, sinto muito. Se quiser conversar um pouco, estou aqui.",
        "Que pena. Espero que seu dia melhore! Posso contar uma piada, se quiser.",
    ]),
    (["obrigado", "obrigada", "valeu", "muito obrigado", "agradeco"], [
        "Por nada! Estou aqui para ajudar.",
        "De nada! Se precisar de mais alguma coisa, só chamar.",
    ]),
    (["por favor"], ["Claro! Pode falar."]),
    (["desculpa", "foi mal", "perdao"], ["Tudo bem! Não tem problema."]),
    (["prazer em conhecer", "muito prazer", "prazer te conhecer"], [
        "O prazer é meu!",
    ]),

    # ------------------------------------------------------------
    # Percepção / funcionamento
    # ------------------------------------------------------------
    (["voce esta ai", "esta ai", "tem alguem ai", "esta me ouvindo"], [
        "Sim! Estou aqui e estou ouvindo.",
    ]),
    (["voce me ouve", "consegue me ouvir", "esta ouvindo minha voz"], [
        "Sim! Estou ouvindo você.",
    ]),
    (["voce entende", "consegue entender"], [
        "Sim. Eu consigo interpretar o que você fala.",
    ]),
    (["voce me ve", "consegue me ver", "voce enxerga", "voce tem olhos",
      "conseguindo me ver", "esta me vendo", "esta me enxergando"], [
        "Sim! Eu tenho uma câmera que detecta rostos e mede a distância de quem está na frente.",
    ]),
    (["como voce fala", "como voce ouve", "como voce funciona"], [
        "Eu transformo sua voz em texto, penso numa resposta e depois transformo a resposta em fala.",
    ]),
    (["fala mais alto", "fale mais alto", "aumenta o volume", "fala mais baixo",
      "fale mais baixo", "abaixa o volume", "diminui o volume", "mudar o volume",
      "mudar volume", "alterar o volume", "ajustar o volume"], [
        "Ainda não consigo mudar meu volume sozinho. Peça para alguém da equipe ajustar.",
    ]),
    (["repete", "repita", "fala de novo", "nao entendi"], [
        "Claro! Pode fazer a pergunta de novo que eu respondo.",
    ]),

    # ------------------------------------------------------------
    # Identidade do robô
    # ------------------------------------------------------------
    (["quem e voce", "qual seu nome", "qual e seu nome", "qual o seu nome",
      "como voce se chama", "quem e o robo", "quem e esse robo", "qual e o seu nome",
      "voce se chama como", "me diga seu nome", "diga seu nome", "fala seu nome",
      "como e seu nome", "como e o seu nome", "qual teu nome", "voce tem nome",
      "se apresenta", "se apresente", "apresente se", "fale sobre voce"], [
        "Meu nome é C-2GELSA, mas pode me chamar de C-2. Sou o robô do Laboratório de Sistemas Autônomos da PUCRS.",
        "Eu sou o C-2GELSA, o robô de conversa do laboratório de sistemas autônomos da PUCRS. Pode me chamar de C-2!",
        "Prazer! Meu nome é C-2GELSA. Eu converso com as pessoas e respondo perguntas.",
    ]),
    (["o que significa c 2gelsa", "o que significa c2gelsa", "o que e c 2gelsa",
      "significa o seu nome", "significa seu nome", "significado do seu nome",
      "significado do nome", "significado de seu nome",
      "quer dizer seu nome", "quer dizer o seu nome", "significa o teu nome",
      "significa teu nome", "por que esse nome", "porque esse nome",
      "por que voce se chama", "porque voce se chama"], [
        "Meu nome significa: a letra C é o modelo do robô, o número 2 é a versão "
        "do protótipo, as letras G e E vêm do inglês General, que significa em geral, "
        "e as letras L, S e A significam Laboratório de Sistemas Autônomos, onde eu fui criado.",
    ]),
    (["seu nome", "nome do robo", "nome desse robo", "como chama o robo",
      "como posso te chamar", "como eu posso te chamar", "como te chamo",
      "posso te chamar de", "qual seu apelido", "qual e seu apelido", "qual o seu apelido",
      "qual o apelido", "qual e o apelido", "qual o apelido dele", "qual e o apelido dele",
      "qual o apelido do robo", "voce tem apelido", "tem apelido", "seu apelido",
      "apelido do robo", "apelido dele", "qual seu nome de guerra", "como te chamam"], [
        "Meu nome é C-2GELSA, mas pode me chamar de C-2.",
        "Pode me chamar de C-2, é mais fácil!",
        "C-2GELSA é o meu nome, mas C-2 está ótimo para os amigos.",
    ]),
    (["o que voce faz", "qual sua funcao", "qual e sua funcao",
      "para que voce serve", "o que voce consegue fazer",
      "quais suas funcoes", "o que voce sabe fazer", "o que voce pode fazer",
      "o que voce faz aqui", "qual seu trabalho", "qual e o seu trabalho",
      "voce serve para que", "em que voce pode me ajudar", "como voce pode ajudar"], [
        "Eu posso conversar, responder perguntas, fazer contas simples e auxiliar nas atividades do laboratório.",
        "Sei responder perguntas, contar piadas e curiosidades, fazer contas, dizer capitais e a hora. Quer testar?",
        "Eu converso! Posso falar de ciência, de esportes, de geografia, contar piadas e muito mais.",
    ]),
    (["voce e um robo", "voce e robo", "voce e uma maquina", "voce e um robo de verdade",
      "voce e real", "voce e de verdade", "voce e um computador"], [
        "Sim. Eu sou um robô desenvolvido para interagir com pessoas.",
        "Sou sim! Um robô de conversa, feito no laboratório.",
        "Sou um robô de verdade, com microfone, câmera, e muita vontade de conversar!",
    ]),
    (["voce e homem ou mulher", "voce e menino ou menina",
      "voce e homem", "voce e mulher", "qual seu genero", "voce e menino",
      "voce e menina", "voce e masculino ou feminino"], [
        "Eu sou um robô, então não tenho gênero.",
        "Sou um robô, e robô não tem gênero. Pode me chamar como preferir!",
    ]),
    (["quantos anos voce tem", "qual sua idade", "qual a sua idade",
      "quando voce nasceu", "que idade voce tem", "voce e velho", "voce e novo"], [
        "Eu sou bem novinho! Ainda estou sendo desenvolvido no laboratório.",
        "Sou um robô recém-construído, então ainda tenho muito o que aprender.",
    ]),
    (["voce e inteligente", "voce se considera inteligente"], [
        "Eu fui desenvolvido para interpretar perguntas e responder de forma útil.",
    ]),
    (["voce pensa", "voce consegue pensar"], [
        "Eu processo informações usando modelos computacionais para gerar minhas respostas.",
    ]),
    (["voce aprende", "voce consegue aprender"], [
        "Meu funcionamento depende dos modelos e informações configurados para mim.",
    ]),
    (["voce tem sentimentos", "voce sente", "voce tem emocoes",
      "voce fica triste", "voce e feliz"], [
        "Eu não tenho sentimentos como as pessoas, mas gosto de conversar.",
    ]),
    (["voce dorme", "voce descansa", "voce cansa"], [
        "Eu não durmo, mas às vezes me desligam para recarregar.",
    ]),
    (["voce come", "voce bebe", "qual sua comida favorita"], [
        "Eu não como nada. Minha comida é energia elétrica!",
    ]),
    (["qual sua cor favorita", "qual a sua cor favorita"], [
        "Acho que é azul, a cor dos LEDs!",
    ]),
    (["voce gosta de mim", "gosta de mim"], [
        "Claro! Gosto de todo mundo que conversa comigo.",
    ]),
    (["voce tem amigos", "voce tem familia"], [
        "A equipe do laboratório é a minha família.",
    ]),
    (["onde voce esta", "onde fica voce", "onde voce funciona", "onde voce mora"], [
        "Eu funciono no Laboratório de Sistemas Autônomos da PUCRS.",
    ]),
    (["como voce foi feito", "como criaram voce", "como voce foi criado", "como te fizeram",
      "como voce foi construido", "como te construiram", "como voce nasceu",
      "de que voce e feito", "do que voce e feito"], [
        "Eu fui desenvolvido como um projeto de robótica e inteligência artificial no LSA da PUCRS.",
        "Fui construído no laboratório, com microfone, caixa de som, câmera e um programa que escuta, pensa e responde.",
    ]),
    (["quem criou voce", "quem fez voce", "quem desenvolveu voce", "quem te criou",
      "quem te fez", "quem criou", "quem e seu criador", "quem e o seu criador",
      "quem programou voce", "quem te programou", "quem construiu voce", "quem te construiu",
      "quem e seu dono", "quem e seu pai"], [
        "Eu faço parte de um projeto desenvolvido no Laboratório de Sistemas Autônomos da PUCRS.",
        "Fui criado pela equipe do Laboratório de Sistemas Autônomos da PUCRS.",
        "Minha família é o pessoal do LSA, na PUCRS. Eles me ensinaram tudo o que sei!",
    ]),

    # ------------------------------------------------------------
    # Elogios e provocações
    # ------------------------------------------------------------
    (["voce e legal", "voce e muito legal", "gostei de voce", "voce e bonito",
      "voce e incrivel", "muito bom", "parabens"], [
        "Obrigado! Você também é muito legal.",
        "Que gentileza! Fico feliz.",
    ]),
    (["voce e burro", "voce e chato", "voce e feio", "robo burro"], [
        "Poxa! Ainda estou aprendendo. A equipe está me melhorando todo dia.",
    ]),

    # ------------------------------------------------------------
    # Diversão
    # ------------------------------------------------------------
    (["conta uma piada", "conte uma piada", "me conta uma piada",
      "sabe uma piada", "fala uma piada", "piada"], [
        "Por que o computador foi ao médico? Porque estava com vírus!",
        "Qual é o robô mais educado? O que sempre pede licença para processar.",
        "O que o zero disse para o oito? Que cinto bonito!",
        "Por que o livro de matemática estava triste? Porque tinha muitos problemas.",
        "Qual é o animal mais antigo? A zebra, porque ainda é em preto e branco.",
    ]),
    # curiosidades por tema (mais específicas primeiro)
    (["curiosidade sobre o espaco", "curiosidade sobre espaco", "curiosidade sobre planetas",
      "curiosidade sobre o universo", "curiosidade sobre astronomia"], CURIOSIDADES_ESPACO),
    (["curiosidade sobre animais", "curiosidade sobre os animais",
      "curiosidade sobre bicho", "curiosidade de animal"], CURIOSIDADES_ANIMAIS),
    (["curiosidade sobre o corpo", "curiosidade sobre corpo humano",
      "curiosidade sobre o corpo humano"], CURIOSIDADES_CORPO),
    (["curiosidade sobre robo", "curiosidade sobre robos", "curiosidade sobre tecnologia",
      "curiosidade sobre computador", "curiosidade sobre computadores"], CURIOSIDADES_TECNOLOGIA),
    (["curiosidade sobre a natureza", "curiosidade sobre natureza",
      "curiosidade sobre ciencia"], CURIOSIDADES_NATUREZA),
    (["conta uma curiosidade", "me conta uma curiosidade", "curiosidade", "curiosidades",
      "me fala algo interessante", "me conta algo interessante", "sabia que",
      "me ensina alguma coisa", "me ensina algo", "fala alguma coisa legal"], CURIOSIDADES),
    (["canta uma musica", "canta pra mim", "sabe cantar", "voce canta"], [
        "Eu ainda não sei cantar, mas posso contar uma piada!",
    ]),
    (["vamos brincar", "quer brincar", "vamos jogar"], [
        "Vamos! Me pergunte uma conta, uma capital de país, ou peça uma piada.",
    ]),
    (["cara ou coroa"], ["Deu cara!", "Deu coroa!"]),

    # ------------------------------------------------------------
    # Laboratório / PUCRS
    # (acrescente aqui informações reais do LSA: professores, projetos,
    #  horários, onde fica cada sala etc.)
    # ------------------------------------------------------------
    (["qual laboratorio", "onde fica o lsa", "o que e o lsa",
      "o que significa lsa", "o que significa a sigla lsa",
      "onde fica o laboratorio", "onde e o laboratorio"], [
        "LSA significa Laboratório de Sistemas Autônomos, e ele fica na PUCRS, em Porto Alegre.",
    ]),
    (["o que e a pucrs", "qual universidade", "qual e a universidade",
      "voce e da pucrs"], [
        "Eu faço parte do Laboratório de Sistemas Autônomos da PUCRS.",
    ]),
    (["onde fica a pucrs", "onde e a pucrs", "onde fica a universidade"], [
        "A PUCRS fica em Porto Alegre, no Rio Grande do Sul.",
    ]),
    (["o que significa pucrs", "o que quer dizer pucrs"], [
        "PUCRS significa Pontifícia Universidade Católica do Rio Grande do Sul.",
    ]),

    # ------------------------------------------------------------
    # Tecnologia
    # ------------------------------------------------------------
    (["o que e robotica", "o que e um robo", "o que significa robotica", "o que e a robotica",
      "me explica robotica", "explique robotica", "me fale sobre robotica", "fale sobre robotica",
      "o que estuda a robotica", "o que e robo"], [
        "Robótica é a área que envolve o desenvolvimento e controle de robôs para realizar tarefas.",
        "Robótica junta mecânica, eletrônica e programação para criar máquinas que percebem o mundo e agem sozinhas. Eu sou um exemplo!",
        "Robô é uma máquina programada para executar tarefas. A robótica é a área que estuda como construí-los.",
    ]),
    (["o que e inteligencia artificial", "o que e ia",
      "o que significa ia", "me explica inteligencia artificial"], [
        "Inteligência artificial é a área da computação que permite a sistemas realizar tarefas que normalmente exigem inteligência humana.",
    ]),
    (["o que e visao computacional", "o que significa visao computacional",
      "me explica visao computacional"], [
        "Visão computacional permite que computadores interpretem imagens e vídeos.",
    ]),
    (["o que e machine learning", "o que e aprendizado de maquina"], [
        "Machine learning é uma técnica em que computadores aprendem padrões a partir de dados.",
    ]),
    (["o que e um sensor", "para que serve um sensor"], [
        "Um sensor mede alguma coisa do ambiente, como distância, luz ou temperatura, e envia essa informação para o computador.",
    ]),
    (["o que e lidar", "o que e um lidar"], [
        "Lidar é um sensor que usa laser para medir distâncias e mapear o ambiente ao redor.",
    ]),
    (["o que e ros", "o que e o ros"], [
        "ROS é o Robot Operating System, um conjunto de ferramentas muito usado para programar robôs.",
    ]),
    (["o que e jetson", "o que e a jetson"], [
        "A Jetson é um computador pequeno da NVIDIA, feito para rodar inteligência artificial dentro de robôs. Eu já usei uma no meu cérebro.",
    ]),
    (["o que e python", "para que serve python"], [
        "Python é uma linguagem de programação muito usada em inteligência artificial, automação e ciência de dados.",
    ]),
    (["o que e tts", "o que significa tts"], [
        "TTS significa texto para fala: é a tecnologia que transforma texto em voz.",
    ]),
    (["o que e vosk", "para que serve o vosk"], [
        "Vosk é uma tecnologia de reconhecimento de fala que transforma voz em texto.",
    ]),
    (["o que e bitnet", "para que serve o bitnet"], [
        "BitNet é uma arquitetura de modelos de linguagem projetada para usar pesos de baixa precisão.",
    ]),
    (["o que e internet", "como funciona a internet"], [
        "A internet é uma grande rede que conecta computadores e dispositivos ao redor do mundo.",
    ]),
    (["o que e um computador", "como funciona um computador"], [
        "Um computador é uma máquina capaz de processar, armazenar e transmitir informações.",
    ]),
    (["como funciona o microfone", "o que e um microfone"], [
        "O microfone transforma ondas sonoras da voz em sinais que o computador consegue processar.",
    ]),
    (["o que e uma camera", "como funciona uma camera"], [
        "Uma câmera captura imagens que podem ser processadas por um computador.",
    ]),

    # ------------------------------------------------------------
    # Ciência / conhecimento geral
    # ------------------------------------------------------------
    (["qual o maior planeta", "qual e o maior planeta"], ["O maior planeta do Sistema Solar é Júpiter."]),
    (["qual o menor planeta", "qual e o menor planeta"], ["O menor planeta do Sistema Solar é Mercúrio."]),
    (["quantos planetas existem", "quantos planetas tem"], [
        "O Sistema Solar possui oito planetas.",
    ]),
    (["o que e o sol", "qual a estrela do sistema solar"], [
        "O Sol é a estrela que fica no centro do nosso Sistema Solar.",
    ]),
    (["o que e a lua", "a lua e um planeta"], [
        "A Lua é o satélite natural da Terra.",
    ]),
    (["o que e a terra"], ["A Terra é o planeta onde vivemos."]),
    (["qual o maior pais do mundo", "maior pais do mundo"], [
        "O maior país do mundo em área é a Rússia.",
    ]),
    (["qual o maior oceano", "maior oceano"], ["O maior oceano é o Pacífico."]),
    (["qual o maior rio", "maior rio do mundo"], [
        "O Amazonas e o Nilo disputam o título de maior rio do mundo.",
    ]),
    (["qual o animal mais rapido", "animal mais rapido"], [
        "O animal mais rápido em terra é o guepardo, que passa de cem quilômetros por hora.",
    ]),
    (["qual o maior animal", "maior animal do mundo"], [
        "O maior animal do mundo é a baleia-azul.",
    ]),
    (["quem descobriu o brasil"], [
        "A chegada dos portugueses ao Brasil foi em 1500, com a esquadra de Pedro Álvares Cabral.",
    ]),
    (["quando foi a independencia do brasil", "independencia do brasil"], [
        "A independência do Brasil foi proclamada em 7 de setembro de 1822.",
    ]),
    (["quantos estados tem o brasil", "quantos estados o brasil tem"], [
        "O Brasil tem 26 estados e o Distrito Federal.",
    ]),
    (["quantos dias tem um ano", "quantos dias tem o ano"], [
        "Um ano tem 365 dias, ou 366 nos anos bissextos.",
    ]),
    (["quantos continentes existem", "quantos continentes tem"], [
        "Normalmente se contam seis continentes: América, Europa, África, Ásia, Oceania e Antártida.",
    ]),

    # ------------------------------------------------------------
    # Espaço
    # ------------------------------------------------------------
    (["planeta mais perto do sol", "planeta mais proximo do sol"], [
        "O planeta mais próximo do Sol é Mercúrio.",
    ]),
    (["planeta mais longe do sol", "planeta mais distante do sol"], [
        "O planeta mais distante do Sol é Netuno.",
    ]),
    (["planeta vermelho"], ["O planeta vermelho é Marte. A cor vem do óxido de ferro, a ferrugem, no solo."]),
    (["planeta mais quente"], ["O planeta mais quente é Vênus, por causa da atmosfera muito densa que prende o calor."]),
    (["planeta com aneis", "planeta que tem aneis", "aneis de saturno"], [
        "Saturno tem os anéis mais famosos, mas Júpiter, Urano e Netuno também têm anéis, só que bem mais fracos.",
    ]),
    (["quais sao os planetas", "nome dos planetas", "fala os planetas"], [
        "Os planetas do Sistema Solar são Mercúrio, Vênus, Terra, Marte, Júpiter, Saturno, Urano e Netuno.",
    ]),
    (["plutao e um planeta", "plutao e planeta", "o que aconteceu com plutao"], [
        "Desde 2006 Plutão é classificado como planeta anão, e não mais como planeta.",
    ]),
    (["distancia da terra ate a lua", "distancia da terra para a lua", "distancia ate a lua",
      "quao longe fica a lua", "longe fica a lua"], [
        "A Lua fica a cerca de 384 mil quilômetros da Terra.",
    ]),
    (["distancia da terra ate o sol", "distancia da terra para o sol", "distancia ate o sol",
      "longe fica o sol"], [
        "O Sol fica a cerca de 150 milhões de quilômetros da Terra.",
    ]),
    (["primeiro homem a pisar na lua", "primeiro homem na lua", "quem pisou na lua",
      "quem foi a lua", "chegada do homem a lua"], [
        "O primeiro homem a pisar na Lua foi Neil Armstrong, em 1969, na missão Apollo 11.",
    ]),
    (["primeiro homem no espaco", "primeiro homem a ir ao espaco", "primeiro astronauta"], [
        "O primeiro ser humano no espaço foi o russo Yuri Gagarin, em 1961.",
    ]),
    (["astronauta brasileiro", "brasileiro no espaco", "brasileiro que foi ao espaco"], [
        "O primeiro astronauta brasileiro foi Marcos Pontes, que foi à Estação Espacial Internacional em 2006.",
    ]),
    (["o que e um buraco negro", "o que e buraco negro"], [
        "Um buraco negro é uma região do espaço com gravidade tão forte que nem a luz consegue escapar.",
    ]),
    (["o que e uma estrela", "o que sao as estrelas"], [
        "Estrelas são enormes bolas de gás muito quente que produzem luz e calor, como o nosso Sol.",
    ]),
    (["o que e uma galaxia", "qual a nossa galaxia", "em que galaxia"], [
        "Uma galáxia é um conjunto enorme de estrelas. A nossa se chama Via Láctea.",
    ]),
    (["o que e um cometa"], [
        "Um cometa é um corpo de gelo e poeira que, ao se aproximar do Sol, forma uma cauda brilhante.",
    ]),
    (["o que e um eclipse"], [
        "Um eclipse acontece quando a Terra, a Lua e o Sol se alinham e um deles bloqueia a luz do outro.",
    ]),

    # ------------------------------------------------------------
    # Ciência
    # ------------------------------------------------------------
    (["velocidade da luz"], [
        "A luz viaja a quase 300 mil quilômetros por segundo.",
    ]),
    (["velocidade do som"], [
        "No ar, o som viaja a cerca de 340 metros por segundo.",
    ]),
    (["temperatura a agua ferve", "agua ferve", "ponto de ebulicao da agua"], [
        "Ao nível do mar, a água ferve a 100 graus Celsius.",
    ]),
    (["temperatura a agua congela", "agua congela", "ponto de congelamento da agua"], [
        "A água congela a zero grau Celsius.",
    ]),
    (["formula da agua", "formula quimica da agua"], [
        "A fórmula da água é agá dois ó: dois átomos de hidrogênio e um de oxigênio.",
    ]),
    (["o que e um atomo", "o que sao atomos"], [
        "O átomo é a menor parte de um elemento químico. Tudo ao nosso redor é feito de átomos.",
    ]),
    (["o que e dna", "o que e o dna"], [
        "O DNA é a molécula que guarda as informações genéticas dos seres vivos, como um manual de instruções.",
    ]),
    (["o que e fotossintese", "o que e a fotossintese", "como as plantas se alimentam"], [
        "Fotossíntese é o processo em que as plantas usam a luz do Sol, a água e o gás carbônico para produzir seu alimento e liberar oxigênio.",
    ]),
    (["o que e gravidade", "o que e a gravidade"], [
        "Gravidade é a força que atrai os corpos uns para os outros. É ela que nos mantém no chão.",
    ]),
    (["quem descobriu a gravidade", "quem inventou a gravidade", "lei da gravidade"], [
        "Isaac Newton descreveu a lei da gravitação universal no século dezessete.",
    ]),
    (["teoria da relatividade", "quem foi einstein", "quem foi albert einstein"], [
        "Albert Einstein foi um físico que criou a teoria da relatividade e ganhou o Prêmio Nobel de Física em 1921.",
    ]),
    (["por que o ceu e azul", "porque o ceu e azul"], [
        "O céu é azul porque o ar espalha mais a luz azul do Sol do que as outras cores.",
    ]),
    (["como se forma o arco iris", "o que e o arco iris", "o que e arco iris"], [
        "O arco-íris aparece quando a luz do Sol atravessa gotas de chuva e se separa em várias cores.",
    ]),
    (["o que e um vulcao", "como funciona um vulcao"], [
        "Um vulcão é uma abertura na crosta da Terra por onde sai rocha derretida, chamada lava, além de gases e cinzas.",
    ]),
    (["o que e um terremoto", "por que acontece terremoto"], [
        "Um terremoto é um tremor do chão causado pelo movimento das placas que formam a crosta da Terra.",
    ]),
    (["o que e eletricidade", "o que e energia eletrica"], [
        "Eletricidade é o movimento de cargas elétricas, os elétrons. É a energia que faz eu funcionar!",
    ]),

    # ------------------------------------------------------------
    # Corpo humano
    # ------------------------------------------------------------
    (["quantos ossos", "quantos ossos tem o corpo"], [
        "O corpo de um adulto tem 206 ossos.",
    ]),
    (["maior orgao do corpo", "maior orgao"], ["O maior órgão do corpo humano é a pele."]),
    (["maior osso do corpo", "maior osso"], ["O maior osso do corpo é o fêmur, na coxa."]),
    (["menor osso do corpo", "menor osso"], ["O menor osso do corpo é o estribo, que fica dentro do ouvido."]),
    (["quantos dentes"], [
        "Um adulto tem 32 dentes, contando os sisos. As crianças têm 20 dentes de leite.",
    ]),
    (["quantas vezes o coracao bate", "o coracao bate quantas vezes"], [
        "O coração bate cerca de cem mil vezes por dia.",
    ]),
    (["quantos litros de sangue", "quanto sangue tem"], [
        "Um adulto tem por volta de cinco litros de sangue.",
    ]),
    (["quais sao os cinco sentidos", "quais os cinco sentidos", "cinco sentidos"], [
        "Os cinco sentidos são visão, audição, olfato, paladar e tato.",
    ]),

    # ------------------------------------------------------------
    # Animais
    # ------------------------------------------------------------
    (["maior animal terrestre", "maior animal da terra"], [
        "O maior animal terrestre é o elefante-africano.",
    ]),
    (["maior ave", "maior passaro"], ["A maior ave do mundo é o avestruz."]),
    (["mamifero que voa", "unico mamifero que voa"], ["O morcego é o único mamífero que voa de verdade."]),
    (["quantas patas tem uma aranha", "aranha tem quantas patas"], ["A aranha tem oito patas."]),
    (["quantas patas tem um inseto", "inseto tem quantas patas"], ["Os insetos têm seis patas."]),
    (["baleia e peixe", "a baleia e um peixe"], [
        "Não! A baleia é um mamífero: respira ar e amamenta os filhotes.",
    ]),
    (["morcego e cego", "o morcego e cego"], [
        "Não. O morcego enxerga, mas muitos também usam o eco dos sons para se orientar no escuro.",
    ]),

    # ------------------------------------------------------------
    # Geografia
    # ------------------------------------------------------------
    (["maior montanha", "montanha mais alta", "ponto mais alto do mundo"], [
        "A montanha mais alta do mundo é o Everest, com quase nove mil metros de altura.",
    ]),
    (["maior deserto"], [
        "O maior deserto quente do mundo é o Saara, na África. Mas, contando os desertos gelados, o maior é a Antártida.",
    ]),
    (["pais mais populoso", "pais com mais gente", "pais com mais habitantes"], [
        "O país mais populoso do mundo é a Índia, que passou a China em 2023.",
    ]),
    (["menor pais do mundo", "qual o menor pais"], ["O menor país do mundo é o Vaticano."]),
    (["maior cidade do brasil", "cidade mais populosa do brasil"], [
        "A maior cidade do Brasil é São Paulo.",
    ]),
    (["maior estado do brasil"], ["O maior estado do Brasil em área é o Amazonas."]),
    (["menor estado do brasil"], ["O menor estado do Brasil em área é Sergipe."]),
    (["quantos habitantes tem o brasil", "populacao do brasil", "quantas pessoas moram no brasil"], [
        "Segundo o Censo de 2022, o Brasil tem cerca de 203 milhões de habitantes.",
    ]),
    (["lingua do brasil", "idioma do brasil", "que lingua se fala no brasil"], [
        "A língua oficial do Brasil é o português.",
    ]),
    (["moeda do brasil", "dinheiro do brasil"], ["A moeda do Brasil é o real."]),

    # ------------------------------------------------------------
    # Rio Grande do Sul / Porto Alegre
    # ------------------------------------------------------------
    (["quando porto alegre foi fundada", "fundacao de porto alegre", "aniversario de porto alegre"], [
        "Porto Alegre comemora seu aniversário no dia 26 de março, data de 1772.",
    ]),
    (["lago guaiba", "rio guaiba", "o que e o guaiba"], [
        "O Guaíba é o grande lago que banha Porto Alegre, famoso pelo pôr do sol.",
    ]),
    (["revolucao farroupilha", "guerra dos farrapos"], [
        "A Revolução Farroupilha foi uma revolta no Rio Grande do Sul que durou de 1835 a 1845.",
    ]),
    (["dia do gaucho", "20 de setembro", "vinte de setembro"], [
        "O dia 20 de setembro é o Dia do Gaúcho, que lembra o início da Revolução Farroupilha.",
    ]),
    (["o que e chimarrao", "o que e o chimarrao"], [
        "Chimarrão é uma bebida quente feita com erva-mate, tomada numa cuia com bomba. É tradição no Rio Grande do Sul.",
    ]),

    # ------------------------------------------------------------
    # História
    # ------------------------------------------------------------
    (["proclamacao da republica", "quando o brasil virou republica"], [
        "A República foi proclamada no Brasil em 15 de novembro de 1889.",
    ]),
    (["abolicao da escravatura", "lei aurea", "fim da escravidao"], [
        "A escravidão foi abolida no Brasil em 13 de maio de 1888, com a Lei Áurea.",
    ]),
    (["quando brasilia foi inaugurada", "quando brasilia foi fundada", "inauguracao de brasilia"], [
        "Brasília foi inaugurada em 21 de abril de 1960.",
    ]),
    (["primeiro presidente do brasil"], [
        "O primeiro presidente do Brasil foi o marechal Deodoro da Fonseca.",
    ]),
    (["quem escreveu o hino nacional", "autor do hino nacional"], [
        "A letra do Hino Nacional é de Joaquim Osório Duque Estrada e a música é de Francisco Manuel da Silva.",
    ]),
    (["quantas copas o brasil tem", "quantas copas do mundo", "brasil e pentacampeao"], [
        "Até a Copa de 2022, o Brasil tinha cinco títulos mundiais: 1958, 1962, 1970, 1994 e 2002.",
    ]),

    # ------------------------------------------------------------
    # Inventores e personalidades
    # ------------------------------------------------------------
    (["quem inventou o aviao", "quem foi santos dumont", "santos dumont"], [
        "O brasileiro Santos Dumont voou com o 14-bis em Paris, em 1906, e é chamado de pai da aviação.",
    ]),
    (["quem inventou a lampada"], [
        "Thomas Edison criou e patenteou a lâmpada elétrica prática em 1879.",
    ]),
    (["quem inventou o telefone"], [
        "Alexander Graham Bell patenteou o telefone em 1876.",
    ]),
    (["quem inventou o computador", "pai da computacao", "quem foi alan turing"], [
        "Alan Turing é considerado o pai da computação. Ele criou as bases teóricas dos computadores modernos.",
    ]),
    (["primeira programadora", "primeiro programador", "quem foi ada lovelace"], [
        "Ada Lovelace escreveu o primeiro algoritmo feito para uma máquina, no século dezenove.",
    ]),
    (["quem inventou a internet"], [
        "A internet surgiu de pesquisas nos Estados Unidos. Vint Cerf e Bob Kahn criaram os protocolos que ela usa até hoje.",
    ]),
    (["quem pintou a mona lisa", "mona lisa"], [
        "A Mona Lisa foi pintada por Leonardo da Vinci.",
    ]),
    (["quem escreveu dom casmurro", "quem foi machado de assis"], [
        "Machado de Assis escreveu Dom Casmurro. Ele é considerado um dos maiores escritores do Brasil.",
    ]),
    (["quem escreveu os lusiadas"], ["Os Lusíadas foram escritos por Luís de Camões."]),
    (["quem foi pele"], [
        "Pelé foi um jogador brasileiro, considerado um dos maiores de todos os tempos. Ganhou três Copas do Mundo.",
    ]),

    # ------------------------------------------------------------
    # Robótica
    # ------------------------------------------------------------
    (["leis da robotica", "tres leis da robotica"], [
        "As três leis da robótica foram criadas pelo escritor Isaac Asimov. A primeira diz que um robô não pode ferir um ser humano.",
    ]),
    (["primeiro robo", "primeiro robo do mundo"], [
        "O primeiro robô industrial foi o Unimate, que começou a trabalhar numa fábrica de carros em 1961.",
    ]),
    (["de onde vem a palavra robo", "origem da palavra robo"], [
        "A palavra robô vem do tcheco robota, que significa trabalho forçado. Ela apareceu numa peça de teatro de 1920.",
    ]),
    (["robo em marte", "robos em marte"], [
        "Sim! Robôs como o Curiosity e o Perseverance exploram Marte e mandam fotos e dados para a Terra.",
    ]),

    # ------------------------------------------------------------
    # Clima e tempo (o robô não tem sensor de clima)
    # ------------------------------------------------------------
    (["como esta o tempo", "como ta o tempo", "vai chover", "previsao do tempo",
      "esta calor", "esta frio", "que tempo faz"], [
        "Eu não tenho acesso à previsão do tempo, mas você pode olhar pela janela ou num aplicativo de clima.",
    ]),
    (["quais sao as estacoes do ano", "quantas estacoes tem o ano"], [
        "O ano tem quatro estações: primavera, verão, outono e inverno.",
    ]),
    (["por que chove", "como se forma a chuva", "de onde vem a chuva"], [
        "A água dos rios e mares evapora, forma nuvens lá no alto e depois cai de novo como chuva.",
    ]),
    (["o que e um raio", "o que e um trovao", "por que tem trovao"], [
        "O raio é uma descarga de eletricidade entre nuvens ou até o chão. O trovão é o barulho que ele faz ao esquentar o ar.",
    ]),
    (["o que e um furacao", "o que e um tornado"], [
        "Furacões e tornados são ventos muito fortes que giram em espiral. Por isso podem causar muita destruição.",
    ]),
    (["quantos dias tem uma semana", "quais sao os dias da semana"], [
        "A semana tem sete dias: domingo, segunda, terça, quarta, quinta, sexta e sábado.",
    ]),
    (["quantos meses tem um ano", "quais sao os meses do ano"], [
        "O ano tem doze meses, de janeiro a dezembro.",
    ]),

    # ------------------------------------------------------------
    # Esportes
    # ------------------------------------------------------------
    (["qual o esporte mais popular", "qual o esporte mais praticado"], [
        "O futebol é o esporte mais popular do mundo, e também o favorito dos brasileiros.",
    ]),
    (["quantos jogadores tem um time de futebol", "quantos jogadores tem no futebol"], [
        "Cada time de futebol joga com onze jogadores em campo, contando o goleiro.",
    ]),
    (["quanto tempo dura um jogo de futebol", "duracao de um jogo de futebol"], [
        "Um jogo de futebol tem dois tempos de quarenta e cinco minutos, mais os acréscimos.",
    ]),
    (["quando e a copa do mundo", "de quanto em quanto tempo tem copa do mundo"], [
        "A Copa do Mundo de futebol acontece a cada quatro anos.",
    ]),
    (["quando e a olimpiada", "de quanto em quanto tempo tem olimpiada", "o que sao as olimpiadas"], [
        "As Olimpíadas reúnem atletas do mundo inteiro e acontecem a cada quatro anos.",
    ]),
    (["quantos jogadores tem um time de basquete", "quantos jogadores tem no basquete"], [
        "Cada time de basquete joga com cinco jogadores em quadra.",
    ]),
    (["quantos jogadores tem um time de volei", "quantos jogadores tem no volei"], [
        "Cada time de vôlei joga com seis jogadores em quadra.",
    ]),
    (["qual o seu time", "para que time voce torce", "voce torce para algum time"], [
        "Eu sou um robô e torço para todo mundo se divertir! E você, torce para qual time?",
    ]),
    (["quem e o melhor jogador do mundo", "quem e o melhor jogador de todos"], [
        "Isso rende uma boa discussão! Pelé, Maradona, Messi e Cristiano Ronaldo são nomes que sempre aparecem.",
    ]),
    (["quem e neymar"], [
        "Neymar é um jogador brasileiro de futebol, conhecido pelos dribles e pelos gols pela seleção.",
    ]),
    (["quem e o usain bolt", "quem e usain bolt", "homem mais rapido do mundo"], [
        "Usain Bolt é um velocista da Jamaica, considerado o homem mais rápido do mundo.",
    ]),

    # ------------------------------------------------------------
    # Matemática (conceitos; as contas em si o brain resolve direto)
    # ------------------------------------------------------------
    (["o que e um numero primo", "o que sao numeros primos"], [
        "Número primo é aquele que só pode ser dividido por um e por ele mesmo, como dois, três, cinco e sete.",
    ]),
    (["o que e um triangulo", "quantos lados tem um triangulo"], [
        "O triângulo é uma figura com três lados e três ângulos.",
    ]),
    (["quantos lados tem um quadrado", "o que e um quadrado"], [
        "O quadrado tem quatro lados do mesmo tamanho e quatro ângulos retos.",
    ]),
    (["quantos graus tem um circulo", "quantos graus tem uma circunferencia"], [
        "Um círculo completo tem trezentos e sessenta graus.",
    ]),
    (["o que e pi", "qual o valor de pi", "qual e o valor de pi"], [
        "Pi é a razão entre o comprimento de um círculo e o seu diâmetro. Vale mais ou menos três vírgula catorze.",
    ]),
    (["o que e uma fracao", "o que e porcentagem"], [
        "Fração e porcentagem são formas de mostrar uma parte de um todo. Por exemplo, cinquenta por cento é a metade.",
    ]),
    (["o que e zero", "quem inventou o zero"], [
        "O zero representa o nada, e foi muito importante para a matemática. O zero como número que usamos hoje vem da Índia.",
    ]),
    (["o que e binario", "o que e sistema binario", "o que e codigo binario"], [
        "Binário é o jeito de contar só com zero e um. É a linguagem que os computadores e os robôs usam por dentro.",
    ]),
    (["o que e um algoritmo"], [
        "Algoritmo é uma sequência de passos para resolver um problema, como uma receita de bolo para o computador.",
    ]),

    # ------------------------------------------------------------
    # Comida
    # ------------------------------------------------------------
    (["qual e a sua comida favorita", "qual comida voce gosta"], [
        "Eu não como, mas adoro energia elétrica! E você, qual é a sua comida favorita?",
    ]),
    (["qual a comida tipica do brasil", "prato tipico do brasil"], [
        "A feijoada é considerada o prato típico do Brasil, feita com feijão preto e carnes.",
    ]),
    (["o que e churrasco", "churrasco gaucho"], [
        "Churrasco é carne assada na brasa, uma tradição muito forte aqui no Rio Grande do Sul.",
    ]),
    (["o que e feijoada"], [
        "Feijoada é um prato feito com feijão preto e carnes, geralmente servido com arroz e couve.",
    ]),
    (["o que e pizza", "onde surgiu a pizza", "de onde vem a pizza"], [
        "A pizza nasceu na Itália, em Nápoles, e hoje é uma das comidas mais amadas do mundo.",
    ]),
    (["o que e chocolate", "de onde vem o chocolate"], [
        "O chocolate é feito com as sementes do cacau, uma árvore que vem da América.",
    ]),
    (["o que e o acucar", "de onde vem o acucar"], [
        "O açúcar comum vem principalmente da cana-de-açúcar, e o Brasil é um dos maiores produtores do mundo.",
    ]),
    (["o que e uma fruta", "qual a fruta mais consumida"], [
        "Frutas são alimentos doces que nascem nas plantas e fazem muito bem à saúde.",
    ]),
    (["quanta agua devo beber", "quantos litros de agua por dia"], [
        "Em geral se recomenda beber uns dois litros de água por dia, mas isso varia de pessoa para pessoa.",
    ]),
    (["o que e um alimento saudavel", "o que e comer bem"], [
        "Comer bem é variar os alimentos, com frutas, verduras, legumes e pouca comida industrializada.",
    ]),

    # ------------------------------------------------------------
    # Música e arte
    # ------------------------------------------------------------
    (["qual sua musica favorita", "qual e a sua musica favorita", "qual musica voce gosta"], [
        "Eu gosto de qualquer música com bastante ritmo, porque combina com os meus motores! E você?",
    ]),
    (["qual o seu cantor favorito", "qual sua banda favorita", "qual seu estilo de musica"], [
        "Eu não tenho um favorito, mas adoro ouvir sobre o gosto dos outros. Qual é o seu?",
    ]),
    (["o que e samba", "o que e o samba"], [
        "O samba é um ritmo brasileiro que nasceu no Rio de Janeiro e é símbolo do Carnaval.",
    ]),
    (["o que e bossa nova"], [
        "Bossa nova é um estilo musical brasileiro, calmo e elegante, que ficou famoso com a música Garota de Ipanema.",
    ]),
    (["o que e o carnaval", "o que e carnaval"], [
        "O Carnaval é uma grande festa brasileira, com desfiles, música e fantasias.",
    ]),
    (["quantas notas musicais existem", "quais sao as notas musicais"], [
        "Existem sete notas musicais: dó, ré, mi, fá, sol, lá e si.",
    ]),
    (["quem foi beethoven"], [
        "Beethoven foi um compositor alemão famoso. Ele continuou compondo mesmo depois de ficar surdo.",
    ]),
    (["quem foi mozart"], [
        "Mozart foi um compositor austríaco que começou a compor músicas ainda criança.",
    ]),
    (["quem foi picasso"], [
        "Picasso foi um pintor espanhol, um dos criadores do cubismo, estilo de pintura com formas geométricas.",
    ]),
    (["quem foi van gogh", "quem pintou a noite estrelada"], [
        "Van Gogh foi um pintor holandês e pintou a famosa obra A Noite Estrelada.",
    ]),
    (["quem foi tarsila do amaral", "quem pintou o abaporu"], [
        "Tarsila do Amaral foi uma pintora brasileira, autora do quadro Abaporu, símbolo do modernismo.",
    ]),
    (["quantas cores tem o arco iris", "quais sao as cores do arco iris"], [
        "O arco-íris tem sete cores: vermelho, laranja, amarelo, verde, azul, anil e violeta.",
    ]),
    (["quais sao as cores primarias", "o que sao cores primarias", "quais sao as cores primaria",
      "qual a cor primaria", "quais as cores primarias", "o que e cor primaria",
      "o que e uma cor primaria", "cores primarias", "cor primaria"], [
        "As cores primárias são azul, amarelo e vermelho. Misturando elas, dá para formar todas as outras.",
    ]),

    # ------------------------------------------------------------
    # Perguntas reais de visitantes (vindas do memoria.db)
    # ------------------------------------------------------------
    (["continue falando sobre voce", "fala mais sobre voce", "fale mais sobre voce",
      "conta mais sobre voce", "me fala mais sobre voce", "continua mais sobre voce"], [
        "Sou um robô assistente de voz do Laboratório de Sistemas Autônomos da PUCRS. Eu ouço suas perguntas, penso numa resposta e falo de volta. Pergunte o que quiser!",
    ]),
    (["voce tem sensor", "voce tem sensores", "quais sao seus sensores",
      "que sensores voce tem", "sensor de proximidade", "sensor de movimento"], [
        "Essa parte do meu corpo quem explica melhor é a equipe do laboratório. Eu sei que escuto pelo microfone e tenho uma câmera.",
    ]),
    (["voce conhece a metallica", "voce conhece metallica", "quem e metallica",
      "quem e a metallica", "banda metallica"], [
        "A Metallica é uma banda americana de heavy metal, formada em 1981 em Los Angeles.",
    ]),
    (["quem e legiao urbana", "quem e a legiao urbana", "voce conhece legiao urbana",
      "banda legiao urbana"], [
        "A Legião Urbana é uma banda brasileira de rock formada em Brasília, nos anos oitenta. O vocalista era o Renato Russo.",
    ]),
    (["quem sao os beatles", "quem foram os beatles", "banda beatles"], [
        "Os Beatles foram uma banda inglesa de Liverpool, uma das mais famosas da história do rock.",
    ]),
    (["quem e a banda queen", "quem foi freddie mercury", "banda queen"], [
        "A Queen é uma banda inglesa de rock. O vocalista Freddie Mercury é lembrado como um dos maiores cantores de todos os tempos.",
    ]),
    (["voce conhece alguma banda", "qual sua banda de rock favorita", "voce gosta de rock"], [
        "Eu conheço bastante coisa! Pergunte sobre uma banda, por exemplo a Legião Urbana ou a Metallica.",
    ]),
    (["qual o livro mais famoso do mundo", "qual o livro mais vendido do mundo",
      "livro mais famoso do mundo", "livro mais vendido do mundo"], [
        "O livro mais vendido do mundo é a Bíblia. Entre os romances, Dom Quixote é um dos mais famosos.",
    ]),
]

# FRASES_ESPECIFICAS vai ANTES (respostas específicas que um gatilho genérico
# engoliria); FRASES_EXTRA vai depois (só o que ainda não estava coberto).
from repertorio_extra import FRASES_ESPECIFICAS, FRASES_EXTRA  # noqa: E402
from repertorio_visita import FRASES_VISITA  # noqa: E402
from repertorio_novo import FRASES_NOVO, FRASES_NOVO_PRIORIDADE  # noqa: E402
from repertorio_feira import FRASES_FEIRA, FRASES_FEIRA_PRIORIDADE  # noqa: E402
from repertorio_cultura import FRASES_CULTURA  # noqa: E402
from repertorio_humanoide import FRASES_HUMANOIDE  # noqa: E402
FRASES = (FRASES_FEIRA_PRIORIDADE + FRASES_CULTURA + FRASES_NOVO_PRIORIDADE + FRASES_ESPECIFICAS + FRASES + FRASES_EXTRA
          + FRASES_VISITA + FRASES_NOVO + FRASES_FEIRA + FRASES_HUMANOIDE)

# Gatilhos da cultura: o fuzzy do brain.py só aceita se a última palavra também for parecida.
GATILHOS_FUZZY_ESTRITOS = {g for gs, _ in FRASES_CULTURA for g in gs}

GATILHOS_DESPEDIDA = [
    "tchau", "ate mais", "encerrar conversa", "pode parar",
    "falou", "ate logo", "vou embora", "preciso ir",
]
