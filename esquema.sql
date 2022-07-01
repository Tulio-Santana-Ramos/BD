
CREATE TABLE USUARIO(
	username VARCHAR(40) PRIMARY KEY, 
	tipo BOOLEAN NOT NULL,
	email VARCHAR(40) NOT NULL,
	telefone VARCHAR(20),
	CONSTRAINT email_check CHECK(email LIKE'%@%')
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

CREATE TABLE COMPRA(
	datahora TIMESTAMP,
	cliente VARCHAR(40),
	total NUMERIC(6,2),
	CONSTRAINT pk_compra PRIMARY KEY(datahora, cliente),
	CONSTRAINT fk_compra FOREIGN KEY(cliente)
	REFERENCES CLIENTE(usuario),
	CONSTRAINT total_check CHECK (total >= 0)
);

CREATE TABLE COLECAO(
	nome VARCHAR(40),
	inicio TIMESTAMP,
	fim TIMESTAMP NOT NULL,
	preco NUMERIC(6,2),
	descricao VARCHAR(200),
	CONSTRAINT pk_colecao PRIMARY KEY(nome, inicio),
	CONSTRAINT preco_check CHECK (preco >= 0),
	CONSTRAINT data_check CHECK (fim >= inicio)
);

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
	CONSTRAINT avaliacao_check CHECK (avaliacaoMedia >= 0),
	CONSTRAINT faixa_check CHECK (faixaEtaria >= 0 AND faixaEtaria <= 18),
	CONSTRAINT preco_check CHECK (preco >= 0)
);

CREATE TABLE ALUGUEL(
	datainicio TIMESTAMP,
	datafim TIMESTAMP,
	livro VARCHAR(40),
	cliente VARCHAR(40),
	valor NUMERIC(6,2),
	CONSTRAINT fk_aluguel FOREIGN KEY(cliente)
	REFERENCES CLIENTE(usuario),
	CONSTRAINT data_check CHECK (datafim >= datainicio),
	CONSTRAINT valor_check CHECK (valor >= 0)
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
	nota NUMERIC(3,1),
	CONSTRAINT pk_avalia PRIMARY KEY(cliente, livro),
	CONSTRAINT fk_avalia1 FOREIGN KEY (cliente)
	REFERENCES CLIENTE(usuario),
	CONSTRAINT fk_avalia2 FOREIGN KEY (livro)
	REFERENCES LIVRO(nome),
	CONSTRAINT avalia_check CHECK (nota >= 0)
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
	tipo VARCHAR(10),
	CONSTRAINT pk_categoria PRIMARY KEY(livro, tipo),
	CONSTRAINT fk_categoria FOREIGN KEY (livro)
	REFERENCES LIVRO(nome),
	CONSTRAINT tipo_check CHECK (tipo IN ('Ebook','AudioBook'))
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
	REFERENCES USUARIO(username),
	CONSTRAINT qtd_check CHECK (qtdLivrosPublicados >= 0),
	CONSTRAINT ava_check CHECK (avaliacaoMedia >= 0)
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
	REFERENCES LIVRO(nome),
	CONSTRAINT pag_check CHECK (numPaginas >= 0)
);

CREATE TABLE AUDIOBOOK(
	livro VARCHAR(40) PRIMARY KEY,
	duracao INTEGER,
	dublador VARCHAR(40),
	CONSTRAINT pk_audiobook FOREIGN KEY (livro)
	REFERENCES LIVRO(nome),
	CONSTRAINT duracao_check CHECK (duracao >= 0)
);

CREATE TABLE AUTOR(
	cpf VARCHAR(11) PRIMARY KEY,
	nome VARCHAR(40),
	qtLivrosPublicados INTEGER,
	email VARCHAR(40),
	telefone VARCHAR(12),
	CONSTRAINT qt_check CHECK (qtLivrosPublicados >= 0),
	CONSTRAINT email_check CHECK(email LIKE'%@%')
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
