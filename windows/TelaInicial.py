import PySimpleGUI as sg
import psycopg2 as sql

class TelaInicial:

    def __init__(self):
        sg.theme('Dark Amber')
        self.layout = [[sg.Text(
                        "Seja Bem Vindo!\nAtravés dessa interface será possível acessar o sistema da Webook\nInsira login e senha de administrator:\n")],
                        [sg.InputText('Usuário'), sg.Input('Senha')], [sg.Button('Login'), sg.Button('Sair da Aplicação')]
                    ]
        self.window = sg.Window('Webook', self.layout)

    def start(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Sair da Aplicação':
                break
            elif event == 'Login':
                try:
                    connection = sql.connect(database = 'webook', user = values['Usuário'], password = values['Senha'], host = '127.0.0.1', port = '3000')
                    self.window.Close()
                    return connection
                except:
                    sg.popup('Houve um erro durante seu login, tente novamente')