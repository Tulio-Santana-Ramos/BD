import PySimpleGUI as sg
import psycopg2 as sql

class TelaInserir():

    def __init__(self, con): # Construtor -> Declaração dos componentes da Tela e montagem de layout
        sg.theme('Dark Amber')
        self.layout = [[sg.Text("Para realizar uma inserção de Livro, precisa-se das seguintes informações:\nPor favor crie novos Autor e Editora, além do Livro\nEm caso de campos nulos, apenas deixe o campo vazio\n")],
                        [sg.Text('Nome-Livro', size = (12, 1)), sg.InputText(key = 'NL')], [sg.Text('Edição', size = (12, 1)), sg.InputText(key = 'LE')],
                        [sg.Text('Ano Publicação', size = (12, 1)), sg.InputText(key = 'LA')], [sg.Text('Sinopse', size = (12, 1)), sg.InputText(key = 'S')],
                        [sg.Text('Avaliação Livro', size = (12, 1)), sg.InputText(key = 'AML')], [sg.Text('Faixa Etária', size = (12, 1)), sg.InputText(key = 'FE')],
                        [sg.Text('Preço', size = (12, 1)), sg.InputText(key = 'LP')], [sg.Radio('Ebook', "RADIO", key = 'Ebook'), sg.Radio('AudioBook', "RADIO", key = 'AudioBook'), sg.Radio('Ambos', "RADIO", key = 'Ambos')],
                        [sg.Text('\nA seguir, insira informações do Autor deste Livro:\n')],
                        [sg.Text('Nome-Autor', size = (12, 1)), sg.InputText(key = 'NA')], [sg.Text('CPF-Autor', size = (12, 1)), sg.InputText(key = 'CPFA')],
                        [sg.Text('Número Livros', size = (12, 1)), sg.InputText(key = 'QLA')], [sg.Text('Email-Autor', size = (12, 1)), sg.InputText(key = 'EA')],
                        [sg.Text('Tel-Autor', size = (12, 1)), sg.InputText(key = 'TA')], [sg.Text('\nPor fim, informe os dados da Editora associada:\n')],
                        [sg.Text('Nome-Editora', size = (12, 1)), sg.InputText(key = 'NE')], [sg.Text('Email-Editora', size = (12, 1)), sg.InputText(key = 'EE')],
                        [sg.Text('CNPJ Editora', size = (12, 1)), sg.InputText(key = 'CNPJ')], [sg.Text('Tel-Editora', size = (12, 1)), sg.InputText(key = 'TE')],
                        [sg.Text('Número Livros', size = (12, 1)), sg.InputText(key = 'QLP')], [sg.Text('Avaliação Editora', size = (12, 1)), sg.InputText(key = 'AME')],
                        [sg.Button('Executar Comando'), sg.Button('Commit'), sg.Button('Rollback'), sg.Button('Menu')]
                    ]
        self.connection = con
        self.cursor = self.connection.cursor()
        self.window = sg.Window('Webook', self.layout, margins = (25, 30), finalize = True, font = 'arial 12')
        self.status = 0

    def validation(self, values):   # Verificação dos Campos
        invalidos = []  # Array para armazenar mensagens de erro

        if len(values['NL']) == 0:  # Checa Nome do Livro, é chave primária
            invalidos.append('Nome-Livro não pode ser nulo')

        if len(values['LE']) == 0:    # Checa Edição do Livro
            invalidos.append('Edição não pode ser nulo')
        elif len(values['LE']) > 0:
            x = [int(i) for i in str(values['LE']) if i.isdigit()]
            if len(x) == 0 or (x[0] <= 0):
                invalidos.append('Edição deve ser igual ou maior que 1')

        if len(values['LA']) != 0 and len(values['LA']) != 4:    # Checa Ano de Publicação do Livro
            invalidos.append('Ano de Publicação deve ter 4 dígitos ou ser nulo')
        elif len(values['LA']) == 4:
            x = [int(i) for i in str(values['LA']) if i.isdigit()]
            if len(x) == 0 or (x[0] <= 0000 or x[0] > 2022):
                invalidos.append('Ano de publicação deve ser maior que 0000 e não pode exceder 2022')

        if len(values['AML']) > 0:    # Checa Avaliação do Livro
            x = [int(i) for i in str(values['AML']) if i.isdigit()]
            if len(x) == 0 or (x[0] > 10 or x[0] < 0):
                invalidos.append('Avaliação Livro pode ser nula ou entre 0 e 10')

        if len(values['FE']) > 0:      # Checa Faixa Etária do Livro
            x = [int(i) for i in str(values['FE']) if i.isdigit()]
            if len(x) == 0 or (x[0] > 18 or x[0] < 0):
                invalidos.append('Faixa Etária pode ser nula ou entre 0 e 18')

        if len(values['LP']) > 0:    # Checa Preço do Livro
            x = [int(i) for i in str(values['AML']) if i.isdigit()]
            if len(x) == 0 or (x[0] < 0):
                invalidos.append('Preço deve ser maior que 0')

        if not values['Ebook'] and not values['AudioBook'] and not values['Ambos']:    # Checa Tipo do Livro no sistema
            invalidos.append('Deve ser selecionado o tipo de Livro')
        elif values['Ebook']:
            self.status = 0
        elif values['AudioBook']:
            self.status = 1
        elif values['Ambos']:
            self.status = 2

        if len(values['CPFA']) == 0:    # Checa CPF do Autor, chave primária
            invalidos.append('CPF Autor não pode ser nulo')

        if len(values['QLA']) > 0:    # Checa Quantidade de Livros Publicados pelo Autor
            x = [int(i) for i in str(values['QLA']) if i.isdigit()]
            if len(x) == 0 or (x[0] < 0):
                invalidos.append('Publicados Autor pode ser nulo ou maior que -1')

        if len(values['NE']) == 0:    # Checa Nome da Editora, chave primária
            invalidos.append('Nome-Editora não pode ser nulo')

        if len(values['QLP']) > 0:    # Checa Quantidade de Livros Pubicados pela Editora
            x = [int(i) for i in str(values['QLP']) if i.isdigit()]
            if len(x) == 0 or (x[0] < 0):
                invalidos.append('Publicados pela Editora pode ser nulo ou maior que -1')

        if len(values['AME']) > 0:    # Checa Avaliação da Editora
            x = [int(i) for i in str(values['AME']) if i.isdigit()]
            if len(x) == 0 or (x[0] > 10 or x[0] < 0):
                invalidos.append('Avaliação Editora pode ser nula ou entre 0 e 10')

        return invalidos    # Retorno da lista de erros encontrados

    def bookType(self): # Verifica tipo de Livro adicionado
        invalidos, comando = [], []
        if self.status == 0:
            layout = [[sg.Text("Insira abaixo os dados específicos do Ebook\n\n")], [sg.Text('Número Páginas', size = (12, 1)), sg.InputText(key = 'PagE')], [sg.Button('Finalizar')]]
        elif self.status == 1:
            layout = [[sg.Text("Insira abaixo os dados específicos do Audiobook\n\n")], [sg.Text('Duração', size = (12, 1)), sg.InputText(key = 'DurA')],
            [sg.Text('Dublador', size = (12, 1)), sg.InputText(key = 'DubA')], [sg.Button('Finalizar')]]
            tipo = 2
        elif self.status == 2:
            layout = [[sg.Text("Insira abaixo os dados específicos dos livros\n\n")], [sg.Text('Número Páginas', size = (12, 1)), sg.InputText(key = 'PagE')],
            [sg.Text('Duração', size = (12, 1)), sg.InputText(key = 'DurA')], [sg.Text('Dublador', size = (12, 1)), sg.InputText(key = 'DubA')], [sg.Button('Finalizar')]]
            tipo = 3
        janela = sg.Window('Webook', layout, margins = (25, 30), finalize = True, font = 'arial 12')

        while True:
            event, values = janela.read()
            if event == sg.WIN_CLOSED or event == 'Finalizar':
                if self.status == 0:
                    if len(values['PagE']) > 0:    # Checa Número de Páginas
                        x = [int(i) for i in values['PagE'] if i.isdigit()]
                        if len(x) == 0 or (x[0] < 0):
                            invalidos.append('Número de páginas não pode ser nulo e deve ser menor que 0')
                elif self.status == 1:
                    if len(values['DurA']) > 0:    # Checa Duração
                        x = [int(i) for i in values['DurA'] if i.isdigit()]
                        if len(x) == 0 or (x[0] < 0):
                            invalidos.append('Duração deve ser inserida em minutos e não pode ser menor que 0')
                elif self.status == 2:
                    if len(values['PagE']) > 0:    # Checa Número de Páginas
                        x = [int(i) for i in values['PagE'] if i.isdigit()]
                        if len(x) == 0 or (x[0] < 0):
                            invalidos.append('Número de páginas não pode ser nulo e deve ser menor que 0')
                    if len(values['DurA']) > 0:    # Checa Duração
                        x = [int(i) for i in values['DurA'] if i.isdigit()]
                        if len(x) == 0 or (x[0] < 0):
                            invalidos.append('Duração deve ser inserida em minutos e não pode ser menor que 0')
                if len(invalidos) == 0:
                    for i in values:    # Preenchimento de valores nulos
                        if(len(i) == 0):
                            i = 'NULL'
                        comando.append(i)
                    janela.close()
                    return comando  # Retorno dos valores obtidos
                else:
                    errors = ''
                    for str in invalidos:       # Impressão de todos os erros do formulário
                        errors += str + '\n'
                    sg.popup(errors)

    def startInserir(self):    # Execução da Tela
        operation = False
        while True:
            event, values = self.window.read()  # Constantemente analisar os vlaores da tela e mostrá-la
            if event == sg.WIN_CLOSED or event == 'Menu':    # Caso feche
                self.window.close()
                return 1    # Retorno indicando para voltar à Tela de Menu
            elif event == 'Executar Comando' or event == 'Commit':  # Caso de Execução e/ou Commit
                invalidos = self.validation(values) # Busca por erros no formulário

                if(len(invalidos) == 0): # Caso não haja erros no formulário
                    for i in values:    # Preenchimento de valores nulos
                        if(len(i) == 0):
                            i = 'NULL'
                    tipos = self.bookType()
                    commands = [    # Este comando visa a inserção de um novo usuário. Isto é necessário visto que também estamos criando uma Editora
                        "INSERT INTO USUARIO (username, tipo, email, telefone) VALUES ('{}', '{}','{}','{}')"
                        .format(values['NE'], 0, values['EE'], values['TE']),
                        # Este, por sua vez, possibilita a criação da Editora, possível uma vez vez que o usuário base foi devidamente criado
                        "INSERT INTO EDITORA (usuario, qtdLivrosPublicados, avaliacaoMedia, cnpj, status) VALUES ('{}', '{}', '{}', '{}', '{}')".format(values['NE'], values['QLP'], values['AME'], values['CNPJ'], 1),
                        # Agora, criaremos o Autor associado à confecção deste Livro
                        "INSERT INTO AUTOR (cpf, nome, qtLivrosPublicados, email, telefone) VALUES ('{}', '{}', '{}', '{}', '{}')".format(values['CPFA'], values['NA'], values['QLA'], values['EA'], values['TA']),
                        # Então, criaremos o Livro com as informações passadas no formulário
                        "INSERT INTO LIVRO (nome, edicao, anoPublicacao, sinopse, avaliacaoMedia, faixaEtaria, preco) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(values['NL'], values['LE'], values['LA'], values['S'], values['AML'], values['FE'], values['LP']),
                        # Por fim, associaremos todas as entidades com uma nova entrada na tabela de Publica
                        "INSERT INTO PUBLICA (livro, autor, editora) VALUES ('{}', '{}', '{}')".format(values['NL'], values['CPFA'], values['NE'])
                    ]
                    try:
                        for ex in commands: # Execução dos comandos
                            self.cursor.execute(ex)
                            if(event == 'Commit'):
                                self.connection.commit()
                                operation = True
                        if(len(tipos) == 1):    # Para caso de ebook
                            self.cursor.execute("INSERT INTO EBOOK (livro, numPaginas) VALUES ('{}', '{}')".format(values['NE'], tipos[0]))
                            if(event == 'Commit'):
                                self.connection.commit()
                                operation = True
                        elif(len(tipos) == 2):  # Para caso de audio book
                            self.cursor.execute("INSERT INTO AUDIOBOOK (livro, duracao, dublador) VALUES ('{}', '{}', '{}')".format(values['NE'], tipos[0], tipos[1]))
                            if(event == 'Commit'):
                                self.connection.commit()
                                operation = True
                        elif(len(tipos) == 3):  # Para caso de ambos
                            self.cursor.execute("INSERT INTO EBOOK (livro, numPaginas) VALUES ('{}', '{}')".format(values['NE'], tipos[0]))
                            if(event == 'Commit'):
                                self.connection.commit()
                                operation = True
                            self.cursor.execute("INSERT INTO AUDIOBOOK (livro, duracao, dublador) VALUES ('{}', '{}', '{}')".format(values['NE'], tipos[1], tipos[2]))
                            if(event == 'Commit'):
                                self.connection.commit()
                                operation = True

                    except sql.Error as e:
                        sg.popup('Ocorreu um erro!\n{0}'.format(e)) # Em caso de erro, um pop-up indicará oque ocorreu
                else:
                    errors = ''
                    for str in invalidos:       # Impressão de todos os erros do formulário
                        errors += str + '\n'
                    sg.popup(errors)
            elif event == 'Rollback' and operation: # Em caso de rollback
                try:
                    self.connection.rollback()
                    sg.popup('Rollback efetuado com sucesso!')
                except sql.Error as e:
                    sg.popup('Ocorreu um erro!\n{0}'.format(e)) # Em caso de erro, um pop-up indicará oque ocorreu
            elif event == 'Rollback' and not operation: # Em caso de rollback sem operação anterior
                sg.popup('Este comando só pode ser executado após um commit')