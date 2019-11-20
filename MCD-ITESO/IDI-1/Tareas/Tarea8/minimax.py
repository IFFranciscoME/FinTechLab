
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Juego de Trazo Maximo con Inteligencia Artificial (Minimax)                                         -- #
# -- Repositorio:                                                                                                  -- #
# -- FranciscoME                                                                                                   -- #
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np
import time


# -- -------------------------------------------------------------------------- Funcion Global : Inicializar Juego -- #
# ------------------------------------------------------------------------------------------------------------------- #

def inicializar():
    # Jugador CPU
    jug_0 = Jugador(jug_posicion=[0, 0], jug_iscpu=True, jug_ismax=True, jug_nombre='skynet', jug_simbolo='*')
    # Jugador Humano
    jug_1 = Jugador(jug_posicion=[in_mat, in_mat], jug_iscpu=False, jug_ismax=False, jug_nombre='John Connor',
                    jug_simbolo='#')
    # Inicializar tablero
    jg_tablero = Tablero(tab_min=in_min, tab_max=in_max, tab_dims=in_mat, tab_jugs=[jug_0, jug_1], tab_dif=in_dif,
                         tab_score=0)

    # -- ----------------------------------------------------------------------------------------- Inicializar CPU -- #
    # Simbolo en celda
    jg_tablero.tab_celdas[0][0].cel_simbolo = jg_tablero.tab_jugadores[0].jug_simbolo
    # Celda visitada
    jg_tablero.tab_celdas[0][0].cel_visitada = True
    # Controlador de la celda
    jg_tablero.tab_celdas[0][0].cel_controlador = jg_tablero.tab_jugadores[0].jug_nombre
    # Posicion del jugador
    jg_tablero.tab_jugadores[0].jug_posicion[0] = 0
    jg_tablero.tab_jugadores[0].jug_posicion[1] = 0
    # Puntos del jugador
    jg_tablero.tab_jugadores[1].jug_puntos = jg_tablero.tab_celdas[0][0].cel_valor

    # -- ------------------------------------------------------------------------------------- Inicializar JUGADOR -- #
    # Simbolo en celda
    jg_tablero.tab_celdas[7][7].cel_simbolo = jg_tablero.tab_jugadores[1].jug_simbolo
    # Celda visitada
    jg_tablero.tab_celdas[7][7].cel_visitada = True
    # Controlador de la celda
    jg_tablero.tab_celdas[7][7].cel_controlador = jg_tablero.tab_jugadores[1].jug_nombre
    # Posicion del jugador
    jg_tablero.tab_jugadores[1].jug_posicion[0] = 7
    jg_tablero.tab_jugadores[1].jug_posicion[1] = 7
    # Puntos del jugador
    jg_tablero.tab_jugadores[1].jug_puntos = jg_tablero.tab_celdas[7][7].cel_valor

    print('todo bien inicializar')

    return jg_tablero


# -- ------------------------------------------------------------------------- Funcion Global : Entrada de usuario -- #
# ------------------------------------------------------------------------------------------------------------------- #

def jugar():
    # While con bandera de si el juego termino

    # Solicitar movimiento a jugador
    jg_mov = input_usuario()

    # Validar Movimiento - Verificar que sea movimiento valido
    cel_mov = juego_tablero.validar_mov(mov_jg=1, mov_dir=jg_mov)
    print(cel_mov)
    # Actualizar celda destino con movimiento de jugador
    juego_tablero.realizar_mov(mov_jg=1, mov_dir=jg_mov)
    print(juego_tablero)
    # Calcular Score de tablero
    # Desplegar score en el tablero
    # Mostrar mensaje que cpu esta moviendo
    # Calcular movimiento a cpu
    # Actualizar celda destino con movimiento de cpu
    # Calcular score de tablero

    # Repetir proceso mientras no haya un Break en el while
    return jg_mov


# -- ------------------------------------------------------------------------- Funcion Global : Entrada de usuario -- #
# ------------------------------------------------------------------------------------------------------------------- #

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
        time.sleep(2)
        print(" \n ")
        print("** Movimiento no valido, intenta de nuevo ** ")
        print(" \n ")
        time.sleep(2)

        return input_usuario()


# -- ---------------------------------------------------------------------------------------------- Clase: Tablero -- #
# ------------------------------------------------------------------------------------------------------------------- #

class Jugador(object):
    def __init__(self, jug_posicion, jug_iscpu, jug_ismax=None, jug_nombre=None, jug_simbolo=None):
        """
        :param jug_posicion: list : [1, 2] : posicion en el tablero del jugador
        :param jug_iscpu: bool : True/False : bandera si el jugador es cpu (si no es cpu es humano)
        """
        # Inicializar la posicion en el tablero del jugador
        self.jug_posicion = jug_posicion
        # Inicializar la bandera sobre si el jugador es el CPU
        self.jug_iscpu = jug_iscpu
        # Inicializar si el jugador es max
        self.jug_ismax = jug_ismax
        # Inicializar el nombre del jugador
        self.jug_nombre = jug_nombre
        # Inicializar el simbolo en el tablero del jugador
        self.jug_simbolo = jug_simbolo
        # Inicializar celdas que ha visitado el jugador
        self.jug_celdasvis = None
        # Inicializar puntos que lleva el jugador
        self.jug_puntos = None


# -- ---------------------------------------------------------------------------------------------- Clase: Tablero -- #
# ------------------------------------------------------------------------------------------------------------------- #

class Tablero(object):

    # Inicializar el tablero
    def __init__(self, tab_score, tab_dims, tab_min, tab_max, tab_dif, tab_jugs):
        # El score del tablero
        self.tab_score = tab_score
        # El tamaño del tablero [8, 8]
        self.tab_size = tab_dims
        # Valor minimo para simular los aleatorios
        self.tab_min = tab_min
        # Valor maximo para simular los aleatorios
        self.tab_max = tab_max
        # Nivel de dificultad
        self.tab_dif = tab_dif
        # Nombre del jugador
        self.tab_jugadores = tab_jugs
        # Celdas dentro de tablero
        # self.tab_celdas = [[Celda(cel_valor=np.random.randint(tab_min, tab_max), cel_posicion=(i, j))
        #                     for j in range(tab_dims)] for i in range(tab_dims)]
        self.tab_celdas = [[Celda(cel_valor=np.random.randint(tab_min, tab_max), cel_posicion=(i, j))
                            for i in range(tab_dims)] for j in range(tab_dims)]

    def __str__(self):
        res = '\n'
        # Filas
        for i in range(len(self.tab_celdas)):
            # Columnas
            res += '|'
            for j in range(len(self.tab_celdas)):
                res += f'{self.tab_celdas[i][j]}|'
            res += '\n'
        return res

    # Para validar un movimiento de un jugador
    def validar_mov(self, mov_jg, mov_dir):

        # Solicitar posicion actual de jugador elegido
        x = self.tab_jugadores[mov_jg].jug_posicion[0]
        y = self.tab_jugadores[mov_jg].jug_posicion[1]

        # Validacion 1 = Movimiento dentro del tablero
        if mov_dir == 'arriba' and 0 < y - 1 <= 7:
            y = y - 1
            x = x
        elif mov_dir == 'derecha' and 0 < x + 1 <= 7:
            x = x + 1
            y = y
        elif mov_dir == 'abajo' and 0 < y + 1 <= 7:
            y = y + 1
            x = x
        elif mov_dir == 'izquierda' and 0 < x - 1 <= 7:
            x = x - 1
            y = y
        else:
            return False

        # Validacion 2 = Celda no esta ocupada
        if self.tab_celdas[x][y].cel_visitada:
            return {'validez': False, 'posicion': None}
        else:
            return {'validez': True, 'posicion': [x, y]}

    # Para realizar el movimiento
    def realizar_mov(self, mov_jg, mov_dir):
        # Proceder si el movimiento es valido
        val = self.validar_mov(mov_jg, mov_dir)
        if val['validez']:
            x = val['posicion'][0]
            y = val['posicion'][1]
            jugador = mov_jg

            # print('x seria: ' + str(x))
            # print('y seria: ' + str(y))
            # print('la posicion actual del jugador es: ' + str(juego_tablero.tab_jugadores[mov_jg].jug_posicion[0]) +
            #      ',' + str(juego_tablero.tab_jugadores[mov_jg].jug_posicion[0]))
            # print('la nueva posicion seria: ' + str(x) + ',' + str(y))
            # print('valor de la celda destino: ' + str(juego_tablero.tab_celdas[y][x].cel_valor))

            # Actualizar posicion de jugador
            juego_tablero.tab_jugadores[mov_jg].jug_posicion[0] = y
            juego_tablero.tab_jugadores[mov_jg].jug_posicion[1] = x
            # Actualizar el Controlador de la celda
            juego_tablero.tab_celdas[y][x].cel_controlador = juego_tablero.tab_jugadores[jugador].jug_nombre
            # Actualizar Simbolo en celda
            juego_tablero.tab_celdas[y][x].cel_simbolo = juego_tablero.tab_jugadores[jugador].jug_simbolo
            # Actualizar que Celda esta visitada
            juego_tablero.tab_celdas[y][x].cel_visitada = True
            # Actualizar score de tablero
            juego_tablero.tab_jugadores[jugador].jug_puntos += juego_tablero.tab_celdas[y][x].cel_valor
            # print('puntos ganados: ' + str(juego_tablero.tab_jugadores[jugador].jug_puntos))


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
        # Para identificar cual jugador controla la celda (visito la celda)
        self.cel_controlador = None
        # Para usar simbolo segun jugador en la impresion del tablero
        self.cel_simbolo = ''

    def __str__(self):
        if len(str(self.cel_valor)) % 2 == 0:

            if self.cel_controlador == juego_tablero.tab_jugadores[0].jug_nombre:
                return f'{juego_tablero.tab_jugadores[0].jug_simbolo}{self.cel_valor}' \
                       f'{juego_tablero.tab_jugadores[0].jug_simbolo}'

            elif self.cel_controlador == juego_tablero.tab_jugadores[1].jug_nombre:
                return f'{juego_tablero.tab_jugadores[1].jug_simbolo}{self.cel_valor}' \
                       f'{juego_tablero.tab_jugadores[1].jug_simbolo}'
            else:
                return f' {self.cel_valor } '
        else:
            if self.cel_controlador == juego_tablero.tab_jugadores[0].jug_nombre:
                return f'{juego_tablero.tab_jugadores[0].jug_simbolo}0{self.cel_valor}' \
                       f'{juego_tablero.tab_jugadores[0].jug_simbolo}'

            elif self.cel_controlador == juego_tablero.tab_jugadores[1].jug_nombre:
                return f'{juego_tablero.tab_jugadores[1].jug_simbolo}0{self.cel_valor}' \
                       f'{juego_tablero.tab_jugadores[1].jug_simbolo}'
            else:
                return f' 0{ self.cel_valor } '

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
    in_min = 1

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

    juego_tablero = inicializar()

    # Imprimir tablero
    print(juego_tablero)
    # time.sleep(1.5)

    # -- ------------------------------------------------------------------------------------------ Ciclo de juego -- #

    # Funcion jugar
    jugar()
