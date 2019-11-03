
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Estructuras de datos
# -- Codigo: estructura_arbol.py
# -- Autor: Francisco ME
# -- Repositorio:
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np

# Previo
# -- funcion generadora de arboles binarios
# -- Cantidad de
# -- visualizacion de arbol: Dendograma

# 1. Una función que encuentre el mínimo valor de un árbol dado por su raíz.

# 2. Una función que reciba un entero y devuelva True o False de acuerdo a si está o no en el árbol
# que tiene como raíz el nodo que llamó la función. Haga que imprima todos los datos de los nodos
# que fueron revisados (si no se encuentra imprimiría todos).

# 3. Una función que reciba un entero y devuelva la cantidad de incidencias del valor en el árbol que
# tiene como raíz el nodo que llamó la función.


class Nodo:
    """

    """
    def __init__(self, dato_ini):
        """
        :param dato_ini:
        dato_nodo = 3
        """
        # Por default se inicializa con un None
        self.izq = None
        # Por default se inicializa con un None
        self.der = None
        # Se indica que el dato inicial se asigna al dato del nodo
        self.dato_nodo = dato_ini
        # print('se instancio un nodo con dato: ' + str(dato_ini))

    def insertar(self, dato_in):
        """
        :param dato_in:
        :return:
        """

        # ale = np.random.choice(['izq', 'der'], 1, replace=True)[0]

        if self.dato_nodo:
            if self.izq is None:
                self.izq = Nodo(dato_in)
            elif self.der is None:
                self.der = Nodo(dato_in)
            else:
                # getattr(self, ale).insertar(dato_in)
                self.izq.insertar(dato_in)
        else:
            self.dato_nodo = dato_in

    def insertar_bst(self, dato_insertar):
        """
        :param dato_insertar:
        :return:
        """
        # print('se busca insertar en algun nodo el siguiente dato: ' + str(dato_insertar))
        if self.dato_nodo:
            # print('el nodo consultado ya tiene el dato: ' + str(self.dato_nodo))
            # verificar si el dato a insertar es menor que el dato del nodo mandar al siguiente nodo de la izquierda
            if dato_insertar < self.dato_nodo:
                # verificar si no existe dato en el nodo de la izquierda
                if self.izq is None:
                    # instanciar un nuevo nodo por la izquierda
                    # print('se creo un nodo en la izq, porque: ' + str(dato_insertar) + ' < ' + str(self.dato_nodo))
                    self.izq = Nodo(dato_insertar)
                # verificar si si existe dato en el nodo de la izquierda
                else:
                    # volver a correr la funcion desde este nodo
                    # print('izquierda del nodo actual esta ocupada')
                    self.izq.insertar_bst(dato_insertar)
            # verificar si el dato a insertar es mayor que el dato del nodo, mandar al siguiente nodo de la derecha
            elif dato_insertar > self.dato_nodo:
                # verificar si no existe dato en el nodo de la derecha
                if self.der is None:
                    # instanciar un nuevo nodo por la derecha
                    # print('se creo un nodo en la der, porque: ' + str(dato_insertar) + ' > ' + str(self.dato_nodo))
                    self.der = Nodo(dato_insertar)
                # verificar si si existe dato en el nodo de la derecha
                else:
                    # volver a correr la funcion desde este nodo
                    # print('derecha del nodo actual esta ocupada')
                    self.der.insertar_bst(dato_insertar)
        else:
            # print('entro en el self.dato_nodo = False con: ' + str(self.dato_nodo))
            self.dato_nodo = dato_insertar

    def buscar_min(self, dato_min):
        """
        :param dato_min:
        :return:
        """

        if dato_min < self.dato_nodo:
            if self.izq is None:
                return None, None
            return self.izq.buscar_min(dato_min)
        elif dato_min > self.dato_nodo:
            if self.der is None:
                return None, None
            return self.der.buscar_min(dato_min)
        else:
            # encontro el nodo donde esta el dato deseado
            # print('aqui: ' + str(self.dato_nodo))
            if self.izq is None:
                # print('self.izq es None')
                # este fue el ultimo nodo
                return self.dato_nodo
            else:
                # print('self.izq no es None')
                return self.izq.buscar_min(self.izq.dato_nodo)

    def existencia(self, dato_exi, lista_exi=[]):
        """
        Funcion que busca la existencia de un numero en algun nodo del arbol
        :param dato_exi: Dato a buscar su existencia
        :param lista_exi: Lista donde se guardaran los nodos consultados
        :return: dato_exi, lista_exi
        """

        # Si el valor es el mismo que el nodo a consultar
        if dato_exi == self.dato_nodo:
            lista_exi.append(self.dato_nodo)
            return True, lista_exi
        # en caso de que no haya dato en el nodo de la izq
        elif dato_exi < self.dato_nodo and self.izq is None:
            return False, lista_exi
        # en caso de que no haya dato en el nodo de la der
        elif dato_exi >= self.dato_nodo and self.der is None:
            return False, lista_exi
        # revisar si el valor es el mismo que el nodo y que el nodo de la izq y der existan
        elif dato_exi != self.dato_nodo and self.izq is None and self.der is None:
            return False, lista_exi
        else:
            if dato_exi < self.dato_nodo:
                lista_exi.append(self.dato_nodo)
                return self.izq.existencia(dato_exi)
            elif dato_exi >= self.dato_nodo:
                lista_exi.append(self.dato_nodo)
                return self.der.existencia(dato_exi)

    def buscar(self, dato_b):
        """
        Funcion para buscar cantidad de incidencias de un dato en el arbol
        :return:
        """
        if self.dato_nodo == dato_b:
            print('encontro ' + str(self.dato_nodo) + ' == ' + str(dato_b))
            return True
        elif self.dato_nodo > dato_b:
            if self.izq:
                print('busco en nodo izq ' + str(self.dato_nodo) + '>' + str(dato_b))
                return self.izq.buscar(dato_b)
            else:
                return False
        else:
            if self.der:
                print('busco en nodo der ' + str(self.dato_nodo) + '<' + str(dato_b))
                return self.der.buscar(dato_b)
            else:
                return False

    def incidencia(self, dato, lista_inc=0):
        if self.dato_nodo:
            print('entro buscar a: ' + str(dato) + ' empezando por: ' + str(self.dato_nodo))

            if self.buscar(dato):
                print('contar 1')
                # lista_inc += 1
                return self.der.incidencia(dato) or self.izq.incidencia(dato)
            else:
                print('contar 0')
                # lista_inc += 1
                return print('contar 0')
        else:
            return 'termino'


# # arbol de imagen
# arbol = Nodo(8)
# arbol.insertar(3)
# arbol.insertar(10)
# arbol.insertar(2)
# arbol.insertar(6)
# arbol.insertar(15)
# arbol.insertar(2)
# arbol.insertar(5)
# arbol.insertar(9)
# arbol.insertar(15)
# arbol.insertar(2)

# arbolp = arbol

# Arbol con crecimiento aleatorio
regar = list(np.random.choice(list(range(1, 10)), 12, replace=True))
arbol = Nodo(10)
arbol_bst = Nodo(10)
[arbol.insertar(i) for i in regar]
[arbol_bst.insertar_bst(i) for i in regar]

print('los valores fueron: ')
print([10] + regar)
# Req 1: Encontrarle el minimo a una rama
arbol.buscar_min(2)
arbol_bst.buscar_min(2)

# Req 2: Encontrar la existencia de un numero y mostrar la ruta buscada
existe, lista = arbol.existencia(2)
print(existe)
print(lista)

# # Req 3
# print(crecimiento)
incidenciass = arbol.incidencia(2)
print(incidenciass)
