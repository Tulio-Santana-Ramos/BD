
/*
	TODO:
	*CRIAR O DATABASE
	*DEFINIR MELHOR OS TIPOS DOS ATRIBUTOS E TAMANHOS DE VARCHAR, NUMBER
	*DEFINIR POSSÍVEIS CHECKS PARA ALGUNS ATRIBUTOS SE NECESSARIO
	*DOCUMENTAR
*/


/*
	datahora pode ser DATE?
	DATE pode ser chave primaria?
*/

CREATE TABLE USUARIO(
	username VARCHAR(20) PRIMARY KEY,
	tipo VARCHAR(1) NOT NULL,
	email VARCHAR(20) NOT NULL,
	telefone VARCHAR(20)
);

CREATE TABLE CLIENTE(
	usuario VARCHAR(20) PRIMARY KEY,
	dataNascimento DATE,
	nome VARCHAR(20) NOT NULL,
	titular ?,
	numero VARCHAR(20),
	csv ?,
	cpf VARCHAR(11),
	UNIQUE(cpf),
	CONSTRAINT fk_us FOREIGN KEY(usuario)
	REFERENCES USUARIO(username)
);

CREATE TABLE LISTA_AMIGOS(
	dono VARCHAR(20),
	amigo VARCHAR(20),
	CONSTRAINT pk_lista PRIMARY KEY(dono, amigo),
	CONSTRAINT fk_lista FOREIGN KEY(dono, amigo)
	REFERENCES CLIENTE(usuario, usuario)
);

CREATE TABLE COMPRA(
	datahora DATE,
	cliente VARCHAR(20),
	total  ? -- NUMBER?
	CONSTRAINT pk_compra PRIMARY KEY(datahora, cliente),
	CONSTRAINT fk_compra FOREIGN KEY(cliente)
	REFERENCES CLIENTE(usuario)
);

CREATE TABLE ALUGUEL(
	datainicio DATE,
	datafim DATE,
	livro ?,
	cliente VARCHAR(20),
	valor ? -- NUMBER?
	CONSTRAINT fk_aluguel FOREIGN KEY(cliente)
	REFERENCES CLIENTE(usuario)
);

CREATE TABLE PRESENTEAR(
	cliente1 VARCHAR(20),
	cliente2 VARCHAR(20),
	livro ?,
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
	cliente VARCHAR(20),
	livro ?,
	CONSTRAINT pk_avalia PRIMARY KEY(cliente, livro),
	CONSTRAINT fk_avalia1 FOREIGN KEY (cliente)
	REFERENCES CLIENTE(usuario),
	CONSTRAINT fk_avalia2 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome)
);

CREATE TABLE POSSUI(
	cliente VARCHAR(20),
	datahora DATE,
	livro ?,
	CONSTRAINT pk_possui PRIMARY KEY(cliente, datahora, livro),
	CONSTRAINT fk_possui1 FOREIGN KEY (cliente, datahora)
	REFERENCES COMPRA(cliente, datahora),
	CONSTRAINT fk_possui2 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome)
);

CREATE TABLE DETEM(
	cliente VARCHAR(20),
	datahora DATE,
	colecao ?,
	CONSTRAINT pk_detem PRIMARY KEY(cliente, datahora, colecao),
	CONSTRAINT fk_detem1 FOREIGN KEY(cliente, datahora)
	REFERENCES COMPRA(cliente, datahora),
	CONSTRAINT fk_detem2 FOREIGN KEY(colecao)
	REFERENCES COLECAO(nome),
);

CREATE TABLE CATEGORIA(
	livro ?,
	tipo ?,
	CONSTRAINT pk_categoria PRIMARY KEY(livro, tipo),
	CONSTRAINT fk_categoria FOREIGN KEY (livro)
	REFERENCES LIVRO(nome)
);

CREATE TABLE LISTA_DESEJOS(
	cliente VARCHAR(20),
	livro ?,
	CONSTRAINT pk_lista_desejos PRIMARY KEY(cliente, livro),
	CONSTRAINT pk_lista_desejos1 FOREIGN KEY (cliente)
	REFERENCES CLIENTE(usuario),
	CONSTRAINT pk_lista_desejos2 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome)
);

CREATE TABLE EDITORA(
	usuario VARCHAR(20) PRIMARY KEY,
	qtdLivrosPublicados INT,
	avaliacaoMedia ?,
	cnpj VARCHAR(14),
	status VARCHAR(1),
	UNIQUE(cnpj),
	CONSTRAINT fk_editora FOREIGN KEY (usuario)
	REFERENCES USUARIO(username)
);

CREATE TABLE PRODUTO(
	nome VARCHAR(20) PRIMARY KEY,
	preço ? -- NUMBER?,
	classe VARCHAR(1) NOT NULL
);

CREATE TABLE COLECAO(
	nome VARCHAR(20),
	inicio DATE NOT NULL,
	fim DATE NOT NULL,
	preco ? -- NUMBER?
	descricao,
	CONSTRAINT pk_colecao PRIMARY KEY(nome, inicio),
	CONSTRAINT fk_colecao FOREIGN KEY (nome)
	REFERENCES PRODUTO(nome)
);

CREATE TABLE LIVRO(
	nome VARCHAR(20) PRIMARY KEY,
	edicao ? ,
	categoria ?,
	anoPublicacao VARCHAR(4),
	sinopse VARCHAR(200),
	avaliacaoMedia ? -- NUMBER?
	faixaEtaria INT,
	UNIQUE(nome, edicao),
	CONSTRAINT fk_livro FOREIGN KEY(nome)
	REFERENCES PRODUTO(nome)
);

CREATE TABLE CONTEM(
	livro VARCHAR(20),
	colecao VARCHAR(20),
	CONSTRAINT pk_contem1 PRIMARY KEY (livro)
	REFERENCES LIVRO(nome),
	CONSTRAINT pk_contem2 PRIMARY KEY (colecao)
	REFERENCES COLECAO(nome),
);

CREATE TABLE EBOOK(
	livro VARCHAR(20) PRIMARY KEY,
	numPaginas INT NOT NULL,
	CONSTRAINT pk_ebook FOREIGN KEY (livro)
	REFERENCES LIVRO(nome),
);

CREATE TABLE AUDIOBOOK(
	livro VARCHAR(20) PRIMARY KEY,
	duracao ? -- NUMBER?,
	dublador VARCHAR(20),
	CONSTRAINT pk_audiobook FOREIGN KEY (livro)
	REFERENCES LIVRO(nome),
);

CREATE TABLE AUTOR(
	cpf VARCHAR(11) PRIMARY KEY,
	nome VARCHAR(20),
	qtLivrosPublicados INT,
	email VARCHAR(30),
	telefone VARCHAR(12)
);

CREATE TABLE PUBLICA(
	livro VARCHAR(20),
	autor VARCHAR(11),
	editora VARCHAR(20) NOT NULL,
	CONSTRAINT pk_publica PRIMARY KEY(livro, autor),
	CONSTRAINT fk_publica1 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome),
	CONSTRAINT fk_publica2 FOREIGN KEY (autor)
	REFERENCES AUTOR(cpf)
);

