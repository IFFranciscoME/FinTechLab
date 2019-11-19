
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Juego de Trazo Maximo con Inteligencia Artificial (Minimax)                                         -- #
# -- Repositorio:                                                                                                  -- #
# -- FranciscoME                                                                                                   -- #
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np


# -- ------------------------------------------------------------------------- Funcion Global : Entrada de usuario -- #
# ------------------------------------------------------------------------------------------------------------------- #

def input_usuario():

    print("------------------------------------------------------------- ")
    print("------------ ¿Qué movimiento quieres hacer? ----------------- ")
    print("------------------------------------------------------------- ")
    in_mov = int(input("'1 => arriba', '2 => derecha', '3 => abajo', '4 => izquierda' "))
    if in_mov == 1:
        return 'arriba'
    elif in_mov == 2:
        return 'derecha'
    elif in_mov == 3:
        return 'abajo'
    elif in_mov == 4:
        return 'izquierda'
    else:
        print(" \n ")
        print("************************************************************* ")
        print("******** Movimiento no valido, intenta de nuevo ************* ")
        print("************************************************************* ")
        print(" \n ")

        return input_usuario()


# -- ---------------------------------------------------------------------------------------------- Clase: Tablero -- #
# ------------------------------------------------------------------------------------------------------------------- #

class Tablero(object):

    # Inicializar el tablero
    def __init__(self, tab_size, tab_min, tab_max, tab_dif, tab_player):
        # El tamaño del tablero [8, 8]
        self.tab_size = tab_size
        # Valor minimo para simular los aleatorios
        self.tab_min = tab_min
        # Valor maximo para simular los aleatorios
        self.tab_max = tab_max
        # Nivel de dificultad
        self.tab_dif = tab_dif
        # Nombre del jugador
        self.tab_player = tab_player
        # Celdas dentro de tablero
        self.tab_celdas = [[Celda(cel_valor=np.random.randint(tab_min, tab_max), cel_posicion=(i, j))
                            for j in range(tab_size)] for i in range(tab_size)]

    def __str__(self):
        res = ""
        for i in range(len(self.tab_celdas)):
            for j in range(len(self.tab_celdas)):
                res += f'|__{self.tab_celdas[i][j]}__'
            res += '|\n'
        return res


# -- ------------------------------------------------------------------------------------------------ Clase: Celda -- #
# ------------------------------------------------------------------------------------------------------------------- #

class Celda(object):
    def __init__(self, cel_valor, cel_posicion):
        # Valor dentro de la celda
        self.cel_valor = cel_valor
        # Ubicacion en el tablero de la celda
        self.cel_posicion = cel_posicion
        # Para identificar si la celda fue visitada (independiente de quien la visito)
        self.cel_visitada = False
        # Para identificar el jugador que visito la celda
        self.cel_visitante = None


# Validar
# input_usuario()
# mientras no ocurra termino
# mostrar tablero
# pedir entrada de jugador
# validar que sea entreada valida
# mover jugador actualizando tablero
# mostrar tablero actualizado
# calcular entrada cpu
# mover jugador actualizando tablero
# mostrar tablero actualizado

# -- ------------------------------------------------------------------------------------------------ Seccion Main -- #
# ------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    # Mensaje de bienvenida
    print('\nSkynet: ¿Estás listo? \n')
    # solicitar Dificultad
    in_dif = int(input("Elige dificultad | 3 => 'facil', '5 => 'dificil: "))

    # solicitar min para aleatorios
    in_min = int(input("Ingresa el numero mínimo para aleatorios (entero > 0): "))

    # solicitar max para aleatorios
    in_max = int(input("Ingresa el numero máximo para aleatorios (entero > 0): "))

    # solicitar tamaño de matriz
    in_mat = int(input("Ingresa el valor de N para la matriz N x N (entero > 2): "))

    # solicitar nombre de jugador
    in_nom = str(input("Ingresa el nombre del jugador: "))

    # imprimir mensaje de inicio
    print("\n ... Inicializando Juego ... \n")

    # Inicializar tablero
    juego_tablero = Tablero(tab_min=1, tab_max=15, tab_size=8, tab_player=in_nom, tab_dif=in_dif)

    # Imprimir tablero
    print(juego_tablero)

