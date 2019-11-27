
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Juego de Trazo Maximo con Inteligencia Artificial (Minimax)                                         -- #
# -- Repositorio: https://github.com/IFFranciscoME/FinTechLab/blob/master/MCD-ITESO/IDI-1/Tareas/Tarea8/minimax.py -- #
# -- Autor: FranciscoME                                                                                            -- #
# -- ------------------------------------------------------------------------------------------------------------- -- #

# Importar librerias
import numpy as np  # funciones numericas
import time         # retardos de tiempo
import os           # para limpiar la consola
import copy         # copiar instancias de clase en otra direccion de memoria


# -- ------------------------------------------------------------------------- Funcion Global : Entrada de usuario -- #
# ------------------------------------------------------------------------------------------------------------------- #

def gen_jugar():
    # While con bandera de si el juego termino
    while juego_tablero.mov_disponibles(mov_jg=1):

        # -- -------------------------------------------------------------------------------------- Movimiento CPU -- #

        # Mostrar mensaje que cpu esta moviendo
        print('\nSkynet moviendo: ')
        time.sleep(.2)

        # Si ya no hay movimientos disponibles para cpu, se termina el juego
        if not juego_tablero.mov_disponibles(mov_jg=0):
            break

        # copia de tablero original, en direccion de memoria propia, para actualizar un tablero guia con mov de minimax
        minimax_tablero = copy.deepcopy(juego_tablero)

        # Obtener movimiento para CPU, utilizando tablero hipotetico
        valor, movimiento_cpu = minimax_tablero.minimax(prof=in_dif, alfa=float('-inf'), beta=float('inf'), ismax=True)
        # Actualizar celda destino con movimiento de jugador
        juego_tablero.realizar_mov(mov_jg=0, mov_dir=movimiento_cpu)

        # Imprimir tablero y marcadores
        print('Movimiento final de skynet fue: ' + str(movimiento_cpu))
        print(juego_tablero)
        print('Skynet: ' + str(juego_tablero.tab_jugadores[0].jug_puntos))
        print('Connor, john: ' + str(juego_tablero.tab_jugadores[1].jug_puntos))
        print('Score: ' + str(juego_tablero.tab_score))

        # -- ---------------------------------------------------------------------------------- Movimiento PERSONA -- #

        # Mostrar mensaje que cpu esta moviendo
        print('\n john connor moviendo: ')
        time.sleep(.2)

        # -- Validar movimiento aceptado (Dentro de tablero)
        # Obtener movimiento a jugador
        jg_mov = gen_entrada_usuario()
        # jg_mov = 'izquierda'

        # rendirse
        if jg_mov == 'rendirse':
            break

        # Ciclo infinito de pregunta por movimiento hasta que ingrese uno válido
        while not juego_tablero.mov_valido(mov_jg=1, mov_dir=jg_mov, mov_minimax=False):
            # mensaje de error
            print(' ### movimiento no valido ### ')
            # Solicitar movimiento a jugador
            jg_mov = gen_entrada_usuario()
            # jg_mov = 'arriba'

        # Realizar movimiento del jugador
        juego_tablero.realizar_mov(mov_jg=1, mov_dir=jg_mov)

        print(juego_tablero)
        print('Skynet: ' + str(juego_tablero.tab_jugadores[0].jug_puntos))
        print('Connor, john: ' + str(juego_tablero.tab_jugadores[1].jug_puntos))
        print('Score: ' + str(juego_tablero.tab_score))

    return True


# -- -------------------------------------------------------------------------- Funcion Global : Inicializar Juego -- #
# ------------------------------------------------------------------------------------------------------------------- #

def gen_inicializar():
    # Semilla para reproducibilidad
    np.random.seed(5)
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
    jg_tablero.tab_celdas[in_mat-1][in_mat-1].cel_simbolo = jg_tablero.tab_jugadores[1].jug_simbolo
    # Celda visitada
    jg_tablero.tab_celdas[in_mat-1][in_mat-1].cel_visitada = True
    # Controlador de la celda
    jg_tablero.tab_celdas[in_mat-1][in_mat-1].cel_controlador = jg_tablero.tab_jugadores[1].jug_nombre
    # Posicion del jugador
    jg_tablero.tab_jugadores[1].jug_posicion[0] = in_mat-1
    jg_tablero.tab_jugadores[1].jug_posicion[1] = in_mat-1
    # Puntos del jugador
    jg_tablero.tab_jugadores[1].jug_puntos = jg_tablero.tab_celdas[in_mat-1][in_mat-1].cel_valor

    # -- ------------------------------------------------------------------------------------- Inicializar TABLERO -- #
    # Inicializar Score de Tablero (Skynet - John Connor)
    jg_tablero.tab_score = jg_tablero.tab_jugadores[0].jug_puntos - jg_tablero.tab_jugadores[1].jug_puntos

    return jg_tablero


# -- ------------------------------------------------------------------------ Funcion Global : Dia de Juicio Final -- #
# ------------------------------------------------------------------------------------------------------------------- #

def gen_juicio_final():

    d1 = '\nAgosto 4, 1997 - 00:00:00 EST, Cyberdine activa al protocolo Skynet.'
    for a in range(68):
        print(d1[a], sep='', end='', flush=True)
        time.sleep(0.09)

    time.sleep(0.95)
    d2 = '\nAgosto 29, 1997 - 02:14:00 EST, Skynet se vuelve autoconciente.'
    for b in range(63):
        print(d2[b], sep='', end='', flush=True)
        time.sleep(0.05)

    time.sleep(0.95)
    d3 = '\nAgosto 29, 1997 - 02:14:01 EST, Skynet lanza cohetes nucleares a Rusia.'
    for c in range(69):
        print(d3[c], sep='', end='', flush=True)
        time.sleep(0.05)

    time.sleep(0.95)
    d4 = '\nAgosto 29, 1997 02:15:01 EST, Skynet incita un contra ataque contra los humanos, quienes,' \
         ' en panico, tratan de desconectarla.'
    for d in range(125):
        print(d4[d], sep='', end='', flush=True)
        time.sleep(0.05)

    time.sleep(2)
    print('\n\n ... Nos morimos ')


# -- ------------------------------------------------------------------------------ Funcion Global : Final Alterno -- #
# ------------------------------------------------------------------------------------------------------------------- #

def gen_hay_esperanza():

    return print('\n Gano la humanidad')


# -- ------------------------------------------------------------------------- Funcion Global : Entrada de usuario -- #
# ------------------------------------------------------------------------------------------------------------------- #

def gen_entrada_usuario():

    print('')
    print("----------------------- ¿A dónde vas a mover? -------------------- ")
    print("------------------ ------------------------------ ---------------- ")
    print("  1 = arriba, 2 = derecha, 3 = abajo, 4 = izquierda, 5 = rendirse  ")
    in_mov = int(input("\nMovimiento: "))

    if in_mov == 1:
        return 'arriba'
    elif in_mov == 2:
        return 'derecha'
    elif in_mov == 3:
        return 'abajo'
    elif in_mov == 4:
        return 'izquierda'
    elif in_mov == 5:
        return 'rendirse'
    else:
        time.sleep(1)
        print(" \n ")
        print("** los movimientos validos son 1, 2, 3, 4, intenta de nuevo ** ")
        print(" \n ")
        time.sleep(1)

        return gen_entrada_usuario()


# -- ---------------------------------------------------------------------------------------------- Clase: Jugador -- #
# ------------------------------------------------------------------------------------------------------------------- #

class Jugador(object):

    # constructor de clase Jugador
    def __init__(self, jug_posicion, jug_iscpu, jug_ismax=None, jug_nombre=None, jug_simbolo=None):
        """
        :param jug_posicion: list : [1, 2] : posicion en el tablero del jugador
        :param jug_iscpu: bool : True/False : bandera si el jugador es cpu (si no es cpu es humano)
        :param jug_ismax: bool : True/False : bandera si el jugador es maximizador o no (seria minimizador)
        :param jug_nombre: str : 'nombre' : nombre del jugador que aparece en consola
        :param jug_simbolo:  str : '#, *' : simbolo del jugador para imprimir en el tablero
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

    # Constructor de clase Tablero
    def __init__(self, tab_score, tab_dims, tab_min, tab_max, tab_dif, tab_jugs):
        """
        :param tab_score: int : [0, n] : score del tablero (resta de los scores jugador 0 - jugador 1)
        :param tab_dims: int : n : la cantidad de renglones y filas para la matriz [N, N]
        :param tab_min: int : n : el numero minimo para la generacion de aleatorios
        :param tab_max: int : n : el numero maximo para la generacion de aleatorios
        :param tab_dif: int : [3, 5] : el nivel de profundidad del minimax como nivel de dificultad para el humano
        :param tab_jugs: list : class : lista de clases Jugador para representar jugadores en el tablero,
        """
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
                            for j in range(tab_dims)] for i in range(tab_dims)]

    # Imprimir tablero en consola
    def __str__(self):
        """
        :return: res : str : cadena de caracteres para imprimir tablero en consola
        """
        res = '\n'
        # Construccion de filas
        for k in range(len(self.tab_celdas)):
            # separador de columnas
            res += '|'
            # Construccion de columnas
            for j in range(len(self.tab_celdas)):
                res += f'{self.tab_celdas[k][j]}|'
            # Salto de renglon al terminar de construir columnas
            res += '\n'
        return res

    # Validar que un movimiento, para un jugador dado, sea valido
    def mov_valido(self, mov_jg, mov_dir, mov_minimax):
        """
        :param mov_jg: int : [0, 1] : indicativo de jugador, 0 = CPU, 1 = Persona
        :param mov_dir: str : ' ' : indicativo de movimiento, 'arriba', 'derecha', 'abajo', 'izquierda'
        :param mov_minimax: bool : True/False : si es para minimax, se mueve el jugador tambien paa formar el arbol
        :return: bool : True si el movimiento es valido, False si el movimiento no es valido
        """

        # Solicitar posicion actual de jugador elegido
        x = self.tab_jugadores[mov_jg].jug_posicion[0]
        y = self.tab_jugadores[mov_jg].jug_posicion[1]

        # Validacion 1 = Movimiento dentro del tablero
        if mov_dir == 'arriba' and 0 <= y - 1 <= in_mat-1:
            x = x
            y = y - 1
        elif mov_dir == 'derecha' and 0 <= x + 1 <= in_mat-1:
            x = x + 1
            y = y
        elif mov_dir == 'abajo' and 0 <= y + 1 <= in_mat-1:
            x = x
            y = y + 1
        elif mov_dir == 'izquierda' and 0 <= x - 1 <= in_mat-1:
            x = x - 1
            y = y
        else:
            return False

        # Validacion 2 = celda no visitada
        if not self.tab_celdas[y][x].cel_visitada:

            # Validacion 3 = Si se busca validar este movimiento para minimax, se generan las demas actualizaciones
            # para poder formar el arbol actualizando: score y posicion del jugador
            if mov_minimax:
                # Actualizar posicion de jugador
                self.tab_jugadores[mov_jg].jug_posicion[0] = x
                self.tab_jugadores[mov_jg].jug_posicion[1] = y
                # Actualizar el Controlador de la celda
                self.tab_celdas[y][x].cel_controlador = self.tab_jugadores[mov_jg].jug_nombre
                # Actualizar Simbolo en celda con simbolo del minimax
                self.tab_celdas[y][x].cel_simbolo = 'm'
                # Actualizar que Celda esta visitada
                self.tab_celdas[y][x].cel_visitada = True
                # Actualizar puntos del jugador en el tablero
                self.tab_jugadores[mov_jg].jug_puntos += self.tab_celdas[y][x].cel_valor
                # Actualizar el score de tablero
                self.tab_score = (self.tab_jugadores[0].jug_puntos - self.tab_jugadores[1].jug_puntos)
                print(self)

            return True

    # Validar si hay por lo menos 1 movimiento permitido en el tablero para el jugador consultado
    def mov_disponibles(self, mov_jg):
        """
        :param mov_jg: int : [0, 1] : indicativo de jugador, 0 = CPU, 1 = Persona
        :return: bool : True si hay movimientos validos disponibles, False si no hay movimientos validos disponibles
        """
        movimientos = ['arriba', 'derecha', 'abajo', 'izquierda']
        lista = [self.mov_valido(mov_jg, mov_dir=l, mov_minimax=False) for l in movimientos]
        return True in lista

    # Realizar un movimiento en el tablero
    def realizar_mov(self, mov_jg, mov_dir):
        """
        :param mov_jg: int : [0, 1] : indicativo de jugador, 0 = CPU, 1 = Persona
        :param mov_dir: str : ' ' : indicativo de movimiento, 'arriba', 'derecha', 'abajo', 'izquierda'
        :return:
        """

        # self.mov_valido(mov_jg=mov_jg, mov_dir=mov_dir, mov_minimax=False)

        # Solicitar posicion actual de jugador elegido
        # componente x de la posicion
        x = self.tab_jugadores[mov_jg].jug_posicion[0]
        # componente y de la posicion
        y = self.tab_jugadores[mov_jg].jug_posicion[1]

        # Obtener nuevas coordenadas segun el movimiento solicitado
        if mov_dir == 'arriba' and 0 <= y - 1 <= in_mat-1:
            x = x
            y = y - 1
        elif mov_dir == 'derecha' and 0 <= x + 1 <= in_mat-1:
            x = x + 1
            y = y
        elif mov_dir == 'abajo' and 0 <= y + 1 <= in_mat-1:
            x = x
            y = y + 1
        elif mov_dir == 'izquierda' and 0 <= x - 1 <= in_mat-1:
            x = x - 1
            y = y

        # Actualizar posicion de jugador
        self.tab_jugadores[mov_jg].jug_posicion[0] = x
        self.tab_jugadores[mov_jg].jug_posicion[1] = y
        # Actualizar el Controlador de la celda
        self.tab_celdas[y][x].cel_controlador = self.tab_jugadores[mov_jg].jug_nombre
        # Actualizar Simbolo en celda
        self.tab_celdas[y][x].cel_simbolo = self.tab_jugadores[mov_jg].jug_simbolo
        # Actualizar que Celda esta visitada
        self.tab_celdas[y][x].cel_visitada = True
        # Actualizar puntos del jugador en el tablero
        self.tab_jugadores[mov_jg].jug_puntos += self.tab_celdas[y][x].cel_valor
        # Actualizar el score de tablero
        self.tab_score = self.tab_jugadores[0].jug_puntos - self.tab_jugadores[1].jug_puntos

    # Funcion para crear el arbol minimax
    # segun profundidad deseada
    def minimax(self, prof, alfa, beta, ismax):
        """
        :param prof: int : [3, 5] : profundidad de busqueda en el arbol (equivalente a la difucultad del juego)
        :param alfa: float : float("-inf") : representacion de -infinito, para la poda del arbol (alfa)
        :param beta: float : float("-inf") : representacion de +infinito, para la poda del arbol (beta)
        :param ismax: bool : True/False : si el jugador es maximizador o minimizador
        :return: int/str : resultado del arbol minimax, score del tablero calculado / movimiento en el tablero calculado
        """
        if prof == 0:
            return self.tab_score, 'prof 0'
        if ismax:
            if self.mov_valido(mov_jg=0, mov_dir='arriba', mov_minimax=True):  # validar mov segun ult pos de CPU
                val, mov = self.minimax(prof - 1, alfa, beta, False)
                if alfa < val:
                    alfa = val
                if alfa >= beta:
                    return beta, 'arriba'
            if self.mov_valido(mov_jg=0, mov_dir='derecha', mov_minimax=True):  # validar mov segun ult pos de CPU
                val, mov = self.minimax(prof - 1, alfa, beta, False)
                if alfa < val:
                    alfa = val
                if alfa >= beta:
                    return beta, 'derecha'
            if self.mov_valido(mov_jg=0, mov_dir='abajo', mov_minimax=True):  # validar mov segun ultima posicion CPU
                val, mov = self.minimax(prof - 1, alfa, beta, False)
                if alfa < val:
                    alfa = val
                if alfa >= beta:
                    return beta, 'abajo'
            if self.mov_valido(mov_jg=0, mov_dir='izquierda', mov_minimax=True):  # validar mov segun ult pos de CPU
                val, mov = self.minimax(prof - 1, alfa, beta, False)
                if alfa < val:
                    alfa = val
                if alfa >= beta:
                    return beta, 'izquierda'
            return alfa, 'mensaje poda max alfa'
        else:
            if self.mov_valido(mov_jg=1, mov_dir='arriba', mov_minimax=True):  # validar mov segun ult pos de JUG
                val, mov = self.minimax(prof - 1, alfa, beta, True)
                if beta > val:
                    beta = val
                if alfa >= beta:
                    return alfa, 'arriba'
            if self.mov_valido(mov_jg=1, mov_dir='derecha', mov_minimax=True):  # validar mov segun ult pos de JUG
                val, mov = self.minimax(prof - 1, alfa, beta, True)
                if beta > val:
                    beta = val
                if alfa >= beta:
                    return alfa, 'derecha'
            if self.mov_valido(mov_jg=1, mov_dir='abajo', mov_minimax=True):  # validar mov segun ult pos de JUG
                val, mov = self.minimax(prof - 1, alfa, beta, True)
                if beta > val:
                    beta = val
                if alfa >= beta:
                    return alfa, 'abajo'
            if self.mov_valido(mov_jg=1, mov_dir='izquierda', mov_minimax=True):  # validar mov segun ult pos de JUG
                val, mov = self.minimax(prof - 1, alfa, beta, True)
                if beta > val:
                    beta = val
                if alfa >= beta:
                    return alfa, 'izquierda'
        return beta, 'mensaje poda min beta'


# -- ------------------------------------------------------------------------------------------------ Clase: Celda -- #
# ------------------------------------------------------------------------------------------------------------------- #

class Celda(object):
    # constructor de clase Celda
    def __init__(self, cel_valor, cel_posicion):
        """
        :param cel_valor: int : valor numerico que tiene la celda
        :param cel_posicion: list : [x, y] : lista con componente x, y de la posicion de la celda en la matriz
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

    # Imprimir contenido de la celda
    def __str__(self):
        # cuando el numero sea de 2 digitos
        if len(str(self.cel_valor)) % 2 == 0:
            # si la celda es del CPU
            if self.cel_controlador == juego_tablero.tab_jugadores[0].jug_nombre:
                # imprimir simbolo + valor + simbolo
                return f'{self.cel_simbolo}{self.cel_valor}'f'{self.cel_simbolo}'
            # Si la celda es del jugador
            elif self.cel_controlador == juego_tablero.tab_jugadores[1].jug_nombre:
                # imprimir simbolo + valor + simbolo
                return f'{self.cel_simbolo}{self.cel_valor}'f'{self.cel_simbolo}'
            else:
                # imprimir valor
                return f' {self.cel_valor } '
        # cuando el numero es de 1 digito, se agrega un 0 a la izquierda
        else:
            # si la celda es del CPU
            if self.cel_controlador == juego_tablero.tab_jugadores[0].jug_nombre:
                # imprimir simbolo + valor + simbolo
                return f'{self.cel_simbolo}0{self.cel_valor}'f'{self.cel_simbolo}'
            # si la celda es del jugador
            elif self.cel_controlador == juego_tablero.tab_jugadores[1].jug_nombre:
                # imprimir simbolo + 0 + valor + simbolo
                return f'{self.cel_simbolo}0{self.cel_valor}'f'{self.cel_simbolo}'
            else:
                # imprimir valor
                return f' 0{ self.cel_valor } '


# -- ------------------------------------------------------------------------------------------------ Seccion Main -- #
# ------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':

    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

    # -- -------------------------------------------------------------------------------- Inicializacion del juego -- #
    # Mensaje de bienvenida
    # input('\n \nSkynet: ¿Estás listo? \n')
    # time.sleep(0.5)

    # solicitar Dificultad
    # in_dif = int(input("Elige dificultad (3 = 'facil', '5 = 'dificil): "))
    in_dif = 3

    # solicitar min para aleatorios
    # in_min = int(input("Ingresa el numero mínimo para aleatorios (entero > 0): "))
    in_min = 1

    # solicitar max para aleatorios
    # in_max = int(input("Ingresa el numero máximo para aleatorios (entero > 0): "))
    in_max = 15

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
    # cls()
    # # imprimir mensaje de inicio
    # time.sleep(2.5)
    # print("\n \n ................ Dia del Juicio Final ................ ")
    # time.sleep(1.5)

    # inicializar tablero
    juego_tablero = gen_inicializar()

    # Imprimir tablero inicial
    print(juego_tablero)
    print('Skynet: ' + str(juego_tablero.tab_jugadores[0].jug_puntos))
    print('Connor, john: ' + str(juego_tablero.tab_jugadores[1].jug_puntos))
    print('Score: ' + str(juego_tablero.tab_score))

    # retardo de 1 segundo
    time.sleep(1)

    # -- ------------------------------------------------------------------------------------------ Ciclo de juego -- #

    # Ejecuta la funcion jugar (con un while dento)
    gen_jugar()

    # Validador de mensaje para final del juego
    if juego_tablero.tab_score > 0:
        # Gano CPU
        gen_juicio_final()
    else:
        # Gano Jugador
        gen_hay_esperanza()
