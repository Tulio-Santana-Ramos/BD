"""
Eduardo Henrique Porto Silva - 11796656
Israel Felipe da Silva - 11796531
Tulio Santana Ramos - 11795526
São Carlos
2022
"""
import PySimpleGUI as sg

class TelaMenu:

    def __init__(self): # Construtor -> Declaração dos componentes da Tela e montagem de layout
        sg.theme('Dark Amber')
        self.layout = [[sg.Text(
                        "Você agora tem acesso ao banco de dados de nossa companhia.\n\nSelecione abaixo qual operação deseja efetuar:\n\n")],
                        [sg.Button('Inserir Livro'), sg.Button('Consultar'), sg.Button('Encerrar Sessão')]
                    ]
        self.window = sg.Window('Webook', self.layout, margins = (25, 30), finalize = True, font = 'arial 12')

    def startMenu(self):    # Execução da Tela
        while True:
            event, values = self.window.read()  # Constantemente analisar os valores da tela e mostrá-la
            if event == sg.WIN_CLOSED or event == 'Encerrar Sessão':    # Caso feche
                self.window.close()
                return 0  # Retorno indicando para voltar à Tela de Login
            elif event == 'Inserir Livro' or event == 'Consultar':  # Caso selecione alguma operação específica
                self.window.close()
                if(event == 'Inserir Livro'):   return 2    # Retorno indicando para ir à Tela de Inserção
                elif(event == 'Consultar'): return 3        # Retorno indicando para ir à Tela de Consulta