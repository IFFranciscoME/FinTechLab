
import numpy as np
import pandas as pd
import random
import math

# -- -------------------------------------------------------------------------------  Ejercicio 1: Aguja de buffon -- #
# -- -------------------------------------------------------------------------------- ---------------------------- -- #

n = 1000
cruces = np.zeros((1, n))

for i in range(0, n):
    angulo = np.random.rand()*math.pi/2
    # print(angulo)
    d = np.random.rand()*1/2
    # print(d)

    if d <= (math.sin(angulo)/2):
        cruces[0, i] = 1

frac = cruces.sum()/n
estimate = 2/frac

print(estimate)

# -- ---------------------------------------------------------------------------------  Ejercicio 2: Rutas Tarea 3 -- #
# -- ---------------------------------------------------------------------------------- -------------------------- -- #

# Basado en la Tarea 3 realice el siguiente código en Python. Use para hacer pruebas la tabla adjunta.
random.seed(30)
# leer datos de entrada
data = pd.read_excel('tarea5IDI1.xlsx', sheet_name='15c')
# asignar a index los nombres de las ciudades
data.index = data.iloc[:, 0]
# quitar columna 'Ciudad'
data = data.drop(' ', axis=1)
# hacer un array con solo el contenido del dataframe
np_data = np.array(data)
# armar el recorrido random
recorrido_n = list(np.arange(len(data.index)))
random.shuffle(recorrido_n)

# -------------------------------------------------------------------------------------------------------- Tarea 3 -- #

rutas = []
distancias = []

# 12.- Repita los pasos del 1 al 11 M = 100 veces
for _ in range(0, 100):
    # 1.- Declare una variable T = 100
    T = 1000

    # 2.- Tome una ruta cualquiera inicial C1
    C1 = recorrido_n

    # 10.- Repita los pasos 3 al 9 hasta que T < 1
    while T > 1:
        # 8.- repita N = 30 veces los pasos del 3 al 7
        for N in range(0, 30):
            # 3.- Obtenga una nueva C2 intercambiando de forma aleatoria dos posiciones de C1
            C2 = list(C1)
            intercambios = list(np.random.choice(C1, 2, replace=False))
            C2[intercambios[0]], C2[intercambios[1]] = C2[intercambios[1]], C2[intercambios[0]]

            # 4.- Calcule la distancia total de cada una E1 y E2
            E1 = sum([np_data[C1[j]][C1[j+1]] for j in range(0, len(C1)-1)])
            E2 = sum([np_data[C2[k]][C2[k+1]] for k in range(0, len(C2)-1)])

            # 5.- Calcule q = e^(E1-E2)/T
            q = math.e**((E1-E2)/T)

            # 6.- Obtenga un número aleatorio real p [0,1]
            p = np.random.random(1)[0]

            # 7.- si p < q haga que C1 tome el valor de C2
            if p < q:
                C1 = C2

            # 11.- Guarde el valor de C1 en una lista de rutas y su distancia en una lista de distancias
            # lista de rutas
            rutas.append(C1)
            # lista de distancias totales por ruta
            distancias.append(sum([np_data[C1[i]][C1[i+1]] for i in range(0, len(C1)-1)]))

        # 9.- Disminuya en 10% el valor de T
        T = T*.90

distancia_minima = np.argmin(distancias)
ruta_distancia_minima = rutas[distancia_minima]
ciudades = list(data.index)
recorrido = [ciudades[ruta_distancia_minima[c]] for c in range(0, len(ciudades))]
print('el recorrido fue: \n')
print(recorrido)
print('\n con una distancia de: ' + str(distancia_minima))
