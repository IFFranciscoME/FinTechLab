
import numpy as np
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


