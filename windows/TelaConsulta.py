import PySimpleGUI as sg
import psycopg2 as sql

class TelaConsulta:

    def __init__(self, con):
        sg.theme('Dark Amber')
        self.layout = [[sg.Text(
                        "Você agora tem acesso ao banco de dados de nosso companhia.\nEm caso de alteração das tabelas, lembre-se de utilizar de efetuar o commit e/ou callback.\n")],
                        [sg.InputText('Query SQL')], [sg.Button('Executar'), sg.Button('Commit'), sg.Button('Rollback')]
                    ]
        self.connection = con
        self.cursor = self.connection.cursor()
        self.window = sg.Window('Webook', self.layout)

    def start(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                print('Até uma próxima oportunidade!')
                self.cursor.close()
                self.connection.close()
                break
            elif event == 'Executar':
                try:
                    self.cursor.execute(values['Query SQL'])
                    for row in self.cursor:
                        print(row)
                except:
                    print('Houve um problema na execução de sua query, tente verificá-la novamente')
            elif event == 'Commit':
                try:
                    self.cursor.execute(values['Query SQL'])
                    self.connection.commit()
                    print('Commit efetuado com sucesso')
                except:
                    print('Houve um erro durante o commit, verifique a conexão com o banco e a query inserida')
            elif event == 'Rollback':
                try:
                    self.connection.rollback()
                    print('Rollback efetuado com sucesso')
                except:
                    print('Houve um erro na tentativa de roolback')