/*
Eduardo Henrique Porto Silva - 11796656
Israel Felipe da Silva - 11796531
Tulio Santana Ramos - 11795526
São Carlos
2022
*/

/*
 Tabela Usuário Guarda informações do Usuário que pode ser cliente ou editora
@atributo username representa o username identificador do usuário
@atributo tipo cliente ou editora
@atributo email email do usuário
@atributo telefone telefone do usuário
@constraint email_check verifica se email contém '@'
*/
CREATE TABLE USUARIO(
	username VARCHAR(40) PRIMARY KEY, 
	tipo BOOLEAN NOT NULL,
	email VARCHAR(40) NOT NULL,
	telefone VARCHAR(20),
	CONSTRAINT email_check CHECK(email LIKE'%@%')
);

/*
 Tabela Cliente Guarda informações do usuário do tipo Cliente
@atributo usuario username do cliente
@atributo dataNascimento data de nascimento do cliente
@atributo nome nome do cliente
@atributo titular nome titular cartão de crédito
@atributo numero número cartão de crédito
@atributo csv csv cartão de crédito
@atributo cpf cpf do cliente
*/
CREATE TABLE CLIENTE(
	usuario VARCHAR(40) PRIMARY KEY,
	dataNascimento DATE, 
	nome VARCHAR(40) NOT NULL,
	titular VARCHAR(40), 
	numero VARCHAR(16), 
	csv VARCHAR(3), 
	cpf VARCHAR(11) NOT NULL,
	UNIQUE(cpf),
	CONSTRAINT fk_us FOREIGN KEY(usuario)
	REFERENCES USUARIO(username) ON DELETE CASCADE
);

/*
 Tabela Lista_Amigos Guarda informações de listas de amigos de cada cliente
@atributo dono dono da lista
@atributo amigo amigo pertencente a lista do dono
*/
CREATE TABLE LISTA_AMIGOS(
	dono VARCHAR(40),
	amigo VARCHAR(40),
	CONSTRAINT pk_lista PRIMARY KEY(dono, amigo),
	CONSTRAINT fk_lista1 FOREIGN KEY(dono) REFERENCES CLIENTE(usuario) ON DELETE CASCADE,
    CONSTRAINT fk_lista2 FOREIGN KEY(amigo) REFERENCES CLIENTE(usuario) ON DELETE CASCADE
);

/*
 Tabela Compra Guarda informações de Compras realizadas por clientes
@atributo datahora data e hora da compra
@atributo cliente cliente que efetuou a compra
@atributo total total da compra
@constraint total_check garante que o total é um número > 0
*/
CREATE TABLE COMPRA(
	datahora TIMESTAMP,
	cliente VARCHAR(40),
	total NUMERIC(6,2),
	CONSTRAINT pk_compra PRIMARY KEY(datahora, cliente),
	CONSTRAINT fk_compra FOREIGN KEY(cliente)
	REFERENCES CLIENTE(usuario),
	CONSTRAINT total_check CHECK (total > 0)
);

/*
 Tabela Coleção Guarda informações de Coleções de livros
@atributo nome nome da coleção
@atributo inicio data e hora do inicio da coleção
@atributo fim data e hora do fim da coleção
@atributo preco preço da coleção
@atributo descricao descrição da coleção
@constraint preco_check garante que o preço é um número > 0
@constraint preco_check garante que a data de fim é > data de inicio
*/
CREATE TABLE COLECAO(
	nome VARCHAR(40),
	inicio TIMESTAMP,
	fim TIMESTAMP NOT NULL,
	preco NUMERIC(6,2),
	descricao VARCHAR(200),
	CONSTRAINT pk_colecao PRIMARY KEY(nome, inicio),
	CONSTRAINT preco_check CHECK (preco > 0),
	CONSTRAINT data_check CHECK (fim > inicio)
);

/*
 Tabela Livro Guarda informações de Livros
@atributo nome nome do livro
@atributo edicao edição do livro
@atributo anoPublicacao ano de publicação do livro
@atributo sinopse sinopse do livro
@atributo avaliacaoMedia avaliação média dos clientes sobre o livro
@atributo faixaEtaria faixa etária do livro
@atributo preco preço do livro
@constraint edicao_check garante que a edição é um número >= 0
@constraint avaliacao_check garante que 0 <= avaliação média <= 10 
@constraint faixa_check garante que a faixa etária é um número >= 0
@constraint preco_check garante que o preço é um número > 0
*/
CREATE TABLE LIVRO(
	nome VARCHAR(40) PRIMARY KEY,
	edicao INTEGER NOT NULL,
	anoPublicacao VARCHAR(4),
	sinopse VARCHAR(200),
	avaliacaoMedia NUMERIC(3,1),
	faixaEtaria INTEGER,
	preco NUMERIC(6,2),
	UNIQUE(nome, edicao),
	CONSTRAINT edicao_check CHECK (edicao >= 0),
	CONSTRAINT avaliacao_check CHECK (avaliacaoMedia >= 0 AND avaliacaoMedia <= 10),
	CONSTRAINT faixa_check CHECK (faixaEtaria >= 0 AND faixaEtaria <= 18),
	CONSTRAINT preco_check CHECK (preco > 0)
);

/*
 Tabela Aluguel Guarda informações de um aluguel efetuado por cliente
@atributo datainicio data de inicio do aluguel
@atributo datafim data de fim do aluguel
@atributo livro livro alugado
@atributo cliente cliente que efetuou o aluguel
@atributo valor valor do aluguel
@constraint data_check garante que a data de fim do aluguel > data de inicio
@constraint valor_check garante que o valor do alguel é um número > 0
*/
CREATE TABLE ALUGUEL(
	datainicio TIMESTAMP,
	datafim TIMESTAMP,
	livro VARCHAR(40),
	cliente VARCHAR(40),
	valor NUMERIC(6,2),
	CONSTRAINT fk_aluguel FOREIGN KEY(cliente)
	REFERENCES CLIENTE(usuario) ON DELETE CASCADE,
	CONSTRAINT data_check CHECK (datafim > datainicio),
	CONSTRAINT valor_check CHECK (valor > 0)
);

/*
 Tabela Presentear Guarda informações de presentes dados de clientes a outros clientes
@atributo cliente1 cliente que vai presentear
@atributo cliente2 cliente que vai receber
@atributo livro livro a ser presenteado
@atributo mensagem mensagem enviada com o presente
*/
CREATE TABLE PRESENTEAR(
	cliente1 VARCHAR(40),
	cliente2 VARCHAR(40),
	livro VARCHAR(40),
	mensagem VARCHAR(200),
	CONSTRAINT pk_presentear PRIMARY KEY(cliente1, cliente2, livro),
	CONSTRAINT fk_presentear1 FOREIGN KEY (cliente1)
	REFERENCES CLIENTE(usuario),
	CONSTRAINT fk_presentear2 FOREIGN KEY (cliente2)
	REFERENCES CLIENTE(usuario),
	CONSTRAINT fk_presentear3 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome)
);

/*
 Tabela Avalia Guarda informações de avaliações de livros dada por clientes
@atributo cliente cliente que realiza a avaliação
@atributo livro livro avaliado
@atributo nota nota da avaliação
@constraint avalia_check garante que 0 <= nota <= 10
*/
CREATE TABLE AVALIA(
	cliente VARCHAR(40),
	livro VARCHAR(40),
	nota NUMERIC(3,1),
	CONSTRAINT pk_avalia PRIMARY KEY(cliente, livro),
	CONSTRAINT fk_avalia1 FOREIGN KEY (cliente)
	REFERENCES CLIENTE(usuario),
	CONSTRAINT fk_avalia2 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome),
	CONSTRAINT avalia_check CHECK (nota >= 0 AND nota <= 10)
);

/*
 Tabela Possui Guarda informações de livros possuídos por clientes
@atributo cliente cliente que possui um livro
@atributo datahora data e hora em que o livro foi comprado
@atributo livro livro que o cliente possui 
*/
CREATE TABLE POSSUI(
	cliente VARCHAR(40),
	datahora TIMESTAMP,
	livro VARCHAR(40),
	CONSTRAINT pk_possui PRIMARY KEY(cliente, datahora, livro),
	CONSTRAINT fk_possui1 FOREIGN KEY (cliente, datahora)
	REFERENCES COMPRA(cliente, datahora) ON DELETE CASCADE,
	CONSTRAINT fk_possui2 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome) ON DELETE CASCADE
);

/*
 Tabela Detem Guarda informações de Coleções possuídas por clientes
@atributo cliente cliente que possuí a coleção
@atributo datahoraCompra data e hora da compra da coleção pelo cliente
@atributo colecao coleção comprada pelo cliente
@atributo datahoraColecao data e hora de quando a coleção lançou
*/
CREATE TABLE DETEM(
	cliente VARCHAR(40),
	datahoraCompra TIMESTAMP,
	colecao VARCHAR(40),
    datahoraColecao TIMESTAMP,
	CONSTRAINT pk_detem PRIMARY KEY(cliente, datahoraCompra, colecao, datahoraColecao),
	CONSTRAINT fk_detem1 FOREIGN KEY(cliente, datahoraCompra)
	REFERENCES COMPRA(cliente, datahora) ON DELETE CASCADE,
	CONSTRAINT fk_detem2 FOREIGN KEY(colecao,datahoraColecao)
	REFERENCES COLECAO(nome, inicio) ON DELETE CASCADE
);

/*
 Tabela Categoria Guarda se o livro é Ebook ou AudioBook ou os dois
@atributo livro nome do livro
@atributo tipo categoria do livro
@constraint tipo_check garante que o tipo é Ebook ou AudioBook
*/
CREATE TABLE CATEGORIA(
	livro VARCHAR(40),
	tipo VARCHAR(10),
	CONSTRAINT pk_categoria PRIMARY KEY(livro, tipo),
	CONSTRAINT fk_categoria FOREIGN KEY (livro)
	REFERENCES LIVRO(nome) ON DELETE CASCADE,
	CONSTRAINT tipo_check CHECK (tipo IN ('Ebook','AudioBook'))
);

/*
 Tabela Lista Desejos Guarda informações de livros que estão na lista de desejos de cada cliente
@atributo cliente nome do cliente
@atributo livro livro de desejo do cliente
*/
CREATE TABLE LISTA_DESEJOS(
	cliente VARCHAR(40),
	livro VARCHAR(40),
	CONSTRAINT pk_lista_desejos PRIMARY KEY(cliente, livro),
	CONSTRAINT pk_lista_desejos1 FOREIGN KEY (cliente)
	REFERENCES CLIENTE(usuario) ON DELETE CASCADE,
	CONSTRAINT pk_lista_desejos2 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome) ON DELETE CASCADE
);

/*
 Tabela Editora Guarda informações sobre as editoras
@atributo usuario username da conta
@atributo qtdLivrosPublicados quantidade de livros publicados
@atributo avaliacaoMedia avaliação média da editora
@atributo cnpj CNPJ da editora
@atributo status TRUE se a editora estiver ativa na plataforma ou FALSE caso contrário
@constraint qtd_check garante que a quantidade de livros publicados é um número >= 0
@constraint ava_check garante que 0 <= avaliação média <= 10
*/
CREATE TABLE EDITORA(
	usuario VARCHAR(40) PRIMARY KEY,
	qtdLivrosPublicados INTEGER,
	avaliacaoMedia NUMERIC(3,1),
	cnpj VARCHAR(14),
	status BOOLEAN NOT NULL,
	UNIQUE(cnpj),
	CONSTRAINT fk_editora FOREIGN KEY (usuario)
	REFERENCES USUARIO(username) ON DELETE CASCADE,
	CONSTRAINT qtd_check CHECK (qtdLivrosPublicados >= 0),
	CONSTRAINT ava_check CHECK (avaliacaoMedia >= 0 AND avaliacaoMedia <= 10)
);

/*
 Tabela Contem Guarda informações de livros que pertencem a determinada coleção
@atributo livro nome do livro
@atributo nomeColecao nome da coleção que contém o livro
@atributo inicioColecao data e hora de quando a coleção lançou
*/
CREATE TABLE CONTEM(
	livro VARCHAR(40),
	nomeColecao VARCHAR(40),
    inicioColecao TIMESTAMP,
	CONSTRAINT pk_contem1 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome),
	CONSTRAINT pk_contem2 FOREIGN KEY (nomeColecao, inicioColecao)
	REFERENCES COLECAO(nome,inicio)
);

/*
 Tabela Ebook Guarda informações de livros que são Ebook
@atributo livro nome do livro
@atributo numPaginas número de páginas do livro
@constraint pag_check garante que o número de páginas é um número >= 0
*/
CREATE TABLE EBOOK(
	livro VARCHAR(40) PRIMARY KEY,
	numPaginas INTEGER NOT NULL,
	CONSTRAINT pk_ebook FOREIGN KEY (livro)
	REFERENCES LIVRO(nome) ON DELETE CASCADE,
	CONSTRAINT pag_check CHECK (numPaginas >= 0)
);

/*
 Tabela AudioBook Guarda informações de livros que são Audiobook
@atributo livro nome do livro
@atributo duracao duração em minutos do Audiobook
@atributo dublador nome do dublador do Audiobook
@constraint duracao_check garante que a duração é um número >= 0
*/
CREATE TABLE AUDIOBOOK(
	livro VARCHAR(40) PRIMARY KEY,
	duracao INTEGER,
	dublador VARCHAR(40),
	CONSTRAINT pk_audiobook FOREIGN KEY (livro)
	REFERENCES LIVRO(nome) ON DELETE CASCADE,
	CONSTRAINT duracao_check CHECK (duracao >= 0)
);

/*
 Tabela Autor Guarda informações de autores
@atributo cpf Cpf do autor
@atributo nome nome do autor
@atributo qtLivrosPublicados quantidade de livros publicados
@atributo email email do autor
@atributo telefone telefone do autor
@constraint qt_check garante que a quantidade de livros publicados é um número >= 0
@constraint email_check  garante que o email contém um '@'
*/
CREATE TABLE AUTOR(
	cpf VARCHAR(11) PRIMARY KEY,
	nome VARCHAR(40),
	qtLivrosPublicados INTEGER,
	email VARCHAR(40),
	telefone VARCHAR(12),
	CONSTRAINT qt_check CHECK (qtLivrosPublicados >= 0),
	CONSTRAINT email_check CHECK(email LIKE'%@%')
);

/*
 Tabela Publica guarda informações de um autor que publica um livro em uma determinada editora
@atributo livro nome do livro
@atributo autor nome do autor
@atributo editora nome da editora
*/
CREATE TABLE PUBLICA(
	livro VARCHAR(40),
	autor VARCHAR(11),
	editora VARCHAR(40) NOT NULL,
	CONSTRAINT pk_publica PRIMARY KEY(livro, autor),
	CONSTRAINT fk_publica1 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome),
	CONSTRAINT fk_publica2 FOREIGN KEY (autor)
	REFERENCES AUTOR(cpf),
  	CONSTRAINT fk_publica3 FOREIGN KEY (editora)
	REFERENCES EDITORA(usuario)
);
