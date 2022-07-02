import PySimpleGUI as sg
import psycopg2 as sql

class TelaInserir():

    def __init__(self, con):
        sg.theme('Dark Amber')
        self.layout = [[sg.Text(
                        "Para realizar uma inserção de Livro, preencha todos os dados abaixo\n\n")]
                    ]
        self.connection = con
        self.cursor = self.connection.cursor()
        self.window = sg.Window('Webook', self.layout, margins = (25, 30), finalize = True, font = 'arial 12')

    def startInserir(self):
        pass