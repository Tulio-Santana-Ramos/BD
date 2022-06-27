import windows.TelaInicial as TelaInicial
import windows.TelaConsulta as TelaConsulta

def main():
    Inicio = TelaInicial.TelaInicial()
    sql = Inicio.start()
    commands = TelaConsulta.TelaConsulta(sql)
    commands.start()