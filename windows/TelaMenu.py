import PySimpleGUI as sg
import psycopg2 as sql

class TelaMenu:

    def __init__(self, con):
        sg.theme('Dark Amber')
        self.layout = [[sg.Text(
                        "Você agora tem acesso ao banco de dados de nossa companhia.\n\nSelecione abaixo qual operação deseja efetuar:\n\n")],
                        [sg.Button('Inserir Livro'), sg.Button('Consultar'), sg.Button('Encerrar Sessão')]
                    ]
        self.connection = con
        self.cursor = self.connection.cursor()
        self.window = sg.Window('Webook', self.layout, margins = (25, 30), finalize = True, font = 'arial 12')

    def startMenu(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Encerrar Sessão':
                self.window.close()
                if(event == 'Encerrar Sessão'):   return 0
            elif event == 'Inserir Livro' or event == 'Consultar':
                self.window.close()
                if(event == 'Inserir Livro'):   return 2
                elif(event == 'Consultar'): return 3