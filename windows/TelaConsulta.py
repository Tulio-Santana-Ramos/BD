"""
Eduardo Henrique Porto Silva - 11796656
Israel Felipe da Silva - 11796531
Tulio Santana Ramos - 11795526
São Carlos
2022
"""
import PySimpleGUI as sg
import psycopg2 as sql

class TelaConsulta:

    def __init__(self, con): # Construtor -> Declaração dos componentes da Tela e montagem de layout
        sg.theme('Dark Amber')
        self.layout = [[sg.Text("Abaixo, pode-se selecionar qual consulta se deseja efetuar no banco de dados.\n\n")],
                        [sg.Text("Em Consulta 1, insira uma string para obter o nome, username e quantidade de livros comprados da série inserida.\nEm Consulta 2, insira um número (ano) para obter o nome e username de usuários que compraram coleções do período inserido até o dado mais recente.\n")],
                        [sg.Text("Para a Consulta 3, insira o nome de um autor para obter todos os livros em que está associado\n")],
                        [sg.Text('Livro Consulta 1:', size = (15, 1)), sg.InputText(key = 'C1')], [sg.Text('Ano Consulta 2:', size = (15, 1)), sg.InputText(key = 'C2')], 
                        [sg.Text('Autor Consulta 3:', size = (15, 1)), sg.InputText(key = 'C3')], [sg.Button('Consulta 1'), sg.Button('Consulta 2'), sg.Button('Consulta 3'), sg.Button('Menu')] ]
        self.connection = con
        self.cursor = self.connection.cursor()
        self.window = sg.Window('Webook', self.layout, margins = (25, 30), finalize = True, font = 'arial 12')
        self.num = 0

    def show_results(self, columns, data, title):   # Setup de nova janela, em formato de tabela, para representar as informações das consultas
        layout = [[sg.Table(values = data, headings = columns, max_col_width = 30, key = 'RESULT', row_height = 35,
                justification = 'right', auto_size_columns = True, display_row_numbers = True, tooltip = 'Resultado de sua consulta')],
                [sg.Button('Fechar')]]
        res_window = sg.Window(title, layout, modal = True)

        while True:
            event, values = res_window.read()
            if event == sg.WIN_CLOSED or event == 'Fechar':
                break
        res_window.close()

    def validation(self, c, values):    # Verificação dos campos
        invalidos = []
        if c == 1:  # Para caso Consulta 1
            if(len(values['C1']) == 0):
                invalidos.append('Para fazer a Consulta 1, insira um nome de livro/série no campo determinado')
        elif c == 2:    # Para caso Consulta 2
            if len(values['C2']) != 4:
                invalidos.append('Para fazer a Consulta 2, insira um valor no campo determinado')
            elif len(values['C2']) == 4:
                x = [int(i) for i in values['C2'] if i.isdigit()]
                if len(x) == 0 or (x[0] <= 0000 or x[0] >= 2022):
                    invalidos.append('Ano da Consulta 2 deve ser maior que 0000 e menor que 2022')
                else:
                    self.num = x[0]
        elif c == 3:    # Para caso Consulta 3
            if(len(values['C3']) == 0):
                invalidos.append('Para fazer a Consulta 3, insira um nome de autor no campo determinado')
            else:
                nums = [int(x) for x in values['C3'].split() if x.isdigit()]
                if len(nums) != 0:
                    invalidos.append('Para fazer a Consulta 3, insira um nome de autor válido no campo determinado')
            
        return invalidos    # Retorno da lista de erros encontrados

    def startConsulta(self):    # Execução da Tela
        
        columns = [ # Conjunto de atributos retornados nas consultas 1, 2 e 3, respectivamente
            ['username', 'nome', 'quantidade'], ['username', 'nome', 'quantidade'], ['nome Livro', 'edição', 'avaliação média']
            ]

        while True:
            event, values = self.window.read()  # Constantemente analisar os vlaores da tela e mostrá-la
            if event == sg.WIN_CLOSED or event == 'Menu':    # Caso feche
                self.window.close()
                return 1    # Retorno indicando para voltar à Tela de Menu
            elif event == 'Consulta 1' or event == 'Consulta 2' or event == 'Consulta 3':   # Em caso de alguma consulta ser selecionada

                query = [int(x) for x in event.split() if x.isdigit()]  # Obter dígito da consulta selecionada
                invalidos = self.validation(query[0], values)   # Verificar se campo selecionado está válido

                if(len(invalidos) == 0):    # Em caso de nenhum erro
                    # Lista de comandos
                    commands = [# Este comando visa a busca de username, nome e contagem do total de livros, de determinada série inserida, comprados. Ordenação do usuário que mais comprou para o menor
                        "SELECT CL.usuario, CL.nome, COUNT(*) AS \"QUANTIDADE\" FROM CLIENTE CL JOIN ( SELECT C.cliente, C.datahora FROM COMPRA C JOIN POSSUI P ON C.cliente = P.cliente AND C.datahora = P.datahora WHERE UPPER(livro) LIKE ('%{}%') ) AS R ON CL.usuario = R.cliente GROUP BY CL.usuario, CL.nome ORDER BY COUNT(*) DESC".format(values['C1'].upper()),
                        # Este, por sua vez, visa usernames, nomes e contagem do total de coleções compradas por usuários. Sendo considerado apenas o período inserido pelo usuário
                        "SELECT CL.usuario, CL.nome, COUNT(*) FROM CLIENTE CL JOIN (SELECT C.cliente, C.datahora FROM COMPRA C JOIN (SELECT * FROM DETEM WHERE EXTRACT(YEAR FROM datahoraCompra) >= {}) AS DT ON DT.cliente = C.cliente AND C.datahora = DT.datahoraCompra ) AS R ON R.CLIENTE = CL.USUARIO GROUP BY CL.usuario, CL.nome ORDER BY COUNT(*) DESC".format(self.num),
                        # Por fim, buscar todos os nomes de livros, suas edições e avaliação média associados a determinado autor(a) inserido
                        "SELECT L.nome, L.edicao, L.avaliacaoMedia FROM LIVRO L JOIN PUBLICA P on L.nome = P.livro JOIN AUTOR A on P.autor = A.cpf WHERE UPPER(A.nome) = '{}'".format(values['C3'].upper())
                    ]

                    try:    # Executar o determinado comando, passar suas colunas por parâmetro e exibir tabela de resultados
                        self.cursor.execute(commands[query[0] - 1])
                        poluted = str(self.cursor.fetchall())
                        print(poluted)

                        poluted = poluted.split("), (")

                        poluted[0] = poluted[0][2:len(poluted[0])]

                        poluted[len(poluted)-1] = poluted[len(poluted)-1][0:len(poluted[len(poluted)-1])-2]
                        cleaned = []

                        for line in poluted:
                            cleaned.append(line.split(","))
                        self.show_results(columns[query[0] - 1], cleaned, str(event))   # Chamada da tela de resultados
                    except sql.Error as e:
                        sg.popup('Ocorreu um erro!\n{0}'.format(e)) # Em caso de erro, um pop-up indicará oque ocorreu
                else:
                    errors = ''
                    for strs in invalidos:       # Impressão de todos os erros do formulário
                        errors += strs + '\n'
                    sg.popup(errors)