
import numpy as np


class Tablero(object):

    # Inicializar el tablero
    def __init__(self, size, player, dificultad, val_min, val_max):
        # El tamaño del tablero [8, 8]
        self.size = size
        # Nombre del jugador
        self.player = player
        # Nivel de dificultad
        self.dificultad = dificultad
        # valor minimo para simular los aleatorios
        self.val_min = val_min
        # valor maximo para simular los aleatorios
        self.val_max = val_max
        # lista de las celdas para crear
        self.cells = [[Celda(np.random.randint(val_min, val_max), (i, j)) for j in range(size)] for i in range(size)]

    # Funcion para imprimir tablero
    def __str__(self):
        res = ""
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                res += f'|__{self.cells[i][j]}__'
            res += '|\n'
        return res

    # # if 1 digit:
    # #   is controller visiting:
    # #       f'{self.controller.symbol
    #
    # # Calcular el score que cada jugador lleva
    # def score(self):
    #
    #     return 1
    #
    # # validar si se puede hacer el movimiento
    # def validar_movimiento(self, casilla):
    #
    #     return True  # False
    #
    # def play(self):
    #     # while terminado:
    #         # hacer el turno
    #
    #     return 1
    #
    # # ejecutar un turno sabiendo quien le toca
    # def turno(self):
    #     if cpu:
    #         # Hacer el arbol
    #         return 'cpu'
    #     if player:
    #         # Pedir entrada
    #         return 'player'

    # Calcular las casillas posibles para un movimiento
    # def casillas_posibles(self):


class Celda(object):
    def __init__(self, valor, ubicacion):
        # Valor dentro de la celda
        self.valor = valor
        # Para identificar el jugador que visito la celda
        self.controller = None
        # Para identificar si la celda fue visitada (independiente de quien la visito)
        self.visitada = False
        # Ubicacion en el tablero de la celda
        self.locacion = ubicacion

    # Fucion para imprimir contenido de celda
    def __str__(self):
        if len(str(self.valor)) % 2 == 0:
            if self.controller:
                if self.controller.is_visiting(self):
                    return f'{self.controller.simbolo*2}{self.valor}{self.controller.simbolo*2}'
                else:
                    return f'{self.controller.simbolo}{self.valor}{self.controller.simbolo}'
            else:
                return f'  {self.valor}'
        else:
            if self.controller:
                if self.controller.is_visiting(self):
                    return f'{self.controller.simbolo*1}{self.valor}{self.controller.simbolo*1}'
                else:
                    return f'{self.controller.simbolo}{self.valor}{self.controller.simbolo}'
            else:
                return f'   {self.valor}'


class Jugador(object):
    def __init__(self, ismax, iscpu, simbolo):
        # si es un max o un min
        self.ismax = ismax
        # si es el cpu o una persona
        self.iscpu = iscpu
        # el simbolo para distinguirlo en el tablero
        self.simbolo = simbolo
        # los puntos que lleva
        self.puntos = 0


jugadores = [Jugador(ismax=True, iscpu=True, simbolo='*'), Jugador(ismax=False, iscpu=False, simbolo='°')]
juego = Tablero(size=8, player=jugadores, dificultad=3, val_min=1, val_max=15)
print(juego)

# if __name__ == '__main__':
#     juego = Tablero(size=8, player='persona', dificultad=3, val_min=1, val_max=15)

# --- VERSION 2 --


from queue import Queue as queue
import numpy as np


class Nodo:
    def __init__(self, value, left=None, right=None, ismin=False):
        self.value = value
        self.left = left
        self.right = right
        self.ismin = ismin


class Tree:
    def __init__(self, value=None):
        self.node = Nodo(value)

    def insert(self, value, node=None):
        if node is None:
            node = self.node
        if node.value is None:
            node.value = value
            return
        if node.left is None:
            node.left = Nodo(value)
            return
        if node.right is None:
            node.right = Nodo(value)
            return
        return self.insert(value, node.left)

    def generateminimax(self, values):
        aux = queue()
        current = self.node
        counter = 1
        for val in values:
            level = np.floor(np.log2(counter)) + 1
            ismin = level % 2 == 0
            if not current.value:
                current.value = val
                current.isMin = ismin
            elif not current.left:
                current.left = Nodo(val, ismin=ismin)
                aux.put(current.left)
            elif not current.right:
                current.right = Nodo(val, ismin=ismin)
                aux.put(current.right)
                current = aux.get()
            counter = counter + 1

    def minimax(self, node):
        # Caso base (para recursividad)
        if not node.left and not node.right:
            return node.value
        lista_nodos = []
        if node.left:
            lista_nodos.append(self.minimax(node.left))
        if node.right:
            lista_nodos.append(self.minimax(node.right))

        if not node.ismin:
            return max(lista_nodos)
        else:
            return min(lista_nodos)


lista = [10, 4, 5, 10, 3, 42, 3, 2, 3, 4, 10, 3, 5, 6, 10]
tree = Tree()
tree.generateminimax(lista)

print(tree.minimax(tree.node))
