
# -- ---------------------------------------------------------------------------------------------------------------- #
# -- Proyecto: Utilidades para arboles binarios
# -- Archivo: binarytree.py
# -- Repositorio:
# -- Autor: FranciscoME
# -- ---------------------------------------------------------------------------------------------------------------- #

import numpy.random as random

# -- Generar un arbol aleatoriamente
# -- Elegir si sera Binary Tree o Binary Search Tree


class Nodo(object):
    def __init__(self, value, left=None, right=None):
        """
        :param value: valor del nodo
        :param left: hijo izquierdo
        :param right: hijo derecho
        """
        self.left = left
        self.right = right
        self.value = value


# -- ----------------------------------------------------------------------- generar valores aleatorios para nodos -- #

def f_valores_ale(height):
    """
    :param height:
    :return:
    """
    max_node_count = 2 ** (height + 1) - 1
    node_values = list(range(max_node_count))
    random.shuffle(node_values)
    return node_values


# -- --------------------------------------------------------------------------------- generar n hojas aleatorias  -- #

def f_hojas_ale(height):
    """
    :param height:
    :return:
    """

    max_leaf_count = 2 ** height
    half_leaf_count = max_leaf_count // 2

    roll_1 = random.randint(0, half_leaf_count)
    roll_2 = random.randint(0, max_leaf_count - half_leaf_count)

    return roll_1 + roll_2 or half_leaf_count


# -- ------------------------------------------------------------------------------------------------- crear arbol -- #

def f_crear(altura):
    """
    :param altura: niveles que tendra el arbol
    :return:
    """

    valores = f_valores_ale(altura)
    n_hojas = f_hojas_ale(altura)
    root = Nodo(valores.pop(0))
    hojas = set()

    for value in valores:
        node = root
        profundidad = 0
        inserted = False

        while profundidad < altura and not inserted:
            lado = random.choice(('left', 'right'))
            if getattr(node, lado) is None:
                setattr(node, lado, Nodo(value))
                inserted = True
            node = getattr(node, lado)
            profundidad += 1

        if inserted and profundidad == altura:
            hojas.add(node)
        if len(hojas) == n_hojas:
            break

    return root


# instancia_arbol = Nodo(10)
# arbol = f_crear(3)
