import windows.TelaInicial as TelaInicial
import windows.TelaConsulta as TelaConsulta

def main():
    Inicio = TelaInicial.TelaInicial()
    sql = Inicio.start()
    if(sql != 0):
        commands = TelaConsulta.TelaConsulta(sql)
        commands.start()

main()