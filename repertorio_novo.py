"""
repertorio_novo.py
Mais respostas fixas do C-2GELSA. Mesmo formato do repertorio.py:
([gatilhos sem acento/pontuação, minúsculas], [respostas]).

FRASES_NOVO_PRIORIDADE vai no INÍCIO de FRASES (gatilhos que um genérico, como
"quem criou", engolia) e FRASES_NOVO no FINAL: o que já existe tem prioridade,
então aqui só entra o que ainda não estava coberto. Só fatos gerais e estáveis
(nada que mude, como presidente atual ou campeão recente).
Depois de editar: reiniciar o servidor_conversa.py e rodar de novo o
gerar_gramatica.py (as frases novas precisam entrar na lista do reconhecedor).
"""

FRASES_NOVO_PRIORIDADE = [
    (['quem criou a internet'], [
        'A internet nasceu de uma rede militar americana, a Arpanet, no fim dos anos sessenta, e foi crescendo com o trabalho de muita gente.',
    ]),
    (['quem criou o sitio do picapau amarelo'], [
        'Monteiro Lobato foi um escritor brasileiro, criador do Sítio do Picapau Amarelo, com a Emília, o Visconde e a Narizinho.',
    ]),
]

FRASES_NOVO = [
    (['quantas vezes o brasil foi campeao do mundo', 'quantas vezes o brasil foi campeao mundial'], [
        'O Brasil é pentacampeão do mundo! Ganhou cinco Copas: em 1958, 1962, 1970, 1994 e 2002.',
    ]),
    (['quem ganhou a copa de 2002'], [
        'O Brasil ganhou a Copa de 2002, na Coreia do Sul e no Japão, e foi pentacampeão.',
    ]),
    (['quem ganhou a copa de dois mil e dez', 'quem ganhou a copa de 2010'], [
        'A Espanha ganhou a Copa de 2010, na África do Sul.',
    ]),
    (['quem ganhou a copa de dois mil e quatorze', 'quem ganhou a copa de 2014'], [
        'A Alemanha ganhou a Copa de 2014, jogada aqui no Brasil.',
    ]),
    (['quem ganhou a copa de dois mil e dezoito', 'quem ganhou a copa de 2018'], [
        'A França ganhou a Copa de 2018, na Rússia.',
    ]),
    (['quem ganhou a copa de 2022'], [
        'A Argentina ganhou a Copa de 2022, no Catar, com o Messi.',
    ]),
    (['me fale sobre copas do mundo', 'fale sobre as copas do mundo', 'o que e a copa do mundo', 'o que e copa do mundo'], [
        'A Copa do Mundo é o maior campeonato de futebol entre seleções, e acontece a cada quatro anos. O Brasil é o país com mais títulos: cinco.',
    ]),
    (['quem e cristiano ronaldo', 'quem e o cristiano ronaldo', 'cristiano ronaldo'], [
        'Cristiano Ronaldo é um jogador de futebol português, um dos maiores artilheiros da história.',
    ]),
    (['quem e messi', 'quem e o messi', 'quem e lionel messi'], [
        'Lionel Messi é um jogador argentino, considerado um dos melhores de todos os tempos. Ele foi campeão do mundo em 2022.',
    ]),
    (['quem e pele', 'quem e o rei do futebol', 'quem foi o rei do futebol'], [
        'Pelé foi um jogador brasileiro, chamado de Rei do Futebol. É o único jogador que ganhou três Copas do Mundo.',
    ]),
    (['o que e o impedimento'], [
        'Impedimento é quando um jogador está na frente do último defensor no momento em que recebe o passe. Aí o lance é anulado.',
    ]),
    (['o que e escanteio', 'o que e um escanteio'], [
        'Escanteio é a cobrança feita da bandeirinha do canto do campo, quando a bola sai pela linha de fundo tocada por um defensor.',
    ]),
    (['o que e penalti', 'o que e um penalti'], [
        'Pênalti é uma cobrança direta contra o goleiro, da marca a onze metros do gol, dada quando há falta dentro da grande área.',
    ]),
    (['quantos jogadores tem um time de basquete', 'quantos jogadores tem no basquete'], [
        'Cada time de basquete joga com cinco jogadores em quadra.',
    ]),
    (['quantos jogadores tem um time de volei', 'quantos jogadores tem no volei'], [
        'Cada time de vôlei joga com seis jogadores em quadra.',
    ]),
    (['quem e ayrton senna', 'quem foi ayrton senna', 'quem foi o senna', 'quem foi senna'], [
        'Ayrton Senna foi um piloto brasileiro de Fórmula 1, tricampeão mundial, e é um dos maiores ídolos do automobilismo.',
    ]),
    (['de quanto em quanto tempo ocorrem as olimpiadas'], [
        'As Olimpíadas acontecem a cada quatro anos.',
    ]),
    (['o que e uma maratona', 'quantos quilometros tem uma maratona'], [
        'Maratona é uma corrida de rua de quarenta e dois quilômetros, mais precisamente quarenta e dois quilômetros e cento e noventa e cinco metros.',
    ]),
    (['o que e xadrez', 'como funciona o xadrez', 'voce joga xadrez', 'voce sabe jogar xadrez'], [
        'Xadrez é um jogo de tabuleiro para duas pessoas, em que cada uma tenta dar xeque-mate no rei do adversário. Computadores jogam muito bem: em 1997 o Deep Blue venceu o campeão mundial Garry Kasparov.',
    ]),
    (['como funciona um motor eletrico', 'como funciona o motor eletrico', 'o que e um motor eletrico', 'motor eletrico'], [
        'Um motor elétrico usa ímãs e eletricidade: a corrente cria um campo magnético que faz o eixo girar. É o que move as rodas de um robô.',
    ]),
    (['o que faz um processador', 'o que e processador', 'como funciona um processador'], [
        'O processador é o cérebro do computador: ele executa as instruções dos programas, milhões de vezes por segundo.',
    ]),
    (['o que e memoria ram', 'o que e ram', 'o que e a memoria ram'], [
        'A memória RAM é onde o computador guarda, de forma temporária, o que está usando no momento. Quando desliga, ela se apaga.',
    ]),
    (['o que e sensor'], [
        'Sensor é um dispositivo que mede alguma coisa do mundo, como luz, distância, temperatura ou movimento, e transforma isso em um sinal que o robô consegue entender.',
    ]),
    (['o que e um atuador', 'o que sao atuadores', 'o que e atuador'], [
        'Atuador é a parte do robô que faz movimento, como um motor ou um braço mecânico.',
    ]),
    (['o que e aprendizagem de maquina'], [
        'Aprendizado de máquina é quando o computador aprende a partir de exemplos, em vez de seguir regras escritas por uma pessoa. Assim ele reconhece rostos, voz e muito mais.',
    ]),
    (['o que e a nuvem', 'o que e computacao em nuvem', 'o que e cloud'], [
        'Computação em nuvem é usar computadores de outro lugar, pela internet, para guardar arquivos ou rodar programas, em vez de usar só o seu.',
    ]),
    (['o que e uma senha forte', 'como criar uma senha segura', 'como fazer uma senha forte'], [
        'Uma senha forte é longa, mistura letras, números e símbolos, e não repete a de outros sites. Nunca conte a sua para ninguém!',
    ]),
    (['o que e um bit', 'o que e um byte'], [
        'Bit é a menor informação do computador, um zero ou um um. Um byte é um grupo de oito bits.',
    ]),
    (['quem foi isaac newton', 'quem foi newton', 'quem e newton'], [
        'Isaac Newton foi um cientista inglês que descobriu a lei da gravitação universal e as três leis do movimento.',
    ]),
    (['quem foi turing', 'quem e alan turing'], [
        'Alan Turing foi um matemático inglês, um dos pais da computação e da inteligência artificial. Ele ajudou a decifrar códigos na Segunda Guerra Mundial.',
    ]),
    (['quem foi marie curie', 'quem foi madame curie'], [
        'Marie Curie foi uma cientista polonesa que estudou a radioatividade. Foi a primeira pessoa a ganhar dois prêmios Nobel, em áreas diferentes.',
    ]),
    (['como funciona o coracao', 'para que serve o coracao', 'o que faz o coracao'], [
        'O coração é um músculo que funciona como uma bomba: ele empurra o sangue para o corpo todo, levando oxigênio para todas as células.',
    ]),
    (['para que serve o pulmao', 'o que faz o pulmao', 'como funciona o pulmao'], [
        'Os pulmões trazem o oxigênio do ar para o sangue e tiram de lá o gás carbônico, que a gente solta ao expirar.',
    ]),
    (['para que serve o cerebro', 'o que faz o cerebro', 'como funciona o cerebro'], [
        'O cérebro controla o corpo todo: pensa, lembra, sente e manda os movimentos. Ele tem cerca de oitenta e seis bilhões de neurônios.',
    ]),
    (['quanto tempo devo dormir', 'quantas horas de sono'], [
        'Adultos precisam dormir entre sete e nove horas por noite. Crianças e adolescentes precisam de ainda mais.',
    ]),
    (['quanta agua tenho que beber'], [
        'Em geral, uma boa média é de uns dois litros de água por dia, mas depende da pessoa e do calor. Em caso de dúvida, pergunte a um médico.',
    ]),
    (['como nasce um vulcao'], [
        'Vulcão é uma abertura na crosta da Terra por onde sai magma, gases e cinzas, vindos do interior do planeta.',
    ]),
    (['como acontece um terremoto'], [
        'Terremoto é um tremor da terra, causado pelo movimento das placas tectônicas, que são enormes pedaços da crosta terrestre.',
    ]),
    (['o que e um ciclone'], [
        'Furacões, tornados e ciclones são tempestades com ventos que giram em grande velocidade. O furacão é gigante e se forma sobre o mar quente, e o tornado é um funil de vento bem menor.',
    ]),
    (['o que e aquecimento global', 'o que e o aquecimento global'], [
        'Aquecimento global é o aumento da temperatura média da Terra, causado principalmente pelos gases que a queima de petróleo, carvão e gás lança no ar.',
    ]),
    (['por que o ceu e da cor azul'], [
        'O céu é azul porque o ar espalha a luz azul do Sol mais do que as outras cores, e por isso vemos azul para todo lado.',
    ]),
    (['por que a agua do mar e salgada'], [
        'O mar é salgado porque a chuva e os rios, ao longo de milhões de anos, levaram os sais das rochas para ele.',
    ]),
    (['como acontece a chuva'], [
        'A água dos rios e mares evapora, sobe, esfria e vira nuvem. Quando as gotinhas ficam pesadas demais, caem como chuva.',
    ]),
    (['o que e eclipse'], [
        'Eclipse é quando um astro passa na frente de outro. No eclipse do Sol, a Lua tapa o Sol, e no da Lua, a sombra da Terra cobre a Lua.',
    ]),
    (['qual o animal mais forte do mundo', 'qual e o animal mais forte do mundo'], [
        'Proporcionalmente ao tamanho, o besouro rinoceronte é um dos mais fortes. Entre os grandes, o elefante é imbatível em força.',
    ]),
    (['quantos anos vive uma tartaruga', 'quanto tempo vive uma tartaruga'], [
        'Algumas tartarugas passam de cem anos de vida, e as gigantes podem chegar a cento e cinquenta.',
    ]),
    (['o que foi um dinossauro'], [
        'Os dinossauros foram répteis que dominaram a Terra por mais de cento e sessenta milhões de anos. Uns comiam plantas e outros comiam carne.',
    ]),
    (['quantos estados existem no brasil'], [
        'O Brasil tem vinte e seis estados e mais o Distrito Federal, onde fica Brasília.',
    ]),
    (['quando foi descoberto o brasil'], [
        'Os portugueses, comandados por Pedro Álvares Cabral, chegaram ao Brasil em 22 de abril de 1500.',
    ]),
    (['quando o brasil ficou independente', 'quando foi a proclamacao da independencia'], [
        'O Brasil proclamou sua independência de Portugal em 7 de setembro de 1822, às margens do rio Ipiranga.',
    ]),
    (['quando foi proclamada a republica'], [
        'A República do Brasil foi proclamada em 15 de novembro de 1889.',
    ]),
    (['quem foi dom pedro primeiro', 'quem foi dom pedro i', 'quem foi dom pedro'], [
        'Dom Pedro Primeiro foi o primeiro imperador do Brasil, e proclamou a independência em 1822.',
    ]),
    (['quem foi tiradentes'], [
        'Tiradentes foi um dos líderes da Inconfidência Mineira, movimento que queria a independência do Brasil. Ele foi condenado e morreu em 1792.',
    ]),
    (['quando comecou a segunda guerra mundial', 'quando foi a segunda guerra mundial', 'quando terminou a segunda guerra mundial'], [
        'A Segunda Guerra Mundial começou em 1939 e terminou em 1945.',
    ]),
    (['quem e machado de assis'], [
        'Machado de Assis foi um grande escritor brasileiro, fundador da Academia Brasileira de Letras. Escreveu Dom Casmurro e Memórias Póstumas de Brás Cubas.',
    ]),
    (['quem foi monteiro lobato', 'quem e monteiro lobato'], [
        'Monteiro Lobato foi um escritor brasileiro, criador do Sítio do Picapau Amarelo, com a Emília, o Visconde e a Narizinho.',
    ]),
    (['quem foi shakespeare', 'quem e shakespeare', 'quem foi william shakespeare'], [
        'William Shakespeare foi um escritor inglês, autor de Romeu e Julieta, Hamlet e Macbeth.',
    ]),
    (['quem e o autor de dom quixote', 'quem escreveu dom quixote'], [
        'Dom Quixote foi escrito pelo espanhol Miguel de Cervantes, no começo do século dezessete.',
    ]),
    (['quem pintou monalisa'], [
        'A Mona Lisa foi pintada por Leonardo da Vinci, há mais de quinhentos anos. Ela está no Museu do Louvre, em Paris.',
    ]),
    (['quem foi leonardo da vinci', 'quem e leonardo da vinci'], [
        'Leonardo da Vinci foi um gênio italiano do Renascimento: pintor, inventor e cientista. Fez a Mona Lisa e desenhou até máquinas voadoras.',
    ]),
    (['qual a moeda do pais'], [
        'A moeda do Brasil é o real.',
    ]),
    (['qual a bandeira do brasil', 'como e a bandeira do brasil', 'o que significa a bandeira do brasil'], [
        'A bandeira do Brasil é verde, com um losango amarelo e um círculo azul que tem a frase Ordem e Progresso e vinte e sete estrelas, uma para cada estado e uma para o Distrito Federal.',
    ]),
    (['o que e o folclore', 'o que e folclore'], [
        'Folclore é o conjunto das histórias, lendas, músicas e festas populares de um povo, passadas de geração em geração. No Brasil temos o Saci, a Mula Sem Cabeça, o Curupira e a Iara.',
    ]),
    (['quem e o saci', 'quem e o saci perere', 'o que e o saci'], [
        'O Saci-Pererê é um personagem do folclore brasileiro: um menino negro de uma perna só, com gorro vermelho e cachimbo, que faz travessuras.',
    ]),
    (['quem e o curupira', 'o que e o curupira'], [
        'O Curupira é um protetor das florestas do folclore brasileiro. Tem os pés virados para trás, para confundir quem entra no mato.',
    ]),
    (['o que e a festa junina', 'o que sao as festas juninas', 'o que e festa junina'], [
        'As festas juninas acontecem em junho, com fogueira, quadrilha, comidas de milho e roupas de caipira, para homenagear Santo Antônio, São João e São Pedro.',
    ]),
    (['o que e o natal', 'por que se comemora o natal', 'o que e natal'], [
        'O Natal é comemorado em 25 de dezembro, em memória do nascimento de Jesus, e também é época de reunir a família e trocar presentes.',
    ]),
    (['o que e a pascoa', 'o que e pascoa'], [
        'A Páscoa é uma festa cristã que lembra a ressurreição de Jesus. No Brasil, a tradição é dar ovos de chocolate.',
    ]),
    (['recomenda uma comida', 'me recomenda uma comida', 'o que eu como hoje', 'o que eu posso comer', 'sugira uma comida', 'me sugere uma comida'], [
        'Que tal um arroz com feijão, bife e salada? É simples, nutritivo e muito brasileiro!',
        'Uma boa pedida é uma massa com molho de tomate. Fácil e gostosa!',
        'Que tal uma sopa quentinha de legumes? Faz bem e esquenta!',
    ]),
    (['qual a sobremesa tipica do brasil', 'sobremesa tipica do brasil', 'qual a sobremesa do brasil'], [
        'O brigadeiro é a sobremesa mais brasileira de todas, feito de leite condensado, chocolate e granulado.',
    ]),
    (['o que e um churrasco'], [
        'Churrasco é carne assada na brasa, especialidade do Rio Grande do Sul, que aqui chamamos de gaúcho.',
    ]),
    (['o que e um gaucho', 'quem e o gaucho'], [
        'Gaúcho é como são chamados os habitantes do Rio Grande do Sul, e também os peões tradicionais dos pampas, com bombacha e chimarrão.',
    ]),
    (['como fazer um bolo', 'como se faz bolo'], [
        'Um bolo simples leva três ovos, duas xícaras de farinha, uma de açúcar, uma de leite, meia de óleo e uma colher de fermento. Misture tudo e asse por quarenta minutos.',
    ]),
    (['como fazer cafe', 'como se faz cafe'], [
        'Ferva a água, coloque o pó de café no filtro e vá derramando a água devagar. Em poucos minutos o café está pronto.',
    ]),
    (['qual e a melhor hora para estudar', 'me da dicas para estudar'], [
        'Estude em horários fixos, em lugar silencioso e com pausas curtas a cada meia hora. Explicar a matéria em voz alta ajuda muito!',
    ]),
    (['como ser mais feliz'], [
        'Cuidar do sono, fazer exercício, passar tempo com quem a gente gosta e fazer algo que dê prazer ajudam muito a ser feliz.',
    ]),
    (['estou me sentindo triste'], [
        'Sinto muito! Respire fundo e converse com alguém de confiança. Se quiser, posso contar uma piada para animar.',
    ]),
    (['estou com fome', 'to com fome'], [
        'Então é hora de comer! Eu só me alimento de eletricidade, mas você pode escolher algo bem gostoso.',
    ]),
    (['estou com sono', 'to com sono'], [
        'Descanse um pouco! Dormir bem é importante. Eu, por enquanto, só preciso estar ligado na tomada.',
    ]),
    (['estou com calor', 'que calor', 'ta calor'], [
        'Beba bastante água e procure uma sombra! Eu também esquento quando penso muito.',
    ]),
    (['estou com frio', 'que frio', 'ta frio'], [
        'Que tal um casaco e uma bebida quente? Eu não sinto frio, mas meus circuitos agradecem um lugar agradável.',
    ]),
    (['estou feliz', 'to feliz', 'estou muito feliz', 'hoje eu estou feliz'], [
        'Que bom! A sua alegria me deixa feliz também.',
    ]),
    (['estou entediado', 'to entediado', 'estou com tedio', 'to com tedio', 'estou sem nada para fazer'], [
        'Vamos conversar, então! Posso contar uma piada, uma curiosidade ou propor uma charada.',
    ]),
    (['conta uma charada', 'me conta uma charada', 'fala uma charada', 'me fala uma charada', 'uma charada', 'faz uma charada'], [
        'O que é, o que é: quanto mais se tira, maior fica? A resposta é o buraco!',
        'O que é, o que é: tem dentes mas não morde? É o alho!',
        'O que é, o que é: cai em pé e corre deitado? É a chuva!',
        'O que é, o que é: anda com os pés na cabeça? É o piolho!',
        'O que é, o que é: tem coroa mas não é rei? É o abacaxi!',
        'O que é, o que é: tem pescoço mas não tem cabeça? É a garrafa!',
    ]),
    (['me conta um trava lingua', 'fala um trava lingua', 'conta um trava lingua', 'um trava lingua', 'me fala um trava lingua'], [
        'O rato roeu a roupa do rei de Roma.',
        'Três pratos de trigo para três tigres tristes.',
        'O peito do pé de Pedro é preto.',
        'A aranha arranha a rã. A rã arranha a aranha. Nem a aranha arranha a rã, nem a rã arranha a aranha.',
    ]),
    (['fala um proverbio', 'fale um proverbio', 'me fala um ditado', 'fala um ditado', 'ditado popular'], [
        'Água mole em pedra dura, tanto bate até que fura.',
        'Quem não arrisca, não petisca.',
        'De grão em grão, a galinha enche o papo.',
        'Devagar se vai ao longe.',
    ]),
    (['pode me dar um conselho', 'preciso de um conselho'], [
        'Respire fundo, faça uma coisa de cada vez e seja gentil, com os outros e com você mesmo.',
        'Aprenda com os erros, mas não fique preso a eles. Cada dia é uma nova chance.',
    ]),
    (['uma historia curta'], [
        'Era uma vez um robozinho que queria aprender a sorrir. Ele conversou com muita gente e descobriu que sorrir era só contar uma piada para quem estivesse por perto. Fim!',
        'Havia uma tartaruga e uma lebre que apostaram uma corrida. A lebre dormiu no meio do caminho e a tartaruga, devagar e sempre, chegou primeiro.',
    ]),
    (['joga uma moeda', 'joga a moeda', 'jogue a moeda'], [
        'Joguei a moeda e deu cara!',
        'Joguei a moeda e deu coroa!',
    ]),
    (['joga um dado', 'jogue o dado', 'joga o dado', 'rola um dado'], [
        'Joguei o dado e saiu o número um.',
        'Joguei o dado e saiu o número dois.',
        'Joguei o dado e saiu o número três.',
        'Joguei o dado e saiu o número quatro.',
        'Joguei o dado e saiu o número cinco.',
        'Joguei o dado e saiu o número seis.',
    ]),
    (['pedra papel tesoura', 'joga pedra papel tesoura'], [
        'Eu escolho pedra! Você escolhe e a gente vê quem ganhou. Mas é de mentirinha, eu não tenho mãos!',
        'Eu escolho tesoura! Mas sem mãos, é só imaginação.',
    ]),
]
