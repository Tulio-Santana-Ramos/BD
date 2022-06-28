import PySimpleGUI as sg
import psycopg2 as sql

class TelaInicial:

    def __init__(self):
        sg.theme('Dark Amber')
        self.layout = [[sg.Text(
                        "Seja Bem Vindo!\nAtravés dessa interface será possível acessar o sistema da Webook\nInsira login e senha de administrator:\n")],
                        [sg.Text('Usuário', size = (7, 1)), sg.InputText()],
                        [sg.Text('Senha', size = (7, 1)), sg.InputText("", key = 'Password', password_char = '*')],
                        [sg.Button('Login'), sg.Button('Sair da Aplicação')]
                    ]
        self.window = sg.Window('Webook', self.layout, margins = (25, 30), finalize = True, font = 'arial 12')

    def start(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Sair da Aplicação':
                self.window.close()
                break
            elif event == 'Login':
                try:
                    connection = sql.connect(database = 'postgres', user = values[0], password = values[1], host = '127.0.0.1', port = '5432')
                    self.window.Close()
                    return connection
                except:
                    sg.popup('Houve um erro durante seu login, tente novamente')