
# -- EJERCICIO 8
import pandas as pd
import numpy as np
from collections import deque

# Utilizando el archivo datfraex.xlsx y escriba código en Python que lea hoja xy en un Dataframe xy
xy = pd.read_excel('datfraex.xlsx', sheet_name='xy')

# y sobre este agregue una columna llamada Budget que contenga los valores en dólares de los valores
# de la columna Presupuesto (que están en pesos). Use la tasa de cambio 1 USD = 19.23 MXN.
xy['Budget'] = xy['Presupuesto']/19.23

# Imprima los años en los que los presupuestos (en pesos) fueron menores del promedio de todos.
print(list(xy.index[xy['Budget'] <= xy['Budget'].mean()]))

# -- EJERCICIO 10
# Emule el experimento de obtener la suma de tres dados. Genere una lista aleatoria con los
# resultados de 2500 lanzamientos. De acuerdo a los resultados,
# imprima cuál es el resultado más probable y cuál el menos.

# cantidad de veces que se repite el experimento de lanzar 3 dados
n = 2500
# realizar el experimento
suma = [(np.random.randint(1, 6, 1) + np.random.randint(1, 6, 1) + np.random.randint(1, 6, 1))[0] for _ in range(n)]
# identificar los resultados de las sumas que ocurrieron (los valores unicos)
ocurrencias = list(set(suma))
# contar cuantas veces ocurrio cada resultado de la suma
conteos = [suma.count(i) for i in ocurrencias]
# identificar el numero que mas veces ocurrio y por lo tanto seria el "mas probable"
mas_probable = ocurrencias[np.argmax(conteos)]
print('el mas probable fue: ' + str(mas_probable))
# identificar el numero que menos veces ocurrio y por lo tanto seria el "menos probable"
menos_probable = ocurrencias[np.argmin(conteos)]
print('el menos probable fue: ' + str(menos_probable))

# -- Ejercicio 9
# Históricamente en un banco se reciben a 35 clientes cada hora. Emule de forma aleatoria el comportamiento
# del número de clientes en el banco durante 10 días (jornadas de 8 horas). Imprima el día en qué se atendió
# a más clientes y en el que se atendió a menos.

ctexhora = 35
dias = 10
jornada = 8
horario = range(9, 17)
comportamiento = pd.DataFrame(np.random.poisson(ctexhora, [dias, jornada]))
comportamiento.columns = horario
comportamiento.index = ['lunes_18', 'martes_19', 'miercoles_20', 'jueves_21', 'viernes_22',
                        'lunes_25', 'martes_26', 'miercoles_27', 'jueves_28', 'viernes_29']

comportamiento['clientes_totales'] = [sum(comportamiento.iloc[i, :]) for i in range(dias)]

dia_max = comportamiento.index[np.where(comportamiento['clientes_totales'] == max(comportamiento['clientes_totales']))]
print('el dia con MAS clientes fue: ' + str(dia_max[0]))
dia_min = comportamiento.index[np.where(comportamiento['clientes_totales'] == min(comportamiento['clientes_totales']))]
print('el dia con MENOS clientes fue: ' + str(dia_min[0]))

# -- Ejercicio 11
# En base a la clase nodo para un árbol binario, escriba un método en la clase llamado imprimerev que imprima
# los nodos por profundidad en sentido inverso.


# Clase Nodo
class Nodo:
    # Constructor de la clase
    def __init__(self, dato):
        """
        :param dato: dato dentro del nodo
        """
        # dato dentro del nodo
        self.dato = dato
        # nodo de izquierda
        self.izquierda = None
        # nodo de derecha
        self.derecha = None


def reversa(raiz):
    # lista para guardar info final
    final = list()
    # lista auxiliar
    s = list()
    # objeto tipo deque de libreria collections
    queue = deque()
    # se deja la raiz
    queue.append(raiz)

    # while para buscar mientras la lista tenga algo
    while len(queue) > 0:

        # sacar el nodo y volverlo raiz
        raiz = queue.pop()
        s.append(raiz)

        # agregar el nodo derecha
        if raiz.derecha:
            queue.append(raiz.derecha)

        # agregar el nodo izquierda
        if raiz.izquierda:
            queue.append(raiz.izquierda)

    # va sacando los elementos y los deja en la lista para imprimirla al final
    while len(s) > 0:
        raiz = s.pop()
        final.append(raiz.dato)

    # regresa la lista final
    return final


# Regar el arbol para que crezca
arbol = Nodo(2)
arbol.izquierda = Nodo(3)
arbol.derecha = Nodo(5)
arbol.izquierda.izquierda = Nodo(7)
arbol.izquierda.derecha = Nodo(11)
arbol.derecha.izquierda = Nodo(13)
arbol.derecha.derecha = Nodo(17)

# Resultado
resultado = reversa(arbol)
print('resultado obtenido: ' + str(resultado))
print('resultado esperado: 17 13 5 11 7 3 2')
