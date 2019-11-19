# -*- coding: utf-8 -*-
"""


@author: rociocarrasco
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

#%% Generar datos para el clustering
semilla = 2
X,Y = make_blobs(n_samples=1500,random_state=semilla)

plt.scatter(X[:,0],X[:,1])
plt.show()

#%% Aplicar KMeans
#model = KMeans(n_clusters=4,random_state=semilla,init='random')
model = KMeans(n_clusters=3,random_state=semilla,init='k-means++')
model = model.fit(X)
grupos = model.predict(X)

centroides = model.cluster_centers_

plt.scatter(X[:,0],X[:,1],c=grupos)
plt.plot(centroides[:,0],centroides[:,1],'x')
plt.show()

#%% Criterios de seleccion
inercias = np.zeros(15)
for k in np.arange(1,15):
    model = KMeans(n_clusters=k,random_state=semilla,init='random')
    model = model.fit(X)
    inercias[k] = model.inertia_
    
plt.plot(np.arange(1,15),inercias[1:])
plt.xlabel('Num grupos')
plt.ylabel('Inercia global')
plt.show()














