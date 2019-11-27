
import numpy as np
import random

# Inicialice la semilla de aleatoriedad con un valor fijo arbitrario.
random.seed(123)

# Genere una lista L de 100 números enteros en [5,100].
# se le pone el +1 en el 100 ya que la funcion np.random.randint utiliza un intervalo semiabierto en limite sup
L = np.random.randint(5, 100+1)

# Genere una lista M de 100 números reales en [3,10].
M = [random.uniform(3, 10) for _ in range(0, 100)]
# longitud de lista
len(M)

# Genere 20 listas de 50 números reales en [0,10].
listas = [[random.uniform(3, 10) for _ in range(0, 50)] for _ in range(0, 20)]
# listas
len(listas)
# longitud de listas
[len(listas[i]) for i in range(0, 20)]

# Imprima el promedio de cada una de las listas generadas, así como el promedio de los promedios.
# Realice cada una de esas dos acciones en una sola línea de código.
promedios = [np.mean(listas[i]) for i in range(0, 20)]
promedio_de_promedios = np.mean([np.mean(listas[i]) for i in range(0, 20)])
