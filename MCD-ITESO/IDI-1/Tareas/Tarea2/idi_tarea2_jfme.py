
import numpy as np
import random

# - Genere una matriz simétrica A de tamaño NxN con números enteros aleatorios 100<=x<=200,
# y cuya diagonal contenga sólo ceros.

N = 2
A = np.array(np.random.randint(low=100, high=200+1, size=[N, N]))
np.fill_diagonal(A, 0)
print(A)

# - Genere una lista L con los enteros 1,2,...,N acomodados de forma aleatoria.
L = list(np.arange(1, N+1, 1))
random.shuffle(L)
print(L)

# - Obtenga la suma de los elementos de A cuya posición sean las parejas de números consecutivos de L.
# Es decir, si L=[3,1,2,4], se suman los elementos A[3][1]+A[1][2]+A[2][4].

# A[L[0], L[1]]
# A[L[1], L[2]]
# A[L[2], L[3]]
# A[L[3], L[4]]
# A[L[4], L[5]]

suma_a = [A[L[i]][L[i]] for i in range(0, len(L))]

sum(suma_a)
