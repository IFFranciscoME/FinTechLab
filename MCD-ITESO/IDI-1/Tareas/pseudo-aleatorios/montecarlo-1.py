
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Ejercicio motivacion para simulacion montecarlo
# -- Codigo: montecarlo-1.py
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np

# Simulacion de funcion 1/x con metodo de montecarlo
lista = np.mean([1 / (np.random.uniform(1, 2, 10000)) for _ in range(10000)])

# --
gano = 0
gana = 0

resultados = [1, 2, 3, 4, 5, 6]
numeros_a = [7]
numeros_b = [2, 6, 8]

for _ in range(1000):

    d1 = np.random.choice(a=resultados, size=1, replace=True)
    d2 = np.random.choice(a=resultados, size=1, replace=True)
    suma = d1 + d2

    if suma in numeros_a:
        gano += 1
    elif suma in numeros_b:
        gana += 1
    else:
        while True:
            d1 = np.random.choice(a=resultados, size=1, replace=True)
            d2 = np.random.choice(a=resultados, size=1, replace=True)
            suma2 = d1 + d2
            if suma2 in numeros_a:
                gana += 1
            elif suma2 in suma:
                gano += 1
                break

    print(suma)
