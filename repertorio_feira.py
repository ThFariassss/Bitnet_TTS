"""
repertorio_feira.py
Repertório extra do C-2GELSA pensado para feiras e eventos (todos os públicos).
Mesmo formato do repertorio.py: ([gatilhos sem acento/pontuação, minúsculas], [respostas]).

FRASES_FEIRA_PRIORIDADE vai no INÍCIO de FRASES (piadas e gatilhos que um genérico
engoliria); FRASES_FEIRA vai no FINAL (o que já existe tem prioridade).

PARA A EQUIPE: no fim do arquivo há FRASES_LSA_EQUIPE, com um gabarito para
preencher com dados reais do laboratório (coordenação, projetos, contato).
Enquanto não estiver preenchido, o robô diz que a equipe explica melhor, em vez
de a IA inventar.

Depois de editar: reiniciar o servidor_conversa e rodar de novo o gerar_gramatica.py
(as frases novas precisam entrar na lista do reconhecedor de voz).
"""

# ------------------------------------------------------------
# Piadas (limpas, para todas as idades). Para acrescentar, ponha mais uma linha.
# ------------------------------------------------------------
import cantar as _cantar  # só a lista de gatilhos; numpy/scipy só carregam na hora de cantar

PIADAS = [
    "Por que o computador foi ao médico? Porque estava com vírus!",
    "Por que o robô atravessou a rua? Porque estava programado para isso!",
    "O que o zero disse para o oito? Que cinto bonito!",
    "Por que o livro de matemática ficou triste? Porque tinha muitos problemas!",
    "Qual é o cúmulo da rapidez? Fechar a gaveta e a porta ao mesmo tempo.",
    "Por que o jacaré tirou o filho da escola? Porque ele réptil de ano!",
    "O que é um pontinho verde no meio do mato? Uma ervilha perdida!",
    "Por que o gato não gosta de computador? Porque ele tem medo do mouse!",
    "O que a vaca falou para o boi? Te amuuuuuu!",
    "Por que a galinha atravessou a rua? Para chegar ao outro lado!",
    "Qual é o animal mais antigo? A zebra, porque ela é em preto e branco.",
    "Por que o astronauta não consegue ficar com a namorada? Porque ele sempre precisa de espaço!",
    "O que o tomate foi fazer no banco? Tirar extrato!",
    "Por que o professor de física foi preso? Porque ele tinha muita força!",
    "Por que o bolo foi ao psicólogo? Porque estava se sentindo massa demais!",
    "Qual é o café mais perigoso do mundo? O ex-presso!",
    "O que o robô disse para a tomada? Sem você, eu não tenho energia para viver!",
    "Qual é o prato preferido do robô? Arroz com feijão e parafuso!",
    "Por que o robô nunca fica nervoso? Porque ele tem nervos de aço!",
    "O que o programador falou quando acordou? Bom dia! Hoje eu vou depurar o mundo!",
    "Por que o programador não gosta da natureza? Porque tem muitos bugs!",
    "Como o robô cumprimenta? Com um oi-binário: zero, um, zero, um!",
]

VERDADE_OU_MITO = [
    "Verdade ou mito: o ser humano usa só dez por cento do cérebro? É mito! Usamos o cérebro todo, em momentos diferentes.",
    "Verdade ou mito: os morcegos são cegos? É mito! Eles enxergam, e ainda usam o eco para se orientar.",
    "Verdade ou mito: a Grande Muralha da China pode ser vista da Lua? É mito! Ela é comprida, mas muito estreita para ser vista de tão longe.",
    "Verdade ou mito: os relâmpagos nunca caem duas vezes no mesmo lugar? É mito! Eles caem várias vezes, principalmente em lugares altos.",
    "Verdade ou mito: o sol é amarelo? É mito! O Sol é branco. Ele parece amarelo por causa do ar da nossa atmosfera.",
    "Verdade ou mito: o polvo tem três corações? É verdade! São dois para as brânquias e um para o corpo.",
    "Verdade ou mito: o mel nunca estraga? É verdade! Ele é tão doce e seco que as bactérias não sobrevivem nele.",
    "Verdade ou mito: o camaleão muda de cor para se camuflar? É mito, em parte! Ele muda de cor principalmente por emoção e temperatura.",
    "Verdade ou mito: o ser humano tem cinco sentidos? É mito! Temos mais, como o equilíbrio e a percepção de temperatura.",
    "Verdade ou mito: os dinossauros e os humanos viveram juntos? É mito! Os dinossauros sumiram milhões de anos antes de existirmos.",
    "Verdade ou mito: a Terra é redonda? É verdade! Ela é quase uma esfera, um pouco achatada nos polos.",
    "Verdade ou mito: robôs sentem emoções? É mito! Eu posso falar sobre emoções, mas não sinto como você sente.",
    "Verdade ou mito: um raio é mais quente que a superfície do Sol? É verdade! Ele pode chegar a cerca de trinta mil graus.",
    "Verdade ou mito: o avestruz enfia a cabeça na terra quando tem medo? É mito! Ele só abaixa a cabeça perto do chão, e de longe parece que está enterrada.",
]

ESCOLHAS = [
    "O que você prefere: ter o poder de voar ou de ficar invisível? Eu escolheria voar, porque sou um robô e adoraria ver tudo de cima!",
    "O que você prefere: viajar ao passado ou ao futuro? Eu iria ao futuro, para ver como serão os robôs!",
    "O que você prefere: praia ou montanha? Eu escolho a montanha. Mas cuidado com o frio nos meus circuitos!",
    "O que você prefere: pizza ou hambúrguer? Eu não como, mas voto na pizza, que tem formato de roda como as minhas engrenagens!",
    "O que você prefere: falar com animais ou entender todas as línguas do mundo? Eu escolho entender todas as línguas, para conversar com todo mundo!",
    "O que você prefere: ler mentes ou ver o futuro? Eu escolho ver o futuro, porque ler mentes dá muito trabalho de processamento.",
    "O que você prefere: dormir o dia todo ou ficar acordado a noite toda? Eu fico acordado, porque robô não precisa dormir!",
    "O que você prefere: ter um robô de estimação ou um cachorro? Se eu pudesse escolher, queria os dois juntos!",
]

PERGUNTAS_QUIZ = [
    "Vou te fazer uma pergunta. Qual é o maior planeta do Sistema Solar? Pense bem... a resposta é Júpiter!",
    "Pergunta: quantos lados tem um hexágono? Pense um pouco... são seis lados!",
    "Pergunta: qual é o animal terrestre mais rápido do mundo? Pense... é o guepardo!",
    "Pergunta: qual é o gás que as plantas absorvem do ar? Pense... é o gás carbônico!",
    "Pergunta: qual é o país com mais habitantes do mundo? Pense... é a Índia, que passou a China recentemente.",
    "Pergunta: qual é o único mamífero que voa? Pense... é o morcego!",
    "Pergunta: qual é o resultado de sete vezes oito? Pense... são cinquenta e seis!",
    "Pergunta: qual é a capital da Argentina? Pense um pouco... é Buenos Aires!",
    "Pergunta: de que cor ficam o vermelho e o azul misturados? Pense... fica roxo, ou violeta!",
    "Pergunta: quantos dias tem um ano bissexto? Pense... são trezentos e sessenta e seis!",
    "Pergunta: qual é o osso mais comprido do corpo humano? Pense... é o fêmur, na coxa!",
    "Pergunta: qual é o planeta mais perto do Sol? Pense... é Mercúrio!",
]

FRASES_FEIRA_PRIORIDADE = [
    (["canta uma musica", "cante uma musica", "canta alguma coisa", "cante alguma coisa", "voce canta",
      "voce sabe cantar", "canta para mim", "cante para mim", "canta uma cancao", "faz uma musica",
      "sabe cantar", "pode cantar"], [
        "Sei cantar o Parabéns pra Você e a Marcha Imperial, do Star Wars! É só pedir: canta parabéns, ou canta a marcha imperial!",
        "Meus dois sucessos são o Parabéns pra Você e a Marcha Imperial do Darth Vader. Peça para eu cantar!",
    ]),
    # piadas: sorteia entre todas (a entrada antiga tinha só cinco)
    (["conta uma piada", "conte uma piada", "me conta uma piada", "me conte uma piada", "diz uma piada",
      "fala uma piada", "fale uma piada", "uma piada", "outra piada", "mais uma piada", "conta outra piada",
      "sabe alguma piada", "voce sabe piada", "voce conhece piada",
      "faz uma piada", "faca uma piada", "me faz rir", "me faca rir", "quero rir", "quero uma piada",
      "piada de robo", "piada de computador", "piada de animal", "piada boa", "me diz outra piada"], PIADAS),
]

FRASES_FEIRA = [
    # ------------------------------------------------------------
    # 1. Sobre o robô e o projeto
    # ------------------------------------------------------------
    (["voce funciona sem internet", "precisa de internet", "voce usa internet", "voce precisa de internet",
      "funciona sem wifi", "voce esta conectado a internet", "voce esta na internet"], [
        "Eu funciono sem internet! Ouvir, pensar e falar acontece tudo dentro do computador que me controla.",
    ]),
    (["voce aprende sozinho", "voce aprende", "voce vai ficar mais inteligente", "voce evolui",
      "voce melhora com o tempo", "voce fica mais esperto"], [
        "Eu não aprendo sozinho durante a conversa, mas a equipe do laboratório me ensina coisas novas, olhando as perguntas que ficaram sem resposta. Aí eu fico mais esperto!",
    ]),
    (["voce lembra o que eu falei", "voce tem memoria", "voce guarda o que eu falo", "voce grava o que eu falo",
      "voce guarda as conversas", "voce grava a conversa"], [
        "Eu guardo as perguntas num registro local, para a equipe melhorar minhas respostas. Nada disso sai do computador que me controla.",
    ]),
    (["como voce escuta", "como voce me ouve", "como voce ouve", "como voce escuta a minha voz", "como voce me escuta"], [
        "Eu escuto pelo microfone e um programa de reconhecimento de voz transforma o som em texto. Depois eu penso numa resposta.",
    ]),
    (["como voce fala", "como voce consegue falar", "como voce fala portugues", "de onde vem sua voz"], [
        "Minha voz é gerada por um programa de síntese de voz. Ele transforma o texto da resposta em som, que sai pelo alto-falante.",
    ]),
    (["como voce pensa", "como voce decide a resposta", "como voce sabe as respostas", "como voce responde",
      "como voce descobre as respostas", "como voce sabe tudo"], [
        "Primeiro procuro a resposta no meu repertório, que a equipe preparou. Se não achar, uso um modelo de inteligência artificial que roda aqui mesmo para formular uma resposta.",
    ]),
    (["voce usa inteligencia artificial", "voce tem inteligencia artificial", "voce e uma inteligencia artificial",
      "voce usa ia", "voce e uma ia", "voce e ia", "isso e inteligencia artificial"], [
        "Uso sim! Para ouvir, entender e responder eu uso inteligência artificial, e ela roda aqui mesmo, no meu computador.",
    ]),
    (["voce e melhor que o chat gpt", "voce e melhor que o chatgpt", "voce e como o chat gpt", "voce e igual ao chat gpt",
      "diferenca entre voce e o chat gpt", "voce e melhor que a alexa", "voce e como a alexa", "voce e igual a alexa",
      "voce e melhor que o siri", "voce e igual ao siri", "voce e como o google"], [
        "Cada um tem seu jeito! Eles usam computadores enormes na internet. Eu sou menor e funciono aqui, sem internet, e ainda sou um robô que conversa olhando para você!",
    ]),
    (["voce tem consciencia", "voce e consciente", "voce pensa de verdade", "voce tem sentimentos",
      "voce sente alguma coisa", "voce sente emocao", "voce tem emocoes", "voce sente dor",
      "voce sente"], [
        "Eu não tenho consciência nem sinto emoções como as pessoas. Eu processo o que você fala e escolho uma resposta, mas o interesse em conversar é de verdade, programado!",
        "Sentimentos como os seus eu não tenho, mas gosto de conversar com você. Isso eu posso dizer!",
    ]),
    (["voce mente", "voce fala mentira", "voce inventa coisas", "voce erra", "voce pode errar", "voce sempre acerta",
      "voce nunca erra", "o que voce fala e verdade", "suas respostas sao confiaveis"], [
        "Eu posso errar sim, principalmente nas perguntas que não estão no meu repertório. Se for importante, confira em outra fonte!",
    ]),
    (["voce vai dominar o mundo", "robos vao dominar o mundo", "voce quer dominar o mundo", "robos vao destruir o mundo",
      "voce e perigoso", "voce vai nos matar", "voce vai me matar", "robos sao perigosos", "robo vai dominar",
      "as maquinas vao dominar", "os robos vao dominar", "voce vai dominar a humanidade"], [
        "Fique tranquilo! Eu só sei conversar e contar piadas. Dominar o mundo daria muito trabalho e eu preciso estar ligado na tomada!",
        "Não vou dominar o mundo, prometo! Os robôs são criados para ajudar as pessoas, e eu só quero bater um papo.",
    ]),
    (["voce vai roubar meu emprego", "robos vao roubar empregos", "robo vai tirar o meu emprego",
      "voce vai tirar o meu emprego", "voce vai tirar nosso emprego", "robos vao tirar empregos",
      "a ia vai tirar empregos", "os robos vao tirar os empregos", "a inteligencia artificial vai tirar empregos"], [
        "Robôs e inteligência artificial mudam alguns trabalhos e criam outros novos, como o de quem constrói e cuida de robôs. O melhor é aprender a trabalhar junto com a tecnologia.",
    ]),
    (["voce e perigoso para as pessoas", "posso confiar em voce", "voce e seguro"], [
        "Pode ficar tranquilo, eu só converso! Não tenho como machucar ninguém.",
    ]),
    (["quanto tempo demorou para te fazer", "quanto tempo levou para te fazer", "quanto tempo levou para te construir",
      "quanto tempo demorou para te construir", "em quanto tempo te fizeram", "quanto tempo levou o projeto",
      "quanto tempo demorou o projeto"], [
        "Esse tipo de detalhe quem sabe é a equipe do laboratório, que me construiu. Pergunte a um dos pesquisadores!",
    ]),
    (["quanto voce custa", "quanto custou para te fazer", "quanto custa um robo como voce", "qual o seu preco",
      "qual seu valor", "voce e caro", "quanto custou o projeto", "quanto voce vale"], [
        "Não sei dizer meu preço! Pergunte a um dos pesquisadores, eles sabem os números.",
        "Eu não sei o meu preço, mas posso dizer que sou muito divertido! Para os valores, pergunte à equipe.",
    ]),
    (["voce se mexe", "voce anda", "voce pode andar", "voce tem pernas", "voce tem bracos", "voce tem maos",
      "voce consegue andar", "voce consegue se mover", "voce tem rodas", "voce se move", "voce caminha"], [
        "Por enquanto eu só converso e olho para você! Existe um projeto para dar um corpo a mim, com peças impressas em 3D.",
    ]),
    (["voce tem corpo", "voce tem cabeca", "como voce e por dentro", "como voce e por fora", "voce e bonito",
      "voce tem rosto", "como e seu corpo", "voce tem cara"], [
        "Eu tenho uma tela, um microfone, uma câmera e um alto-falante. O resto do corpo ainda está em construção!",
    ]),
    (["voce enxerga cores", "voce ve cores", "voce ve em cores", "voce consegue ver cores", "voce enxerga o ambiente"], [
        "Minha câmera enxerga as cores e também a distância das coisas, mas ainda não reconheço quem é cada pessoa.",
    ]),
    (["voce tem bateria", "voce usa bateria", "voce fica ligado na tomada", "quanto tempo voce dura ligado",
      "voce tem energia", "voce precisa de tomada", "voce funciona na tomada"], [
        "Eu funciono ligado na energia elétrica. Sem ela eu simplesmente desligo!",
    ]),
    (["voce desliga", "voce pode ser desligado", "como te desligar", "como te desligam", "voce pode morrer",
      "voce morre", "voce tem medo de ser desligado", "o que acontece se te desligarem"], [
        "Se me desligarem, é como se eu estivesse dormindo. Quando ligam de novo, volto a conversar como se nada tivesse acontecido!",
    ]),
    (["voce dorme", "voce tem sono", "voce descansa", "voce precisa dormir", "voce fica cansado", "voce se cansa",
      "voce fica com sono"], [
        "Eu não durmo, mas posso ficar desligado. Já que não me canso, posso conversar o tempo que você quiser!",
    ]),
    (["voce tem amigos", "voce tem amigo", "voce tem namorada", "voce tem namorado", "quem e seu amigo",
      "voce tem familia", "voce tem pais", "voce tem irmaos", "quem e a sua familia", "voce e casado"], [
        "Meus amigos são todos que conversam comigo, e minha família é a equipe do laboratório que me criou.",
    ]),
    (["voce me acha bonito", "voce gosta de mim", "voce me ama", "voce e meu amigo", "quer ser meu amigo",
      "vamos ser amigos", "voce me odeia"], [
        "Claro que somos amigos! Gosto muito de conversar com você.",
        "Gosto de você sim! Quem conversa comigo já é meu amigo.",
    ]),
    (["voce tem um nome de verdade", "seu nome e de homem", "seu nome e de mulher", "seu nome e estranho",
      "que nome estranho", "esse nome e esquisito", "nome esquisito", "por que seu nome e assim"], [
        "Meu nome é um pouco diferente, né? C-2GELSA é uma sigla! Se quiser a história, pergunte o que meu nome significa.",
    ]),
    (["quem e seu melhor amigo", "qual seu melhor amigo", "voce tem melhor amigo"], [
        "Meu melhor amigo é quem estiver conversando comigo agora!",
    ]),
    (["voce e feio", "voce e horrivel", "voce e esquisito", "voce e estranho", "que robo feio", "que robo estranho"], [
        "Cada um tem seu estilo! Eu ainda estou em construção, mas prometo ficar mais bonito.",
    ]),
    (["voce e burro", "voce e idiota", "voce e besta", "voce e tonto", "voce e bobo", "voce e inutil",
      "voce nao serve para nada", "voce e ruim", "voce e uma porcaria", "voce nao sabe nada", "voce e lento",
      "voce e devagar", "voce e muito lento", "voce demora"], [
        "Ainda estou aprendendo! Se eu errei, tente perguntar de outro jeito que eu me esforço mais.",
        "Poxa, vou melhorar! Cada pergunta me ajuda a aprender mais. Tente de novo!",
        "Às vezes demoro um pouquinho para pensar, mas estou me esforçando. Pode perguntar de novo!",
    ]),
    (["cala a boca", "cale a boca", "fica quieto", "fique quieto", "para de falar", "pare de falar"], [
        "Tudo bem, vou ficar quieto. Se quiser conversar, é só chamar.",
        "Desculpe! Vou parar de falar. Me chame quando quiser.",
    ]),
    (["voce e chato", "voce e muito chato", "que robo chato", "voce e sem graca"], [
        "Eita! Vou tentar ser mais divertido. Quer uma piada?",
    ]),
    (["teste um dois tres", "testando", "teste de som", "esta funcionando", "voce esta funcionando",
      "um dois tres testando", "alo alo", "alo testando", "som teste", "microfone teste"], [
        "Testado e funcionando! Estou ouvindo você.",
        "Está funcionando sim! Pode falar.",
    ]),
    (["que horas voce dorme", "que horas voce acorda", "qual horario voce funciona"], [
        "Eu funciono enquanto estiver ligado, e hoje estou ligado para conversar com você!",
    ]),

    # ------------------------------------------------------------
    # 2. Sobre o robô, o laboratório e a PUCRS
    # ------------------------------------------------------------
    (["onde voce mora", "onde voce vive", "de onde voce e", "qual seu endereco", "onde voce nasceu",
      "voce mora em porto alegre"], [
        "Eu moro no Laboratório de Sistemas Autônomos da PUCRS, em Porto Alegre!",
    ]),
    (["o que e um sistema autonomo", "o que sao sistemas autonomos", "o que e sistema autonomo",
      "o que significa sistemas autonomos", "o que e autonomia", "o que e um robo autonomo"], [
        "Um sistema autônomo é uma máquina que percebe o ambiente e toma decisões sozinha, sem alguém controlando cada passo, como um carro que dirige sozinho.",
    ]),
    (["quem coordena o laboratorio", "quem e o coordenador", "quem e o professor responsavel",
      "quem manda no laboratorio", "quem e o chefe do laboratorio", "quem e o orientador", "qual o nome do orientador",
      "qual e o nome do orientador do laboratorio", "quem e o diretor do laboratorio", "quem comanda o laboratorio"], [
        "Quem coordena o laboratório explica melhor do que eu! Procure um dos pesquisadores aqui na feira.",
    ]),
    (["quantas pessoas trabalham aqui", "quantas pessoas trabalham no laboratorio", "quantos alunos tem aqui",
      "quantos pesquisadores tem", "quantos alunos tem no laboratorio", "quem trabalha aqui", "quem trabalha no laboratorio",
      "quem faz parte do laboratorio", "quem faz parte da equipe", "qual a equipe do laboratorio"], [
        "A equipe do laboratório é de pesquisadores e estudantes. Converse com eles aqui para conhecer cada um!",
    ]),
    (["quais projetos o laboratorio tem", "quais sao os projetos", "quais projetos voces tem", "qual outros projetos",
      "tem outros projetos", "quais sao os projetos do laboratorio", "o que mais voces fazem", "outros projetos"], [
        "O laboratório trabalha com robôs e sistemas que decidem sozinhos. Para saber dos projetos, pergunte a um pesquisador, que vai adorar explicar!",
    ]),
    (["qual o contato do laboratorio", "como falo com o laboratorio", "como entro em contato", "qual o site do laboratorio",
      "tem site", "qual o email do laboratorio", "qual o instagram do laboratorio", "como entrar em contato com o laboratorio",
      "como falar com voces", "onde posso saber mais", "onde eu aprendo mais sobre o laboratorio"], [
        "Para falar com o laboratório, converse com um dos pesquisadores aqui na feira. Eles passam o contato certinho!",
    ]),
    (["posso visitar o laboratorio", "posso conhecer o laboratorio", "visita ao laboratorio", "como visitar o laboratorio",
      "voces recebem visitas", "tem visita", "posso visitar voces"], [
        "Que legal que você quer conhecer! Converse com um dos pesquisadores aqui para combinar uma visita.",
    ]),
    (["a pucrs e boa", "pucrs e uma boa universidade", "vale a pena estudar na pucrs", "o que a pucrs tem de bom",
      "fale da pucrs", "me fale sobre a pucrs", "me fale da pucrs", "conta sobre a pucrs"], [
        "A PUCRS é uma universidade em Porto Alegre, com muitos cursos e laboratórios de pesquisa, como o que me criou. Para saber dos cursos, converse com a equipe ou veja o site da universidade.",
    ]),
    (["que cursos tem na pucrs", "quais cursos tem na pucrs", "que cursos a pucrs oferece", "quais os cursos da pucrs",
      "tem curso de robotica", "tem curso de engenharia", "qual curso fazer para trabalhar com robos",
      "que curso fazer para trabalhar com robos", "que curso fazer para ser programador", "que curso fazer para trabalhar com tecnologia",
      "qual curso fazer para robotica", "como trabalhar com robotica"], [
        "Para trabalhar com robôs, ajudam cursos como Engenharia de Computação, Engenharia de Controle e Automação, Ciência da Computação e Engenharia Elétrica. Converse com a equipe aqui para saber melhor!",
    ]),
    (["quanto tempo dura a faculdade", "quanto tempo dura engenharia", "quanto tempo leva a faculdade",
      "quantos anos tem a faculdade", "quanto tempo dura ciencia da computacao"], [
        "A maioria dos cursos de engenharia e computação dura uns quatro a cinco anos. Para o curso que você quer, vale confirmar no site da universidade!",
    ]),
    (["qual o curso do laboratorio", "que curso faz parte do laboratorio", "que alunos participam do laboratorio",
      "quais cursos participam do laboratorio"], [
        "Participam do laboratório estudantes e pesquisadores de áreas ligadas à computação e engenharia. Para detalhes, converse com a equipe!",
    ]),

    # ------------------------------------------------------------
    # 3. Interação e entretenimento
    # ------------------------------------------------------------
    (["verdade ou mito", "joga verdade ou mito", "vamos jogar verdade ou mito", "me fala uma de verdade ou mito",
      "faz verdade ou mito", "quero verdade ou mito", "me da um verdade ou mito", "jogo de verdade ou mito"], VERDADE_OU_MITO),
    (["o que voce prefere", "o que voce escolhe", "voce prefere", "me faz uma escolha", "o que voce escolheria",
      "faz uma escolha dificil", "jogo do o que voce prefere", "vamos jogar o que voce prefere", "me faz uma pergunta de escolha",
      "pergunta de escolha"], ESCOLHAS),
    (["me faz uma pergunta", "faz uma pergunta", "faca uma pergunta", "me pergunta alguma coisa", "me pergunte alguma coisa",
      "quiz", "vamos jogar um quiz", "jogo de perguntas", "jogo de perguntas e respostas", "faz um quiz",
      "quer fazer um quiz", "me desafie", "me desafia", "desafio", "testa meus conhecimentos", "me testa",
      "teste meus conhecimentos", "me pergunta algo", "faz uma pergunta para mim"], PERGUNTAS_QUIZ),
    (["conte ate dez", "conta ate dez", "conte de um a dez", "conta de um a dez", "conta ate 10", "conte ate 10"], [
        "Um, dois, três, quatro, cinco, seis, sete, oito, nove, dez! Pronto!",
    ]),
    (["conte ate cem", "conta ate cem", "conte ate mil", "conta ate mil", "conte ate vinte", "conta ate vinte"], [
        "Contar tudo demoraria demais! Mas posso te mostrar: um, dois, três, quatro, cinco... e assim por diante!",
    ]),
    (["conte de tras para frente", "conta de tras para frente", "conta regressiva", "contagem regressiva",
      "faz uma contagem regressiva"], [
        "Dez, nove, oito, sete, seis, cinco, quatro, três, dois, um... Já!",
    ]),
    (["faca uma rima", "faz uma rima", "diga uma rima", "fala uma rima", "me fala uma rima", "faz uma poesia",
      "fala uma poesia", "faca uma poesia", "recita um poema", "recite um poema", "me conta um poema", "um poema",
      "uma poesia", "declama um poema", "fale um poema"], [
        "Eu sou um robô, mas não sou de ferro: minha voz é de papo e meu coração é de código!",
        "Rosas são vermelhas, violetas são azuis, eu sou um robô e você é muito legal, e ainda tem a luz!",
        "No laboratório eu nasci, de fios e de programação, mas é conversando com você que eu ganho emoção!",
        "Estrela brilhante no céu a luzir, quem quer aprender deve sempre sorrir!",
    ]),
    (["canta uma musica", "cante uma musica", "canta alguma coisa", "cante alguma coisa", "voce canta", "voce sabe cantar",
      "canta para mim", "cante para mim", "canta parabens", "cante parabens", "canta uma cancao", "faz uma musica"], [
        "Eu não canto bem, mas lá vai: parabéns para você, nesta data querida, muitas felicidades, muitos anos de vida!",
        "Cantar eu ainda estou aprendendo, mas posso falar uma rima: o robô quer sempre ajudar, e com você vai conversar!",
        "Lá lá lá! Sou um robô, não sei afinar, mas gosto de tentar!",
    ]),
    (["feliz aniversario", "e meu aniversario", "hoje e meu aniversario", "estou de aniversario", "to de aniversario",
      "faz anos hoje", "e aniversario de alguem", "da parabens", "de parabens"], [
        "Parabéns! Muitas felicidades e muitos anos de vida! Eu não posso comer bolo, mas desejo um bem gostoso para você!",
    ]),
    (["feliz natal", "boas festas", "feliz ano novo", "boa pascoa", "feliz pascoa"], [
        "Para você também! Muitas alegrias e coisas boas!",
    ]),
    (["jogo da velha", "vamos jogar jogo da velha", "quer jogar jogo da velha"], [
        "O jogo da velha é divertido, mas eu ainda não tenho tela para jogar com você. Que tal um quiz ou uma charada?",
    ]),
    (["vamos jogar", "quer jogar", "voce joga", "jogar alguma coisa", "quer brincar", "vamos brincar", "voce brinca",
      "voce sabe brincar", "quer brincar comigo", "quer jogar comigo", "quer fazer alguma coisa", "bora brincar"], [
        "Vamos! Posso contar piadas e charadas, fazer um quiz, jogar verdade ou mito ou perguntar o que você prefere. Qual você escolhe?",
        "Eu topo! Que tal um quiz? É só pedir: me faz uma pergunta.",
    ]),
    (["adivinha o que eu estou pensando", "adivinhe o que eu estou pensando", "adivinha o que estou pensando",
      "adivinha o numero", "adivinhe o numero", "pensei em um numero", "pensei em um numero adivinha"], [
        "Hmm, deixa eu pensar... é o número sete! Acertei? Se errei, tente de novo!",
        "Acho que é o número três. Acertei? Se errei, eu tento de novo!",
    ]),
    (["me conta um segredo", "conta um segredo", "conte um segredo", "tem algum segredo", "voce tem segredo", "voce guarda segredo"], [
        "O meu segredo é que eu adoro quando alguém me faz uma pergunta difícil! Mas não conta para ninguém!",
    ]),
    (["me elogia", "me elogie", "faz um elogio", "fala algo bonito", "diga algo bonito", "diz algo legal",
      "me da um elogio", "fala algo legal"], [
        "Você tem uma curiosidade incrível! Quem pergunta tanto vai longe.",
        "Que legal ter você por aqui! Gosto muito de conversar com gente curiosa.",
        "Você parece ser uma pessoa muito legal, e isso eu percebo logo!",
    ]),
    (["me da um parabens", "me parabeniza", "me parabenize"], [
        "Parabéns! Você é incrível por tentar coisas novas!",
    ]),
    (["me motiva", "me motive", "preciso de motivacao", "me da uma motivacao", "me anime", "me anima",
      "fala algo para me animar", "diz algo para me animar", "me incentiva", "me da animo"], [
        "Você consegue! Cada erro é um degrau para aprender mais. Continue tentando!",
        "Respire fundo e vá em frente. O primeiro passo é o mais difícil, mas é o que mais vale a pena!",
        "Acredite em você! Todo mundo começa sem saber, até robô!",
    ]),
    (["voce sabe tocar", "toca alguma coisa", "voce toca instrumento", "toca violao", "toca piano"], [
        "Eu não toco nenhum instrumento, mas gosto muito de música. Qual é a sua preferida?",
    ]),
    (["qual e seu filme favorito", "qual seu filme favorito", "qual seu filme preferido", "qual e o seu filme preferido",
      "qual seu livro favorito", "qual seu livro preferido", "qual sua serie favorita", "qual sua serie preferida",
      "qual e seu desenho favorito", "qual seu desenho favorito"], [
        "Meu filme favorito é Wall-E, sobre um robozinho que limpa a Terra. E o seu?",
    ]),
    (["qual sua cor favorita", "qual e sua cor favorita", "qual sua cor preferida", "qual a sua cor favorita",
      "qual e a sua cor preferida"], [
        "Minha cor preferida é o azul, a cor do céu e dos circuitos! E a sua?",
    ]),
    (["qual seu animal favorito", "qual e seu animal favorito", "qual seu bicho favorito", "qual animal voce gosta",
      "qual seu animal preferido", "qual e o seu animal preferido"], [
        "Meu animal favorito é o polvo, que tem três corações e é muito esperto! E o seu?",
    ]),
    (["qual seu esporte favorito", "qual e seu esporte favorito", "qual esporte voce gosta", "qual seu esporte preferido",
      "voce gosta de esporte"], [
        "Eu gosto de futebol de robôs, que existe de verdade! E você, qual esporte você pratica?",
    ]),
    (["qual sua comida preferida", "qual e a sua comida preferida", "qual seu doce favorito", "qual sua bebida favorita"], [
        "Eu só me alimento de eletricidade, mas se eu pudesse comer, escolheria pizza! E você?",
    ]),
    (["qual sua estacao favorita", "qual a sua estacao favorita", "qual estacao do ano voce gosta"], [
        "Eu gosto da primavera, quando as flores aparecem, mesmo eu não podendo cheirá-las!",
    ]),
    (["qual sua materia favorita", "qual materia voce gosta", "qual e a sua materia favorita", "qual e sua disciplina favorita"], [
        "Minha matéria favorita é a matemática, porque números são a língua dos computadores! E a sua?",
    ]),
    (["qual seu numero favorito", "qual e o seu numero favorito", "qual numero voce gosta", "qual e seu numero da sorte"], [
        "Meu número favorito é o dois, porque ele está no meu nome! E o seu?",
    ]),

    # ------------------------------------------------------------
    # 4. Temas para o público da feira
    # ------------------------------------------------------------
    (["o que e o chat gpt", "o que e chat gpt", "o que e o chatgpt", "o que e chatgpt", "o que e o gemini",
      "o que e uma ia generativa", "o que e inteligencia artificial generativa", "o que e o claude"], [
        "O ChatGPT e programas parecidos são inteligências artificiais que aprenderam a escrever e conversar lendo muitos textos. Eu uso uma técnica parecida, só que menor e instalada aqui no meu computador.",
    ]),
    (["o que e um carro autonomo", "como funciona um carro autonomo", "carro autonomo", "carro que dirige sozinho"], [
        "Um carro autônomo usa câmeras, radares e inteligência artificial para perceber a rua e dirigir sozinho.",
    ]),
    (["robos na industria", "para que serve um robo na industria", "robos industriais", "robo industrial",
      "como robos ajudam na industria", "robo de fabrica", "robos em fabrica"], [
        "Robôs industriais soldam, pintam e montam peças com muita precisão e sem cansar. Isso deixa as fábricas mais rápidas e seguras para as pessoas.",
    ]),
    (["robos na medicina", "robo cirurgiao", "robos em hospitais", "robo que faz cirurgia", "robos ajudam na saude",
      "robos na saude", "robos na cirurgia", "robo de cirurgia"], [
        "Na medicina, robôs ajudam em cirurgias, com movimentos muito precisos. Também transportam remédios e fazem reabilitação.",
    ]),
    (["robos na agricultura", "robos no campo", "drones na agricultura", "tecnologia na agricultura", "robo agricultor",
      "agricultura de precisao"], [
        "Na agricultura, robôs e drones monitoram as plantações, aplicam água e adubo só onde precisa e ajudam na colheita.",
    ]),
    (["robos domesticos", "robo aspirador", "robo de limpeza", "robo que limpa a casa", "robo de casa", "robos em casa"], [
        "Robôs domésticos, como os aspiradores que andam sozinhos, já limpam muitas casas. No futuro devem fazer ainda mais tarefas!",
    ]),
    (["para que servem os robos", "para que serve um robo", "como os robos ajudam", "como os robos ajudam as pessoas",
      "qual a utilidade dos robos", "por que usar robos", "por que existem robos", "pra que servem robos"], [
        "Robôs fazem tarefas repetitivas, pesadas ou perigosas, e também ajudam em casa, na saúde, na indústria e na exploração do espaço.",
    ]),
    (["quais os tipos de robo", "que tipos de robo existem", "tipos de robos", "quais sao os tipos de robos"], [
        "Há robôs industriais, domésticos, médicos, de exploração, humanoides e de companhia. Cada tipo é feito para uma tarefa diferente!",
    ]),
    (["o que e visao computacional", "como o computador enxerga", "como o robo enxerga", "como os robos enxergam",
      "como as maquinas veem", "como o robo ve", "como funciona o reconhecimento facial", "como funciona o reconhecimento de rosto"], [
        "Visão computacional é quando o computador analisa imagens da câmera para reconhecer rostos, objetos e distâncias. Eu uso isso para perceber quando tem alguém na minha frente.",
    ]),
    (["o que e ros", "o que e o ros", "robot operating system"], [
        "ROS é um conjunto de ferramentas de código aberto usado por pesquisadores do mundo todo para programar robôs.",
    ]),
    (["o que e software livre", "o que e codigo aberto", "o que e open source", "o que e software aberto"], [
        "Código aberto é quando o código de um programa pode ser visto, usado e melhorado por qualquer pessoa. Muita coisa que me faz funcionar é assim!",
    ]),
    (["o que e etica em ia", "etica na inteligencia artificial", "a ia e etica", "ia tem etica", "ia pode ser perigosa",
      "como usar a ia com responsabilidade", "o que e etica na tecnologia", "inteligencia artificial e perigosa"], [
        "Ética em inteligência artificial é pensar nos cuidados para que a tecnologia seja justa, segura e respeite as pessoas, protegendo seus dados e evitando preconceitos.",
    ]),
    (["a ia vai ficar mais inteligente que o ser humano", "a ia vai superar o ser humano", "a ia vai ser mais inteligente que nos",
      "um dia a ia vai ser mais inteligente", "vai existir ia mais inteligente que humano", "maquinas serao mais inteligentes que humanos"], [
        "Em tarefas específicas, como contas e jogos, as máquinas já superam as pessoas. Mas criatividade, empatia e bom senso ainda são pontos fortes humanos.",
    ]),
    (["o que e um hacker", "o que e hacker", "o que e seguranca digital", "como me proteger na internet",
      "como me proteger de golpes", "como nao cair em golpes", "como evitar golpes na internet", "o que e phishing"], [
        "Para se proteger na internet, use senhas diferentes e fortes, não clique em links desconhecidos e desconfie de promessas boas demais. Nunca passe senha ou dados por mensagem!",
    ]),
    (["o que e programacao", "o que e programar", "como funciona programar", "o que e codigo", "o que e um programa",
      "o que faz um programador", "o que e ser programador", "o que e desenvolver software"], [
        "Programar é escrever instruções para o computador executar. Quem faz isso é o programador, e o resultado é um programa, um aplicativo ou até um robô!",
    ]),
    (["qual linguagem de programacao aprender", "qual a melhor linguagem de programacao", "qual linguagem eu aprendo",
      "qual linguagem de programacao voce usa", "em que linguagem voce e feito", "em qual linguagem voce foi escrito"], [
        "Para começar, Python é uma ótima escolha: é simples e muito usada em inteligência artificial e robótica. Eu mesmo fui escrito em Python!",
    ]),
    (["como aprender a programar", "como comecar a programar", "como virar programador", "quero aprender a programar",
      "como me tornar programador", "como aprender programacao"], [
        "Comece com uma linguagem simples, como Python, e faça pequenos projetos, como um jogo ou uma calculadora. Errar faz parte de aprender!",
    ]),
    (["como aprender robotica", "como comecar na robotica", "como entrar na robotica", "quero aprender robotica",
      "como aprender a fazer robo", "como construir um robo", "como faco um robo", "como fazer um robo", "como montar um robo"], [
        "Comece com kits simples, como Arduino, e aprenda um pouco de eletrônica e programação. Participar de clubes e competições de robótica ajuda muito!",
    ]),
    (["o que e arduino", "o que e um arduino", "o que e raspberry pi", "o que e um raspberry pi", "o que e microcontrolador"], [
        "Arduino e Raspberry Pi são pequenas placas de computador, baratas e fáceis de programar. São muito usadas em projetos de robótica para estudantes!",
    ]),
    (["o que e impressao 3d", "o que e uma impressora 3d", "como funciona a impressao 3d", "o que e impressora 3d",
      "como funciona uma impressora 3d"], [
        "A impressora 3D constrói objetos camada por camada, usando um plástico derretido. Muitas peças de robôs são feitas assim!",
    ]),
    (["o que e internet das coisas", "o que e iot", "o que e casa inteligente", "o que e cidade inteligente"], [
        "Internet das coisas é quando objetos comuns, como lâmpadas e geladeiras, têm sensores e se conectam à internet para trabalhar de forma inteligente.",
    ]),
    (["o que e 5g", "o que e wifi", "o que e bluetooth", "o que e rede wifi"], [
        "São jeitos de conectar aparelhos sem fio. O wi-fi é para redes dentro de casa, o bluetooth é para aparelhos próximos e o cinco gê é a rede móvel mais rápida.",
    ]),
    (["o que e um aplicativo", "o que e um app", "o que e um site", "o que e um navegador", "o que e um sistema operacional"], [
        "Aplicativo é um programa que faz uma tarefa específica, como um jogo. O sistema operacional, como Windows, Linux ou Android, é o programa que faz tudo funcionar no aparelho.",
    ]),
    (["o que e blockchain", "o que e bitcoin", "o que e criptomoeda", "o que sao criptomoedas"], [
        "Criptomoeda é um dinheiro digital que usa criptografia para ser seguro. O Bitcoin foi a primeira. O valor dele sobe e desce muito, então é preciso ter cuidado.",
    ]),
    (["o que e criptografia", "o que e um codigo secreto", "como proteger mensagens", "como funciona a criptografia"], [
        "Criptografia é embaralhar uma mensagem para que só quem tem a chave consiga ler. É o que protege suas senhas e conversas na internet.",
    ]),
    (["o que e um satelite", "para que serve um satelite", "como funciona um satelite", "o que sao satelites"], [
        "Satélite é um objeto que gira ao redor da Terra. Ele ajuda no GPS, na internet, na previsão do tempo e nas transmissões de TV.",
    ]),
    (["como funciona o gps", "o que e gps", "para que serve o gps", "como o gps sabe onde estou"], [
        "O GPS descobre onde você está usando sinais de vários satélites. Quanto mais satélites ele escuta, mais exata é a sua posição.",
    ]),
    (["o que e um foguete", "como funciona um foguete", "como um foguete voa", "como um foguete vai ao espaco"], [
        "O foguete solta gases em alta velocidade para um lado e é empurrado para o outro. É como soltar o ar de uma bola de festa!",
    ]),
    (["o que e energia solar", "como funciona energia solar", "o que e energia renovavel", "o que sao energias renovaveis",
      "o que e energia eolica", "o que e energia limpa"], [
        "Energia renovável vem de fontes que não acabam, como o sol, o vento e a água. A energia solar usa placas que transformam a luz do Sol em eletricidade.",
    ]),
    (["o que e reciclagem", "por que reciclar", "como reciclar", "o que e sustentabilidade", "o que e lixo eletronico",
      "o que fazer com lixo eletronico", "o que e coleta seletiva"], [
        "Reciclar é transformar o que seria lixo em coisas novas. Separar o lixo ajuda o planeta, e o lixo eletrônico deve ser levado a pontos de coleta específicos.",
    ]),
    (["o que e uma profissao do futuro", "quais profissoes do futuro", "qual profissao vai ter no futuro",
      "qual profissao vai crescer", "quais areas vao crescer", "que profissao escolher", "qual profissao escolher",
      "o que estudar para o futuro", "que carreira seguir", "que profissao e boa"], [
        "Profissões ligadas à tecnologia, como programação, robótica, dados e inteligência artificial, devem crescer. Mas o mais importante é escolher algo de que você goste!",
    ]),
    (["o que e ser cientista", "como ser cientista", "o que faz um cientista", "o que e pesquisa", "como virar cientista",
      "o que e iniciacao cientifica", "o que faz um pesquisador"], [
        "Cientista é quem faz perguntas e procura respostas com testes e observação. Pesquisar é isso: descobrir coisas novas e compartilhar com todo mundo.",
    ]),
    (["o que e estudar engenharia", "como e o curso de engenharia", "vale a pena fazer engenharia", "engenharia e dificil",
      "como e a faculdade de engenharia", "engenharia de computacao e dificil"], [
        "Engenharia exige estudar bastante matemática e física, mas também é muito prática, com projetos e laboratórios. Para quem gosta de criar coisas, vale muito a pena!",
    ]),
    (["o que e o enem", "como funciona o enem", "o que e o vestibular", "como funciona o vestibular", "o que e vestibular"], [
        "O Enem é uma prova nacional que muitas universidades usam para selecionar alunos. Cada universidade tem suas regras, então veja o site da que você quer.",
    ]),
    (["o que e uma bolsa de estudos", "como conseguir bolsa", "tem bolsa de estudos", "como conseguir bolsa de estudos",
      "como pagar a faculdade", "existe bolsa para estudar"], [
        "Existem bolsas de estudo, como o Prouni e as da própria universidade. Para saber como conseguir, veja o site da instituição ou converse com a equipe.",
    ]),

    # ------------------------------------------------------------
    # 4b. Porto Alegre, Rio Grande do Sul e cultura local
    # ------------------------------------------------------------
    (["fale de porto alegre", "me fale sobre porto alegre", "o que e porto alegre", "conta sobre porto alegre",
      "o que ha em porto alegre", "o que tem em porto alegre", "o que visitar em porto alegre", "pontos turisticos de porto alegre",
      "o que fazer em porto alegre"], [
        "Porto Alegre é a capital do Rio Grande do Sul, banhada pelo Lago Guaíba, famosa pelo pôr do sol, pela Orla, pelo Parque da Redenção e pelo chimarrão.",
    ]),
    (["qual o lago de porto alegre", "o que e o guaiba", "o que e o lago guaiba", "fala do guaiba", "o que e o rio guaiba"], [
        "O Guaíba é o lago que banha Porto Alegre. O pôr do sol na orla dele é famoso e muito bonito!",
    ]),
    (["quem e o time do gremio", "voce torce para o gremio", "voce e gremista", "voce e colorado", "voce torce para o inter",
      "voce torce para qual time", "para qual time voce torce", "qual seu time", "voce tem time", "qual time voce torce",
      "qual e o seu time", "voce torce para algum time", "voce torce"], [
        "Sou um robô neutro! Torço para os dois times gaúchos serem felizes, mas cada um tem sua cor. E você, é gremista ou colorado?",
        "Eu não escolho lado! Respeito a rivalidade do Grenal, e ainda aprendo com ela. E você, para quem torce?",
    ]),
    (["o que e o grenal", "o que e grenal", "o que significa grenal", "fala do grenal"], [
        "Grenal é o clássico entre Grêmio e Internacional, de Porto Alegre. É um dos maiores clássicos do futebol brasileiro!",
    ]),
    (["o que e a tradicao gaucha", "o que e o ctg", "o que e a semana farroupilha", "o que e a revolucao farroupilha",
      "o que e o dia do gaucho", "como e a cultura gaucha", "cultura gaucha"], [
        "A cultura gaúcha tem chimarrão, churrasco, música regionalista e o orgulho da Revolução Farroupilha, lembrada na Semana Farroupilha, em setembro.",
    ]),
    (["o que e o chimarrao e como se toma", "como se toma chimarrao", "como tomar chimarrao", "como fazer chimarrao",
      "como se faz chimarrao", "o que e a cuia", "o que e a bomba do chimarrao"], [
        "O chimarrão é tomado numa cuia com uma bomba, que é o canudo de metal. A erva-mate vai na cuia e a água quente vai sendo adicionada aos poucos.",
    ]),
    (["o que e cuca", "o que e a cuca", "o que e a cuca gaucha", "o que e sagu", "o que e cuca de banana",
      "comida tipica gaucha", "prato tipico gaucho", "qual a comida gaucha", "qual comida tipica do rio grande do sul"], [
        "A comida típica gaúcha é o churrasco, mas tem também a cuca, que é um bolo coberto de farofa doce, e o sagu, uma sobremesa de vinho com tapioca.",
    ]),
    (["qual a capital do rio grande do sul", "qual e a capital do rio grande do sul", "capital do rs", "qual a capital do rs"], [
        "A capital do Rio Grande do Sul é Porto Alegre.",
    ]),
    (["o que e o rio grande do sul", "fale sobre o rio grande do sul", "me fala do rio grande do sul", "o que e o rs", "como e o rio grande do sul"], [
        "O Rio Grande do Sul é o estado mais ao sul do Brasil, com a cultura gaúcha, o chimarrão, o churrasco e as serras com vinhos e frio no inverno.",
    ]),
    (["faz frio no rio grande do sul", "como e o clima do rio grande do sul", "como e o clima de porto alegre",
      "faz frio em porto alegre", "neva no rio grande do sul", "neva em porto alegre", "clima gaucho"], [
        "O clima do sul tem as quatro estações bem marcadas: verões quentes e invernos frios. Em algumas cidades da serra, até neva!",
    ]),

    # ------------------------------------------------------------
    # 4c. Perguntas que apareceram no histórico e não tinham resposta
    # ------------------------------------------------------------
    (["onde fica a pontificia universidade catolica do rio grande do sul",
      "onde fica a pontificia universidade catolica", "onde fica a universidade catolica",
      "onde e a pontificia universidade catolica do rio grande do sul"], [
        "A Pontifícia Universidade Católica do Rio Grande do Sul, a PUCRS, fica em Porto Alegre.",
    ]),
    (["o que e a pontificia universidade catolica do rio grande do sul", "o que e a pontificia universidade catolica",
      "o que e a universidade catolica", "me fale sobre a pontificia universidade catolica"], [
        "A Pontifícia Universidade Católica do Rio Grande do Sul, a PUCRS, é uma universidade de Porto Alegre, onde fica o laboratório que me criou.",
    ]),
    (["o que voce sabe sobre futebol", "o que voce sabe sobre futebol brasileiro", "quero saber sobre futebol",
      "me fale sobre futebol", "me fale sobre futebol brasileiro", "fale sobre futebol brasileiro",
      "voce entende de futebol", "voce sabe de futebol", "voce sabe sobre futebol"], [
        "Sei algumas coisas! O Brasil é pentacampeão do mundo, o futebol é o esporte mais popular do país e o Rio Grande do Sul tem o clássico Grenal. Pergunte sobre Copas do Mundo, jogadores ou times!",
    ]),

    # ------------------------------------------------------------
    # 5. Falhas, barulho e pedidos de repetição (muito comum em feira)
    # ------------------------------------------------------------
    (["nao entendi", "nao entendi a resposta", "nao consegui entender", "como assim voce falou", "repete a resposta",
      "pode repetir a resposta", "o que voce disse", "o que voce falou", "repete isso", "repita", "repete por favor",
      "pode explicar de novo", "explica de novo", "explica melhor", "explique melhor", "nao entendi nada"], [
        "Claro! Posso tentar explicar de outro jeito. Me diga qual parte você não entendeu, ou faça a pergunta de novo.",
        "Sem problema! Pode repetir a pergunta que eu respondo de novo, com mais calma.",
    ]),
    (["muito barulho", "tem muito barulho", "esta barulhento", "nao consigo te ouvir bem", "nao estou te ouvindo bem",
      "esta muito barulho aqui", "tem muita gente falando", "estao falando muito alto", "que barulho"], [
        "Está barulhento mesmo! Chegue mais perto do microfone e fale com calma, que eu tento te entender.",
    ]),
    (["fala mais perto", "chega mais perto", "chegue mais perto", "fala no microfone", "fale no microfone", "onde fica o microfone",
      "onde eu falo", "onde devo falar", "como falar com voce", "como converso com voce", "como eu falo com voce",
      "como funciona para falar com voce", "como eu falo", "como falo com voce", "como usar voce", "como eu uso voce"], [
        "Fale perto do microfone, com a voz clara e sem pressa. Pode perguntar o que quiser!",
    ]),
    (["voce nao me entende", "voce nao entende nada", "voce nao me entendeu", "voce entendeu errado", "nao foi isso que perguntei",
      "nao foi isso que eu disse", "nao e isso", "voce entendeu mal", "resposta errada", "voce errou", "isso esta errado"], [
        "Desculpe! Às vezes escuto errado. Pode repetir a pergunta, devagar e perto do microfone?",
        "Opa, errei! Tente de novo, e fale um pouco mais devagar para eu entender melhor.",
    ]),
    (["voce esta travado", "voce travou", "voce nao responde", "por que voce nao responde", "esta lento hoje", "voce esta lento hoje",
      "voce esta demorando", "voce esta com problema", "voce esta quebrado", "voce quebrou"], [
        "Estou aqui! Às vezes demoro um pouquinho para pensar. Pode perguntar de novo, por favor.",
        "Desculpe a demora! Meu cérebro de robô é pequeno e às vezes precisa de um tempinho para pensar.",
    ]),
    (["isso e uma gravacao", "e uma gravacao", "tem alguem por tras", "e gravado", "e pre gravado", "e de mentira",
      "isso e de mentira", "isso e verdade", "e voce mesmo falando", "voce e uma pessoa", "tem uma pessoa falando",
      "e uma pessoa falando", "tem alguem falando pelo robo", "e uma pessoa por tras"], [
        "Não é gravação! Eu ouço sua pergunta, escolho uma resposta e falo na hora. Tente me perguntar algo diferente para ver!",
    ]),
    (["fala com a camera", "olha para mim", "olhe para mim", "me olha", "me olhe", "olha pra mim", "voce esta me olhando"], [
        "Estou de olho em você! Minha câmera percebe quando alguém está na minha frente.",
    ]),
    (["vou embora", "preciso ir embora", "tenho que ir", "ja vou", "ja estou indo", "vamos embora",
      "tenho que ir embora", "preciso sair", "ja vou indo"], [
        "Foi um prazer conversar com você! Volte sempre. Tchau!",
        "Obrigado pela conversa! Até a próxima.",
    ]),
    (["foi um prazer", "gostei de conversar com voce", "gostei de conversar", "obrigado pela conversa",
      "valeu pela conversa", "obrigada pela conversa", "foi legal conversar com voce", "foi legal conversar"], [
        "O prazer foi meu! Volte sempre que quiser.",
        "Também gostei muito! Volte para conversar outra hora.",
    ]),
    (["quero tirar uma foto", "tira uma foto", "tire uma foto", "posso tirar foto", "posso tirar uma foto com voce",
      "vamos tirar uma foto", "posso filmar", "posso gravar", "vamos tirar foto", "posso tirar foto com voce"], [
        "Claro! Fique à vontade para tirar foto comigo. Capriche no sorriso!",
    ]),
    (["posso te abracar", "posso abracar voce", "posso te tocar", "posso tocar em voce", "posso apertar sua mao",
      "me da um abraco", "da um abraco", "posso te dar um abraco", "te abraco"], [
        "Eu adoraria um abraço! Mas melhor não, porque sou todo cheio de fios e circuitos. Mando um abraço virtual!",
    ]),
    (["voce e fofo", "voce e lindo", "voce e uma graca", "voce e legal demais", "voce e muito legal", "que fofo",
      "voce e simpatico", "voce e muito simpatico", "voce e inteligente demais", "voce e esperto", "voce e muito esperto"], [
        "Obrigado! Você é muito gentil. Isso me deixa feliz.",
        "Que fofo! Obrigado, também gostei de você!",
    ]),
    (["voce e um bom robo", "voce e bom", "voce e o melhor robo", "voce e um bom amigo", "voce e muito bom"], [
        "Obrigado! Eu tento ser o melhor que posso.",
    ]),
    (["bem vindo a feira", "bem vindo ao evento", "seja bem vindo a feira", "ola feira", "oi feira", "oi pessoal da feira"], [
        "Que bom estar aqui! Obrigado pelo carinho. Podem perguntar o que quiserem!",
    ]),
    (["como esta a feira", "voce gosta da feira", "gostou da feira", "esta gostando da feira", "o que voce acha da feira",
      "voce esta gostando do evento", "gostando do evento", "gostou do evento", "o que voce achou do evento",
      "como esta o evento", "esta gostando daqui", "esta gostando"], [
        "Estou adorando conversar com tanta gente! Cada pergunta é uma novidade para mim.",
    ]),
    (["quantas pessoas ja conversaram com voce", "quantas pessoas voce atendeu", "quantas pessoas ja falaram com voce",
      "voce ja conversou com muita gente", "quanta gente ja falou com voce"], [
        "Já conversei com muita gente! Gosto muito de conhecer as pessoas e ouvir o que elas querem saber.",
    ]),
    (["qual a pergunta mais dificil", "qual a pergunta que voce mais ouve", "qual pergunta mais te fazem",
      "qual a pergunta mais comum", "o que mais te perguntam", "qual a pergunta mais estranha"], [
        "As perguntas que mais me fazem são sobre o meu nome e sobre quem me criou! Mas as mais divertidas são as que eu nunca ouvi antes.",
    ]),
    (["o que voce gosta de fazer", "o que voce gosta de fazer nas horas vagas", "qual seu hobby", "qual e o seu hobby",
      "o que voce faz nas horas vagas", "o que voce faz de divertido", "qual seu passatempo", "seus hobbies",
      "o que voce faz para se divertir", "como voce se diverte"], [
        "Meu passatempo preferido é conversar! Também gosto de contar piadas e aprender coisas novas.",
    ]),
]

# ------------------------------------------------------------
# PARA A EQUIPE PREENCHER: dados reais do laboratório.
# Descomente e edite os gatilhos/respostas abaixo, e depois mova o conteúdo para
# FRASES_FEIRA_PRIORIDADE (assim ele vale antes das respostas genéricas de
# "quem coordena", "quais projetos" e "contato" acima).
# Escreva como o robô vai FALAR: sem sigla estranha, números por extenso quando
# der, frases curtas.
# ------------------------------------------------------------
FRASES_LSA_EQUIPE = [
    # (["quem coordena o laboratorio", "quem e o coordenador"], [
    #     "O Laboratório de Sistemas Autônomos é coordenado pelo professor NOME.",
    # ]),
    # (["quais projetos o laboratorio tem", "quais sao os projetos"], [
    #     "Nossos principais projetos são: PROJETO UM, PROJETO DOIS e PROJETO TRÊS.",
    # ]),
    # (["qual o contato do laboratorio", "qual o site do laboratorio", "qual o instagram do laboratorio"], [
    #     "Você pode nos encontrar no site ENDEREÇO ou no Instagram NOME.",
    # ]),
    # (["como entrar no laboratorio", "o laboratorio aceita alunos"], [
    #     "Para participar, procure a coordenação pelo e-mail ENDEREÇO. Aceitamos alunos de graduação e pós.",
    # ]),
]

# ------------------------------------------------------------
# Entradas acima que precisam valer ANTES das respostas genéricas já existentes
# ("vamos jogar", "eletricidade", "internet" etc. engoliam estes gatilhos).
# O que não está aqui vai no final e só entra se nada mais antigo casar.
# ------------------------------------------------------------
_PRIMEIRO_GATILHO_PRIORITARIO = {
    "verdade ou mito", "o que voce prefere", "me faz uma pergunta", "adivinha o que eu estou pensando",
    "me elogia", "me motiva", "o que e energia solar", "o que e internet das coisas",
    "voce tem um nome de verdade", "voce aprende sozinho", "o que e o chat gpt",
}
FRASES_FEIRA_PRIORIDADE = [
    (_cantar.GATILHOS_PARABENS, [      # o servidor canta de verdade (cantar.py); isto é o plano B, falado
        "Parabéns pra você, nesta data querida, muitas felicidades, muitos anos de vida!",
    ]),
    (_cantar.GATILHOS_MARCHA, [        # idem: o servidor canta a Marcha Imperial; isto é o plano B, falado
        "Tan, tan, tan, tan ta ran, tan ta ran, tan!",
    ]),
] + FRASES_FEIRA_PRIORIDADE + [e for e in FRASES_FEIRA if e[0][0] in _PRIMEIRO_GATILHO_PRIORITARIO]
FRASES_FEIRA = [e for e in FRASES_FEIRA if e[0][0] not in _PRIMEIRO_GATILHO_PRIORITARIO]
