/*
Selecionar nome, nome de usuario e quantidade de livros comprados da série Harry Potter, ordenados pelo usuário que mais comprou
*/

SELECT CL.usuario, CL.nome, COUNT(*) AS "QUANTIDADE" FROM CLIENTE CL JOIN 

	( SELECT C.cliente, C.datahora FROM COMPRA C JOIN POSSUI P
    ON C.cliente = P.cliente AND C.datahora = P.datahora
    WHERE UPPER(livro) LIKE ('%HARRY POTTER%') ) AS R 
    
ON CL.usuario = R.cliente
GROUP BY CL.usuario, CL.nome
ORDER BY COUNT(*) DESC

/*
Selecionar a quantidade de Ebooks vendidos por mês em 2022, tal que, tenham pertencido a pelo menos uma coleção
*/

SELECT EXTRACT(MONTH FROM R.datahora), COUNT(*) FROM
  (SELECT * FROM POSSUI WHERE EXTRACT(YEAR FROM datahora) = 2022)
  AS R JOIN
	(
		SELECT E.livro FROM EBOOK E JOIN CONTEM C ON E.livro = C.livro
  ) AS K

ON R.livro = K.livro 
GROUP BY EXTRACT(MONTH FROM R.datahora)
ORDER BY EXTRACT(MONTH FROM R.datahora)

/*
Liste todos os Livros e, para aqueles disponíveis como Ebook e AudioBook, liste sua duração e número de páginas   
*/

SELECT L.nome, L.edicao, L.anoPublicacao, L.edicao, Z.numPaginas, Z.duracao
	FROM LIVRO L LEFT JOIN
    (
        
      (SELECT A.livro, A.duracao, K.numPaginas FROM
          
          (SELECT E.livro, E.numPaginas FROM
             
               (SELECT LV.nome FROM LIVRO LV) AS R
              
           JOIN EBOOK E ON E.livro = R.nome ) AS K
          
      JOIN AUDIOBOOK A ON A.livro = K.livro )
        
    ) AS Z ON Z.livro = L.nome


/*
Liste o Email de Editoras que já publicaram pelo menos 1 livro com avaliação média maior ou igual a 8
*/

SELECT U.username, U.email, L.nome
	FROM USUARIO U JOIN EDITORA E on U.username = E.usuario
    JOIN PUBLICA P on E.usuario = P.editora
    JOIN LIVRO L on P.livro = L.nome
    WHERE L.avaliacaoMedia >= 8.0

/*
Liste nome dos usuários que compraram coleções dentro de um período de 3 anos, ordenados pelos que mais compraram
*/

SELECT CL.usuario, CL.nome, COUNT(*) FROM CLIENTE CL JOIN 

	(SELECT C.cliente, C.datahora FROM COMPRA C JOIN
     	(
          SELECT * FROM DETEM WHERE EXTRACT(YEAR FROM datahoraCompra) >= 2020
    	) AS DT
     ON DT.cliente = C.cliente AND C.datahora = DT.datahoraCompra ) AS R

ON R.CLIENTE = CL.USUARIO
GROUP BY CL.usuario, CL.nome
ORDER BY COUNT(*) DESC

