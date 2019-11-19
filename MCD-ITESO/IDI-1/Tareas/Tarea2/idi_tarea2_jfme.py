
import numpy as np
import random

# - Genere una matriz simétrica A de tamaño NxN con números enteros aleatorios 100<=x<=200,
# y cuya diagonal contenga sólo ceros.
N = 4
A = np.array(np.random.randint(low=100, high=200+1, size=[N, N]))
np.fill_diagonal(A, 0)
# https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.randint.html
# print(A)

# - Genere una lista L con los enteros 1,2,...,N acomodados de forma aleatoria.
L = list(np.arange(1, N+1))
random.shuffle(L)
# https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.shuffle.html
# print(L)

# - Obtenga la suma de los elementos de A cuya posición sean las parejas de números consecutivos de L.
# Es decir, si L=[3,1,2,4], se suman los elementos A[3][1] + A[1][2] + A[2][4].

# NOTA: El conteo para indexacion en python comienza desde 0 y en el inciso pasado se pidio generar la lista desde 1
# se restara 1 a cada numero para desplazar la indexacion en A, conservando el orden de los "lugares" accesados.

print('La matriz A es: ' + '\n' + str(A))
print('\n')
print('La lista L es: ' + str(L))
print('\n')
for i in range(0, len(L)-1):
    print('A[' + str(L[i]) + ',' + str(L[i+1]) + ']' + ' : ' + str(A[L[i]-1][L[i+1]-1]))

suma = sum([A[L[i]-1][L[i+1]-1] for i in range(0, len(L)-1)])
print('------------')
print('total  : ' + str(suma))
