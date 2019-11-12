
# function minimax(position, depth, maximizingPlayer)
# 	if depth == 0 or game over in position
# 		return static evaluation of position
#
# 	if maximizingPlayer
# 		maxEval = -infinity
# 		for each child of position
# 			eval = minimax(child, depth - 1, false)
# 			maxEval = max(maxEval, eval)
# 		return maxEval
#
# 	else
# 		minEval = +infinity
# 		for each child of position
# 			eval = minimax(child, depth - 1, true)
# 			minEval = min(minEval, eval)
# 		return minEval
#
#
# initial call
# minimax(currentPosition, 3, true)


class Nodo:
    # Constructor de la funcion
    def __init__(self, data, ismax):
        """
        :param data: dato del nodo: int
        :param ismax: nodo de movimiento de jugador (True=maximizador, False=minimizador): [True, False]
        """
        self.ismax = ismax
        self.data = data
        self.left = None   # No necesario por default tiene None
        self.right = None  # No necesario por defautl tiene None

    # Insertar nodos para arbol minimax
    def insertar(self, dato, lado, ismax):
        """
        :param dato: dato del nodo: int
        :param lado: si es nodo izquierdo o derecho: str ['left', 'right']
        :param ismax: nodo de movimiento de jugador (True=maximizador, False=minimizador): [True, False]
        :return:
        """
        if self.data:
            if lado == 'left':
                if self.left is None:
                    self.left = Nodo(dato, ismax)
                elif self.right is None:
                    self.right = Nodo(dato, ismax)
                else:
                    self.left.insertar(dato, lado, ismax)
            elif lado == 'right':
                if self.right is None:
                    self.right = Nodo(dato, ismax)
                elif self.left is None:
                    self.left = Nodo(dato, ismax)
                else:
                    self.right.insertar(dato, lado, ismax)
        else:
            self.data = dato

    def minimax(self, profundidad, ismax):
        """
        :param profundidad: nivel de profundidad a buscar: int
        :param ismax: nodo de movimiento de jugador (True=maximizador, False=minimizador): [True, False]
        :return: self.data: int
        """

        print('entrada con profundidad: ' + str(profundidad))
        # Si ya se alcanzo la profundidad desdeada, regresar dato de nodo
        if profundidad == 0:
            print('profundidad == 0')
            return self.data

        # Nodo de jugador maximizador
        if ismax:
            print('ismax == True')
            # El -"infinito" programatico como un numero muy pequeño
            maxeval = -float('inf')
            # Si tiene nodo hijo izquierdo
            if self.left:
                print('ismax = True & self.left == True - entra desde: ' + str(self.data) +
                      ' - profundidad = ' + str(profundidad - 1))
                mmeval = self.left.minimax(profundidad=profundidad-1, ismax=False)
                maxeval = max(maxeval, mmeval)
                return maxeval
            # Si tiene hijo derecho
            elif self.right:
                print('ismax = True & self.right == True - entra con: ' + str(self.data) +
                      ' - profundidad = ' + str(profundidad - 1))
                mmeval = self.right.minimax(profundidad=profundidad-1, ismax=False)
                maxeval = max(maxeval, mmeval)
                return maxeval
            else:
                return self.data

        # Nodo de jugador minimizador
        else:
            print('ismax == False')
            # El +"infinito" programatico como un numero muy grande
            mineval = +float('inf')
            # Si tiene hijo izquierdo
            if self.left:
                print('ismax = False & self.left == True - entra desde: ' + str(self.data) +
                      ' - profundidad = ' + str(profundidad - 1))
                mmeval = self.left.minimax(profundidad=profundidad-1, ismax=True)
                print('calcular el min')
                mineval = min(mineval, mmeval)
                return mineval
            # Si tiene hijo derecho
            elif self.right:
                print('ismax = False & self.right == True - entra con: ' + str(self.data) +
                      ' - profundidad = ' + str(profundidad - 1))
                mmeval = self.right.minimax(profundidad=profundidad-1, ismax=True)
                mineval = min(mineval, mmeval)
                return mineval


# Se inicializa el arbol con un nodo 10 y que sea maximizador
arbol = Nodo(data=10, ismax=True)

arbol.insertar(dato=20, lado='left', ismax=False)
arbol.insertar(dato=21, lado='right', ismax=False)

arbol.insertar(dato=31, lado='left', ismax=True)
arbol.insertar(dato=32, lado='right', ismax=True)

arbol.insertar(dato=33, lado='left', ismax=True)
arbol.insertar(dato=34, lado='right', ismax=True)

# prof = 0                  _____ |10| _____
#                          /                \
# prof = 1              (20)                (21)
#                     /      \             /    \
# prof = 2         |31|      |33|       |34|    |32|


arbol.minimax(profundidad=3, ismax=True)
