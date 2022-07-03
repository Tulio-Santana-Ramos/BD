import windows.TelaInicial as TelaInicial
import windows.TelaMenu as TelaMenu
import windows.TelaInserir as TelaInserir
import windows.TelaConsulta as TelaConsulta

def main():
    screen = 0  # Seleção de qual tela deve ser utilizada

    while True: # Enquanto usuário não optar por sair
        match screen:
            case 0: # Tela Inicial de Login
                start = TelaInicial.TelaInicial()
                con = start.startInicial()
                if(con == -1):  # Verifica se usuário optou por fechar a aplicação
                    screen = -1
                elif(type(con) != int):  # Verifica se objeto de conexão foi retornado
                    screen = 1

            case 1: # Tela do Menu
                menu = TelaMenu.TelaMenu()
                screen = menu.startMenu()

            case 2: # Tela de Inserção Livro
                insert = TelaInserir.TelaInserir(con)
                screen = insert.startInserir()

            case 3: # Tela de Consulta
                consult = TelaConsulta.TelaConsulta(con)
                screen = consult.startConsulta()

            case -1: # Finalização do programa
                break

main()