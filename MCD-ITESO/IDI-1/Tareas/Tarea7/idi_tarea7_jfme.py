
import numpy as np


class Nodo:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def generaramp(lista, root, i, n_lon):
    # Sustituto del while, comparar contador de nivel que se visita con longitud de lista de entrada
    if i < n_lon:
        temp = Nodo(lista[i])
        # print('el nodo tiene: ' + str(temp))
        root = temp
        # agregar izquierdo
        root.left = generaramp(lista, root.left, 2 * i + 1, n_lon)
        # agregar derecho
        root.right = generaramp(lista, root.right, 2 * i + 2, n_lon)
    return root


n = 7
lista_entrada = list(np.arange(1, n + 1, 1))
longitud = len(lista_entrada)
raiz = None
arbol = generaramp(lista_entrada, raiz, 0, longitud)
