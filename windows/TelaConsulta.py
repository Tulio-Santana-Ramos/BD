import PySimpleGUI as sg
import psycopg2 as sql

class TelaConsulta:

    def __init__(self, con):
        sg.theme('Dark Amber')
        self.layout = [[sg.Text(
                        "Você agora tem acesso ao banco de dados de nossa companhia.\n\nEm caso de alteração das tabelas, lembre-se de utilizar de efetuar o commit e/ou callback.\n\nNão é necessário inserir ' ; ' ao final de seus comandos\n\n")],
                        [sg.Text('Query SQL'), sg.InputText()], [sg.Button('Executar Comando'), sg.Button('Commit'), sg.Button('Rollback'), sg.Button('Encerrar Operações')]
                    ]
        self.connection = con
        self.cursor = self.connection.cursor()
        self.window = sg.Window('Webook', self.layout, margins = (25, 30), finalize = True, font = 'arial 12')

    def startConsulta(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Encerrar Operações':
                sg.popup('Até uma próxima oportunidade!')
                self.cursor.close()
                self.connection.close()
                self.window.close()
                break
            elif event == 'Executar Comando':
                try:
                    self.cursor.execute(str(values[0]))
                    if(str(values[0]).lower().find('select') != -1):
                        result = self.cursor.fetchall()
                        for row in result:
                            print(str(row))             
                except:
                    sg.popup('Houve um problema na execução de sua query, tente verificá-la novamente')
            elif event == 'Commit':
                try:
                    self.cursor.execute(str(values[0]))
                    self.connection.commit()
                    print('Commit efetuado com sucesso')
                except:
                    sg.popup('Houve um erro durante o commit, verifique a conexão com o banco e a query inserida')
            elif event == 'Rollback':
                try:
                    self.connection.rollback()
                    print('Rollback efetuado com sucesso')
                except:
                    sg.popup('Houve um erro durante o roolback, verifique sua conexão com o banco de dados')