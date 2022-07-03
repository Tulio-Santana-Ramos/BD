import PySimpleGUI as sg
import psycopg2 as sql
import re
import string

class TelaConsulta:

    def __init__(self, con): # Construtor -> Declaração dos componentes da Tela e montagem de layout
        sg.theme('Dark Amber')
        self.layout = [[sg.Text("Abaixo, pode-se selecionar qual consulta se deseja efetuar no banco de dados.\n\n")],
                        [sg.Button('Consulta 1'), sg.Button('Consulta 2'), sg.Button('Consulta 3'), sg.Button('Menu')] ]
        self.connection = con
        self.cursor = self.connection.cursor()
        self.window = sg.Window('Webook', self.layout, margins = (25, 30), finalize = True, font = 'arial 12')

    def show_results(self, columns, data, title):   # Setup de nova janela, em formato de tabela, para representar as informações das consultas
        layout = [sg.Table(values = data, headings = columns, max_col_width = 30, key = 'RESULT', row_height = 35,
                justification = 'right', auto_size_columns = True, display_row_numbers = True, tooltip = 'Resultado de sua consulta')]
        res_window = sg.Window(title, layout, modal = True)

        while True:
            event = res_window.read()
            if event == sg.WIN_CLOSED:
                break
        res_window.close()

    def startInserir(self):    # Execução da Tela
        commands = [# Este comando visa a inserção de um novo usuário. Isto é necessário visto que também estamos criando uma Editora
                    'INSERT INTO USUARIO (username, tipo, email, telefone) VALUES ({},1,{},{})'.format(values['NE'], values['EE'], values['TE']),
                    # Este, por sua vez, possibilita a criação da Editora, possível uma vez vez que o usuário base foi devidamente criado
                    'INSERT INTO EDITORA (usuario, qtdLivrosPublicados, avaliacaoMedia, cnpj, status) VALUES ({}, {}, {}, {}, {})'.format(values['NE'], values['QLP'], values['AME'], values['CNPJ'], int(self.status)),
                    # Agora, criaremos o Autor associado à confecção deste Livro
                    'INSERT INTO AUTOR (cpf, nome, qtLivrosPublicados, email, telefone) VALUES ({}, {}, {}, {}, {})'.format(values['CPFA'], values['NA'], values['QLA'], values['EA'], values['TA']),
                    # Então, criaremos o Livro com as informações passadas no formulário
                    'INSERT INTO LIVRO (nome, edicao, anoPublicacao, sinopse, avaliacaoMedia, faixaEtaria, preco) VALUES ({}, {}, {}, {}, {}, {}, {})'.format(values['NL'], values['LE'], values['LA'], values['S'], values['AML'], values['FE'], values['LP']),
                    # Por fim, associaremos todas as entidades com uma nova entrada na tabela de Publica
                    'INSERT INTO PUBLICA (livro, autor, editora) VALUES ({}, {}, {})'.format(values['NL'], values['CPFA'], values['NE'])
                ]
        columns = [ # Conjunto de atributos retornados nas consultas 1, 2 e 3, respectivamente
            ['conjunto de colunas query 1'], ['conjunto de colunas query 2'], ['conjunto de colunas query 3']
            ]

        while True:
            event, values = self.window.read()  # Constantemente analisar os vlaores da tela e mostrá-la
            if event == sg.WIN_CLOSED or event == 'Menu':    # Caso feche
                self.window.close()
                return 1    # Retorno indicando para voltar à Tela de Menu
            elif event == 'Consulta 1' or event == 'Consulta 2' or event == 'Consulta 3':   # Em caso de alguma consulta ser selecionada
                query = [int(x) for x in event.split() if x.isdigit()]  # Obter dígito da consulta selecionada
                try:    # Executar o determinado comando, passar suas colunas por parâmetro e exibir tabela de resultados
                    self.cursor.execute(commands[query[0] - 1])
                    poluted = str(self.cursor.fetchall())
                    cleaned = re.sub('['+string.punctuation+']', '', poluted).split()   # Limpeza da string resultante e divisão das colunas específicas
                    self.show_results(columns[query[0] - 1], cleaned, str(event))
                except sql.Error as e:
                    sg.popup('Ocorreu um erro!\n{0}'.format(e)) # Em caso de erro, um pop-up indicará oque ocorreu