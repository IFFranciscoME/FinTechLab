
from queue import Queue


class Nodo(object):

    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None

    def insertar(self, dato, lado):
        if self.dato:
            if lado == 'izq':
                if self.izq is None:
                    self.izq = Nodo(dato)
                elif self.der is None:
                    self.der = Nodo(dato)
                else:
                    self.izq.insertar(dato, lado)
            elif lado == 'der':
                if self.der is None:
                    self.der = Nodo(dato)
                elif self.izq is None:
                    self.izq = Nodo(dato)
                else:
                    self.der.insertar(dato, lado)
        else:
            self.dato = dato

    def buscar_bfs(self):
        cola = Queue()
        lista = []
        cola.put(self)
        lista.append(self.dato)
        print(lista)
        while not cola.empty():
            dato = cola.get()
            print(dato)
            if dato.der:
                cola.put(self.der)
                lista.append(self.der.dato)
            elif dato.izq:
                cola.put(self.izq)
                lista.append(self.izq.dato)

        print(lista)


arbol = Nodo(2)
arbol.insertar(5, 'izq')
arbol.insertar(7, 'der')

arbol.insertar(1, 'izq')
arbol.insertar(6, 'der')

arbol.insertar(3, 'der')
arbol.insertar(4, 'izq')

arbol.buscar_bfs()

import numpy as np
np.random.binomial()
