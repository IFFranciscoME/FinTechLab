
import pandas as pd
import random
import numpy as np

random.seed(30)

# leer datos de entrada
data = pd.read_excel('dist.xlsx', sheet_name='8c_test')
# asignar a index los nombres de las ciudades
data.index = data['Ciudad']
# quitar columna 'Ciudad'
data = data.drop('Ciudad', axis=1)
# hacer un array con solo el contenido del dataframe
np_data = np.array(data)

# La tabla adjunta contiene las distancias entre 8 ciudades de México.
# Genere código en Python que:
# En base a una lista de las ciudades dada en un orden cualquiera
# calcule la distancia total de hacer el recorrido en ese orden.

# armar el recorrido random
recorrido_n = list(np.arange(len(data.index)))
random.shuffle(recorrido_n)

# -- ---------------------------------------------------------------------------------------------------------------- #
# Modifique su código de la Actividad 3 para que:
# se calcule la distancia si la ruta es cíclica (es decir, se regresa al punto inicial)
recorrido_n.append(recorrido_n[0])
# -- ---------------------------------------------------------------------------------------------------------------- #

# ciudades a recorrer en el recorrido random
recorrido_c = [data.columns[recorrido_n[i]] for i in range(0, len(recorrido_n))]
# calculo de distancia recorrida
suma = sum([np_data[recorrido_n[i]][recorrido_n[i+1]] for i in range(0, len(recorrido_n)-1)])
print('la distancia total recorrida fue: ' + str(suma))

# -- ---------------------------------------------------------------------------------------------------------------- #
# en vez de calcular las N listas de formar aleatoria, inicie con una lista aleatoria y
# calcule la siguiente lista intercambiando dos posiciones aleatorias.
# -- ---------------------------------------------------------------------------------------------------------------- #

# armar el recorrido en orden
recorrido_n = list(np.arange(len(data.index)))

# reordenar aleatoriamente el recorrido
random.shuffle(recorrido_n)

# lista de posiciones para hacer intermcabios
intercambios = list(np.random.choice(recorrido_n, 2, replace=False))

# intercambiar contenido utilizando los indices
recorrido_n[intercambios[0]], recorrido_n[intercambios[1]] = recorrido_n[intercambios[1]], recorrido_n[intercambios[0]]

# calculo de distancia total recorrida
sum([np_data[recorrido_n[i]][recorrido_n[i+1]] for i in range(0, len(recorrido_n)-1)])

