
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Ejercicio motivacion para simulacion montecarlo
# -- Codigo: montecarlo-1.py
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np

TIMES_TO_REPEAT = 10**5
LENGTH = 10**5
CENTER = [LENGTH/2, LENGTH/2]


def in_circle(point):
    x = point[0]
    y = point[1]
    center_x = CENTER[0]
    center_y = CENTER[1]
    radius = LENGTH/2
    return (x - center_x)**2 + (y - center_y)**2 < radius**2


count = inside_count = 0
for i in range(TIMES_TO_REPEAT):
    point = np.random.randint(1, LENGTH), np.random.randint(1, LENGTH)
    if in_circle(point):
        inside_count += 1
    count += 1

pi = (inside_count / count) * 4

print(pi)

