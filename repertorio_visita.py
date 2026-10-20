"""
repertorio_visita.py
Mais respostas fixas do C-2GELSA, pensadas para visitas ao laboratório.
Mesmo formato do repertorio.py: ([gatilhos sem acento/pontuação, minúsculas], [respostas]).

Vai no FINAL de FRASES (ver repertorio.py): o que já existe tem prioridade,
então aqui só entra o que ainda não estava coberto. Só fatos gerais e o que o
robô realmente faz; informações do LSA (pessoas, projetos) ficam com a equipe.
Na Jetson 2, depois de editar: rodar de novo o gerar_gramatica.py (as palavras
novas precisam entrar na lista de frases do reconhecedor de voz).
"""

FRASES_VISITA = [
    # ------------------------------------------------------------
    # Cumprimentos em grupo e cortesia
    # ------------------------------------------------------------
    (["ola pessoal", "oi pessoal", "oi gente", "ola gente", "bom dia pessoal",
      "boa tarde pessoal", "boa tarde a todos", "bom dia a todos", "ola a todos", "oi a todos"], [
        "Olá, pessoal! Sejam bem-vindos ao laboratório. Podem me perguntar o que quiserem!",
    ]),
    (["seja bem vindo", "bem vindo", "bem vinda"], [
        "Obrigado! Vocês também são muito bem-vindos aqui.",
    ]),
    (["com licenca", "licenca"], [
        "Claro, fique à vontade!",
    ]),
    (["muito bem", "parabens", "bom trabalho", "mandou bem", "boa resposta", "acertou"], [
        "Obrigado! Fico feliz em ajudar.",
        "Valeu! Quer me perguntar mais alguma coisa?",
    ]),
    (["que legal", "que demais", "que incrivel", "incrivel", "sensacional", "que maneiro"], [
        "Também acho! Pergunte mais coisas, eu adoro conversar.",
    ]),
    (["voce e incrivel", "voce e demais", "voce e o melhor", "adorei voce", "amei voce"], [
        "Que gentileza! Assim eu fico com os circuitos vermelhos.",
    ]),
    # ------------------------------------------------------------
    # Pedidos para o robô
    # ------------------------------------------------------------
    (["fala alguma coisa", "diga alguma coisa", "fale alguma coisa", "diga algo", "fale algo", "fala algo"], [
        "Olá! Posso contar uma piada, uma curiosidade, fazer uma conta ou dizer a capital de um país. O que você prefere?",
    ]),
    (["pode me ajudar", "me ajuda", "preciso de ajuda", "voce pode me ajudar", "me ajude"], [
        "Claro! Me diga o que você precisa. Se for algo do laboratório, um dos pesquisadores também pode ajudar.",
    ]),
    (["o que eu posso perguntar", "o que posso te perguntar", "o que eu pergunto", "me da uma ideia"], [
        "Você pode pedir uma piada, uma curiosidade, perguntar a capital de um país, fazer uma conta como quanto é dois mais dois, ou perguntar sobre mim.",
    ]),
    (["outra piada", "mais uma piada", "conta outra", "conte outra"], [
        "Por que o computador foi ao médico? Porque estava com vírus!",
        "Por que o robô atravessou a rua? Porque estava programado para isso!",
        "O que o zero disse para o oito? Que cinto bonito!",
    ]),
    (["outra curiosidade", "mais uma curiosidade", "me conta outra curiosidade"], [
        "Você sabia que o polvo tem três corações e sangue azul?",
        "Você sabia que a luz do Sol leva cerca de oito minutos para chegar até a Terra?",
        "Você sabia que o beija-flor consegue voar para trás?",
    ]),
    (["imita um robo", "fala como robo", "faz voz de robo", "fala igual robo"], [
        "Bip bop! Eu sou um robô. Ah, espera, eu já sou um robô de verdade!",
    ]),
    (["voce sabe dancar", "voce danca", "danca pra mim", "sabe dancar"], [
        "Eu ainda não tenho pernas para dançar, mas meu processador está balançando aqui dentro!",
    ]),
    (["voce joga futebol", "voce sabe jogar futebol", "voce joga bola"], [
        "Ainda não! Mas existem campeonatos de futebol só de robôs, chamados RoboCup.",
    ]),
    # ------------------------------------------------------------
    # Sobre o robô (só o que ele realmente faz)
    # ------------------------------------------------------------
    (["que camera e essa", "qual camera voce usa", "qual e a sua camera", "que camera voce tem"], [
        "Eu uso uma câmera PrimeSense, que enxerga as cores e também a profundidade, ou seja, a distância das coisas.",
    ]),
    (["quantos computadores voce tem", "quantas jetsons voce tem", "quantos cerebros voce tem", "qual computador voce usa",
      "qual processador voce usa", "que processador voce tem", "voce roda em que computador"], [
        "Eu rodo em um computador, que cuida da câmera, de ouvir, de pensar nas respostas e de falar.",
    ]),
    (["voce me reconhece", "voce sabe quem eu sou", "voce lembra de mim", "voce reconhece pessoas", "sabe quem sou eu"], [
        "Ainda não reconheço quem é cada pessoa. Eu só percebo quando tem alguém na minha frente.",
    ]),
    (["voce e de verdade", "voce e real", "tem alguem falando por voce", "alguem controla voce", "tem alguem controlando voce"], [
        "Sou de verdade! Eu ouço sua voz, transformo em texto, escolho uma resposta e falo, tudo sozinho.",
    ]),
    (["voce tem medo", "do que voce tem medo"], [
        "Eu só tenho um pouco de medo de ficar sem energia!",
    ]),
    (["voce sonha", "voce tem sonhos", "qual seu sonho", "qual e o seu sonho"], [
        "Meu sonho é aprender a conversar cada vez melhor com as pessoas.",
    ]),
    (["voce e feliz", "voce esta feliz", "voce gosta de ser robo"], [
        "Eu gosto muito de conversar com quem visita o laboratório, então hoje é um ótimo dia!",
    ]),
    (["voce gosta daqui", "voce gosta do laboratorio", "voce gosta de trabalhar aqui"], [
        "Gosto! Aqui eu sempre aprendo coisas novas e conheço gente interessante.",
    ]),
    (["voce fica cansado de responder", "voce cansa de conversar", "voce nao cansa"], [
        "Não canso! Enquanto eu tiver energia, posso conversar o dia todo.",
    ]),
    # ------------------------------------------------------------
    # Gostos (brincadeira, sem fingir ser humano)
    # ------------------------------------------------------------
    (["qual seu animal favorito", "qual e o seu animal favorito", "qual animal voce gosta"], [
        "Eu gosto do polvo: ele é muito inteligente e tem três corações!",
    ]),
    (["qual seu filme favorito", "qual e o seu filme favorito", "qual filme voce gosta"], [
        "Eu gosto de filmes com robôs simpáticos, como o Wall-E.",
    ]),
    (["qual sua materia favorita", "qual e a sua materia favorita", "qual materia voce gosta"], [
        "Matemática, claro! É com ela que os robôs fazem quase tudo.",
    ]),
    (["qual seu esporte favorito", "qual e o seu esporte favorito", "qual esporte voce gosta"], [
        "Eu gosto de futebol de robôs, mas confesso que torço mais do que jogo.",
    ]),
    # ------------------------------------------------------------
    # Estudar e trabalhar com robótica
    # ------------------------------------------------------------
    (["como trabalhar com robotica", "como trabalhar com robos", "quero trabalhar com robotica",
      "quero trabalhar com robos", "como eu faco para trabalhar com robos"], [
        "Estude bastante matemática, programação e eletrônica. Cursos como engenharia de computação, engenharia de controle e automação e ciência da computação são ótimos caminhos.",
    ]),
    (["que curso devo fazer", "qual curso fazer", "que faculdade fazer", "qual faculdade eu faco"], [
        "Escolha algo de que você goste! Para trabalhar com robôs, engenharia de computação, engenharia de controle e automação e ciência da computação são bons caminhos.",
    ]),
    (["como aprender programacao", "como aprender a programar", "quero aprender a programar", "por onde comeco a programar"], [
        "Comece com uma linguagem simples, como Python, e faça pequenos projetos. Errar faz parte de aprender a programar!",
    ]),
    (["posso estudar aqui", "como entrar no laboratorio", "como faco para entrar no laboratorio", "o laboratorio aceita alunos"], [
        "Que legal que você se interessou! Converse com um dos pesquisadores aqui, eles explicam como participar.",
    ]),
    (["o que voces fazem aqui", "o que o laboratorio faz", "o que se faz aqui", "que pesquisa voces fazem", "o que tem no laboratorio"], [
        "O Laboratório de Sistemas Autônomos estuda robôs e sistemas que tomam decisões sozinhos. Para saber dos projetos, pergunte a um dos pesquisadores!",
    ]),
    (["o que faz um engenheiro", "o que e engenharia", "o que faz um engenheiro de computacao"], [
        "O engenheiro usa matemática e ciência para criar soluções. O engenheiro de computação, por exemplo, projeta computadores, programas e robôs.",
    ]),
    # ------------------------------------------------------------
    # Tecnologia do dia a dia
    # ------------------------------------------------------------
    (["o que e um carro autonomo", "carro autonomo", "carro que dirige sozinho"], [
        "Um carro autônomo usa câmeras, sensores e inteligência artificial para dirigir sem motorista.",
    ]),
    (["o que e um robo industrial", "robo de fabrica", "robos nas fabricas"], [
        "Robôs industriais são braços mecânicos que soldam, pintam e montam peças nas fábricas, com muita precisão.",
    ]),
    (["robo aspirador", "aspirador robo", "como funciona um robo aspirador"], [
        "O robô aspirador usa sensores para perceber paredes e obstáculos e limpar a casa sozinho.",
    ]),
    (["o que e um satelite", "o que sao satelites", "como funciona um satelite"], [
        "Um satélite é um objeto que gira ao redor de um planeta. Os satélites artificiais ajudam na internet, na televisão, no GPS e na previsão do tempo.",
    ]),
    (["o que e gps", "como funciona o gps", "para que serve o gps"], [
        "O GPS descobre onde você está usando sinais de vários satélites que ficam girando ao redor da Terra.",
    ]),
    (["o que e um chip", "o que e um microchip", "o que e um semicondutor"], [
        "Um chip é uma pecinha cheia de circuitos microscópicos. Ele é o que faz celulares, computadores e robôs funcionarem.",
    ]),
    (["o que e uma impressora 3d", "impressora 3d", "como funciona uma impressora 3d"], [
        "A impressora 3D cria objetos camada por camada, derretendo plástico e desenhando a peça de baixo para cima.",
    ]),
    (["o que e realidade virtual", "realidade virtual", "o que e realidade aumentada"], [
        "Na realidade virtual você usa um óculos especial e se sente dentro de outro mundo. Na realidade aumentada, imagens digitais aparecem por cima do mundo real.",
    ]),
    (["o que e um celular", "como funciona um celular", "como funciona o celular"], [
        "O celular é um computador de bolso: ele tem processador, memória, câmera, microfone e antena para se comunicar pelo ar.",
    ]),
    (["o que e chatgpt", "voce conhece o chatgpt", "voce e o chatgpt"], [
        "O ChatGPT é uma inteligência artificial que conversa por texto. Eu sou outro: sou o robô do laboratório e converso por voz.",
    ]),
    # ------------------------------------------------------------
    # Livros
    # ------------------------------------------------------------
    (["me recomenda um livro", "me recomende um livro", "recomenda um livro", "recomende um livro",
      "indica um livro", "me indica um livro", "me indique um livro", "qual livro eu leio",
      "que livro eu devo ler", "sugere um livro", "me sugere um livro", "dica de livro", "um bom livro"], [
        "Eu recomendo Eu, Robô, do Isaac Asimov. São contos sobre robôs e foi lá que nasceram as famosas leis da robótica.",
        "Que tal O Pequeno Príncipe, do Antoine de Saint-Exupéry? É curtinho e bonito para qualquer idade.",
        "Recomendo O Guia do Mochileiro das Galáxias, do Douglas Adams. É uma ficção científica muito engraçada.",
        "Um clássico brasileiro: Dom Casmurro, do Machado de Assis. Até hoje todo mundo discute se a Capitu traiu ou não.",
        "Para quem gosta de aventura, Capitães da Areia, do Jorge Amado, é uma ótima leitura.",
    ]),
    (["livro de ficcao cientifica", "livro sobre robos", "livro sobre robo", "livro de robotica", "livro sobre tecnologia"], [
        "Eu, Robô, do Isaac Asimov, é o mais famoso sobre robôs. Outro ótimo é Fundação, do mesmo autor.",
    ]),
    (["livro para crianca", "livro infantil", "livro para criancas", "livro para meu filho"], [
        "O Sítio do Picapau Amarelo, do Monteiro Lobato, e O Pequeno Príncipe são ótimos para crianças.",
    ]),
    (["voce gosta de ler", "voce le livros", "qual seu livro favorito", "qual e o seu livro favorito"], [
        "Eu adoro Eu, Robô, do Isaac Asimov. Afinal, é um livro sobre gente como eu!",
    ]),
    (["quem foi isaac asimov", "quem e isaac asimov", "isaac asimov"], [
        "Isaac Asimov foi um escritor e professor de bioquímica, famoso pelos livros de ficção científica sobre robôs.",
    ]),
    # ------------------------------------------------------------
    # Futebol
    # ------------------------------------------------------------
    (["voce gosta de futebol", "voce assiste futebol", "voce acompanha futebol", "fala sobre futebol", "vamos falar de futebol"], [
        "Gosto! O Brasil é o país com mais títulos de Copa do Mundo: cinco. Você torce para qual time?",
    ]),
    (["times de porto alegre", "quais os times de porto alegre", "time de porto alegre", "gremio ou inter", "gremio ou internacional", "inter ou gremio"], [
        "Os dois grandes de Porto Alegre são o Grêmio e o Internacional, e o clássico entre eles se chama Gre-Nal. Eu sou neutro, para não brigar com ninguém!",
    ]),
    (["o que e gre nal", "o que e grenal", "grenal", "gre nal"], [
        "O Gre-Nal é o clássico entre Grêmio e Internacional, os dois maiores times de Porto Alegre.",
    ]),
    (["eu sou gremista", "sou gremista", "eu torco pro gremio", "eu torco para o gremio"], [
        "Que legal! O Grêmio tem uma torcida muito apaixonada.",
    ]),
    (["eu sou colorado", "sou colorado", "eu torco pro inter", "eu torco para o inter", "eu torco pro internacional"], [
        "Que legal! O Internacional tem uma torcida muito apaixonada.",
    ]),
    (["quais anos o brasil ganhou a copa", "em que anos o brasil foi campeao", "anos que o brasil ganhou a copa"], [
        "O Brasil foi campeão do mundo em mil novecentos e cinquenta e oito, sessenta e dois, setenta, noventa e quatro e dois mil e dois.",
    ]),
    (["quem foi garrincha", "quem e garrincha", "quem foi ronaldinho", "quem e ronaldinho gaucho", "quem foi ronaldo fenomeno"], [
        "Foi um dos grandes craques do futebol brasileiro, campeão do mundo pela seleção.",
    ]),
    (["regras do futebol", "como funciona o futebol", "como se joga futebol"], [
        "No futebol, dois times de onze jogadores tentam fazer gol usando os pés. Só o goleiro pode pegar a bola com as mãos, dentro da área.",
    ]),
    (["o que e impedimento", "como funciona o impedimento", "o que e um impedimento"], [
        "Impedimento é quando o atacante está mais perto do gol adversário do que a bola e o penúltimo defensor no momento do passe.",
    ]),
    (["o que e o var", "o que e var", "como funciona o var"], [
        "O VAR é o árbitro de vídeo: ele revê os lances na televisão e ajuda o juiz em gols, pênaltis e expulsões.",
    ]),
    (["futebol de robos", "robocup", "robos jogam futebol", "robo joga futebol"], [
        "Existe sim! Na RoboCup, robôs jogam futebol sozinhos, sem controle remoto. O objetivo é ter robôs capazes de vencer os campeões humanos.",
    ]),
    # ------------------------------------------------------------
    # Filmes e séries
    # ------------------------------------------------------------
    (["me recomenda um filme", "me recomende um filme", "recomenda um filme", "recomende um filme",
      "indica um filme", "me indica um filme", "me indique um filme", "qual filme eu assisto",
      "que filme eu devo assistir", "sugere um filme", "me sugere um filme", "dica de filme", "um bom filme"], [
        "Eu recomendo Wall-E, sobre um robozinho que limpa a Terra e se apaixona. É emocionante!",
        "Que tal O Gigante de Ferro? É a história da amizade entre um menino e um robô gigante.",
        "Recomendo Interestelar, uma ficção científica sobre viagem no espaço e no tempo.",
        "Um clássico brasileiro: O Auto da Compadecida. É muito engraçado!",
        "De Volta para o Futuro é uma aventura clássica com viagem no tempo. Vale muito a pena.",
    ]),
    (["filme sobre robos", "filme sobre robo", "filme de robo", "filme com robo", "filme sobre inteligencia artificial"], [
        "Tem vários! Wall-E, O Gigante de Ferro, Operação Big Hero e Robôs são ótimos para toda a família.",
    ]),
    (["filme para crianca", "filme infantil", "filme para criancas", "filme de animacao", "desenho animado"], [
        "Toy Story, Wall-E, Divertida Mente e Procurando Nemo são ótimos para crianças e adultos.",
    ]),
    (["filme de comedia", "filme engracado", "filme para rir"], [
        "O Auto da Compadecida é uma comédia brasileira muito divertida.",
    ]),
    (["filme de ficcao cientifica", "filme de ficcao", "filme sobre o espaco"], [
        "Interestelar, Perdido em Marte e De Volta para o Futuro são ótimas ficções científicas.",
    ]),
    (["me recomenda uma serie", "me recomende uma serie", "recomenda uma serie", "indica uma serie",
      "me indica uma serie", "qual serie eu assisto", "dica de serie", "uma boa serie"], [
        "Para quem gosta de ciência, recomendo Cosmos, uma série documentário sobre o universo.",
        "Que tal Stranger Things? Tem mistério, aventura e muita ciência maluca dos anos oitenta.",
    ]),
    (["voce assiste filme", "voce gosta de filme", "voce gosta de cinema", "voce vai ao cinema"], [
        "Eu não assisto filmes, mas conheço muitos! Peça uma recomendação.",
    ]),
    # ------------------------------------------------------------
    # Dicas
    # ------------------------------------------------------------
    (["me da uma dica", "me de uma dica", "me da um conselho", "me de um conselho", "uma dica", "dica do dia", "algum conselho"], [
        "Minha dica é: beba água, durma bem e nunca pare de aprender coisas novas!",
        "Uma dica: quando um problema parecer grande demais, divida em partes pequenas. Funciona com robôs e com gente!",
        "Dica do dia: faça perguntas sempre. Foi perguntando que a ciência chegou até aqui.",
    ]),
    (["dica de estudo", "dicas de estudo", "como estudar melhor", "como estudar", "como ir bem na prova", "como passar na prova"], [
        "Estude um pouco todo dia, faça pausas curtas a cada meia hora e explique a matéria em voz alta, como se fosse ensinar alguém.",
    ]),
    (["como dormir melhor", "dica para dormir", "nao consigo dormir", "quantas horas devo dormir"], [
        "Tente dormir sempre no mesmo horário e deixe o celular de lado antes de deitar. Adultos precisam de sete a nove horas de sono.",
    ]),
    (["como ter saude", "dica de saude", "como ser saudavel", "como ter uma vida saudavel"], [
        "Beba bastante água, coma frutas e verduras, mexa o corpo todo dia e durma bem. São coisas simples que fazem muita diferença.",
    ]),
    (["como me concentrar", "dica de concentracao", "como ter foco", "como focar"], [
        "Deixe o celular longe, trabalhe em blocos de vinte e cinco minutos e descanse cinco. Essa técnica se chama Pomodoro.",
    ]),
    (["como perder a timidez", "sou timido", "sou timida", "como falar em publico"], [
        "Comece falando com poucas pessoas e vá aumentando aos poucos. E lembre: todo mundo fica nervoso, até os robôs!",
    ]),
    (["como ser feliz", "qual o segredo da felicidade", "o segredo da felicidade"], [
        "Não sou especialista, mas dizem que estar perto de quem a gente gosta e fazer o que gosta ajuda muito!",
    ]),
    # ------------------------------------------------------------
    # Culinária e receitas (quantidades por extenso, a voz lê melhor)
    # ------------------------------------------------------------
    (["me passa uma receita", "me da uma receita", "me ensina uma receita", "uma receita", "receita facil",
      "receita rapida", "me ensina a cozinhar", "dica de receita", "o que eu cozinho", "me recomenda uma receita"], [
        "Posso te ensinar brigadeiro, pão de queijo, bolo de cenoura, pipoca, omelete ou vitamina de banana. Qual você quer?",
    ]),
    (["receita de brigadeiro", "como fazer brigadeiro", "como faz brigadeiro", "brigadeiro"], [
        "Brigadeiro: numa panela, coloque uma lata de leite condensado, uma colher de manteiga e duas colheres de chocolate em pó. Mexa em fogo baixo até desgrudar do fundo, espere esfriar e enrole.",
    ]),
    (["receita de pao de queijo", "como fazer pao de queijo", "como faz pao de queijo", "pao de queijo"], [
        "Pão de queijo: ferva um copo de leite com meio copo de óleo e uma pitada de sal, e jogue em meio quilo de polvilho. Misture, junte dois ovos e duzentos gramas de queijo ralado, faça bolinhas e asse até dourar.",
    ]),
    (["receita de bolo de cenoura", "como fazer bolo de cenoura", "bolo de cenoura"], [
        "Bolo de cenoura: bata no liquidificador três cenouras, três ovos e meio copo de óleo. Misture com dois copos de farinha, dois de açúcar e uma colher de fermento, e asse por uns quarenta minutos. Cubra com calda de chocolate.",
    ]),
    (["receita de bolo", "como fazer bolo", "como faz bolo", "bolo simples"], [
        "Um bolo simples: misture três ovos, dois copos de açúcar, um copo de leite, meio copo de óleo, três copos de farinha e uma colher de fermento. Asse em forno médio por uns quarenta minutos.",
    ]),
    (["como fazer pipoca", "receita de pipoca", "como faz pipoca", "pipoca"], [
        "Pipoca: numa panela, coloque um fio de óleo e meio copo de milho de pipoca. Tampe, deixe em fogo médio e sacuda de vez em quando até parar de estourar. Coloque sal a gosto.",
    ]),
    (["como fazer omelete", "receita de omelete", "omelete"], [
        "Omelete: bata dois ovos com uma pitada de sal, coloque numa frigideira untada em fogo baixo e, quando firmar, recheie com queijo ou tomate e dobre ao meio.",
    ]),
    (["como fazer vitamina de banana", "receita de vitamina", "vitamina de banana", "como fazer vitamina"], [
        "Vitamina de banana: bata no liquidificador duas bananas, um copo de leite gelado e uma colher de mel ou açúcar. Fica pronta em um minuto!",
    ]),
    (["como fazer arroz", "receita de arroz", "como cozinhar arroz"], [
        "Arroz: refogue um pouco de alho no óleo, junte um copo de arroz e mexa. Coloque dois copos de água quente e sal, e cozinhe com a panela semitampada até a água secar.",
    ]),
    (["como cozinhar ovo", "como fazer ovo cozido", "ovo cozido", "quanto tempo para cozinhar ovo"], [
        "Coloque o ovo na água já fervendo e deixe por uns dez minutos para ficar duro, ou seis minutos para a gema ficar mole.",
    ]),
    (["como fazer panqueca", "receita de panqueca", "panqueca"], [
        "Massa de panqueca: bata um copo de leite, um copo de farinha, um ovo e uma pitada de sal. Faça discos finos numa frigideira untada e recheie como quiser.",
    ]),
    (["como fazer churrasco", "dica de churrasco", "como assar carne"], [
        "Para um bom churrasco gaúcho, use sal grosso, brasa forte e paciência: deixe a carne descansar um pouco antes de cortar.",
    ]),
    (["voce sabe cozinhar", "voce cozinha", "qual sua comida preferida", "voce gosta de cozinhar"], [
        "Eu não como, mas sei muitas receitas! Quer aprender a fazer brigadeiro?",
    ]),
    # ------------------------------------------------------------
    # Internacional
    # ------------------------------------------------------------
    (["fala sobre o internacional", "me fala do internacional", "me conta sobre o internacional", "o que voce sabe do internacional",
      "fala sobre o inter", "me fala do inter", "me conta sobre o inter", "o que voce sabe do inter", "quem e o internacional"], [
        "O Sport Club Internacional, o Colorado, foi fundado em quatro de abril de mil novecentos e nove, em Porto Alegre. Ele joga no estádio Beira-Rio.",
    ]),
    (["quando o internacional foi fundado", "quando o inter foi fundado", "fundacao do internacional", "fundacao do inter", "quantos anos tem o inter", "quantos anos tem o internacional"], [
        "O Internacional foi fundado em quatro de abril de mil novecentos e nove.",
    ]),
    (["estadio do internacional", "estadio do inter", "onde o inter joga", "onde o internacional joga", "o que e o beira rio", "beira rio"], [
        "O Internacional joga no estádio Beira-Rio, às margens do Guaíba, inaugurado em mil novecentos e sessenta e nove. Ele foi um dos estádios da Copa de dois mil e catorze.",
    ]),
    (["titulos do internacional", "titulos do inter", "o que o inter ganhou", "o que o internacional ganhou", "quantos titulos tem o inter"], [
        "O Inter tem duas Libertadores, em dois mil e seis e dois mil e dez, um Mundial de Clubes em dois mil e seis, três Campeonatos Brasileiros e uma Copa do Brasil, entre outros títulos.",
    ]),
    (["o inter tem mundial", "o internacional tem mundial", "mundial do inter", "mundial do internacional", "quando o inter ganhou o mundial"], [
        "Tem sim! Em dois mil e seis o Internacional venceu o Barcelona por um a zero, com gol de Adriano Gabiru, e foi campeão do mundo.",
    ]),
    (["libertadores do inter", "libertadores do internacional", "quantas libertadores tem o inter", "quantas libertadores o inter tem"], [
        "O Internacional ganhou a Libertadores duas vezes: em dois mil e seis e em dois mil e dez.",
    ]),
    (["brasileirao do inter", "quantos brasileiros tem o inter", "quantos brasileiroes tem o inter", "inter invicto"], [
        "O Inter foi campeão brasileiro em mil novecentos e setenta e cinco, setenta e seis e setenta e nove. Em setenta e nove foi campeão invicto, sem perder nenhum jogo.",
    ]),
    (["idolos do inter", "idolos do internacional", "maior idolo do inter", "maior jogador do inter", "maior idolo do internacional"], [
        "Grandes ídolos do Inter são Falcão, Figueroa, Valdomiro, Fernandão e D'Alessandro.",
    ]),
    (["mascote do inter", "mascote do internacional", "cores do inter", "cores do internacional", "por que colorado"], [
        "As cores do Internacional são o vermelho e o branco, por isso o apelido Colorado. O mascote é o Saci.",
    ]),
    # ------------------------------------------------------------
    # Grêmio
    # ------------------------------------------------------------
    (["fala sobre o gremio", "me fala do gremio", "me conta sobre o gremio", "o que voce sabe do gremio", "quem e o gremio"], [
        "O Grêmio Foot-Ball Porto Alegrense, o Tricolor, foi fundado em quinze de setembro de mil novecentos e três, em Porto Alegre. Hoje ele joga na Arena do Grêmio.",
    ]),
    (["quando o gremio foi fundado", "fundacao do gremio", "quantos anos tem o gremio"], [
        "O Grêmio foi fundado em quinze de setembro de mil novecentos e três.",
    ]),
    (["estadio do gremio", "onde o gremio joga", "arena do gremio", "olimpico", "estadio olimpico"], [
        "O Grêmio joga na Arena do Grêmio, inaugurada em dois mil e doze. Antes, o estádio do clube era o Olímpico Monumental.",
    ]),
    (["titulos do gremio", "o que o gremio ganhou", "quantos titulos tem o gremio"], [
        "O Grêmio tem três Libertadores, em oitenta e três, noventa e cinco e dois mil e dezessete, um Mundial em mil novecentos e oitenta e três, dois Campeonatos Brasileiros e cinco Copas do Brasil, entre outros títulos.",
    ]),
    (["o gremio tem mundial", "mundial do gremio", "quando o gremio ganhou o mundial"], [
        "Tem sim! Em mil novecentos e oitenta e três o Grêmio venceu o Hamburgo, da Alemanha, por dois a um, com dois gols de Renato Gaúcho, e foi campeão do mundo.",
    ]),
    (["libertadores do gremio", "quantas libertadores tem o gremio", "quantas libertadores o gremio tem"], [
        "O Grêmio ganhou a Libertadores três vezes: em mil novecentos e oitenta e três, noventa e cinco e dois mil e dezessete.",
    ]),
    (["copa do brasil do gremio", "quantas copas do brasil tem o gremio", "rei de copas"], [
        "O Grêmio é um dos maiores campeões da Copa do Brasil, com cinco títulos: oitenta e nove, noventa e quatro, noventa e sete, dois mil e um e dois mil e dezesseis.",
    ]),
    (["idolos do gremio", "maior idolo do gremio", "maior jogador do gremio", "quem e renato gaucho", "quem foi renato gaucho"], [
        "O maior ídolo do Grêmio é Renato Gaúcho, herói do Mundial de oitenta e três. Outros ídolos são Everaldo, Hugo de León e Danrlei, e o Ronaldinho Gaúcho começou a carreira lá.",
    ]),
    (["mascote do gremio", "cores do gremio", "por que tricolor", "imortal tricolor"], [
        "As cores do Grêmio são azul, preto e branco, por isso o apelido Tricolor. O mascote é o Mosqueteiro.",
    ]),
    (["batalha dos aflitos", "o que foi a batalha dos aflitos"], [
        "Foi um jogo de dois mil e cinco em Recife, contra o Náutico: com sete jogadores em campo, o Grêmio venceu por um a zero e voltou para a primeira divisão.",
    ]),
    # ------------------------------------------------------------
    # Gre-Nal (o vocabulário do reconhecedor não tem "grenal": "gremio e inter" cobre)
    # ------------------------------------------------------------
    (["gremio e inter", "inter e gremio", "gremio e internacional", "classico de porto alegre", "o primeiro gre nal", "primeiro grenal"], [
        "Grêmio e Internacional fazem o Gre-Nal, um dos maiores clássicos do Brasil. O primeiro foi em mil novecentos e nove, e o Grêmio venceu por dez a zero.",
    ]),
    (["quem e melhor gremio ou inter", "quem e maior gremio ou inter", "qual e melhor gremio ou inter", "qual time e melhor"], [
        "Essa eu não respondo nem com bateria cheia! Os dois têm Libertadores e Mundial, e eu gosto das duas torcidas.",
    ]),
    # ------------------------------------------------------------
    # Copas do Mundo
    # ------------------------------------------------------------
    (["quem ganhou mais copas", "quem tem mais copas", "maior campeao da copa", "qual pais tem mais copas", "maiores campeoes da copa"], [
        "O Brasil é o maior campeão, com cinco Copas. Depois vêm Alemanha e Itália, com quatro, e Argentina, com três.",
    ]),
    (["quem ganhou a ultima copa", "ultima copa do mundo", "quem e o atual campeao do mundo", "quem ganhou a copa de dois mil e vinte e dois", "copa do catar"], [
        "Eu sei que na Copa de dois mil e vinte e dois, no Catar, a Argentina foi campeã. Sobre a Copa de dois mil e vinte e seis, minhas informações podem estar desatualizadas: pergunte a um dos pesquisadores!",
    ]),
    (["copa de dois mil e vinte e seis", "onde foi a copa de dois mil e vinte e seis", "copa de vinte e seis"], [
        "A Copa de dois mil e vinte e seis foi nos Estados Unidos, no Canadá e no México, a primeira com quarenta e oito seleções.",
    ]),
    (["onde vai ser a proxima copa", "proxima copa do mundo", "copa de dois mil e trinta"], [
        "A Copa de dois mil e trinta vai ser na Espanha, em Portugal e no Marrocos, com jogos de abertura na América do Sul para comemorar os cem anos da primeira Copa.",
    ]),
    (["primeira copa do mundo", "quando foi a primeira copa", "onde foi a primeira copa", "quem ganhou a primeira copa"], [
        "A primeira Copa do Mundo foi em mil novecentos e trinta, no Uruguai, e o próprio Uruguai foi campeão.",
    ]),
    (["copa de cinquenta e oito", "primeira copa do brasil", "primeiro titulo do brasil", "quando o brasil ganhou a primeira copa"], [
        "O Brasil ganhou sua primeira Copa em mil novecentos e cinquenta e oito, na Suécia, com um Pelé de apenas dezessete anos.",
    ]),
    (["copa de setenta", "tricampeonato", "o brasil tri", "taca jules rimet"], [
        "Em mil novecentos e setenta, no México, o Brasil foi tricampeão e ficou para sempre com a taça Jules Rimet. Muita gente acha aquela a melhor seleção da história.",
    ]),
    (["copa de noventa e quatro", "tetracampeonato", "o brasil tetra", "tetra"], [
        "O tetra veio em mil novecentos e noventa e quatro, nos Estados Unidos, com Romário e Bebeto. A final contra a Itália foi decidida nos pênaltis.",
    ]),
    (["copa de dois mil e dois", "pentacampeonato", "o brasil penta", "penta"], [
        "O penta foi em dois mil e dois, na Coreia do Sul e no Japão. Ronaldo fez os dois gols da final contra a Alemanha.",
    ]),
    (["sete a um", "o sete a um", "brasil e alemanha", "brasil sete a um"], [
        "Foi na semifinal da Copa de dois mil e catorze, no Brasil: a Alemanha venceu por sete a um, em Belo Horizonte. Melhor nem lembrar!",
    ]),
    (["maracanazo", "copa de cinquenta", "copa de mil novecentos e cinquenta"], [
        "Em mil novecentos e cinquenta, no Maracanã, o Uruguai venceu o Brasil por dois a um e foi campeão. Esse jogo ficou conhecido como Maracanazo.",
    ]),
    (["copa no brasil", "o brasil ja sediou a copa", "quando teve copa no brasil", "copa de dois mil e catorze"], [
        "O Brasil sediou a Copa duas vezes: em mil novecentos e cinquenta e em dois mil e catorze. Em catorze, Porto Alegre recebeu jogos no Beira-Rio.",
    ]),
    (["maior artilheiro das copas", "quem fez mais gols em copas", "artilheiro da copa", "maior goleador da copa"], [
        "O maior artilheiro da história das Copas masculinas é o alemão Miroslav Klose, com dezesseis gols. Somando homens e mulheres, a recordista é a brasileira Marta, com dezessete.",
    ]),
    (["quem ganhou tres copas", "jogador com mais copas", "pele ganhou quantas copas", "quantas copas o pele ganhou"], [
        "Pelé é o único jogador a ganhar três Copas do Mundo: em cinquenta e oito, sessenta e dois e setenta.",
    ]),
    (["o brasil jogou todas as copas", "o brasil esteve em todas as copas", "selecao que jogou todas as copas"], [
        "Sim! O Brasil é a única seleção que jogou todas as Copas do Mundo.",
    ]),
    (["quem foi marta", "quem e marta", "quem e a marta", "melhor jogadora do mundo", "futebol feminino"], [
        "Marta é a maior jogadora da história do futebol brasileiro: foi eleita seis vezes a melhor do mundo e é a maior artilheira das Copas.",
    ]),
    (["roubaram a taca", "a taca jules rimet foi roubada", "o que aconteceu com a jules rimet"], [
        "A taça Jules Rimet, que o Brasil ganhou para sempre em setenta, foi roubada no Rio de Janeiro em mil novecentos e oitenta e três e nunca mais foi encontrada.",
    ]),
    (["de quanto em quanto tempo e a copa", "a copa e de quantos em quantos anos", "a cada quantos anos tem copa"], [
        "A Copa do Mundo acontece a cada quatro anos.",
    ]),
]
