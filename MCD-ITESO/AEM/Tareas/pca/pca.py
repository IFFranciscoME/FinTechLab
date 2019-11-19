#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: Rocío Carrasco
"""

import sklearn
import mglearn
from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

#Muestra lo que hace el algoritmo del PCA
mglearn.plots.plot_pca_illustration()
plt.show()

# Base de datos de  cáncer de mama
cancer=load_breast_cancer()
print(cancer.feature_names)
print(cancer.feature_names.shape)

pca=PCA(n_components=2)
pca.fit(cancer.data)
transformada=pca.transform(cancer.data)
print(cancer.data.shape)
print(transformada.shape)
# Graficar componentes principales     
mglearn.discrete_scatter(transformada[:,0],transformada[:,1], cancer.target)
plt.legend(cancer.target_names,loc='best')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.show()

# Escalar los datos
escala=MinMaxScaler()
escala.fit(cancer.data)
escalada=escala.transform(cancer.data)
pca.fit(escalada)
transformada=pca.transform(escalada)
mglearn.discrete_scatter(transformada[:,0],transformada[:, 1],  cancer.target)
plt.legend(cancer.target_names, loc='best')
plt.gca()
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.show()

#%% Comprobar hasta cuantas dimensiones es posible reducir
import numpy as np
w,v = np.linalg.eig(pca.get_covariance()) # Calcular los vectores y valores propios de la martiz de covarianza
indx = np.argsort(w)[::-1] # ordenar los valores de mayor a menor
porcentaje = w[indx]/np.sum(w) # calcular el procentaje de varianza en cada componente
porcent_acum = np.cumsum(porcentaje) # calcular el porcentaje acumulado de los componentes

#%% Verificar el aporte de cada variable en un 
#componente principal
matrix_transform = pca.components_.T
# La matriz de transformacion tiene como columnas 
#el vector propio asociado a cada componente principal
# La magnitud de cada elemento de ese vector propio es 
#el aporte de cada variable en ese componente principal

# Graficamente ese aporte se puede ver si graficamos 
#el vector propio
plt.bar(np.arange(30),matrix_transform[:,0])
plt.xlabel('Num variable real')
plt.ylabel('Magnitud vector asociado')
plt.show()
