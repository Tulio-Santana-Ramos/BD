import PySimpleGUI as sg
import psycopg2 as sql

class TelaInicial:

    def __init__(self): # Construtor -> Declaração dos componentes da Tela e montagem de layout
        sg.theme('Dark Amber')
        self.layout = [[sg.Text(
                        "Seja Bem Vindo!\n\nAtravés dessa interface será possível acessar o sistema da Webook\n\nInsira login e senha de administrator:\n\n")],
                        [sg.Text('Usuário', size = (7, 1)), sg.InputText()],
                        [sg.Text('Senha', size = (7, 1)), sg.InputText(password_char = '*')],
                        [sg.Button('Login'), sg.Button('Sair da Aplicação')]
                    ]
        self.window = sg.Window('Webook', self.layout, margins = (25, 30), finalize = True, font = 'arial 12')

    def startInicial(self): # Execução da Tela
        while True:
            event, values = self.window.read()  # Constantemente analisar os vlaores da tela e mostrá-la
            if event == sg.WIN_CLOSED or event == 'Sair da Aplicação':  # Caso feche
                self.window.close()
                return -1   # Retorno indicando saída total da aplicação
            elif event == 'Login':  # Caso tente logar
                try:    # Conexão com a Base de Dados -> Para testes, altere o nome de 'database' para o nome de sua database
                    connection = sql.connect(database = 'projeto', user = str(values[0]), password = str(values[1]), host = "localhost")
                    self.window.close()
                    return connection   # Uma vez conectado, retorna-se o objeto connection e fecha-se a tela
                except sql.Error as e:
                    sg.popup('Ocorreu um erro!\n{0}'.format(e)) # Em caso de erro, um pop-up indicará oque ocorreu