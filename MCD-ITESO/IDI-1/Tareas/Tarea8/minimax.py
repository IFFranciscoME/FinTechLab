
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Juego de Trazo Maximo con Inteligencia Artificial (Minimax)                                         -- #
# -- Repositorio:                                                                                                  -- #
# -- FranciscoME                                                                                                   -- #
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np
# import time


# -- ------------------------------------------------------------------------- Funcion Global : Entrada de usuario -- #
# ------------------------------------------------------------------------------------------------------------------- #

def jugar():
    # While con bandera de si el juego termino

    # Solicitar movimiento a jugador
    movimiento = input_usuario()
    # Verificar que sea movimiento valido

    # Actualizar celda destino con movimiento de jugador
    # Calcular Score de tablero
    # Desplegar score en el tablero
    # Mostrar mensaje que cpu esta moviendo
    # Calcular movimiento a cpu
    # Actualizar celda destino con movimiento de cpu
    # Calcular score de tablero

    # Repetir proceso mientras no haya un Break en el while


def input_usuario():

    print("---------- ¿Qué movimiento quieres hacer? --------------- ")
    print("---------- ------------------------------ --------------- ")
    print("  1 = arriba, 2 = derecha, 3 = abajo, 4 = izquierda       ")
    print("---------- ------------------------------ --------------- ")
    in_mov = int(input("Movimiento: "))

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
        print("** Movimiento no valido, intenta de nuevo ** ")
        print(" \n ")

        return input_usuario()


# -- ---------------------------------------------------------------------------------------------- Clase: Tablero -- #
# ------------------------------------------------------------------------------------------------------------------- #

class Jugador(object):
    def __init__(self, jug_posicion, jug_iscpu):
        """
        :param jug_posicion: list : [1, 2] : posicion en el tablero del jugador
        :param jug_iscpu: bool : True/False : bandera si el jugador es cpu (si no es cpu es humano)
        """
        # Inicializar la posicion en el tablero del jugador
        self.jug_posicion = jug_posicion
        # Inicializar la bandera sobre si el jugador es el CPU
        self.jug_iscpu = jug_iscpu
        # Inicializar el nombre del jugador
        self.jug_nombre = None
        #  Inicializar el simbolo en el tablero del jugador
        self.jug_simbolo = None


# -- ---------------------------------------------------------------------------------------------- Clase: Tablero -- #
# ------------------------------------------------------------------------------------------------------------------- #

class Tablero(object):

    # Inicializar el tablero
    def __init__(self, tab_score, tab_size, tab_min, tab_max, tab_dif, tab_player):
        # El score del tablero
        self.tab_score = tab_score
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

        # inicializar en celda (0, 0) a CPU
        # inicializar en celda (N, N) a Persona

    def __str__(self):
        res = "\n"
        # Filas
        for i in range(len(self.tab_celdas)):
            # Columnas
            res += '|'
            for j in range(len(self.tab_celdas)):
                res += f'{self.tab_celdas[i][j]}|'
            res += '\n'
        return res


# -- ------------------------------------------------------------------------------------------------ Clase: Celda -- #
# ------------------------------------------------------------------------------------------------------------------- #

class Celda(object):
    def __init__(self, cel_valor, cel_posicion):
        """
        :param cel_valor:
        :param cel_posicion:
        """
        # Valor dentro de la celda
        self.cel_valor = cel_valor
        # Ubicacion en el tablero de la celda
        self.cel_posicion = cel_posicion
        # Para identificar si la celda fue visitada (independiente de quien la visito)
        self.cel_visitada = False
        # Para identificar el jugador que visito la celda (True == cpu, False == jugador)
        self.cel_visitante = True
        # Para usar simbolo segun jugador en la impresion del tablero
        self.cel_simbolo = '*' if self.cel_visitante else ' '

    def __str__(self):
        if len(str(self.cel_valor)) % 2 == 0:
            return f'{self.cel_simbolo} {self.cel_valor} {self.cel_simbolo}'
        else:
            return f'{self.cel_simbolo} 0{self.cel_valor} {self.cel_simbolo}'

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

    # -- -------------------------------------------------------------------------------- Inicializacion del juego -- #
    # Mensaje de bienvenida
    # print('\n \nSkynet: ¿Estás listo? \n')
    # input("Press Enter to continue...\n")
    # time.sleep(0.5)

    # solicitar Dificultad
    # in_dif = int(input("Elige dificultad | 3 => 'facil', '5 => 'dificil: "))
    in_dif = 3

    # solicitar min para aleatorios
    # in_min = int(input("Ingresa el numero mínimo para aleatorios (entero > 0): "))
    in_min = 10

    # solicitar max para aleatorios
    # in_max = int(input("Ingresa el numero máximo para aleatorios (entero > 0): "))
    in_max = 20

    # solicitar tamaño de matriz
    # in_mat = int(input("Ingresa el valor de N para la matriz N x N (entero > 2): "))
    in_mat = 8

    # solicitar nombre de jugador
    # in_nom = str(input("Ingresa el nombre del jugador: "))
    in_nom = 'jugador'

    # Dinamica John Connor
    # loading = 'John Connor'
    # time.sleep(2)
    # print('\nBuen intento ...\n')
    # time.sleep(2)
    # for i in range(11):
    #    print(loading[i], sep='', end=' ', flush=True)
    #    time.sleep(0.25)

    # imprimir mensaje de inicio
    # time.sleep(3)
    # print("\n \n ................ Dia del Juicio Final ................ \n")
    # time.sleep(2)

    # Inicializar tablero
    juego_tablero = Tablero(tab_min=in_min, tab_max=in_max, tab_size=in_mat,
                            tab_player=in_nom, tab_dif=in_dif, tab_score=0)

    # Inicializar jugadores
    jug_0 = Jugador(jug_posicion=[0, 0], jug_iscpu=True)
    jug_1 = Jugador(jug_posicion=[in_mat, in_mat], jug_iscpu=False)

    # Imprimir tablero
    print(juego_tablero)
    # time.sleep(1.5)

    # -- ------------------------------------------------------------------------------------------ Ciclo de juego -- #

    # Funcion jugar
    jugar()
