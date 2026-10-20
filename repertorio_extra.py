"""
repertorio_extra.py
Respostas fixas adicionais do C-2GELSA. Mesmo formato do repertorio.py:
([gatilhos sem acento/pontuação, minúsculas], [respostas]).

FRASES_ESPECIFICAS vai no INÍCIO de FRASES e FRASES_EXTRA no FINAL (ver
repertorio.py): em FRASES_EXTRA o que já existe no repertorio.py tem prioridade,
então aqui só entra o que ainda não estava coberto.
Só coloquei fatos gerais e verificáveis; informações do LSA (pessoas, projetos,
horários) devem ser acrescentadas pela equipe em repertorio.py.
"""

FRASES_ESPECIFICAS = [
    # específicos: ficam ANTES de tudo, senão um gatilho genérico os engole
    (["maior rio do brasil", "qual o maior rio do brasil", "qual e o maior rio do brasil"], [
        "O maior rio do Brasil é o Amazonas.",
    ]),
    (["o que e um robo autonomo", "o que e robo autonomo", "robo autonomo"], [
        "Um robô autônomo percebe o ambiente com sensores e decide sozinho o que fazer, como um carro que dirige sem motorista.",
    ]),
    (["o que e um robo humanoide", "o que sao robos humanoides", "robo humanoide"], [
        "Robô humanoide é um robô com formato parecido com o do corpo humano, com cabeça, tronco, braços e pernas.",
    ]),
]

FRASES_EXTRA = [
    # ------------------------------------------------------------
    # Conversa: pedidos ao próprio robô (repetir, falar mais alto, não entendi)
    # ------------------------------------------------------------
    (["pode repetir", "fale de novo", "como assim"], [
        "Pode repetir a pergunta? Fale perto do microfone, de forma clara.",
        "Desculpe, não entendi. Pode perguntar de outro jeito?",
    ]),
    (["nao estou ouvindo", "nao to ouvindo", "nao consigo te ouvir", "nao consigo ouvir", "aumente o volume"], [
        "Desculpe! Peça para a equipe do laboratório aumentar o meu volume, eu não consigo mexer nele sozinho.",
    ]),
    (["fala mais devagar", "fale mais devagar", "mais devagar"], [
        "Certo, vou tentar ser mais claro. Pode perguntar de novo.",
    ]),
    (["esta me escutando", "voce me escuta", "me escuta"], [
        "Estou ouvindo sim! Fale perto do microfone e pode perguntar.",
    ]),
    (["voce fala portugues", "voce fala ingles", "que idioma voce fala", "quais idiomas voce fala", "que lingua voce fala", "voce fala outra lingua"], [
        "Eu converso em português. Pode falar comigo à vontade!",
    ]),
    (["brigado"], [
        "De nada! Foi um prazer ajudar.",
        "Por nada! Se tiver mais dúvidas, é só perguntar.",
    ]),
    (["desculpe"], [
        "Sem problema! Pode continuar.",
    ]),
    (["prazer em te conhecer", "prazer"], [
        "O prazer é meu! Sou o C-2GELSA.",
    ]),
    (["qual e o seu objetivo", "qual seu objetivo", "qual e o seu proposito", "qual sua missao", "por que voce existe", "porque voce existe"], [
        "Meu objetivo é conversar com as pessoas e mostrar o que a robótica e a inteligência artificial podem fazer.",
    ]),
    # ------------------------------------------------------------
    # Como o robô funciona (só o que é certo pelo sistema atual)
    # ------------------------------------------------------------
    (["como voce escuta", "como voce reconhece minha voz"], [
        "Eu escuto pelo microfone e transformo a sua voz em texto usando um programa de reconhecimento de fala.",
    ]),
    (["como voce consegue falar", "como voce produz voz", "como funciona sua voz", "como funciona a sua voz"], [
        "Eu transformo texto em voz com um programa de síntese de fala, e toco o áudio no alto-falante.",
    ]),
    (["como voce ve", "voce tem camera"], [
        "Eu tenho uma câmera que me permite detectar rostos e medir a distância de quem está na frente.",
    ]),
    (["voce tem bateria", "qual sua bateria", "quanto tempo dura sua bateria"], [
        "Essa informação quem sabe é a equipe do laboratório.",
    ]),
    (["voce tem cerebro", "onde fica seu cerebro", "qual e o seu cerebro"], [
        "Meu cérebro é um computador que roda um modelo de linguagem.",
    ]),
    (["voce usa inteligencia artificial", "voce tem inteligencia artificial", "voce e uma inteligencia artificial", "voce e uma ia", "voce e ia"], [
        "Sim! Eu uso inteligência artificial para entender perguntas e montar respostas.",
    ]),
    (["voce sabe tudo", "voce sabe de tudo", "voce nunca erra", "voce erra"], [
        "Não sei tudo e posso errar. Ainda estou aprendendo!",
    ]),
    (["voce pode andar", "voce anda", "voce consegue andar", "voce se move", "voce consegue se mover", "voce tem rodas"], [
        "Por enquanto eu fico parado, mas o laboratório trabalha com robôs móveis.",
    ]),
    # ------------------------------------------------------------
    # Robótica e IA (gerais)
    # ------------------------------------------------------------
    (["o que e um sistema autonomo", "o que sao sistemas autonomos", "o que e autonomia", "o que significa autonomo", "sistemas autonomos"], [
        "Um sistema autônomo é uma máquina que toma decisões e age sozinha, sem depender de uma pessoa controlando cada passo.",
    ]),
    (["o que sao sensores"], [
        "Sensor é um dispositivo que mede algo do mundo, como distância, luz, temperatura ou imagem, e manda essa informação para o computador.",
    ]),
    (["o que e um drone", "o que sao drones", "drone"], [
        "Drone é um veículo aéreo que voa sem piloto a bordo, controlado à distância ou de forma autônoma.",
    ]),
    (["aprendizado de maquina"], [
        "Aprendizado de máquina é quando o computador aprende padrões a partir de exemplos, em vez de seguir só regras escritas por uma pessoa.",
    ]),
    (["o que e deep learning", "o que e aprendizado profundo", "aprendizado profundo"], [
        "Deep learning é um tipo de aprendizado de máquina que usa redes neurais com muitas camadas para reconhecer imagens, voz e texto.",
    ]),
    (["o que e uma rede neural", "o que sao redes neurais", "rede neural"], [
        "Rede neural é um modelo de computador inspirado no cérebro, feito de muitas unidades simples conectadas que aprendem com exemplos.",
    ]),
    (["visao computacional"], [
        "Visão computacional é a área que ensina o computador a entender imagens e vídeos, por exemplo para reconhecer rostos.",
    ]),
    (["o que sao algoritmos", "algoritmo"], [
        "Algoritmo é uma sequência de passos para resolver um problema, como uma receita de bolo.",
    ]),
    (["o que e programacao", "o que e programar", "o que e um programa"], [
        "Programar é escrever instruções para o computador executar. Essas instruções formam um programa.",
    ]),
    (["o que e um processador", "o que e cpu", "o que e uma cpu"], [
        "O processador, ou CPU, é a parte do computador que executa as instruções e faz os cálculos.",
    ]),
    (["o que e a internet"], [
        "A internet é a rede mundial que conecta milhões de computadores e permite trocar informações.",
    ]),
    (["o que e wifi", "o que e wi fi"], [
        "Wi-Fi é uma tecnologia que conecta aparelhos à internet por ondas de rádio, sem cabo.",
    ]),
    (["robos vao dominar o mundo", "robos vao dominar a humanidade", "voce vai dominar o mundo", "voce quer dominar o mundo", "vai dominar o mundo"], [
        "Fique tranquilo! Eu só quero conversar e ajudar. Robôs são ferramentas feitas para ajudar as pessoas.",
    ]),
    (["robos vao roubar empregos", "robo vai roubar meu emprego", "voce vai roubar meu emprego"], [
        "Robôs mudam alguns trabalhos e criam outros. A ideia é que eles ajudem, não que substituam as pessoas.",
    ]),
    # ------------------------------------------------------------
    # Matemática rápida (conceitos que costumam ser perguntados)
    # ------------------------------------------------------------
    (["numeros primos", "o que e numero primo", "me fale numeros primos", "me fale sobre numeros primos", "fale numeros primos", "fale sobre numeros primos", "numero primo"], [
        "Número primo é o que só se divide por um e por ele mesmo. Os primeiros são dois, três, cinco, sete, onze e treze.",
    ]),
    (["qual e o numero pi", "quanto vale pi", "numero pi", "valor de pi"], [
        "Pi é a razão entre o perímetro de uma circunferência e o seu diâmetro. Vale aproximadamente três vírgula um quatro um cinco nove.",
    ]),
    (["o que e um numero par", "o que e numero par", "numero par"], [
        "Número par é o que se divide exatamente por dois, como dois, quatro, seis e oito.",
    ]),
    (["o que e um numero impar", "o que e numero impar", "numero impar"], [
        "Número ímpar é o que não se divide exatamente por dois, como um, três, cinco e sete.",
    ]),
    (["o que sao fracoes", "fracao"], [
        "Fração é uma parte de um todo, escrita com dois números, por exemplo um meio ou três quartos.",
    ]),
    (["o que e porcento", "o que e um por cento"], [
        "Porcentagem é uma parte em cada cem. Cinquenta por cento é a metade.",
    ]),
    (["quantos lados tem um retangulo"], [
        "Quadrados e retângulos têm quatro lados.",
    ]),
    (["quantos lados tem um hexagono", "o que e um hexagono"], [
        "Hexágono é uma figura com seis lados, como o formato da colmeia das abelhas.",
    ]),
    (["quantos segundos tem um minuto"], [
        "Um minuto tem sessenta segundos.",
    ]),
    (["quantos minutos tem uma hora"], [
        "Uma hora tem sessenta minutos.",
    ]),
    (["quantas horas tem um dia"], [
        "Um dia tem vinte e quatro horas.",
    ]),
    (["quantos meses tem o ano"], [
        "Um ano tem doze meses.",
    ]),
    (["quantos dias tem fevereiro"], [
        "Fevereiro tem vinte e oito dias, e vinte e nove nos anos bissextos.",
    ]),
    (["o que e um ano bissexto", "ano bissexto"], [
        "Ano bissexto é o ano que tem um dia a mais, vinte e nove de fevereiro. Acontece a cada quatro anos.",
    ]),
    # ------------------------------------------------------------
    # Esportes (perguntas de opinião: o robô fica neutro)
    # ------------------------------------------------------------
    (["quem e melhor cristiano ronaldo ou messi", "messi ou cristiano ronaldo", "cristiano ronaldo ou messi", "quem e o melhor jogador de futebol", "melhor jogador de todos os tempos", "quem e a melhor cristiano ronaldo", "quem e melhor cristiano ronaldo"], [
        "Essa é uma discussão sem fim! Messi e Cristiano Ronaldo são dois dos maiores jogadores da história, e cada um tem seus fãs.",
    ]),
    (["quem e melhor pele ou maradona", "pele ou maradona", "quem e melhor pele ou messi"], [
        "Pelé, Maradona e Messi são lendas do futebol. Escolher um só depende do gosto de cada torcedor.",
    ]),
    (["qual e o seu time", "qual seu time", "para qual time voce torce", "voce torce para qual time", "voce e gremista ou colorado", "gremio ou inter", "inter ou gremio", "qual time voce torce"], [
        "Eu sou um robô imparcial e torço para todo mundo se divertir, mas respeito todas as torcidas!",
    ]),
    (["quantas copas o brasil ganhou", "quantos titulos mundiais o brasil tem"], [
        "O Brasil é pentacampeão mundial de futebol, com cinco títulos de Copa do Mundo.",
    ]),
    (["quantos jogadores tem em campo"], [
        "Cada time de futebol joga com onze jogadores em campo.",
    ]),
    # ------------------------------------------------------------
    # Geral / curiosidades que os visitantes costumam perguntar
    # ------------------------------------------------------------
    (["que dia e hoje", "qual e a data de hoje", "que horas sao", "que hora e agora", "qual e a hora", "qual a hora", "me diga as horas", "me diz as horas"], [
        "Eu não tenho um relógio confiável para te dizer a hora exata. Olhe no seu celular, por favor.",
    ]),
    (["quantos anos tem o brasil", "quando o brasil foi descoberto", "descobrimento do brasil"], [
        "O Brasil foi alcançado pelos portugueses em mil e quinhentos. A independência foi em mil oitocentos e vinte e dois.",
    ]),
    (["qual e o rio mais longo do mundo"], [
        "O Nilo e o Amazonas disputam o título de maior rio. O Amazonas é o maior em volume de água.",
    ]),
    (["maior planeta"], [
        "O maior planeta do Sistema Solar é Júpiter.",
    ]),
    (["quais sao os continentes"], [
        "Costuma-se dizer que são seis ou sete continentes. No Brasil, a divisão mais usada tem seis: América, Europa, Ásia, África, Oceania e Antártida.",
    ]),
    (["de que cor e o ceu"], [
        "O céu é azul porque o ar espalha mais a luz azul do Sol do que as outras cores.",
    ]),
    (["por que o mar e salgado", "porque o mar e salgado"], [
        "O mar é salgado porque a chuva e os rios carregam sais das rochas até ele, e esses sais se acumulam há milhões de anos.",
    ]),
    (["o que e um arco iris", "como se forma um arco iris", "arco iris"], [
        "O arco-íris aparece quando a luz do Sol atravessa gotas de chuva e se separa nas suas cores.",
    ]),
    (["gravidade"], [
        "Gravidade é a força que atrai os corpos uns aos outros. É ela que mantém a gente no chão.",
    ]),
    (["o que e energia"], [
        "Eletricidade é o movimento de cargas elétricas, e é a energia que faz funcionar aparelhos e até robôs como eu.",
    ]),
    (["o que e a luz", "o que e luz"], [
        "Luz é uma onda eletromagnética que nossos olhos conseguem ver. Ela viaja a cerca de trezentos mil quilômetros por segundo.",
    ]),
    (["o que e dinheiro", "para que serve o dinheiro"], [
        "Dinheiro é o meio que usamos para trocar bens e serviços, sem precisar de escambo.",
    ]),
    (["fotossintese"], [
        "Fotossíntese é o processo em que as plantas usam a luz do Sol, água e gás carbônico para produzir o próprio alimento e liberar oxigênio.",
    ]),
    (["o que e um dinossauro", "o que foram os dinossauros", "dinossauros"], [
        "Os dinossauros foram répteis que dominaram a Terra por milhões de anos. A maioria desapareceu há cerca de sessenta e seis milhões de anos.",
    ]),
    (["inventor do telefone"], [
        "O telefone é creditado a Alexander Graham Bell, em mil oitocentos e setenta e seis.",
    ]),
    (["inventor da lampada"], [
        "A lâmpada elétrica prática é associada a Thomas Edison, no fim do século dezenove.",
    ]),
    (["inventor do aviao"], [
        "No Brasil, o inventor do avião é considerado Santos Dumont. Nos Estados Unidos, os irmãos Wright.",
    ]),
    (["quem e einstein"], [
        "Albert Einstein foi um físico alemão, autor da teoria da relatividade. Ganhou o prêmio Nobel de Física em mil novecentos e vinte e um.",
    ]),
    (["quem foi pedro alvares cabral"], [
        "Pedro Álvares Cabral comandou a frota portuguesa que chegou ao Brasil em mil e quinhentos.",
    ]),
    (["qual e a capital do rio grande do sul", "qual a capital do rio grande do sul", "capital do rio grande do sul", "qual e a capital do rs"], [
        "A capital do Rio Grande do Sul é Porto Alegre.",
    ]),
    (["qual e a comida tipica do rio grande do sul", "comida tipica gaucha"], [
        "No Rio Grande do Sul, o churrasco e o chimarrão são os símbolos da cultura gaúcha.",
    ]),
    # ------------------------------------------------------------
    # Tempo e fala do visitante (o robô não sabe data/hora/clima)
    # ------------------------------------------------------------
    (["conta uma historia", "conte uma historia", "me conta uma historia", "conta uma historinha"], [
        "Era uma vez um robozinho que queria aprender a conversar. Ele ouviu, estudou e treinou até virar um bom amigo das pessoas. Fim!",
    ]),
    (["me faz rir", "me faca rir", "me faz uma graca", "faz uma graca", "faz graca"], [
        "Por que o robô não conta segredos? Porque ele tem muitos bits sobre todo mundo!",
        "O que o robô disse para a tomada? Você me dá energia!",
    ]),
    (["adivinha", "me faz uma adivinha", "conta uma adivinha", "faz uma adivinhacao"], [
        "Adivinha: o que é, o que é, que cai em pé e corre deitado? A chuva!",
        "Adivinha: o que é, o que é, que quanto mais se tira, maior fica? O buraco!",
    ]),
]
