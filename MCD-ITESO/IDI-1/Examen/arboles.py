
import queue
import numpy


class Node:
    # Constructor de clase (inicializador)
    def __init__(self, value, left=None, right=None):
        """
        :param value: int : valor que tendra dentro el nodo
        :param left: 0x1234 : direccion de memoria donde esta el nodo izquierdo
        :param right: 0x1234 : direccion de memoria donde esta el nodo derecho
        :return : sin return especifico
        """
        # Valor del nodo
        self.value = value
        # Indicador de un hijo izquierdo
        self.left = left
        # Indicador de un hijo derecho
        self.right = right

class Tree:
    # Constructor de clase (inicializador)
    def __init__(self, value=None):
        """
        :param value: int : valor con el cual se inicializa el nodo raiz para crear el arbol
        :return : sin return especifico
        """
        self.node = Node(value)

    def insertar(self, value, node=None):
        if node is None:
            node = self.node
        if node.value is None:
            node.value = value
            return
