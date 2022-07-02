import PySimpleGUI as sg
import psycopg2 as sql
import re

class TelaInserir():

    def __init__(self, con): # Construtor -> Declaração dos componentes da Tela e montagem de layout
        sg.theme('Dark Amber')
        self.layout = [[sg.Text("Para realizar uma inserção de Livro, precisa-se das seguintes informações:\n\n")],
                        [sg.Text('Nome-Livro', size = (12, 1)), sg.InputText(key = 'NL')], [sg.Text('Edição', size = (12, 1)), sg.InputText(key = 'LE')],
                        [sg.Text('Ano Publicação', size = (12, 1)), sg.InputText(key = 'LA')], [sg.Text('Sinopse', size = (12, 1)), sg.InputText(key = 'S')],
                        [sg.Text('Avaliação Livro', size = (12, 1)), sg.InputText(key = 'AML')], [sg.Text('Faixa Etária', size = (12, 1)), sg.InputText(key = 'FE')],
                        [sg.Text('Preço', size = (12, 1)), sg.InputText(key = 'LP')],[sg.Text('\nA seguir, insira informações do Autor deste Livro:\n')],
                        [sg.Text('Nome-Autor', size = (12, 1)), sg.InputText(key = 'NA')], [sg.Text('CPF-Autor', size = (12, 1)), sg.InputText(key = 'CPFA')],
                        [sg.Text('Número Livros', size = (12, 1)), sg.InputText(key = 'QLA')], [sg.Text('Email-Autor', size = (12, 1)), sg.InputText(key = 'EA')],
                        [sg.Text('Tel-Autor', size = (12, 1)), sg.InputText(key = 'TA')], [sg.Text('\nPor fim, informe os dados da Editora associada:\n')],
                        [sg.Text('Nome-Editora', size = (12, 1)), sg.InputText(key = 'NE')], [sg.Text('Email-Editora', size = (12, 1)), sg.InputText(key = 'EE')],
                        [sg.Text('CNPJ Editora', size = (12, 1)), sg.InputText(key = 'CNPJ')], [sg.Text('Tel-Editora', size = (12, 1)), sg.InputText(key = 'TE')],
                        [sg.Text('Número Livros', size = (12, 1)), sg.InputText(key = 'QLP')], [sg.Text('Avaliação Editora', size = (12, 1)), sg.InputText(key = 'AME')],
                        [sg.Text('\nEssa Editora pode publicar?\n')], [sg.Radio('Sim', "RADIO", key = 'StatusS'), sg.Radio('Não', "RADIO", key = 'StatusN')],
                        [sg.Button('Executar Comando'), sg.Button('Commit'), sg.Button('Rollback'), sg.Button('Menu')]
                    ]
        self.connection = con
        self.cursor = self.connection.cursor()
        self.window = sg.Window('Webook', self.layout, margins = (25, 30), finalize = True, font = 'arial 12')
        self.status = False

    def validation(self, values):   # Verificação dos Campos
        invalidos = []  # Array para armazenar mensagens de erro
        emailformat = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # Checagem regex para formato de email

        if len(values['NL']) == 0:  # Checa Nome do Livro, é chave primária
            invalidos.append('Nome-Livro não pode ser nulo')

        if len(values['LE']) == 0 or int(values['LE']) <= 0:    # Checa Edição do Livro
            invalidos.append('Edição não pode ser nulo ou menor que 1')

        if len(values['LA']) > 4 or (len(values['LA']) != 0 and int(values['LA']) <= 0):    # Checa Ano de Publicação do Livro
            invalidos.append('Ano de Publicação deve ter 4 digitos e maior que 0 ou nula')

        if len(values['AML']) > 0 and int(values['AML']) < 0 and int(values['AML']) > 10:    # Checa Avaliação do Livro
            invalidos.append('Avaliação Livro pode ser nula ou entre 0 e 10')

        if len(values['FE']) > 0 and int(values['FE']) < 0 and int(values['FE']) > 18:      # Checa Faixa Etária do Livro
            invalidos.append('Faixa Etária pode ser nula ou entre 0 e 18 anos')

        if len(values['LP']) > 0 and int(values['LP']) < 0:    # Checa Preço do Livro
            invalidos.append('Preço deve ser maior que 0')

        if len(values['CPFA']) == 0:    # Checa CPF do Autor, chave primária
            invalidos.append('CPF Autor não pode ser nulo')

        if len(values['QLA']) > 0 and int(values['QLA']) < 0:    # Checa Quantidade de Livros Publicados pelo Autor
            invalidos.append('Publicados Autor pode ser nulo ou maior que -1')

        if len(values['EA']) > 0 and not re.search(values['EA'], emailformat):    # Checa Email do Autor
            invalidos.append('Email Autor pode ser nulo ou seguir o formato <string>@<string>.<string>')

        if len(values['NE']) == 0:    # Checa Nome da Editora, chave primária
            invalidos.append('Nome-Editora não pode ser nulo')

        if len(values['EE']) == 0 or (len(values['EE']) > 0 and not re.search(values['EE'], emailformat)):    # Checa Email Editora
            invalidos.append('Email Editora não pode ser nulo e deve seguir o formato <string>@<string>.<string>')

        if len(values['QLP']) > 0 and int(values['QLP']) < 0:    # Checa Quantidade de Livros Pubicados pela Editora
            invalidos.append('Publicados pela Editora pode ser nulo ou maior que -1')

        if len(values['AME']) > 0 and int(values['AME']) < 0 and int(values['AME']) > 10:    # Checa Avaliação da Editora
            invalidos.append('Avaliação Editora pode ser nula ou entre 0 e 10')

        if not values['StatusS'] and not values['StatusN']:    # Checa Status da Editora no sistema
            invalidos.append('Deve ser selecionado o Status da Editora')
        elif values['StatusS']:
            self.status = True
        elif values['StatusN']:
            self.status = False

        return invalidos    # Retorno da lista de erros encontrados

    def startInserir(self):    # Execução da Tela
        operation = False
        while True:
            event, values = self.window.read()  # Constantemente analisar os vlaores da tela e mostrá-la
            if event == sg.WIN_CLOSED or event == 'Menu':    # Caso feche
                self.window.close()
                return 1    # Retorno indicando para voltar à Tela de Menu
            elif event == 'Executar Comando' or event == 'Commit':  # Caso de Execução e/ou Commit
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
                invalidos = self.validation(values) # Busca por erros no formulário

                if(invalidos == 0): # Caso não haja erros no formulário
                    try:
                        for ex in commands: # Execução dos comandos
                            self.cursor.execute(ex)
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