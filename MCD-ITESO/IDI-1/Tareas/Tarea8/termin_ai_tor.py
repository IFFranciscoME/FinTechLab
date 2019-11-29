
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Juego de Trazo Maximo con Inteligencia Artificial (Minimax)                                         -- #
# -- Repositorio: https://github.com/IFFranciscoME/FinTechLab/blob/master/MCD-ITESO/IDI-1/Tareas/Tarea8/minimax.py -- #
# -- Autor: FranciscoME                                                                                            -- #
# -- ------------------------------------------------------------------------------------------------------------- -- #

# Importar librerias
import numpy as np  # funciones numericas
import time         # retardos de tiempo

# Semilla para reproducibilidad de tableros
np.random.seed(5)


# -- ------------------------------------------------------------------------- Funcion Global : Entrada de usuario -- #
# ------------------------------------------------------------------------------------------------------------------- #

def gen_jugar():
    # While con bandera de si el juego termino
    while juego_tablero.mov_disponibles(mov_jg=1) and juego_tablero.mov_disponibles(mov_jg=0):

        # -- -------------------------------------------------------------------------------------- Movimiento CPU -- #
        # Mostrar mensaje que cpu esta moviendo
        print('\nSkynet moviendo: ')
        time.sleep(.5)

        # Si ya no hay movimientos disponibles para cpu, se termina el juego
        if not juego_tablero.mov_disponibles(mov_jg=0):
            break

        x0 = juego_tablero.tab_jugadores[0].jug_posicion[0]
        y0 = juego_tablero.tab_jugadores[0].jug_posicion[1]
        val = juego_tablero.tab_score

        x1 = juego_tablero.tab_jugadores[1].jug_posicion[0]
        y1 = juego_tablero.tab_jugadores[1].jug_posicion[1]

        # Arbol minimax
        arbol = Nodo(val)
        valor, movimiento_cpu = arbol.minimax_nodo(in_dif, x0, y0, x1, y1, player=0,
                                                   alpha=float('-inf'), beta=float('inf'))

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
        # retardo de tiempo en segundos
        time.sleep(.5)

        if not juego_tablero.mov_disponibles(mov_jg=1):
            break

        # -- Validar movimiento aceptado (Dentro de tablero)
        # Obtener movimiento a jugador
        jg_mov = gen_entrada_usuario()

        # para debugging
        # jg_mov = 'izquierda'

        # revisar si se elige rendirse
        if jg_mov == 'rendirse':
            break

        # Ciclo infinito de pregunta por movimiento hasta que ingrese uno valido
        while not juego_tablero.mov_valido(mov_jg=1, mov_dir=jg_mov, mov_minimax=False):
            # mensaje de error
            print(' ### movimiento no valido ### ')
            # Solicitar movimiento a jugador
            jg_mov = gen_entrada_usuario()
            # para debugging
            # jg_mov = 'arriba'

        # Realizar movimiento del jugador
        juego_tablero.realizar_mov(mov_jg=1, mov_dir=jg_mov)

        # Imprimir tablero y marcadores
        print('Movimiento final de Connor, John fue: ' + str(movimiento_cpu))
        print(juego_tablero)
        print('Skynet: ' + str(juego_tablero.tab_jugadores[0].jug_puntos))
        print('Connor, john: ' + str(juego_tablero.tab_jugadores[1].jug_puntos))
        print('Score: ' + str(juego_tablero.tab_score))

    return True


# -- -------------------------------------------------------------------------- Funcion Global : Inicializar Juego -- #
# ------------------------------------------------------------------------------------------------------------------- #

def gen_inicializar():
    """
    :return: Tablero : Regresa instancia de clase Tablero : Inicializar el tablero del juego
    """

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
    """
    :return: Imprime en pantalla mensajes del juicio final y como todos nos vamos a morir
    """

    d1 = '\nAgosto 04, 1997 - 00:00:00 EST, Cyberdine activa al protocolo Skynet.'
    for a in range(69):
        print(d1[a], sep='', end='', flush=True)
        time.sleep(0.11)

    time.sleep(0.95)
    d2 = '\nAgosto 29, 1997 - 02:14:00 EST, Skynet se vuelve autoconciente.'
    for b in range(63):
        print(d2[b], sep='', end='', flush=True)
        time.sleep(0.11)

    time.sleep(0.95)
    d3 = '\nAgosto 29, 1997 - 02:14:01 EST, Skynet lanza cohetes nucleares a Rusia.'
    for c in range(71):
        print(d3[c], sep='', end='', flush=True)
        time.sleep(0.11)

    time.sleep(0.95)
    d4 = '\nAgosto 29, 1997 - 02:15:01 EST, Skynet incita un contra ataque contra los humanos, quienes,' \
         ' en panico, tratan de desconectarla.'
    for d in range(125):
        print(d4[d], sep='', end='', flush=True)
        time.sleep(0.11)

    # retardo de tiempo en segundos
    time.sleep(2.2)
    # lo inevitable
    print('\n\n ... Nos morimos ')


# -- ------------------------------------------------------------------------------ Funcion Global : Final Alterno -- #
# ------------------------------------------------------------------------------------------------------------------- #

def gen_hay_esperanza():
    """
    :return: imprime en pantalla mensaje : imprime mensaje de esperanza
    """

    print('\n Gano la humanidad ')


# -- ------------------------------------------------------------------------- Funcion Global : Entrada de usuario -- #
# ------------------------------------------------------------------------------------------------------------------- #

def gen_entrada_usuario():
    """
    :return: imprime en pantalla : solicita entrada y regresa movimiento capturado por usuario
    """

    # Imprimir mensaje en pantalla
    print('')
    print("----------------------- ¿A donde vas a mover? -------------------- ")
    print("------------------ ------------------------------ ---------------- ")
    print("  1 = arriba, 2 = derecha, 3 = abajo, 4 = izquierda, 5 = rendirse  ")
    in_mov = input("\nMovimiento: ")

    # revisar cual opcion ingreso el usuario
    if in_mov == '1':
        return 'arriba'
    if in_mov == '2':
        return 'derecha'
    if in_mov == '3':
        return 'abajo'
    if in_mov == '4':
        return 'izquierda'
    if in_mov == '5':
        return 'rendirse'
    else:
        # retardo de tiempo en segundos
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
                            for i in range(tab_dims)] for j in range(tab_dims)]

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
                # print(self)

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
        """
        :return: str : cadena de caracteres para imprimir contenido de celda en consola
        """
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


# -- ------------------------------------------------------------------------------------------------- Clase: Nodo -- #
# ------------------------------------------------------------------------------------------------------------------- #

class Nodo:
    def __init__(self, data=0):
        self.data = data
        self.left = None
        self.right = None
        self.up = None
        self.down = None

    def minimax_nodo(self, depth, row1, column1, row2, column2, player,  alpha, beta):

        if depth == 0:
            return self.data, 'hoja'

        else:
            bandera = 0
            direccion_min = 'vacio'
            direccion_max = 'vacio'

        # -- para movimiento de CPU -- #
        if player == 0:
            row = column1
            column = row1

            # -- Movimiento hacia ARRIBA
            if row - 1 >= 0:
                if not juego_tablero.tab_celdas[row-1][column].cel_visitada:
                    bandera = 1
                    juego_tablero.tab_celdas[row-1][column].cel_visitada = True
                    self.up = Nodo(self.data + juego_tablero.tab_celdas[row-1][column].cel_valor)

                    valor, direccion = self.up.minimax_nodo(depth-1, row-1, column, row2, column2, 1, alpha, beta)
                    juego_tablero.tab_celdas[row-1][column].cel_visitada = False
                    direccion = 'arriba'

                    if valor > alpha:
                        alpha = valor
                        direccion_max = direccion

                    if alpha >= beta:
                        return beta, 'arriba'

            if row + 1 <= in_mat-1:
                if not juego_tablero.tab_celdas[row+1][column].cel_visitada:
                    bandera = 1
                    juego_tablero.tab_celdas[row+1][column].cel_visitada = True
                    self.down = Nodo(self.data + juego_tablero.tab_celdas[row+1][column].cel_valor)

                    valor, direccion = self.down.minimax_nodo(depth-1, row+1, column, row2, column2, 1, alpha, beta)
                    juego_tablero.tab_celdas[row+1][column].cel_visitada = False
                    direccion = 'abajo'

                    if valor > alpha:
                        alpha = valor
                        direccion_max = direccion

                    if alpha >= beta:
                        return beta, 'abajo'

            if column - 1 >= 0:
                if not juego_tablero.tab_celdas[row][column-1].cel_visitada:
                    bandera = 1
                    juego_tablero.tab_celdas[row][column-1].cel_visitada = True
                    self.left = Nodo(self.data + juego_tablero.tab_celdas[row][column-1].cel_valor)

                    valor, direccion = self.left.minimax_nodo(depth-1, row, column-1, row2, column2, 1, alpha, beta)
                    juego_tablero.tab_celdas[row][column-1].cel_visitada = False
                    direccion = 'izquierda'

                    if valor > alpha:
                        alpha = valor
                        direccion_max = direccion

                    if alpha >= beta:
                        return beta, 'izquierda'

            if column + 1 <= in_mat-1:
                if not juego_tablero.tab_celdas[row][column+1].cel_visitada:
                    bandera = 1
                    juego_tablero.tab_celdas[row][column+1].cel_visitada = True
                    self.right = Nodo(self.data + juego_tablero.tab_celdas[row][column+1].cel_valor)

                    valor, direccion = self.right.minimax_nodo(depth-1, row, column+1, row2, column2, 1, alpha, beta)
                    juego_tablero.tab_celdas[row][column+1].cel_visitada = False
                    direccion = 'derecha'

                    if valor > alpha:
                        alpha = valor
                        direccion_max = direccion

                    if alpha >= beta:
                        return beta, 'derecha'

            if bandera == 0:
                return self.data, 'hoja'

            return alpha, direccion_max

        # -- para movimiento de jugador
        else:
            row = column2
            column = row2

            if row - 1 >= 0:
                if not juego_tablero.tab_celdas[row-1][column].cel_visitada:
                    bandera = 1
                    juego_tablero.tab_celdas[row-1][column].cel_visitada = True
                    self.up = Nodo(self.data - juego_tablero.tab_celdas[row-1][column].cel_valor)

                    valor, direccion = self.up.minimax_nodo(depth-1, row-1, column, row2, column2, 0, alpha, beta)
                    juego_tablero.tab_celdas[row-1][column].cel_visitada = False
                    direccion = 'arriba'

                    if beta > valor:
                        beta = valor
                        direccion_min = direccion

                    if alpha >= beta:
                        return alpha, 'arriba'

            if row + 1 <= in_mat-1:
                if not juego_tablero.tab_celdas[row+1][column].cel_visitada:
                    bandera = 1
                    juego_tablero.tab_celdas[row+1][column].cel_visitada = True
                    self.down = Nodo(self.data - juego_tablero.tab_celdas[row+1][column].cel_valor)

                    valor, direccion = self.down.minimax_nodo(depth-1, row+1, column, row2, column2, 0, alpha, beta)
                    juego_tablero.tab_celdas[row+1][column].cel_visitada = False
                    direccion = 'abajo'

                    if beta > valor:
                        beta = valor
                        direccion_min = direccion

                    if alpha >= beta:
                        return alpha, 'abajo'

            if column - 1 >= 0:
                if not juego_tablero.tab_celdas[row][column-1].cel_visitada:
                    bandera = 1
                    juego_tablero.tab_celdas[row][column-1].cel_visitada = True
                    self.left = Nodo(self.data - juego_tablero.tab_celdas[row][column-1].cel_valor)

                    valor, direccion = self.left.minimax_nodo(depth-1, row, column-1, row2, column2, 0, alpha, beta)
                    juego_tablero.tab_celdas[row][column-1].cel_visitada = False
                    direccion = 'izquierda'

                    if beta > valor:
                        beta = valor
                        direccion_min = direccion

                    if alpha >= beta:
                        return alpha, 'izquierda'

            if column + 1 <= in_mat-1:
                if not juego_tablero.tab_celdas[row][column+1].cel_visitada:
                    bandera = 1
                    juego_tablero.tab_celdas[row][column+1].cel_visitada = True
                    self.right = Nodo(self.data - juego_tablero.tab_celdas[row][column+1].cel_valor)

                    valor, direccion = self.right.minimax_nodo(depth-1, row, column+1, row2, column2, 0, alpha, beta)
                    juego_tablero.tab_celdas[row][column+1].cel_visitada = False
                    direccion = 'derecha'

                    if beta > valor:
                        beta = valor
                        direccion_min = direccion

                    if alpha >= beta:
                        return alpha, 'derecha'

            if bandera == 0:
                return self.data, 'hoja'

            return beta, direccion_min


# -- ------------------------------------------------------------------------------------------------ Seccion Main -- #
# ------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':

    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

    # -- -------------------------------------------------------------------------------- Inicializacion del juego -- #
    # Mensaje de bienvenida
    version = int(input('\n \nSkynet: ¿Estás listo?, \n\n '
                        '¿Cual version quieres?: 1 = Completa o 2 = Debugging (parametros fijos)? '))
    # version = 2
    time.sleep(.5)

    if version == 1:
        print('\n')
        # solicitar Dificultad
        in_dif = int(input("Elige dificultad (3 = 'facil', 5 = 'dificil'): "))
        # para debugging
        # in_dif = 3

        # solicitar min para aleatorios
        in_min = int(input("Ingresa el numero mínimo para aleatorios (entero > 0): "))
        # para debugging
        # in_min = 1

        # solicitar max para aleatorios
        in_max = int(input("Ingresa el numero máximo para aleatorios (entero > 0): "))
        # para debugging
        # in_max = 15

        # solicitar tamaño de matriz
        in_mat = int(input("Ingresa el valor de N para la matriz N x N (entero > 2): "))
        # para debugging
        # in_mat = 8

        # solicitar nombre de jugador
        in_nm = str(input("Ingresa el nombre del jugador: "))
        in_nom = 'john connor'

        # Dinamica John Connor
        loading = 'John Connor'
        time.sleep(2)
        print('\nBuen intento ...\n')
        time.sleep(1.5)
        for r in range(11):
            print(loading[r], sep='', end=' ', flush=True)
            time.sleep(0.25)

    else:
        print('\n Parametros: \n Dificultad: 3, Min aleatorio: 1, Max aleatorio: 15, Matriz: 8x8')
        in_dif = 3
        in_min = 1
        in_max = 15
        in_mat = 8
        in_nom = 'Johnn Connor'

    # retardo de tiempo en segundos
    time.sleep(1)

    # imprimir mensaje de inicio
    time.sleep(2.5)
    print("\n \n ................ Dia del Juicio Final ................ ")
    time.sleep(1.5)

    # inicializar tablero
    juego_tablero = gen_inicializar()

    # Imprimir tablero inicial
    print(juego_tablero)
    time.sleep(4)
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
