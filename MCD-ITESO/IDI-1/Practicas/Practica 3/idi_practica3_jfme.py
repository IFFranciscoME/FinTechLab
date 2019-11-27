
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
# ciudades a recorrer en el recorrido random
recorrido_c = [data.columns[recorrido_n[i]] for i in range(0, len(recorrido_n))]
# calculo de distancia recorrida
suma = sum([np_data[recorrido_n[i]][recorrido_n[i+1]] for i in range(0, len(recorrido_n)-1)])
print('la distancia total recorrida fue: ' + str(suma))

# tome un número entero N>100 y calcule el recorrido de menor distancia de N listas aleatorias.
sumas = []
ale = 99999
for i in range(0, ale):
    # armar el recorrido en orden
    recorrido_n = list(np.arange(len(data.index)))
    # reordenar aleatoriamente el recorrido
    random.shuffle(recorrido_n)
    # calculo de distancia total recorrida
    sumas.append(sum([np_data[recorrido_n[i]][recorrido_n[i+1]] for i in range(0, len(recorrido_n)-1)]))

print('la distancia total minima, con: ' + str(ale) + ' aleatorios, fue: ' + str(min(sumas)))
