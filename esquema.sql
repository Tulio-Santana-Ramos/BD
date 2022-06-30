
/*
	*DEFINIR POSSÍVEIS CHECKS PARA ALGUNS ATRIBUTOS SE NECESSARIO
	*DOCUMENTAR
*/

CREATE TABLE USUARIO(
	username VARCHAR(40) PRIMARY KEY, 
	tipo BOOLEAN NOT NULL,
	email VARCHAR(40) NOT NULL, --check <string>@<string>
	telefone VARCHAR(20)
);

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
	REFERENCES USUARIO(username)
);

CREATE TABLE LISTA_AMIGOS(
	dono VARCHAR(40),
	amigo VARCHAR(40),
	CONSTRAINT pk_lista PRIMARY KEY(dono, amigo),
	CONSTRAINT fk_lista1 FOREIGN KEY(dono) REFERENCES CLIENTE(usuario),
    CONSTRAINT fk_lista2 FOREIGN KEY(amigo) REFERENCES CLIENTE(usuario)
);

CREATE TABLE PRODUTO(
	nome VARCHAR(40) PRIMARY KEY,
	preço NUMERIC(6,2),
	classe BOOLEAN NOT NULL
);

CREATE TABLE COMPRA(
	datahora TIMESTAMP,
	cliente VARCHAR(40),
	total NUMERIC(6,2),
	CONSTRAINT pk_compra PRIMARY KEY(datahora, cliente),
	CONSTRAINT fk_compra FOREIGN KEY(cliente)
	REFERENCES CLIENTE(usuario)
);

CREATE TABLE COLECAO(
	nome VARCHAR(40),
	inicio TIMESTAMP NOT NULL,
	fim TIMESTAMP NOT NULL,
	preco NUMERIC(6,2),
	descricao VARCHAR(200),
	CONSTRAINT pk_colecao PRIMARY KEY(nome, inicio),
	CONSTRAINT fk_colecao FOREIGN KEY (nome)
	REFERENCES PRODUTO(nome)
);

CREATE TABLE LIVRO(
	nome VARCHAR(40) PRIMARY KEY,
	edicao 	INTEGER,
	categoria VARCHAR(10) NOT NULL,	--Ebook ou Audio Book
	anoPublicacao VARCHAR(4),
	sinopse VARCHAR(200),
	avaliacaoMedia NUMERIC(3,1),
	faixaEtaria INTEGER,
	UNIQUE(nome, edicao),
	CONSTRAINT fk_livro FOREIGN KEY(nome)
	REFERENCES PRODUTO(nome)
);

CREATE TABLE ALUGUEL(
	datainicio TIMESTAMP,
	datafim TIMESTAMP,
	livro VARCHAR(40),
	cliente VARCHAR(40),
	valor NUMERIC(6,2),
	CONSTRAINT fk_aluguel FOREIGN KEY(cliente)
	REFERENCES CLIENTE(usuario)
);

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

CREATE TABLE AVALIA(
	cliente VARCHAR(40),
	livro VARCHAR(40),
	CONSTRAINT pk_avalia PRIMARY KEY(cliente, livro),
	CONSTRAINT fk_avalia1 FOREIGN KEY (cliente)
	REFERENCES CLIENTE(usuario),
	CONSTRAINT fk_avalia2 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome)
);

CREATE TABLE POSSUI(
	cliente VARCHAR(40),
	datahora TIMESTAMP,
	livro VARCHAR(40),
	CONSTRAINT pk_possui PRIMARY KEY(cliente, datahora, livro),
	CONSTRAINT fk_possui1 FOREIGN KEY (cliente, datahora)
	REFERENCES COMPRA(cliente, datahora),
	CONSTRAINT fk_possui2 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome)
);

CREATE TABLE DETEM(
	cliente VARCHAR(40),
	datahoraCompra TIMESTAMP,
	colecao VARCHAR(40),
    datahoraColecao TIMESTAMP,
	CONSTRAINT pk_detem PRIMARY KEY(cliente, datahoraCompra, colecao, datahoraColecao),
	CONSTRAINT fk_detem1 FOREIGN KEY(cliente, datahoraCompra)
	REFERENCES COMPRA(cliente, datahora),
	CONSTRAINT fk_detem2 FOREIGN KEY(colecao,datahoraColecao)
	REFERENCES COLECAO(nome, inicio)
);

CREATE TABLE CATEGORIA(
	livro VARCHAR(40),
	tipo VARCHAR(10),	--Ebook ou Audio Book
	CONSTRAINT pk_categoria PRIMARY KEY(livro, tipo),
	CONSTRAINT fk_categoria FOREIGN KEY (livro)
	REFERENCES LIVRO(nome)
);

CREATE TABLE LISTA_DESEJOS(
	cliente VARCHAR(40),
	livro VARCHAR(40),
	CONSTRAINT pk_lista_desejos PRIMARY KEY(cliente, livro),
	CONSTRAINT pk_lista_desejos1 FOREIGN KEY (cliente)
	REFERENCES CLIENTE(usuario),
	CONSTRAINT pk_lista_desejos2 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome)
);

CREATE TABLE EDITORA(
	usuario VARCHAR(40) PRIMARY KEY,
	qtdLivrosPublicados INTEGER,
	avaliacaoMedia NUMERIC(3,1),
	cnpj VARCHAR(14),
	status BOOLEAN NOT NULL,
	UNIQUE(cnpj),
	CONSTRAINT fk_editora FOREIGN KEY (usuario)
	REFERENCES USUARIO(username)
);

CREATE TABLE CONTEM(
	livro VARCHAR(40),
	nomeColecao VARCHAR(40),
    inicioColecao TIMESTAMP,
	CONSTRAINT pk_contem1 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome),
	CONSTRAINT pk_contem2 FOREIGN KEY (nomeColecao, inicioColecao)
	REFERENCES COLECAO(nome,inicio)
);

CREATE TABLE EBOOK(
	livro VARCHAR(40) PRIMARY KEY,
	numPaginas INTEGER NOT NULL,
	CONSTRAINT pk_ebook FOREIGN KEY (livro)
	REFERENCES LIVRO(nome)
);

CREATE TABLE AUDIOBOOK(
	livro VARCHAR(40) PRIMARY KEY,
	duracao INTEGER,
	dublador VARCHAR(40),
	CONSTRAINT pk_audiobook FOREIGN KEY (livro)
	REFERENCES LIVRO(nome)
);

CREATE TABLE AUTOR(
	cpf VARCHAR(11) PRIMARY KEY,
	nome VARCHAR(40),
	qtLivrosPublicados INTEGER,
	email VARCHAR(40),
	telefone VARCHAR(12)
);

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