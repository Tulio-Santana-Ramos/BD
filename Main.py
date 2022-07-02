import windows.TelaInicial as TelaInicial
import windows.TelaMenu as TelaMenu
import windows.TelaInserir as TelaInserir
import windows.TelaConsulta as TelaConsulta

def main():
    start, menu = TelaInicial.TelaInicial(), TelaMenu.Menu()
    sql, screen = None, 0

    while True:
        match screen:
            case 0: # Tela Inicial de Login
                sql = start.startInicial()
                if(sql == -1):  screen = -1
                else: screen = 1

            case 1: # Tela do Menu
                screen = menu.startMenu()

            case 2: # Tela de Inserção Livro
                insert = TelaInserir.TelaInserir(sql)
                screen = insert.startInserir()

            case 3: # Tela de Consulta
                consult = TelaConsulta.TelaConsulta(sql)
                screen = consult.startConsulta()

            case -1: # Finalização do programa
                break

main()