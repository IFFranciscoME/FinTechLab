
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Generación y visualización de pseudo-aleatorios
# -- Codigo: pseudo-aleatorios.py
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

# Importar librerias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
from numpy.random import seed

# Fijar la semilla para aleatorios
seed(2)

# Ejercicio 1: Experimento con dados
n = [np.random.randint(low=1, high=6, size=2).sum() for _ in range(1000)]

# Ejercicio 2: Caja con canicas
colores = ['azul', 'roja', 'blanca']
repeticion = [2, 3, 5]
caja = [colores[i] for i in range(len(colores)) for j in range(repeticion[i])]
experimento = [np.random.choice(caja, 3, replace=False) for _ in range(10)]

# Ejercicio 3: Contestar Examen
preguntas = ['pregunta_' + str(i) for i in range(1, 11)]
opciones = ['A', 'B', 'C', 'D']
resultados = pd.DataFrame({'e_' + str(i): np.random.binomial(n=1, p=.25, size=10) for i in range(500)}, index=preguntas)
calificaciones = resultados.sum()

# Ejercicio 4: Crucero de coches
trafico = np.random.poisson(lam=20, size=60)
trafico.min()
trafico.max()

# Ejercicio 5: Estaturas de poblacion
media = 1.68
desvest = 0.14
muestra = np.random.normal(loc=media, scale=desvest, size=500)
muestra.mean()
muestra.min()
muestra.max()

# Ejercicio 6: Barras de metal
minimo = 80
maximo = 90
esperado = 83
clases = 10
muestra = 10000
valores = np.random.triangular(left=minimo, mode=esperado, right=maximo, size=muestra)
plot.hist(x=valores, bins=clases)

# Ejercicio 7: Exponencial Vs Gamma
muestras_e = 10000
media_e = 10
muestras_g = 10000
alfa_g = 2
beta_g = 5
barras = 10
exp = np.random.exponential(scale=media_e, size=muestras_e)
gam = np.random.gamma(shape=alfa_g, scale=beta_g, size=muestras_g)
plot.hist(x=exp, bins=barras)
plot.hist(x=gam, bins=barras)
