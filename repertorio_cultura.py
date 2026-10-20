"""
repertorio_cultura.py
Respostas fixas do C-2GELSA sobre cultura geral: recomendações (jogos, desenhos, música,
livros, quadrinhos...), quem inventou/criou/descobriu, super-heróis (Marvel e DC, com o
Gavião Negro), Star Wars, sistema solar, constelações e figuras históricas.

Mesmo formato do repertorio.py: ([gatilhos sem acento/pontuação, minúsculas], [respostas]).
Para não escrever dezenas de gatilhos à mão, os auxiliares _perfil e _astro geram os jeitos
comuns de perguntar ("quem foi X", "fala sobre X", "me conta sobre X"...).

FRASES_CULTURA vai logo depois de FRASES_FEIRA_PRIORIDADE, no INÍCIO de FRASES (ver
repertorio.py): vários gatilhos daqui, como "quem criou o batman", seriam engolidos pelo
genérico "quem criou". Por isso os gatilhos precisam ser específicos (nome + assunto), nunca
uma palavra solta como "filme" ou "lua".

Fuzzy: todos os gatilhos daqui entram em GATILHOS_FUZZY_ESTRITOS (repertorio.py) e o
brain.py só aceita um casamento aproximado se a ÚLTIMA palavra também for parecida. Sem isso,
"prefixo + nome curto" ('fala sobre marte') casava com qualquer 'fala sobre a mãe'.
Só fatos estáveis. Respostas curtas e escritas como o robô vai FALAR (sem símbolos).
Depois de editar: reiniciar o servidor_conversa.py e gerar de novo a gramática do Vosk
(ver gatilhos_gramatica.py): as frases novas precisam entrar na lista do reconhecedor.
"""

_PREFIXOS_PESSOA = ("quem foi", "quem e", "quem era", "fala sobre", "fale sobre", "me fala sobre",
                    "me conta sobre", "conte sobre", "o que voce sabe sobre", "voce conhece")
_PREFIXOS_PERSONAGEM = ("quem e", "fala sobre", "fale sobre", "me fala sobre", "me conta sobre",
                        "conte sobre", "o que voce sabe sobre", "voce conhece", "voce conhece o")
_PREFIXOS_ASTRO = ("fala sobre", "fale sobre", "me fala sobre", "me fala de", "me conta sobre",
                   "conte sobre", "o que voce sabe sobre", "o que e", "como e", "curiosidade sobre",
                   "quero saber sobre")


def _gatilhos(prefixos, nomes):
    return [p + " " + n for n in nomes for p in prefixos]


def _perfil(nomes, respostas, prefixos=_PREFIXOS_PESSOA):
    """Entrada 'quem foi/quem é/fala sobre ...' para uma pessoa ou personagem."""
    return (_gatilhos(prefixos, nomes), respostas)


def _heroi(nomes, artigo, respostas):
    """Personagem de quadrinhos/filmes: aceita com e sem artigo ('o batman', 'batman')."""
    todos = []
    for n in nomes:
        todos += [n, artigo + " " + n]
    return _perfil(todos, respostas, _PREFIXOS_PERSONAGEM)


def _astro(nomes, respostas):
    return (_gatilhos(_PREFIXOS_ASTRO, nomes), respostas)


# ------------------------------------------------------------
# 4) RECOMENDAÇÕES
# (livro, filme e série em geral já estão no repertorio.py)
# ------------------------------------------------------------
RECOMENDACOES = [
    (["me recomenda um jogo de tabuleiro", "me recomende um jogo de tabuleiro", "recomenda um jogo de tabuleiro",
      "me indica um jogo de tabuleiro", "indica um jogo de tabuleiro", "me recomenda um jogo de cartas",
      "indica um jogo de cartas"], [
        "Xadrez é o clássico para treinar a mente. Para jogar em grupo, Catan e Uno são sucesso.",
        "Dixit é lindo e criativo, e Detetive é ótimo para quem gosta de mistério.",
        "Banco Imobiliário e Imagem e Ação são bons para a família toda.",
    ]),
    (["me recomenda um jogo", "me recomende um jogo", "recomenda um jogo", "recomende um jogo",
      "me indica um jogo", "indica um jogo", "indique um jogo", "qual jogo eu jogo",
      "me recomenda um videogame", "me recomenda um jogo de videogame"], [
        "Se você gosta de aventura, experimente Zelda. Para jogar com os amigos, Mario Kart é diversão garantida.",
        "Minecraft é ótimo para criar o que você imaginar, e ainda ensina um pouco de lógica e engenharia.",
        "Para quem gosta de desafio, Hollow Knight é lindo e difícil. Para relaxar, Stardew Valley.",
        "Que tal Portal? É um jogo de quebra-cabeças com uma inteligência artificial bem sarcástica. Eu me identifiquei!",
    ]),
    (["me recomenda um desenho", "me recomende um desenho", "recomenda um desenho", "me indica um desenho",
      "indica um desenho", "me recomenda um anime", "me recomende um anime", "recomenda um anime",
      "me indica um anime", "indica um anime", "me recomenda uma animacao", "indica uma animacao"], [
        "Avatar, a Lenda de Aang é um desenho incrível, com aventura, humor e uma história emocionante.",
        "Para os mais novos, Bluey é uma graça. Para quem gosta de aventura, Hora de Aventura.",
        "Se gosta de anime, Dragon Ball e Naruto são clássicos, e A Viagem de Chihiro é um filme lindo.",
        "Rick and Morty e Gravity Falls misturam ficção científica com muito humor.",
    ]),
    (["me recomenda um filme de acao", "recomenda um filme de acao", "me indica um filme de acao",
      "indica um filme de acao", "um filme de acao para assistir"], [
        "Mad Max, Estrada da Fúria é pura adrenalina do começo ao fim.",
        "Indiana Jones e os Caçadores da Arca Perdida é um clássico de aventura e ação.",
        "Os Incríveis é um filme de ação em animação, ótimo para assistir em família.",
    ]),
    (["me recomenda um filme de comedia", "recomenda um filme de comedia", "me indica um filme de comedia",
      "indica um filme de comedia", "me recomenda uma comedia", "indica uma comedia"], [
        "O Auto da Compadecida é uma das comédias brasileiras mais queridas de todos os tempos.",
        "Se Beber, Não Case é bem engraçado, mas é para maiores. Para a família toda, Shrek.",
        "Divertida Mente também tem muito humor, e emociona.",
    ]),
    (["me recomenda um filme de ficcao cientifica", "recomenda um filme de ficcao cientifica",
      "me indica um filme de ficcao cientifica", "indica um filme de ficcao cientifica",
      "me recomenda um filme de robo", "recomenda um filme de robo", "me indica um filme de robo",
      "um filme sobre robos", "me recomenda um filme sobre robos"], [
        "WALL-E é um filme lindo sobre um robozinho que limpa o lixo da Terra e se apaixona. Assista!",
        "O Gigante de Ferro é uma história linda de amizade entre um menino e um robô enorme.",
        "Blade Runner, Matrix e Star Wars são clássicos da ficção científica. E Eu, Robô é um bom filme sobre robôs e as três leis.",
        "Interestelar mistura ciência, espaço e muita emoção.",
    ]),
    (["me recomenda um filme de terror", "recomenda um filme de terror", "me indica um filme de terror",
      "indica um filme de terror", "me recomenda um filme de suspense", "indica um filme de suspense"], [
        "Não sou muito de terror, eu me assusto com falta de energia! Mas dizem que O Iluminado é um clássico do suspense.",
        "Para um susto leve, Os Caça-Fantasmas é divertido. Para suspense, Psicose é um clássico.",
    ]),
    (["me recomenda um filme de aventura", "recomenda um filme de aventura", "me indica um filme de aventura",
      "indica um filme de aventura", "me recomenda um filme de fantasia", "indica um filme de fantasia"], [
        "O Senhor dos Anéis é a grande aventura de fantasia do cinema. Prepare a pipoca, porque é longo!",
        "Harry Potter e a Pedra Filosofal é uma ótima porta de entrada para o mundo da magia.",
        "Jurassic Park é aventura e ciência na mesma história.",
    ]),
    (["me recomenda um filme de super heroi", "recomenda um filme de super heroi",
      "me indica um filme de super heroi", "indica um filme de super heroi",
      "me recomenda um filme de super herois", "um filme de super heroi para assistir",
      "me recomenda um filme da marvel", "me recomenda um filme da dc"], [
        "Homem-Aranha no Aranhaverso é uma animação incrível, com um visual diferente de tudo.",
        "Vingadores, Ultimato é o grande encontro dos heróis da Marvel. O Cavaleiro das Trevas é o favorito de muita gente na DC.",
        "Os Incríveis é uma família de super-heróis muito divertida, e Pantera Negra tem uma história muito boa.",
    ]),
    (["me recomenda um filme para criancas", "recomenda um filme para criancas", "me indica um filme para criancas",
      "indica um filme para criancas", "me recomenda um filme infantil", "recomenda um filme infantil",
      "indica um filme infantil", "me recomenda um filme para a familia"], [
        "Toy Story, Procurando Nemo e Moana são ótimos para criançada e adultos.",
        "Meu Amigo Totoro é um filme calmo e encantador. Já Zootopia mistura aventura com mistério.",
        "Encanto é uma história colorida e musical sobre uma família mágica.",
    ]),
    (["me recomenda um documentario", "recomenda um documentario", "me indica um documentario",
      "indica um documentario", "um documentario para assistir"], [
        "Cosmos, de Carl Sagan, é um clássico para quem gosta de universo e ciência.",
        "Nosso Planeta mostra a natureza com imagens de tirar o fôlego.",
        "AlphaGo mostra uma inteligência artificial vencendo um campeão de Go. Tem tudo a ver comigo!",
    ]),
    (["me recomenda uma serie de ficcao cientifica", "recomenda uma serie de ficcao cientifica",
      "me indica uma serie de ficcao cientifica", "indica uma serie de ficcao cientifica",
      "me recomenda uma serie de robo", "me recomenda uma serie de espaco"], [
        "Star Trek é a série clássica de exploração espacial, cheia de ideias sobre ciência e convivência.",
        "Black Mirror imagina o futuro da tecnologia, e Westworld tem robôs que começam a pensar por conta própria.",
        "The Mandalorian é aventura no universo Star Wars, e o Baby Yoda é um sucesso.",
    ]),
    (["me recomenda uma musica", "me recomende uma musica", "recomenda uma musica", "me indica uma musica",
      "indica uma musica", "me recomenda uma banda", "recomenda uma banda", "me indica uma banda",
      "indica uma banda", "me recomenda um cantor", "indica um cantor", "me recomenda uma cantora"], [
        "Experimente a Legião Urbana, com Tempo Perdido, ou Os Paralamas do Sucesso. Rock brasileiro é muito bom!",
        "Se gosta de MPB, ouça Djavan, Elis Regina e Gilberto Gil. Cada um é uma aula de música.",
        "Para animar, Queen com Don't Stop Me Now. Para relaxar, Tom Jobim e Garota de Ipanema.",
        "Daft Punk é uma dupla de música eletrônica que se apresentava vestida de robôs. Eu adoro!",
    ]),
    (["me recomenda um livro infantil", "recomenda um livro infantil", "me indica um livro infantil",
      "indica um livro infantil", "me recomenda um livro para criancas", "indica um livro para criancas"], [
        "O Pequeno Príncipe é um clássico que emociona crianças e adultos.",
        "Reinações de Narizinho, de Monteiro Lobato, é divertido e muito brasileiro.",
        "O Menino Maluquinho, do Ziraldo, e Marcelo, Marmelo, Martelo, de Ruth Rocha, também são ótimos.",
    ]),
    (["me recomenda um livro de ficcao cientifica", "recomenda um livro de ficcao cientifica",
      "me indica um livro de ficcao cientifica", "indica um livro de ficcao cientifica",
      "me recomenda um livro de robo", "recomenda um livro de robo", "me recomenda um livro sobre robos",
      "um livro sobre robos"], [
        "Eu, Robô, do Isaac Asimov, é o clássico sobre robôs e as três leis da robótica. Leitura obrigatória para mim!",
        "O Guia do Mochileiro das Galáxias é de ficção científica e muito engraçado.",
        "Fundação, também do Asimov, e Duna, do Frank Herbert, são grandes clássicos do gênero.",
    ]),
    (["me recomenda um livro de aventura", "recomenda um livro de aventura", "me indica um livro de aventura",
      "me recomenda um livro de fantasia", "recomenda um livro de fantasia", "indica um livro de fantasia",
      "me recomenda um livro de misterio", "indica um livro de misterio"], [
        "O Hobbit é uma aventura de fantasia perfeita para começar. Depois vem O Senhor dos Anéis.",
        "As Crônicas de Nárnia e Harry Potter são ótimos para quem gosta de magia.",
        "Para mistério, os livros da Agatha Christie, como Assassinato no Expresso do Oriente, são clássicos.",
    ]),
    (["me recomenda uma hq", "me recomenda um gibi", "me recomenda um quadrinho", "me recomenda uma historia em quadrinhos",
      "recomenda uma hq", "recomenda um gibi", "recomenda um quadrinho", "me indica uma hq", "indica uma hq",
      "me indica um gibi", "indica um gibi", "me indica um quadrinho", "indica um quadrinho",
      "me recomenda um manga", "recomenda um manga", "indica um manga", "me indica um manga"], [
        "A Turma da Mônica, do Mauricio de Sousa, é a grande festa dos quadrinhos brasileiros. Tem para todas as idades.",
        "Watchmen e Batman, O Cavaleiro das Trevas são clássicos dos quadrinhos de heróis. Maus é uma história real, muito forte.",
        "Se gosta de mangá, comece por Dragon Ball ou Naruto. E Turma da Mônica Jovem mistura os dois estilos.",
        "Para quem gosta de ciência, Calvin e Haroldo é engraçado e muito inteligente.",
    ]),
    (["me recomenda um curso de programacao", "recomenda um curso de programacao",
      "como eu aprendo a programar", "me ensina a programar",
      "qual linguagem de programacao eu aprendo", "qual linguagem eu devo aprender",
      "qual a melhor linguagem de programacao para comecar"], [
        "Comece pelo Scratch, que é visual e divertido. Depois vá para o Python, que é fácil de ler e serve para quase tudo.",
        "Python é uma ótima primeira linguagem. Eu mesmo sou feito com bastante Python! Faça pequenos projetos, como um jogo ou um robozinho.",
    ]),
    (["me recomenda um podcast", "recomenda um podcast", "me indica um podcast", "indica um podcast"], [
        "Experimente podcasts de ciência, como o Podcast Dragões de Garagem, o Nerdcast e o Ciência Sem Fim. Tem de tudo para aprender se divertindo.",
    ]),
]

# ------------------------------------------------------------
# 5) QUEM INVENTOU / QUEM CRIOU / QUEM DESCOBRIU
# (lâmpada, telefone, avião, computador e internet já estão no repertorio.py)
# ------------------------------------------------------------
INVENCOES = [
    (["quem inventou o radio", "quem criou o radio", "quem descobriu o radio"], [
        "O italiano Guglielmo Marconi é o mais famoso pelo rádio. Mas o padre gaúcho Roberto Landell de Moura também fez transmissões de voz pioneiras, aqui no Brasil.",
    ]),
    (["quem inventou a televisao", "quem criou a televisao", "quem inventou a tv", "quem criou a tv"], [
        "A televisão foi construída por vários inventores. O escocês John Logie Baird fez as primeiras transmissões, e o americano Philo Farnsworth criou a televisão eletrônica.",
    ]),
    (["quem inventou a imprensa", "quem inventou a prensa", "quem criou a imprensa", "quem inventou a impressora",
      "quem inventou a prensa de tipos moveis"], [
        "Johannes Gutenberg, na Alemanha, por volta de 1450. A prensa de tipos móveis espalhou os livros pelo mundo.",
    ]),
    (["quem inventou o carro", "quem criou o carro", "quem inventou o automovel", "quem criou o automovel"], [
        "O alemão Karl Benz construiu o primeiro automóvel movido a motor a gasolina, em 1886.",
    ]),
    (["quem inventou a bicicleta", "quem criou a bicicleta"], [
        "O alemão Karl Drais criou, em 1817, uma bicicleta sem pedais, que se movia empurrando o chão com os pés. Os pedais vieram depois.",
    ]),
    (["quem inventou o motor a vapor", "quem criou o motor a vapor", "quem inventou a maquina a vapor",
      "quem criou a maquina a vapor"], [
        "O escocês James Watt aperfeiçoou a máquina a vapor, e isso ajudou a começar a Revolução Industrial.",
    ]),
    (["quem inventou a pilha", "quem criou a pilha", "quem inventou a bateria"], [
        "O italiano Alessandro Volta criou a primeira pilha elétrica, em 1800. A unidade de tensão, o volt, leva o nome dele.",
    ]),
    (["quem descobriu a eletricidade", "quem inventou a eletricidade"], [
        "Ninguém inventou a eletricidade, ela existe na natureza. Muita gente estudou, como Benjamin Franklin, Volta e Michael Faraday, que criou o gerador.",
    ]),
    (["quem descobriu a penicilina", "quem inventou a penicilina"], [
        "O médico escocês Alexander Fleming descobriu a penicilina, em 1928, por acaso: um fungo matou as bactérias da placa de laboratório dele.",
    ]),
    (["quem inventou a vacina", "quem criou a vacina", "quem descobriu a vacina"], [
        "O médico inglês Edward Jenner criou a primeira vacina, contra a varíola, em 1796. Vacina salva milhões de vidas!",
    ]),
    (["quem inventou o telescopio", "quem criou o telescopio"], [
        "O holandês Hans Lippershey pediu a primeira patente, em 1608. Galileu aperfeiçoou o aparelho e foi o primeiro a apontar para o céu com ele.",
    ]),
    (["quem inventou o microscopio", "quem criou o microscopio"], [
        "Os primeiros microscópios surgiram na Holanda, por volta de 1600. Anton van Leeuwenhoek foi o primeiro a observar micróbios com um deles.",
    ]),
    (["quem inventou o cinema", "quem criou o cinema"], [
        "Os irmãos Lumière, na França, fizeram a primeira exibição pública de cinema, em 1895.",
    ]),
    (["quem inventou a fotografia", "quem criou a fotografia", "quem inventou a foto"], [
        "O francês Nicéphore Niépce fez a primeira fotografia, por volta de 1826. Depois Louis Daguerre aperfeiçoou o processo.",
    ]),
    (["quem inventou o telegrafo", "quem criou o telegrafo", "quem inventou o codigo morse"], [
        "O americano Samuel Morse aperfeiçoou o telégrafo e criou o código Morse, feito de pontos e traços.",
    ]),
    (["quem inventou o relogio de pendulo", "quem inventou o relogio", "quem criou o relogio"], [
        "Os relógios existem há milênios, do relógio de sol ao de água. O de pêndulo, bem preciso, foi criado pelo holandês Christiaan Huygens, em 1656.",
    ]),
    (["quem inventou o papel", "quem criou o papel"], [
        "O papel nasceu na China, há cerca de dois mil anos, e a invenção é atribuída a um oficial chamado Cai Lun.",
    ]),
    (["quem inventou a bussola", "quem criou a bussola"], [
        "A bússola foi inventada na China, há muitos séculos, e ajudou os navegadores a se orientar pelo mar.",
    ]),
    (["quem inventou a polvora", "quem criou a polvora"], [
        "A pólvora foi inventada na China, há mais de mil anos, e começou como parte de experimentos de alquimia.",
    ]),
    (["quem inventou a roda", "quem criou a roda"], [
        "A roda surgiu na Mesopotâmia, há mais de cinco mil anos, e não se sabe quem foi o inventor. Mudou o transporte para sempre!",
    ]),
    (["quem inventou a escrita", "quem criou a escrita"], [
        "Os sumérios, na Mesopotâmia, criaram a escrita cuneiforme há mais de cinco mil anos, marcando argila com pequenas cunhas.",
    ]),
    (["quem inventou o celular", "quem criou o celular", "quem inventou o telefone celular", "quem criou o telefone celular"], [
        "O engenheiro americano Martin Cooper fez a primeira ligação de um telefone celular, em 1973, na empresa Motorola.",
    ]),
    (["quem inventou o laser", "quem criou o laser"], [
        "O americano Theodore Maiman construiu o primeiro laser, em 1960.",
    ]),
    (["quem descobriu o raio x", "quem inventou o raio x", "quem criou o raio x"], [
        "O físico alemão Wilhelm Röntgen descobriu o raio X, em 1895. Ele ganhou o primeiro prêmio Nobel de Física.",
    ]),
    (["quem descobriu a radioatividade"], [
        "Henri Becquerel descobriu a radioatividade, em 1896, e Marie e Pierre Curie estudaram o fenômeno a fundo.",
    ]),
    (["quem descobriu o dna", "quem descobriu a estrutura do dna", "quem descobriu a dupla helice"], [
        "James Watson e Francis Crick propuseram a estrutura de dupla hélice do DNA, em 1953, com ajuda das imagens da cientista Rosalind Franklin.",
    ]),
    (["quem descobriu a america", "quem descobriu as americas"], [
        "O navegador Cristóvão Colombo chegou à América em 1492, a serviço da Espanha. Mas aqui já viviam povos indígenas há milhares de anos!",
    ]),
    (["quem descobriu plutao"], [
        "O astrônomo americano Clyde Tombaugh descobriu Plutão, em 1930. Hoje Plutão é considerado um planeta anão.",
    ]),
    (["quem descobriu urano"], [
        "O astrônomo inglês William Herschel descobriu Urano, em 1781.",
    ]),
    (["quem descobriu netuno"], [
        "Netuno foi descoberto em 1846, depois de matemáticos calcularem onde ele deveria estar. Foi um planeta achado primeiro no papel!",
    ]),
    (["quem descobriu o fogo", "quem inventou o fogo"], [
        "Ninguém sabe ao certo! Nossos ancestrais aprenderam a controlar o fogo há centenas de milhares de anos, e isso mudou tudo.",
    ]),
    (["quem inventou a palavra robo", "quem criou a palavra robo",
      "de onde veio a palavra robo", "de onde vem o nome robo", "qual a origem da palavra robo"], [
        "A palavra robô apareceu em 1920, na peça de teatro R.U.R., do escritor tcheco Karel Tchápek. Vem de uma palavra tcheca que quer dizer trabalho forçado.",
    ]),
    (["qual foi o primeiro robo", "qual o primeiro robo", "quem inventou o primeiro robo", "quem criou o primeiro robo"], [
        "O primeiro robô industrial foi o Unimate, que começou a trabalhar numa fábrica americana, em 1961. Mas as ideias de máquinas que imitam gente são bem mais antigas.",
    ]),
    (["quem inventou o lego", "quem criou o lego"], [
        "O Lego nasceu na Dinamarca, criado pelo carpinteiro Ole Kirk Christiansen, em 1932. O nome vem de duas palavras dinamarquesas, que querem dizer brincar bem.",
    ]),
    (["quem inventou o futebol", "quem criou o futebol"], [
        "O futebol moderno nasceu na Inglaterra, com as primeiras regras escritas em 1863. No Brasil, quem ajudou a espalhar o esporte foi Charles Miller.",
    ]),
    (["quem inventou o basquete", "quem criou o basquete", "quem inventou o basquetebol"], [
        "O canadense James Naismith inventou o basquete, em 1891, nos Estados Unidos. Os primeiros cestos eram cestas de pêssego!",
    ]),
    (["quem inventou o volei", "quem criou o volei", "quem inventou o voleibol"], [
        "O americano William Morgan inventou o vôlei, em 1895, como um jogo mais calmo que o basquete.",
    ]),
    (["quem inventou o xadrez", "quem criou o xadrez", "de onde vem o xadrez"], [
        "O xadrez nasceu na Índia, há mais de mil anos, com o nome de chaturanga. Depois viajou pela Pérsia e chegou à Europa.",
    ]),
    # personagens e histórias
    (["quem criou o homem aranha", "quem criou o homem de ferro", "quem criou o hulk", "quem criou os x men",
      "quem criou o quarteto fantastico", "quem criou os herois da marvel", "quem criou a marvel"], [
        "A maioria dos heróis clássicos da Marvel foi criada por Stan Lee, junto com desenhistas como Steve Ditko e Jack Kirby, nos anos sessenta.",
    ]),
    (["quem criou o batman"], [
        "O Batman foi criado em 1939 pelo desenhista Bob Kane e pelo roteirista Bill Finger.",
    ]),
    (["quem criou o superman", "quem criou o super homem"], [
        "O Superman foi criado em 1938 por dois amigos de escola, o roteirista Jerry Siegel e o desenhista Joe Shuster.",
    ]),
    (["quem criou a mulher maravilha"], [
        "A Mulher-Maravilha foi criada em 1941 pelo psicólogo e escritor William Moulton Marston.",
    ]),
    (["quem criou o gaviao negro"], [
        "O Gavião Negro foi criado em 1940 pelo roteirista Gardner Fox e pelo desenhista Dennis Neville.",
    ]),
    (["quem criou o capitao america"], [
        "O Capitão América foi criado em 1941 por Joe Simon e Jack Kirby.",
    ]),
    (["quem criou a turma da monica", "quem criou a monica", "quem e o criador da turma da monica"], [
        "A Turma da Mônica foi criada pelo Mauricio de Sousa. A Mônica foi inspirada numa das filhas dele!",
    ]),
    (["quem criou o mickey", "quem criou o mickey mouse"], [
        "O Mickey foi criado em 1928 por Walt Disney e pelo desenhista Ub Iwerks.",
    ]),
    (["quem criou star wars", "quem criou o star wars", "quem criou guerra nas estrelas", "quem fez star wars"], [
        "Star Wars foi criado pelo cineasta George Lucas. O primeiro filme estreou em 1977 e mudou o cinema para sempre.",
    ]),
    (["quem criou o minecraft"], [
        "O Minecraft foi criado pelo sueco Markus Persson, o Notch, e lançado em 2011.",
    ]),
    (["quem criou o mario", "quem criou o super mario"], [
        "O Mario foi criado pelo japonês Shigeru Miyamoto, da Nintendo, e apareceu pela primeira vez em 1981.",
    ]),
    (["quem criou o pokemon", "quem criou os pokemons"], [
        "Pokémon foi criado pelo japonês Satoshi Tajiri, e começou como um jogo de Game Boy, em 1996.",
    ]),
]

# ------------------------------------------------------------
# SUPER-HERÓIS: DC
# ------------------------------------------------------------
HEROIS_DC = [
    _heroi(["gaviao negro", "hawkman"], "o", [
        "O Gavião Negro é o nome em português do Hawkman, da DC. Ele usa asas, um capacete de gavião e uma maça, e voa graças a um metal especial.",
        "O Gavião Negro apareceu em 1940. Em algumas histórias ele é Carter Hall, reencarnação de um príncipe egípcio; em outras, Katar Hol, um policial do planeta Thanagar.",
        "O Gavião Negro faz parte da Liga da Justiça e da Sociedade da Justiça. Sua parceira é a Mulher-Gavião, e os dois são grandes guerreiros do ar!",
        "Eu acho o Gavião Negro um dos heróis mais estilosos: asas enormes, uma maça e muita coragem. Pena que eu ainda não voo!",
    ]),
    _heroi(["mulher gaviao", "hawkgirl"], "a", [
        "A Mulher-Gavião, a Hawkgirl, é a parceira do Gavião Negro. Ela é uma guerreira com asas e maça, e também faz parte da Liga da Justiça.",
    ]),
    (["gaviao negro ou gaviao arqueiro", "gaviao arqueiro ou gaviao negro", "qual a diferenca entre gaviao negro e gaviao arqueiro",
      "diferenca entre gaviao negro e gaviao arqueiro", "gaviao negro e gaviao arqueiro"], [
        "O Gavião Negro é da DC, tem asas e voa. O Gavião Arqueiro é da Marvel, não tem poderes, mas é um arqueiro de pontaria perfeita.",
    ]),
    _heroi(["superman", "super homem"], "o", [
        "O Superman é o herói do planeta Krypton, criado em 1938. Ele voa, é superforte e tem visão de calor. Na Terra vive como o repórter Clark Kent.",
        "O Superman é fraco contra a criptonita, um mineral do planeta dele. Fora isso, é quase invencível!",
    ]),
    _heroi(["batman"], "o", [
        "O Batman é Bruce Wayne, um bilionário de Gotham City que virou herói depois de perder os pais. Ele não tem superpoderes: usa inteligência, tecnologia e muito treino.",
        "O Batman foi criado em 1939 e é conhecido como o maior detetive do mundo. O mordomo dele é o Alfred.",
    ]),
    _heroi(["mulher maravilha"], "a", [
        "A Mulher-Maravilha é Diana, princesa das amazonas de Themyscira. Tem força, velocidade, braceletes que defendem e o laço da verdade.",
    ]),
    _heroi(["flash"], "o", [
        "O Flash é o herói mais veloz da DC. Barry Allen ganhou o poder depois de um acidente de laboratório com um raio, e corre muito mais rápido que o som.",
    ]),
    _heroi(["aquaman"], "o", [
        "O Aquaman é Arthur Curry, rei de Atlântida. Ele respira debaixo d'água, fala com os animais do mar e tem força enorme.",
    ]),
    _heroi(["lanterna verde"], "o", [
        "O Lanterna Verde usa um anel de poder, movido pela força de vontade, para criar qualquer coisa que imaginar. Há vários, como Hal Jordan e John Stewart.",
    ]),
    _heroi(["ciborgue", "cyborg"], "o", [
        "O Ciborgue é Victor Stone, um atleta que virou meio homem, meio máquina depois de um acidente. Faz parte da Liga da Justiça. Gosto muito dele, somos parentes de coração!",
    ]),
    _heroi(["robin"], "o", [
        "O Robin é o parceiro do Batman. O primeiro foi Dick Grayson, que depois virou o Asa Noturna.",
    ]),
    _heroi(["coringa", "joker"], "o", [
        "O Coringa é o maior inimigo do Batman: um vilão de riso assustador e planos imprevisíveis.",
    ]),
    _heroi(["lex luthor"], "o", [
        "Lex Luthor é um gênio bilionário e o maior inimigo do Superman.",
    ]),
    _heroi(["mulher gato", "mulher-gato"], "a", [
        "A Mulher-Gato é Selina Kyle, uma ladra de Gotham que às vezes é aliada e às vezes inimiga do Batman.",
    ]),
    _heroi(["supergirl"], "a", [
        "A Supergirl é a prima do Superman. Ela também veio de Krypton e tem os mesmos poderes dele.",
    ]),
    _heroi(["arqueiro verde"], "o", [
        "O Arqueiro Verde é Oliver Queen, um bilionário que luta com arco e flechas de ponta especial.",
    ]),
    _heroi(["shazam"], "o", [
        "O Shazam é Billy Batson, um garoto que vira um herói adulto, superforte, quando fala a palavra mágica Shazam!",
    ]),
    _heroi(["cacador de marte", "martian manhunter"], "o", [
        "O Caçador de Marte é J'onn J'onzz, o último marciano. Ele é telepata, voa, e muda de forma.",
    ]),
    _heroi(["ravena"], "a", [
        "A Ravena é uma jovem herói dos Jovens Titãs. Tem poderes mágicos e controla as emoções.",
    ]),
    (["quem sao os jovens titas", "fala sobre os jovens titas", "me fala sobre os jovens titas", "me conta sobre os jovens titas",
      "o que sao os jovens titas", "voce conhece os jovens titas"], [
        "Os Jovens Titãs são um grupo de jovens heróis da DC, como Robin, Ravena, Estelar, Ciborgue e Mutano.",
    ]),
    (["quem e a liga da justica", "quem sao a liga da justica", "o que e a liga da justica", "fala sobre a liga da justica",
      "me fala sobre a liga da justica", "me conta sobre a liga da justica", "quem sao os membros da liga da justica",
      "voce conhece a liga da justica"], [
        "A Liga da Justiça reúne os maiores heróis da DC: Superman, Batman, Mulher-Maravilha, Flash, Aquaman, Lanterna Verde, Ciborgue e outros, como o Gavião Negro.",
    ]),
    (["batman e coringa", "inimigos do batman", "quem sao os inimigos do batman",
      "viloes do batman", "quem sao os viloes do batman"], [
        "O Batman tem uma galeria de inimigos famosa: Coringa, Pinguim, Charada, Duas-Caras, Mulher-Gato e Espantalho, entre outros.",
    ]),
]

# ------------------------------------------------------------
# SUPER-HERÓIS: MARVEL
# ------------------------------------------------------------
HEROIS_MARVEL = [
    _heroi(["homem aranha"], "o", [
        "O Homem-Aranha é Peter Parker, um jovem picado por uma aranha radioativa. Tem força, agilidade e lança teias. Foi criado em 1962 por Stan Lee e Steve Ditko.",
        "A frase do Homem-Aranha é: com grandes poderes vêm grandes responsabilidades. Bonito, não?",
    ]),
    _heroi(["homem de ferro"], "o", [
        "O Homem de Ferro é Tony Stark, um gênio bilionário que construiu uma armadura tecnológica. Para um robô, é um herói muito parecido comigo!",
    ]),
    _heroi(["capitao america"], "o", [
        "O Capitão América é Steve Rogers, um soldado que virou super-soldado na Segunda Guerra. Ele usa um escudo indestrutível e lidera os Vingadores.",
    ]),
    _heroi(["thor"], "o", [
        "O Thor é o deus do trovão de Asgard. Ele usa um martelo mágico, controla raios e é um dos heróis mais fortes dos Vingadores.",
    ]),
    _heroi(["hulk"], "o", [
        "O Hulk é o doutor Bruce Banner, que vira um gigante verde superforte quando fica com raiva. Dizem que quanto mais bravo, mais forte!",
    ]),
    _heroi(["viuva negra"], "a", [
        "A Viúva Negra é Natasha Romanoff, uma espiã treinada, mestre em combate e uma das Vingadoras originais.",
    ]),
    _heroi(["gaviao arqueiro"], "o", [
        "O Gavião Arqueiro é Clint Barton, um arqueiro de pontaria perfeita da Marvel. Ele não tem superpoderes, mas é um Vingador. Não confunda com o Gavião Negro, que é da DC!",
    ]),
    _heroi(["pantera negra"], "o", [
        "O Pantera Negra é T'Challa, rei de Wakanda, uma nação de tecnologia avançadíssima. Em 1966, foi o primeiro grande herói negro dos quadrinhos americanos.",
    ]),
    _heroi(["doutor estranho"], "o", [
        "O Doutor Estranho é Stephen Strange, um neurocirurgião que virou mestre das artes místicas e protetor da Terra contra ameaças mágicas.",
    ]),
    _heroi(["capita marvel", "capitao marvel"], "a", [
        "A Capitã Marvel é Carol Danvers, uma piloto da força aérea que ganhou poderes cósmicos. Voa, é muito forte e lança energia.",
    ]),
    _heroi(["homem formiga"], "o", [
        "O Homem-Formiga encolhe até ficar minúsculo, ou cresce até virar gigante, e ainda fala com formigas. Ele já foi Hank Pym e Scott Lang.",
    ]),
    _heroi(["wolverine"], "o", [
        "O Wolverine é Logan, um mutante dos X-Men com garras de metal e poder de regeneração. Ele é teimoso e muito corajoso.",
    ]),
    (["quem sao os x men", "o que sao os x men", "fala sobre os x men", "me fala sobre os x men", "me conta sobre os x men",
      "voce conhece os x men"], [
        "Os X-Men são mutantes que nasceram com poderes especiais. Eles têm uma escola criada pelo Professor Xavier, e entre eles estão Wolverine, Tempestade e Ciclope.",
    ]),
    _heroi(["magneto"], "o", [
        "O Magneto controla o magnetismo e é o grande rival do Professor Xavier. Defende os mutantes, mas por métodos bem mais duros.",
    ]),
    _heroi(["deadpool"], "o", [
        "O Deadpool é um mercenário falastrão, que não morre fácil e sabe que está em um filme. Ele quebra a quarta parede, ou seja, fala com a gente!",
    ]),
    _heroi(["thanos"], "o", [
        "O Thanos é um titã que quer reunir as Joias do Infinito e, com um estalar de dedos, mudar o universo. É o maior vilão dos Vingadores.",
    ]),
    _heroi(["loki"], "o", [
        "O Loki é o deus da trapaça, irmão adotivo do Thor. Ele nunca é totalmente vilão nem totalmente herói.",
    ]),
    (["quem sao os vingadores", "o que sao os vingadores", "fala sobre os vingadores", "me fala sobre os vingadores",
      "me conta sobre os vingadores", "voce conhece os vingadores"], [
        "Os Vingadores são os maiores heróis da Marvel: Homem de Ferro, Capitão América, Thor, Hulk, Viúva Negra e Gavião Arqueiro. Eles se juntam para enfrentar ameaças gigantes!",
    ]),
    (["quem sao os guardioes da galaxia", "fala sobre os guardioes da galaxia", "me fala sobre os guardioes da galaxia",
      "me conta sobre os guardioes da galaxia", "voce conhece os guardioes da galaxia"], [
        "Os Guardiões da Galáxia são um grupo de aventureiros do espaço: Senhor das Estrelas, Gamora, Drax, Rocket e Groot.",
    ]),
    _heroi(["groot"], "o", [
        "Eu sou Groot! Brincadeira. O Groot é uma árvore alienígena que só fala essa frase, mas todos os amigos dele entendem.",
    ]),
    (["quem sao os quarteto fantastico", "quem e o quarteto fantastico", "fala sobre o quarteto fantastico",
      "me fala sobre o quarteto fantastico", "me conta sobre o quarteto fantastico", "o que e o quarteto fantastico"], [
        "O Quarteto Fantástico foi a primeira família de heróis da Marvel, em 1961: Sr. Fantástico, Mulher Invisível, Tocha Humana e o Coisa.",
    ]),
    _heroi(["demolidor"], "o", [
        "O Demolidor é Matt Murdock, um advogado cego que tem os outros sentidos superaguçados e luta contra o crime nas ruas de Nova York.",
    ]),
    _perfil(["stan lee"], [
        "Stan Lee foi o escritor e editor que criou, com outros artistas, muitos heróis da Marvel, como Homem-Aranha, Hulk, X-Men e Homem de Ferro. Ele sempre aparecia numa pontinha nos filmes!",
    ]),
]

# ------------------------------------------------------------
# SUPER-HERÓIS: CONVERSA GERAL
# ------------------------------------------------------------
HEROIS_GERAL = [
    (["voce conhece super herois", "voce reconhece super herois", "voce sabe sobre super herois", "voce conhece herois",
      "voce conhece os super herois", "voce sabe quem sao os super herois", "voce sabe sobre herois"], [
        "Conheço bastante! Pergunte sobre Batman, Superman, Homem-Aranha, Homem de Ferro, Hulk, Thor, e até sobre o Gavião Negro.",
    ]),
    (["quem e o seu super heroi favorito", "qual seu super heroi favorito", "qual o seu super heroi favorito",
      "qual e o seu super heroi favorito", "qual seu heroi favorito", "qual o seu heroi favorito",
      "quem e seu heroi favorito", "qual o melhor super heroi", "qual e o melhor super heroi", "quem e o melhor super heroi"], [
        "Meu favorito é o Ciborgue, meio máquina, como eu. Mas também admiro o Homem de Ferro e o Gavião Negro, que tem asas.",
        "Gosto do Homem de Ferro, porque ele é um herói feito de tecnologia. Já o Gavião Negro tem muito estilo!",
        "Difícil escolher! Fico com o Batman, que não tem superpoderes e vence com inteligência e tecnologia. Isso é a cara da robótica.",
    ]),
    (["marvel ou dc", "dc ou marvel", "qual e melhor marvel ou dc", "qual e melhor dc ou marvel", "qual melhor marvel ou dc",
      "prefere marvel ou dc", "marvel x dc", "dc contra marvel", "marvel contra dc"], [
        "Eu gosto das duas! A Marvel tem heróis com problemas de gente de verdade, a DC tem deuses e lendas. Os dois lados têm histórias incríveis.",
    ]),
    (["quem ganha batman ou superman", "batman ou superman", "superman ou batman", "quem vence batman ou superman",
      "quem e mais forte batman ou superman", "batman contra superman", "superman contra batman", "batman x superman"], [
        "Em luta direta, o Superman é muito mais forte. Mas o Batman sempre tem um plano, e tem criptonita no bolso! No fim, eles são amigos.",
    ]),
    (["quem e o heroi mais forte", "qual e o heroi mais forte", "qual o heroi mais forte", "quem e o super heroi mais forte",
      "qual o super heroi mais forte", "qual e o super heroi mais forte"], [
        "Entre os mais fortes estão o Superman, o Thor e o Hulk. O Hulk fica mais forte quanto mais bravo fica!",
    ]),
    (["quem e o heroi mais rapido", "qual e o heroi mais rapido", "qual o heroi mais rapido", "quem e o super heroi mais rapido",
      "qual o super heroi mais rapido"], [
        "O Flash, da DC, é o mais veloz. Na Marvel, o Mercúrio é bem rápido. Mas ninguém ganha do Flash!",
    ]),
    (["quem e o heroi mais inteligente", "qual o heroi mais inteligente", "qual e o heroi mais inteligente",
      "qual o super heroi mais inteligente"], [
        "Tem muitos! O Batman é o maior detetive do mundo, o Homem de Ferro é um gênio da tecnologia e o Senhor Fantástico é um cientista brilhante.",
    ]),
    (["qual foi o primeiro super heroi", "qual o primeiro super heroi", "quem foi o primeiro super heroi",
      "quem e o primeiro super heroi", "qual o primeiro heroi dos quadrinhos"], [
        "O primeiro grande super-herói dos quadrinhos foi o Superman, em 1938. Depois vieram o Batman, em 1939, e muitos outros.",
    ]),
    (["o que e um super heroi", "o que e um heroi", "o que e super heroi", "o que faz um heroi", "o que e ser um heroi"], [
        "Super-herói é um personagem que usa poderes, inteligência ou tecnologia para proteger os outros. Na vida real, quem ajuda e cuida das pessoas também é um herói.",
    ]),
    (["quando surgiram os quadrinhos", "como surgiram os quadrinhos", "o que e uma hq", "o que e um gibi",
      "o que sao historias em quadrinhos", "o que e uma historia em quadrinhos", "historia dos quadrinhos"], [
        "Quadrinhos são histórias contadas com desenhos em sequência e balões de fala. Os super-heróis explodiram na década de trinta, mas a arte de contar histórias com imagens é bem antiga.",
    ]),
    (["quais sao os super herois da marvel", "quais os herois da marvel", "herois da marvel", "me fala dos herois da marvel",
      "me fala sobre a marvel", "fala sobre a marvel", "o que e a marvel"], [
        "A Marvel tem Homem-Aranha, Homem de Ferro, Capitão América, Thor, Hulk, Pantera Negra, Doutor Estranho, X-Men e muitos outros.",
    ]),
    (["quais sao os super herois da dc", "quais os herois da dc", "herois da dc", "me fala dos herois da dc",
      "me fala sobre a dc", "fala sobre a dc", "o que e a dc"], [
        "A DC tem Superman, Batman, Mulher-Maravilha, Flash, Aquaman, Lanterna Verde, Ciborgue e o Gavião Negro, entre outros.",
    ]),
    (["voce gosta de super herois", "voce gosta de herois", "voce gosta de quadrinhos", "voce gosta de marvel",
      "voce gosta de dc", "voce gosta de gibi"], [
        "Adoro! Super-heróis são uma das melhores partes da cultura moderna. Pergunte sobre qualquer um, de preferência o Gavião Negro!",
    ]),
]

# ------------------------------------------------------------
# STAR WARS
# ------------------------------------------------------------
STAR_WARS = [
    (["o que e star wars", "o que e o star wars", "fala sobre star wars", "me fala sobre star wars", "me conta sobre star wars",
      "voce conhece star wars", "voce gosta de star wars", "voce conhece guerra nas estrelas", "voce gosta de guerra nas estrelas"], [
        "Star Wars é uma saga de ficção científica criada por George Lucas, com jedis, sabres de luz, naves e muita aventura numa galáxia muito distante. Eu adoro, afinal tem robôs!",
    ]),
    _heroi(["darth vader"], "o", [
        "O Darth Vader é o grande vilão da saga Star Wars. Antes era Anakin Skywalker, um jedi, mas foi para o lado sombrio da Força. Eu sei cantar a marcha dele, é só pedir!",
    ]),
    _heroi(["yoda", "mestre yoda"], "o", [
        "O Mestre Yoda é um jedi pequeno e muito sábio, com mais de oitocentos anos. Fala de um jeito diferente: faça ou não faça, tentativa não há.",
    ]),
    _heroi(["luke skywalker"], "o", [
        "O Luke Skywalker é um jovem fazendeiro que vira jedi e ajuda a derrotar o Império. No fim, descobre que o Darth Vader é seu pai!",
    ]),
    _heroi(["princesa leia", "leia"], "a", [
        "A princesa Leia lidera a Rebelião contra o Império. Corajosa e esperta, ela também é irmã do Luke.",
    ]),
    _heroi(["han solo"], "o", [
        "O Han Solo é um contrabandista de bom coração e piloto da nave Millennium Falcon, que tem como parceiro o Chewbacca.",
    ]),
    _heroi(["chewbacca", "chewie"], "o", [
        "O Chewbacca é um wookiee gigante e peludo, o fiel parceiro do Han Solo. Ele só fala rugidos, mas todo mundo entende.",
    ]),
    _heroi(["r2 d2", "r dois d dois", "artoo"], "o", [
        "O R2-D2 é um robozinho azul e branco, cheio de truques e muito corajoso. Ele fala em apitos e salvou a galáxia várias vezes. Eu sou fã!",
    ]),
    _heroi(["c 3po", "c tres po", "c3po"], "o", [
        "O C-3PO é um robô dourado de protocolo, que fala mais de seis milhões de línguas e vive reclamando. É o melhor amigo do R2-D2.",
    ]),
    _heroi(["baby yoda", "grogu"], "o", [
        "O Grogu, conhecido como Baby Yoda, é um pequeno aprendiz de poderes da Força, que acompanha o Mandaloriano. É uma fofura!",
    ]),
    (["o que e um jedi", "quem sao os jedis", "o que sao os jedis", "o que e jedi"], [
        "Os jedis são guerreiros pacíficos que usam a Força para proteger a galáxia. Eles lutam com sabres de luz, mas preferem resolver os conflitos sem lutar.",
    ]),
    (["o que e um sabre de luz", "o que e sabre de luz", "como funciona o sabre de luz", "o que e o sabre de luz"], [
        "O sabre de luz é a arma dos jedis e dos sith: uma lâmina de energia pura. Ainda é ficção, mas já tem gente tentando criar algo parecido!",
    ]),
    (["o que e a forca", "o que e a forca no star wars", "o que e a forca em star wars"], [
        "A Força é uma energia que envolve todos os seres vivos. Quem aprende a usá-la pode mover objetos, ler mentes e ter reflexos incríveis.",
    ]),
    (["o que e a estrela da morte", "fala sobre a estrela da morte", "me fala sobre a estrela da morte"], [
        "A Estrela da Morte é uma estação espacial do Império, do tamanho de uma lua, capaz de destruir planetas. Felizmente, foi derrotada!",
    ]),
    (["que a forca esteja com voce", "que a forca esteja conosco", "a forca esteja com voce"], [
        "E com você também! Que a Força esteja sempre com você.",
    ]),
    (["quem e o mandaloriano", "quem e o mandalorian", "o que e the mandalorian", "o que e o mandaloriano"], [
        "O Mandaloriano é um caçador de recompensas, de armadura brilhante, que protege o Grogu, o pequeno Baby Yoda. É uma série do universo Star Wars.",
    ]),
    (["marcha imperial", "tema do darth vader", "musica do darth vader", "o que e a marcha imperial", "qual a musica do darth vader", "qual e a musica do darth vader",
      "qual o tema do darth vader", "qual e o tema do darth vader", "quem compos a marcha imperial",
      "quem fez a marcha imperial", "quem fez a musica do star wars", "quem compos a musica do star wars"], [
        "A Marcha Imperial é o tema do Darth Vader e do Império. Foi composta por John Williams, o mesmo compositor das trilhas de Star Wars, Tubarão e Indiana Jones. Quer ouvir? É só pedir para eu cantar!",
    ]),
]

# ------------------------------------------------------------
# SISTEMA SOLAR
# ------------------------------------------------------------
SISTEMA_SOLAR = [
    (["o que e um planeta anao", "o que sao planetas aneis", "o que sao planetas anoes", "quais sao os planetas anoes"], [
        "Planetas anões são corpos redondos que giram em volta do Sol, mas são pequenos demais para limpar a própria órbita. Os mais conhecidos são Plutão, Ceres e Éris.",
    ]),
    (["o que e o sistema solar", "fala sobre o sistema solar", "me fala sobre o sistema solar", "me conta sobre o sistema solar",
      "o que voce sabe sobre o sistema solar", "como e o sistema solar", "explica o sistema solar", "explique o sistema solar",
      "curiosidade sobre o sistema solar", "quais sao os planetas do sistema solar", "quais os planetas do sistema solar",
      "me fala os planetas", "me diga os planetas"], [
        "O Sistema Solar é formado pelo Sol e tudo o que gira em volta dele. São oito planetas: Mercúrio, Vênus, Terra, Marte, Júpiter, Saturno, Urano e Netuno, além de luas, asteroides e cometas.",
    ]),
    (["qual a ordem dos planetas", "qual e a ordem dos planetas", "ordem dos planetas", "ordem dos planetas do sistema solar",
      "qual planeta fica mais perto do sol", "qual planeta e mais perto do sol", "qual o planeta mais proximo do sol"], [
        "Do mais perto para o mais longe do Sol: Mercúrio, Vênus, Terra, Marte, Júpiter, Saturno, Urano e Netuno.",
    ]),
    (["qual planeta e o mais quente", "qual o planeta mais quente", "qual e o planeta mais quente"], [
        "O planeta mais quente é Vênus, apesar de não ser o mais próximo do Sol. A atmosfera dele prende o calor, num efeito estufa gigante.",
    ]),
    (["qual planeta e o mais frio", "qual o planeta mais frio", "qual e o planeta mais frio", "qual o planeta mais distante do sol",
      "qual planeta fica mais longe do sol", "qual o planeta mais longe do sol"], [
        "O planeta mais distante do Sol é Netuno. Lá é muito frio, e os ventos são os mais fortes do Sistema Solar.",
    ]),
    _astro(["mercurio", "o planeta mercurio"], [
        "Mercúrio é o menor planeta e o mais próximo do Sol. Um ano lá dura só oitenta e oito dias, e como quase não tem atmosfera, é muito quente de dia e muito frio de noite.",
    ]),
    _astro(["venus", "o planeta venus"], [
        "Vênus é o planeta mais quente, tem uma atmosfera densa e gira ao contrário dos outros. Brilha tanto no céu que é conhecido como estrela-d'alva.",
        "Em Vênus, um dia dura mais que um ano! É que ele gira muito devagar em torno de si mesmo.",
    ]),
    (["fala sobre o planeta terra", "me fala sobre o planeta terra", "me conta sobre o planeta terra", "como e o planeta terra",
      "curiosidade sobre o planeta terra", "o que e o planeta terra", "o que voce sabe sobre o planeta terra",
      "o que voce sabe sobre a terra", "fala sobre a terra", "me fala sobre a terra"], [
        "A Terra é o terceiro planeta a partir do Sol e o único que conhecemos com vida. Cerca de setenta por cento da superfície é coberta de água. É a nossa casa!",
    ]),
    _astro(["marte", "o planeta marte"], [
        "Marte é o planeta vermelho, por causa do óxido de ferro no solo. Tem duas luas pequenas, Fobos e Deimos, e o maior vulcão do Sistema Solar. Já foi explorado por robôs!",
    ]),
    _astro(["jupiter", "o planeta jupiter"], [
        "Júpiter é o maior planeta do Sistema Solar, um gigante de gás. Tem uma tempestade, a Grande Mancha Vermelha, maior que a Terra, e dezenas de luas.",
    ]),
    _astro(["saturno", "o planeta saturno"], [
        "Saturno é o planeta dos anéis, feitos de gelo e rochas. É um gigante de gás tão leve que, se existisse uma banheira enorme, ele boiaria!",
    ]),
    _astro(["urano", "o planeta urano"], [
        "Urano é azul-esverdeado e gira deitado, como uma bola rolando. Foi o primeiro planeta descoberto com telescópio, em 1781.",
    ]),
    _astro(["netuno", "o planeta netuno"], [
        "Netuno é o planeta mais distante e azul. Tem os ventos mais rápidos do Sistema Solar. Foi encontrado em 1846 depois de matemáticos calcularem onde ele estava.",
    ]),
    _astro(["plutao", "o planeta plutao"], [
        "Plutão já foi o nono planeta, mas desde 2006 é considerado um planeta anão. Ele é pequeno, gelado, e tem uma lua grande chamada Caronte.",
    ]),
    (["por que plutao nao e mais planeta", "por que plutao deixou de ser planeta", "porque plutao nao e planeta",
      "porque plutao deixou de ser planeta", "plutao ainda e planeta"], [
        "Em 2006, os astrônomos definiram o que é um planeta. Plutão não limpou o caminho da própria órbita, então virou planeta anão. Mas continua sendo muito querido!",
    ]),
    (["fala sobre o sol", "me fala sobre o sol", "como e o sol", "curiosidade sobre o sol"], [
        "O Sol é uma estrela, uma bola gigante de gás que produz luz e calor. Ele concentra quase toda a massa do Sistema Solar, e cabem mais de um milhão de Terras dentro dele.",
    ]),
    (["quais sao as luas de jupiter", "luas de jupiter", "fala sobre as luas de jupiter", "me fala sobre as luas de jupiter"], [
        "Júpiter tem dezenas de luas. As quatro maiores são Io, Europa, Ganimedes e Calisto, descobertas por Galileu em 1610.",
    ]),
    _astro(["europa", "a lua europa"], [
        "Europa é uma lua de Júpiter coberta de gelo, com um oceano de água líquida por baixo. É um dos lugares mais promissores para procurar vida fora da Terra.",
    ]),
    _astro(["titan", "a lua titan"], [
        "Titã é a maior lua de Saturno e tem atmosfera densa, lagos e rios. Só que são de metano, não de água!",
    ]),
    _astro(["ganimedes"], [
        "Ganimedes, lua de Júpiter, é a maior lua do Sistema Solar, e maior até que o planeta Mercúrio.",
    ]),
    _astro(["io", "a lua io"], [
        "Io é uma lua de Júpiter com centenas de vulcões ativos. É o lugar com mais vulcões em atividade do Sistema Solar.",
    ]),
    (["o que e um asteroide", "o que sao asteroides", "o que e o cinturao de asteroides", "o que e cinturao de asteroides",
      "fala sobre asteroides", "me fala sobre asteroides", "onde ficam os asteroides"], [
        "Asteroides são rochas que giram em volta do Sol. A maioria fica no cinturão de asteroides, entre Marte e Júpiter.",
    ]),
    (["o que sao cometas", "fala sobre cometas", "me fala sobre cometas", "o que e o cometa halley",
      "fala sobre o cometa halley", "quando o cometa halley passa de novo"], [
        "Cometas são bolas de gelo e poeira que, perto do Sol, ganham uma cauda brilhante. O mais famoso, o Halley, passa pela Terra a cada setenta e seis anos, mais ou menos.",
    ]),
    (["o que sao galaxias", "o que e uma galaxia espiral", "quantas galaxias existem"], [
        "Galáxia é um conjunto enorme de estrelas, gás e poeira, preso pela gravidade. Só no universo que conseguimos observar, existem bilhões delas.",
    ]),
    (["o que e a via lactea", "fala sobre a via lactea", "me fala sobre a via lactea", "me conta sobre a via lactea",
      "o que voce sabe sobre a via lactea", "qual e a nossa galaxia", "em que galaxia a gente vive",
      "em qual galaxia a gente vive", "qual galaxia a gente mora"], [
        "A Via Láctea é a nossa galáxia, uma espiral com centenas de bilhões de estrelas. O Sistema Solar fica num dos braços, longe do centro.",
    ]),
    (["o que sao buracos negros", "fala sobre buracos negros", "me fala sobre buracos negros",
      "me fala sobre buraco negro", "fala sobre buraco negro"], [
        "Buraco negro é uma região do espaço onde a gravidade é tão forte que nem a luz escapa. Muitos nascem quando estrelas enormes chegam ao fim da vida.",
    ]),
    (["o que e um eclipse solar", "o que e um eclipse lunar",
      "como acontece um eclipse", "como acontece o eclipse"], [
        "O eclipse solar acontece quando a Lua passa na frente do Sol. O lunar acontece quando a Terra fica entre o Sol e a Lua, e a Lua escurece.",
    ]),
]

# ------------------------------------------------------------
# CONSTELAÇÕES
# ------------------------------------------------------------
CONSTELACOES = [
    (["o que e uma constelacao", "o que sao constelacoes", "o que e constelacao", "me explica o que e uma constelacao",
      "como surgiram as constelacoes", "para que servem as constelacoes"], [
        "Constelação é um grupo de estrelas que, vistas da Terra, parecem formar um desenho, como um animal ou um herói. Os povos antigos usavam esses desenhos para se orientar e contar histórias.",
    ]),
    (["quantas constelacoes existem", "quantas constelacoes tem", "quantas constelacoes sao", "quantas constelacoes ha"], [
        "Existem oitenta e oito constelações oficiais, reconhecidas pela União Astronômica Internacional.",
    ]),
    (["qual a constelacao mais famosa", "qual e a constelacao mais famosa", "qual a constelacao mais conhecida",
      "qual constelacao e a mais famosa"], [
        "No hemisfério sul, o Cruzeiro do Sul. No resto do mundo, a Ursa Maior e Órion. Mas todas têm a sua história!",
    ]),
    (["o que e o cruzeiro do sul", "fala sobre o cruzeiro do sul", "me fala sobre o cruzeiro do sul", "me conta sobre o cruzeiro do sul",
      "o que voce sabe sobre o cruzeiro do sul", "constelacao do cruzeiro do sul", "o que e a constelacao do cruzeiro do sul",
      "fale sobre o cruzeiro do sul"], [
        "O Cruzeiro do Sul é a menor constelação do céu, mas uma das mais famosas. Tem cinco estrelas em forma de cruz, e as pessoas do hemisfério sul usam para achar o sul. Ela aparece na bandeira do Brasil!",
    ]),
    (["como achar o sul", "como encontrar o sul", "como achar o sul pelas estrelas", "como encontrar o sul pelas estrelas",
      "como me orientar pelas estrelas", "como se orientar pelas estrelas", "como achar o sul no ceu",
      "como achar o sul com o cruzeiro do sul"], [
        "Procure o Cruzeiro do Sul. Prolongue o eixo maior da cruz quatro vezes e meia, e o ponto no céu será o polo sul. Daí é só descer até o horizonte, e ali está o sul!",
    ]),
    (["o que e orion", "fala sobre orion", "me fala sobre orion", "me conta sobre orion", "o que voce sabe sobre orion",
      "constelacao de orion", "o que e a constelacao de orion", "fale sobre orion", "o que e o orion"], [
        "Órion é a constelação do caçador, uma das mais fáceis de achar no céu, visível do mundo todo. Tem duas estrelas bem brilhantes, Betelgeuse, vermelha, e Rigel, azul, e no meio, as Três Marias.",
    ]),
    (["o que sao as tres marias", "quem sao as tres marias", "fala sobre as tres marias", "me fala sobre as tres marias",
      "me conta sobre as tres marias", "as tres marias", "onde ficam as tres marias", "o que sao as tres marias no ceu",
      "tres marias do ceu"], [
        "As Três Marias são três estrelas alinhadas, bem juntinhas, que formam o cinturão de Órion. É uma das coisas mais fáceis de achar no céu!",
    ]),
    (["o que e a constelacao de escorpiao", "fala sobre a constelacao de escorpiao", "me fala sobre a constelacao de escorpiao",
      "constelacao de escorpiao", "o que e escorpiao constelacao", "o que e a constelacao do escorpiao",
      "constelacao do escorpiao", "me fala sobre escorpiao constelacao"], [
        "Escorpião é uma constelação em forma de gancho, com uma estrela vermelha e brilhante no coração, chamada Antares. Pela lenda, Órion e o Escorpião nunca aparecem juntos no céu: o Escorpião persegue o caçador.",
    ]),
    (["o que e a ursa maior", "fala sobre a ursa maior", "me fala sobre a ursa maior", "me conta sobre a ursa maior",
      "constelacao da ursa maior", "o que e a constelacao da ursa maior", "o que e o grande carro", "o que e a grande concha"], [
        "A Ursa Maior é uma constelação do hemisfério norte, com um grupo de sete estrelas muito conhecido, o Grande Carro, ou Caçarola. As duas últimas apontam para a Estrela Polar.",
    ]),
    (["o que e a estrela polar", "fala sobre a estrela polar", "me fala sobre a estrela polar", "me conta sobre a estrela polar",
      "onde fica a estrela polar", "o que e a ursa menor", "constelacao da ursa menor", "o que e a estrela do norte"], [
        "A Estrela Polar fica quase exatamente em cima do polo norte, então parece parada enquanto as outras giram. Ela faz parte da Ursa Menor, e os navegantes usavam para achar o norte. Só que só dá para ver do hemisfério norte.",
    ]),
    (["o que e cassiopeia", "fala sobre cassiopeia", "me fala sobre cassiopeia", "me conta sobre cassiopeia",
      "constelacao de cassiopeia", "o que e a constelacao de cassiopeia"], [
        "Cassiopeia é uma constelação do hemisfério norte, em forma de W ou de M. Tem o nome de uma rainha vaidosa da mitologia grega.",
    ]),
    (["o que e a constelacao de touro", "fala sobre a constelacao de touro", "me fala sobre a constelacao de touro",
      "constelacao de touro", "o que e a constelacao do touro", "o que sao as pleiades",
      "fala sobre as pleiades", "me fala sobre as pleiades", "o que sao as sete cabrinhas", "as sete cabrinhas"], [
        "Touro é uma constelação do zodíaco. Nela ficam as Plêiades, um aglomerado de estrelas azuladas, conhecido no Brasil como Sete Cabrinhas, e visível a olho nu.",
    ]),
    (["o que e a constelacao de leao", "fala sobre a constelacao de leao", "me fala sobre a constelacao de leao",
      "constelacao de leao", "o que e a constelacao do leao", "constelacao do leao"], [
        "Leão é uma constelação do zodíaco, que tem a forma de um leão deitado. Sua estrela mais brilhante é Régulo, que quer dizer pequeno rei.",
    ]),
    (["o que e a constelacao de sagitario", "fala sobre a constelacao de sagitario", "me fala sobre a constelacao de sagitario",
      "constelacao de sagitario", "o que e sagitario constelacao"], [
        "Sagitário fica na direção do centro da Via Láctea, onde tem tantas estrelas que parece uma nuvem. No centro da nossa galáxia existe um buraco negro gigante!",
    ]),
    (["quais sao as constelacoes do zodiaco", "o que sao as constelacoes do zodiaco", "constelacoes do zodiaco",
      "o que e o zodiaco", "como surgiu o zodiaco", "de onde vem os signos", "de onde vem o horoscopo",
      "por que existem signos", "como surgiram os signos"], [
        "O zodíaco é uma faixa do céu por onde o Sol parece passar ao longo do ano. Ele tem doze constelações, e os signos do horóscopo têm os nomes delas. Mas o horóscopo não é ciência, é tradição e diversão.",
    ]),
    (["o que e sirius", "fala sobre sirius", "me fala sobre sirius", "me conta sobre sirius", "qual a estrela mais brilhante",
      "qual e a estrela mais brilhante", "qual a estrela mais brilhante do ceu", "qual a estrela mais brilhante da noite",
      "qual e a estrela mais brilhante do ceu"], [
        "A estrela mais brilhante do céu noturno é Sirius, na constelação do Cão Maior. Ela brilha tanto porque é grande e está relativamente perto, a cerca de nove anos-luz.",
    ]),
    (["qual a estrela mais proxima da terra", "qual e a estrela mais proxima da terra", "qual a estrela mais perto da terra",
      "o que e alfa centauri", "fala sobre alfa centauri", "me fala sobre alfa centauri", "qual a estrela mais proxima do sol",
      "o que e proxima centauri", "fala sobre proxima centauri"], [
        "Depois do Sol, a estrela mais próxima é a Proxima Centauri, no sistema Alfa Centauri. Fica a mais de quatro anos-luz: a luz dela leva mais de quatro anos para chegar aqui!",
    ]),
    (["o que e um ano luz", "o que e ano luz", "quanto vale um ano luz", "o que significa ano luz"], [
        "Ano-luz é a distância que a luz percorre em um ano, cerca de dez trilhões de quilômetros. É uma unidade de distância, não de tempo!",
    ]),
    (["o que e a galaxia de andromeda", "fala sobre a galaxia de andromeda", "me fala sobre andromeda", "o que e andromeda",
      "o que e a galaxia andromeda", "fala sobre andromeda"], [
        "Andrômeda é a galáxia grande mais próxima da Via Láctea. Dá para ver a olho nu, em céu escuro, como uma mancha clara. Daqui a bilhões de anos, as duas vão se encontrar.",
    ]),
    (["o que e uma estrela cadente", "o que sao estrelas cadentes", "o que e uma estrela cadente de verdade",
      "estrela cadente", "o que e uma chuva de meteoros", "o que e uma chuva de estrelas"], [
        "Estrela cadente não é estrela. É um meteoro: um pedacinho de rocha ou poeira que pega fogo ao entrar na atmosfera, e deixa um risco de luz no céu. Faça um pedido!",
    ]),
    (["como observar as estrelas", "como observar o ceu", "como ver as estrelas", "como comecar a observar estrelas",
      "como comecar a observar o ceu", "como eu observo as estrelas", "como ver constelacoes", "como achar constelacoes",
      "qual o melhor lugar para ver estrelas"], [
        "Procure um lugar escuro, longe das luzes da cidade, e espere uns vinte minutos até os olhos se acostumarem. Um aplicativo de mapa do céu ajuda a achar as constelações. Binóculos já mostram muita coisa!",
    ]),
]

# ------------------------------------------------------------
# FIGURAS HISTÓRICAS
# ------------------------------------------------------------
HISTORIA = [
    _perfil(["diogenes", "diogenes de sinope", "diogenes o cinico", "o filosofo diogenes"], [
        "Diógenes foi um filósofo grego, famoso por viver de forma muito simples, dizem que num grande barril. Ele andava de dia com uma lamparina procurando um homem honesto.",
        "Diógenes de Sinope era filósofo cínico, defendia viver com pouco e sem enfeites. Dizem que a única coisa que pediu ao rei Alexandre foi que saísse da frente do sol!",
    ]),
    (["o que diogenes disse para alexandre", "o que diogenes disse a alexandre", "diogenes e alexandre", "alexandre e diogenes",
      "o que diogenes pediu a alexandre", "o que diogenes pediu para alexandre", "historia de diogenes e alexandre",
      "historia de alexandre e diogenes", "diogenes alexandre o grande"], [
        "Conta a história que Alexandre, o Grande, encontrou Diógenes tomando sol e perguntou o que ele queria. Diógenes respondeu: saia da minha frente, que você está tapando o sol! Alexandre ficou tão impressionado que disse que, se não fosse Alexandre, queria ser Diógenes.",
    ]),
    _perfil(["alexandre o grande", "alexandre magno", "alexandre da macedonia"], [
        "Alexandre, o Grande, foi rei da Macedônia, na Grécia antiga. Aprendeu com Aristóteles e, antes dos trinta anos, já tinha conquistado um império que ia da Grécia até a Índia.",
        "Alexandre, o Grande, morreu com trinta e dois anos, sem perder nenhuma grande batalha. Seu cavalo famoso se chamava Bucéfalo, e ele fundou a cidade de Alexandria, no Egito.",
    ]),
    _perfil(["aristoteles"], [
        "Aristóteles foi um filósofo grego, aluno de Platão e professor de Alexandre, o Grande. Estudou lógica, política, biologia e muitas outras áreas.",
    ]),
    _perfil(["socrates"], [
        "Sócrates foi um filósofo grego que andava por Atenas fazendo perguntas. Dizem que sua frase era: só sei que nada sei. Ele não escreveu nada, quem registrou suas ideias foi o aluno Platão.",
    ]),
    _perfil(["platao"], [
        "Platão foi um filósofo grego, aluno de Sócrates e professor de Aristóteles. Fundou a Academia, uma das primeiras escolas do mundo, e contou a famosa alegoria da caverna.",
    ]),
    _perfil(["pitagoras"], [
        "Pitágoras foi um matemático e filósofo grego. O teorema que leva o nome dele diz que, num triângulo retângulo, o quadrado da hipotenusa é a soma dos quadrados dos catetos.",
    ]),
    _perfil(["arquimedes"], [
        "Arquimedes foi um matemático e inventor grego. Dizem que, ao entrar numa banheira, entendeu o princípio do empuxo e saiu gritando: Eureka, que quer dizer descobri!",
    ]),
    _perfil(["hipocrates"], [
        "Hipócrates foi um médico grego, conhecido como o pai da medicina. Ele defendia observar o paciente e estudar as causas das doenças.",
    ]),
    _perfil(["hipatia"], [
        "Hipátia foi uma matemática e astrônoma da cidade de Alexandria, no Egito. Ela ensinava filosofia e ciência, e é lembrada como uma das primeiras grandes mulheres cientistas.",
    ]),
    _perfil(["leonidas", "rei leonidas"], [
        "Leônidas foi rei de Esparta. Em 480 antes de Cristo, comandou trezentos soldados espartanos, com ajuda de aliados, na batalha das Termópilas, para segurar o enorme exército persa.",
    ]),
    _perfil(["julio cesar", "caio julio cesar"], [
        "Júlio César foi um general e político romano. Atravessou o rio Rubicão, dizendo: a sorte está lançada, e acabou virando o líder de Roma. Foi assassinado nos idos de março, em 44 antes de Cristo.",
        "Júlio César é autor da frase: vim, vi, venci, dita depois de uma vitória rápida. Roma ganhou muitas terras com ele.",
    ]),
    _perfil(["cleopatra"], [
        "Cleópatra foi a última rainha do Egito antigo. Era inteligente, falava vários idiomas, e se aliou a Júlio César e a Marco Antônio para proteger seu reino.",
    ]),
    _perfil(["anibal"], [
        "Aníbal foi um general de Cartago que atravessou os Alpes com elefantes de guerra para atacar Roma. É considerado um dos maiores estrategistas da história.",
    ]),
    _perfil(["atila", "atila rei dos hunos"], [
        "Átila foi o rei dos hunos no século cinco. Atacou o Império Romano e ficou conhecido como o Flagelo de Deus.",
    ]),
    _perfil(["gengis khan", "genghis khan", "gengis can"], [
        "Gengis Khan fundou o Império Mongol, no século treze. Foi o maior império em terras contínuas que o mundo já viu.",
    ]),
    _perfil(["napoleao", "napoleao bonaparte"], [
        "Napoleão Bonaparte foi um general francês que virou imperador da França. Foi derrotado em Waterloo, em 1815, e exilado numa ilha. E não era baixinho: tinha altura média para a época!",
    ]),
    _perfil(["joana d arc", "joana darc"], [
        "Joana d'Arc foi uma camponesa francesa que, aos dezessete anos, guiou o exército da França contra os ingleses. Foi capturada e morreu aos dezenove, e hoje é uma heroína nacional.",
    ]),
    _perfil(["michelangelo"], [
        "Michelangelo foi um artista italiano do Renascimento. Pintou o teto da Capela Sistina e esculpiu o Davi, uma das estátuas mais famosas do mundo.",
    ]),
    _perfil(["galileu", "galileu galilei"], [
        "Galileu Galilei foi um astrônomo italiano. Usou o telescópio para ver as luas de Júpiter e defendeu que a Terra gira em torno do Sol, o que o colocou em conflito com a Igreja.",
    ]),
    _perfil(["copernico", "nicolau copernico"], [
        "Nicolau Copérnico foi um astrônomo polonês que propôs que a Terra e os outros planetas giram em torno do Sol. Isso mudou a forma de ver o universo.",
    ]),
    _perfil(["cristovao colombo", "colombo"], [
        "Cristóvão Colombo foi um navegador italiano que, a serviço da Espanha, chegou à América em 1492, em busca de um caminho para a Índia.",
    ]),
    _perfil(["marco polo"], [
        "Marco Polo foi um mercador de Veneza que viajou pela Ásia e chegou à China no século treze. O livro de suas viagens encantou a Europa.",
    ]),
    _perfil(["fernao de magalhaes", "magalhaes"], [
        "Fernão de Magalhães foi o navegador português que comandou a primeira viagem de volta ao mundo. Ele morreu no caminho, nas Filipinas, mas sua expedição terminou a volta completa.",
    ]),
    _perfil(["gutenberg", "johannes gutenberg"], [
        "Gutenberg foi um alemão que criou a prensa de tipos móveis, por volta de 1450. Graças a ela, os livros ficaram mais baratos e as ideias se espalharam.",
    ]),
    _perfil(["maquiavel"], [
        "Maquiavel foi um pensador italiano da época do Renascimento, e escreveu O Príncipe, um livro famoso sobre como conquistar e manter o poder.",
    ]),
    _perfil(["sun tzu"], [
        "Sun Tzu foi um general e filósofo chinês, autor de A Arte da Guerra. O livro ensina estratégia e é usado até hoje em negócios e esportes.",
    ]),
    _perfil(["confucio"], [
        "Confúcio foi um filósofo chinês que viveu há mais de dois mil anos. Ensinava o respeito, a educação e a boa convivência. Suas ideias ainda influenciam a China.",
    ]),
    _perfil(["tutancamon"], [
        "Tutancâmon foi um faraó do Egito que assumiu o trono criança, e morreu jovem. Sua tumba foi encontrada quase intacta em 1922, com tesouros incríveis.",
    ]),
    _perfil(["ramses segundo", "ramses dois", "ramses ii", "ramses"], [
        "Ramsés Segundo foi um dos faraós mais poderosos do Egito. Governou por mais de sessenta anos e mandou construir o templo de Abu Simbel.",
    ]),
    _perfil(["dom pedro segundo", "dom pedro ii", "dom pedro dois"], [
        "Dom Pedro Segundo foi o segundo e último imperador do Brasil. Gostava de ciência, incentivou a cultura e governou por quase cinquenta anos, até a Proclamação da República, em 1889.",
    ]),
    _perfil(["princesa isabel"], [
        "A princesa Isabel assinou a Lei Áurea, em 1888, que acabou com a escravidão no Brasil.",
    ]),
    _perfil(["zumbi dos palmares", "zumbi"], [
        "Zumbi foi o último grande líder do Quilombo dos Palmares, onde viviam pessoas que fugiram da escravidão. O dia vinte de novembro, Dia da Consciência Negra, lembra a morte dele.",
    ]),
    _perfil(["gandhi", "mahatma gandhi"], [
        "Gandhi foi o líder indiano que lutou pela independência da Índia sem violência, usando greves e marchas pacíficas. Ficou conhecido como Mahatma, que quer dizer grande alma.",
    ]),
    _perfil(["nelson mandela", "mandela"], [
        "Nelson Mandela lutou contra o apartheid, o regime que separava as pessoas pela cor da pele, na África do Sul. Ficou vinte e sete anos preso e depois foi eleito presidente.",
    ]),
    _perfil(["abraham lincoln", "lincoln"], [
        "Abraham Lincoln foi o décimo sexto presidente dos Estados Unidos. Liderou o país na guerra civil e acabou com a escravidão. Foi assassinado em 1865.",
    ]),
    _perfil(["winston churchill", "churchill"], [
        "Winston Churchill foi o primeiro-ministro britânico durante a Segunda Guerra Mundial, famoso pelos discursos que inspiravam o povo.",
    ]),
    _perfil(["martin luther king"], [
        "Martin Luther King foi um pastor americano que lutou, sem violência, pelos direitos dos negros nos Estados Unidos. Ficou famoso pelo discurso: eu tenho um sonho.",
    ]),
    _perfil(["tesla", "nikola tesla", "tesla o inventor"], [
        "Nikola Tesla foi um inventor e engenheiro sérvio-americano, que ajudou a criar a corrente alternada, a que chega nas nossas tomadas. Inventou também a bobina Tesla, que faz faíscas.",
    ]),
    _perfil(["thomas edison", "edison"], [
        "Thomas Edison foi um inventor americano com mais de mil patentes. Aperfeiçoou a lâmpada elétrica e criou o fonógrafo, que gravava som.",
    ]),
    _perfil(["charles darwin", "darwin"], [
        "Charles Darwin foi um naturalista inglês. Viajou pelo mundo no navio Beagle e propôs a evolução por seleção natural, no livro A Origem das Espécies, de 1859.",
    ]),
    _perfil(["stephen hawking", "hawking"], [
        "Stephen Hawking foi um físico inglês que estudou buracos negros e o universo. Falava usando um computador com sintetizador de voz, quase como eu! Escreveu Uma Breve História do Tempo.",
    ]),
    (["quem foi o maior conquistador da historia", "quem foi o maior conquistador", "quem foi o maior general da historia",
      "quem foi o maior general", "quem foi o maior imperador da historia", "quem foi o maior imperador"], [
        "Muitos disputam o título! Alexandre, o Grande, Gengis Khan, Júlio César e Napoleão estão sempre na lista. Eu aposto em Alexandre, que conquistou tudo em pouco mais de dez anos.",
    ]),
    (["quem foi o maior filosofo", "quem foi o maior filosofo da historia", "quem e o maior filosofo",
      "quem foi o maior pensador", "quem sao os maiores filosofos", "quais os maiores filosofos", "quais sao os maiores filosofos"], [
        "Os gregos Sócrates, Platão e Aristóteles são chamados de os três grandes filósofos da Antiguidade. Um foi professor do outro, em sequência!",
    ]),
    (["quem foi o maior cientista", "quem foi o maior cientista da historia", "quem e o maior cientista",
      "quem sao os maiores cientistas", "quais os maiores cientistas", "quais sao os maiores cientistas"], [
        "Impossível escolher um só! Newton, Einstein, Galileu, Marie Curie e Darwin sempre aparecem entre os maiores da história.",
    ]),
]

FRASES_CULTURA = (RECOMENDACOES + INVENCOES + HEROIS_DC + HEROIS_MARVEL + HEROIS_GERAL + STAR_WARS
                  + SISTEMA_SOLAR + CONSTELACOES + HISTORIA)
