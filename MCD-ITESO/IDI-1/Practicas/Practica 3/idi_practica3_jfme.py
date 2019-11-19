
import numpy as np
import os
import pandas as pd
import random

random.seed(30)
os.chdir("C:/Users/rodrigsa/Documents/Maestría/Programación/Tarea3Sara")

data = pd.read_excel('/dist.xlsx', sheet_name='8c_test')

# La tabla adjunta contiene las distancias entre 8 ciudades de México.

# Genere código en Python que:
# En base a una lista de las ciudades dada en un orden cualquiera
# calcule la distancia total de hacer el recorrido en ese orden.

# Tome un número entero N>100 y calcule el recorrido de menor distancia de N listas aleatorias.

col = data.Ciudad
vector = col.index

colr = random.sample(range(8),8)
vector1 = col[random.sample(range(8),8)].index #
