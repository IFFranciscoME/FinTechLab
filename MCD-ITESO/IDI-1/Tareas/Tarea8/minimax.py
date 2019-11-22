
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Juego de Trazo Maximo con Inteligencia Artificial (Minimax)                                         -- #
# -- Repositorio:                                                                                                  -- #
# -- FranciscoME                                                                                                   -- #
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np
import time


# -- ------------------------------------------------------------------------- Funcion Global : Entrada de usuario -- #
# ------------------------------------------------------------------------------------------------------------------- #

def jugar():
    jugador = 1
    # While con bandera de si el juego termino
    while juego_tablero.mov_disponibles(jugador):

        # -- ---------------------------------------------------------------------------------- Movimiento PERSONA -- #

        # -- Validar movimiento aceptado (Dentro de tablero)

        # Solicitar movimiento a jugador
        jg_mov = input_usuario()

        # Ciclo infinito de pregunta por movimiento hasta que ingrese uno válido
        while not juego_tablero.mov_tablero(jugador, jg_mov):

            print('movimiento no valido')
            # Solicitar movimiento a jugador
            jg_mov = input_usuario()

        # Regresa coordenadas de movimiento valido por tablero
        x, y = juego_tablero.mov_tablero(mov_jg=1, mov_dir=jg_mov)

        # Actualizar celda destino con movimiento de jugador
        juego_tablero.realizar_mov(mov_jg=1, x=x, y=y)

        # Validar que existan movimientos disponibles
        # mov_disp = juego.tablero.mov_disp(mov_jg=1)
        # if not mov_disp:
        # print('\nDia del juicio final ...')
        # print(juego_tablero)
        # print('Skynet: ' + str(juego_tablero.tab_jugadores[0].jug_puntos))
        # print('Connor, john: ' + str(juego_tablero.tab_jugadores[1].jug_puntos))
        # print('Score: ' + str(juego_tablero.tab_score))
        # break

        print(juego_tablero)
        print('Skynet: ' + str(juego_tablero.tab_jugadores[0].jug_puntos))
        print('Connor, john: ' + str(juego_tablero.tab_jugadores[1].jug_puntos))
        print('Score: ' + str(juego_tablero.tab_score))

        # -- -------------------------------------------------------------------------------------- Movimiento CPU -- #
        # Mostrar mensaje que cpu esta moviendo
        print('\nSkynet moviendo: ')

        # Calcular movimiento a cpu
        time.sleep(.5)

        # Actualizar celda destino con movimiento de cpu
        juego_tablero.realizar_mov(mov_jg=0, x=0, y=2)

        # Imprimir tablero y marcadores
        print(juego_tablero)
        print('Skynet: ' + str(juego_tablero.tab_jugadores[0].jug_puntos))
        print('Connor, john: ' + str(juego_tablero.tab_jugadores[1].jug_puntos))
        print('Score: ' + str(juego_tablero.tab_score))

        # Repetir proceso mientras no haya un Break en el while

    return True


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
    jg_tablero.tab_jugadores[0].jug_posicion[0] = 0  # Componente X
    jg_tablero.tab_jugadores[0].jug_posicion[1] = 0  # Componente Y
    # Puntos del jugador
    jg_tablero.tab_jugadores[0].jug_puntos = jg_tablero.tab_celdas[0][0].cel_valor

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
    # Inicializar Score de Tablero (Skynet - John Connor)
    jg_tablero.tab_score = jg_tablero.tab_jugadores[0].jug_puntos - jg_tablero.tab_jugadores[1].jug_puntos

    return jg_tablero


# -- ------------------------------------------------------------------------ Funcion Global : Dia de Juicio Final -- #
# ------------------------------------------------------------------------------------------------------------------- #

def juicio_final():

    d1 = '\nAgosto 4, 1997 : Cyberdine activa al protocolo Skynet'
    time.sleep(1)
    d2 = '\nAgosto 29, 1997 : 02:14:00 EST Skynet se vuelve autoconciente'
    time.sleep(1)
    d3 = '\nAgosto 29, 1997 : 02:14:01 EST Skynet lanza cohetes nucleares a Rusia'
    time.sleep(1)
    d3 = '\nSkynet incita un contra ataque contra los humanos, quienes, en panico, tratan de desconectarla'
    time.sleep(1)
    d4 = '\n ... '

    # for i in range(11):
    #     print(loading[i], sep='', end=' ', flush=True)
    # time.sleep(0.25)
    # d5 = ' ... llamada entrante '

# -- ------------------------------------------------------------------------- Funcion Global : Entrada de usuario -- #
# ------------------------------------------------------------------------------------------------------------------- #

def input_usuario():

    print('')
    print("----------------- ¿A dónde vas a mover? ----------------- ")
    print("---------- ------------------------------ --------------- ")
    print("  1 = arriba, 2 = derecha, 3 = abajo, 4 = izquierda       ")
    in_mov = int(input("\nMovimiento: "))

    if in_mov == 1:
        return 'arriba'
    elif in_mov == 2:
        return 'derecha'
    elif in_mov == 3:
        return 'abajo'
    elif in_mov == 4:
        return 'izquierda'
    else:
        time.sleep(1)
        print(" \n ")
        print("** Movimiento no valido, intenta de nuevo ** ")
        print(" \n ")
        time.sleep(1)

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
        self.tab_celdas = [[Celda(cel_valor=np.random.randint(tab_min, tab_max), cel_posicion=(i, j))
                            for i in range(tab_dims)] for j in range(tab_dims)]

    def __str__(self):
        res = '\n'
        # Filas
        for k in range(len(self.tab_celdas)):
            # Columnas
            res += '|'
            for j in range(len(self.tab_celdas)):
                res += f'{self.tab_celdas[k][j]}|'
            res += '\n'
        return res

    # Para validar un movimiento dentro del tablero
    def mov_tablero(self, mov_jg, mov_dir):

        # Solicitar posicion actual de jugador elegido
        x = self.tab_jugadores[mov_jg].jug_posicion[0]
        y = self.tab_jugadores[mov_jg].jug_posicion[1]

        # Validacion 1 = Movimiento dentro del tablero
        if mov_dir == 'arriba' and 0 <= y - 1 <= 7:
            x = x
            y = y - 1
        elif mov_dir == 'derecha' and 0 <= x + 1 <= 7:
            x = x + 1
            y = y
        elif mov_dir == 'abajo' and 0 <= y + 1 <= 7:
            x = x
            y = y + 1
        elif mov_dir == 'izquierda' and 0 <= x - 1 <= 7:
            x = x - 1
            y = y
        else:
            return False

        # Validacion 2: que la celda no este visitada
        if not self.tab_celdas[y][x].cel_visitada:
            return x, y

    # Para validar si hay movimientos permitidos
    def mov_disponibles(self, mov_jg):

        # Validar que exista movimiento dentro de tablero & la celda no este ocupada (que ambos sean True)
        # probar hacia arriba
        # x, y = self.mov_tablero(mov_jg, 'arriba')
        if self.mov_tablero(mov_jg, 'arriba'):
            return True

        # probar hacia derecha
        # x, y = self.mov_tablero(mov_jg, 'derecha')
        if self.mov_tablero(mov_jg, 'derecha'):
            return True

        # probar hacia abajo
        # x, y = self.mov_tablero(mov_jg, 'abajo')
        if self.mov_tablero(mov_jg, 'abajo'):
            return True

        # probar hacia izquierda
        # x, y = self.mov_tablero(mov_jg, 'izquierda')
        if self.mov_tablero(mov_jg, 'izquierda'):
            return True

        else:
            return False

    # Realizar un movimiento en el tablero
    def realizar_mov(self, mov_jg, x, y):
        # Actualizar posicion de jugador
        self.tab_jugadores[mov_jg].jug_posicion[0] = x
        self.tab_jugadores[mov_jg].jug_posicion[1] = y
        # Actualizar el Controlador de la celda
        self.tab_celdas[y][x].cel_controlador = self.tab_jugadores[mov_jg].jug_nombre
        # Actualizar Simbolo en celda
        self.tab_celdas[y][x].cel_simbolo = self.tab_jugadores[mov_jg].jug_simbolo
        # Actualizar que Celda esta visitada
        self.tab_celdas[y][x].cel_visitada = True
        # Actualizar score de tablero
        self.tab_jugadores[mov_jg].jug_puntos += self.tab_celdas[y][x].cel_valor
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


# -- ------------------------------------------------------------------------------------------------ Seccion Main -- #
# ------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':

    # -- -------------------------------------------------------------------------------- Inicializacion del juego -- #
    # Mensaje de bienvenida
    # input('\n \nSkynet: ¿Estás listo? \n')
    # time.sleep(0.5)

    # solicitar Dificultad
    # in_dif = int(input("Elige dificultad | 3 = 'facil', '5 = 'dificil: "))
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
    in_nom = 'john connor'

    # Dinamica John Connor
    # loading = 'John Connor'
    # time.sleep(2)
    # print('\nBuen intento ...\n')
    # time.sleep(2)
    # for i in range(11):
    #     print(loading[i], sep='', end=' ', flush=True)
    #     time.sleep(0.25)
    #
    # # imprimir mensaje de inicio
    # time.sleep(2.5)
    # print("\n \n ................ Dia del Juicio Final ................ ")
    # time.sleep(1.5)

    juego_tablero = inicializar()

    # Imprimir tablero inicial
    print(juego_tablero)
    print('Skynet: ' + str(juego_tablero.tab_jugadores[0].jug_puntos))
    print('Connor, john: ' + str(juego_tablero.tab_jugadores[1].jug_puntos))
    print('Score: ' + str(juego_tablero.tab_score))

    time.sleep(1)

    # -- ------------------------------------------------------------------------------------------ Ciclo de juego -- #

    # Funcion jugar
    jugar()

    juicio_final()

