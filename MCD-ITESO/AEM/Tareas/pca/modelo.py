
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Analisis de Componentes Principales para Modelo de Regression Lineal aplicado a Trading
# -- Codigo: Modelo
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import matplotlib.pyplot as plt
import numpy as np                                        # tratamiento cientifico de numeros
import pandas as pd                                       # dataframes
from datetime import datetime                             # tratamiento de datetime
from functools import reduce                              # para la union de los dataframes
from os import listdir, getcwd                            # para leer todos los archivos de un folder
from os.path import isfile, join                          # encontrar y unir archivos en un folder
from datos import pd_hist as precios

from sklearn.decomposition import PCA

# Para visualizar data frames en consola
pd.set_option('display.max_rows', None)                   # sin limite de renglones maximos para mostrar pandas
pd.set_option('display.max_columns', None)                # sin limite de columnas maximas para mostrar pandas
pd.set_option('display.width', None)                      # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas de un pandas dataframe
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso

# -- ------------------------------------------------------------------------------- Datos de CALENDARIO ECONOMICO -- #

# Obtener el director donde se encuentran todos los archivos
directorio = getcwd() + '/archivos/'

# Obtener una lista de todos los archivos de datos
archivos_ce = [f for f in listdir(directorio) if isfile(join(directorio, f))]


# -- Funcion para leer y acomodar los datos de cada archivo que este en la carpeta 'archivos'

def f_datos_ce(p0_ind):

    # print('archivo revisado: ' + str(p0_ind))
    # Datos de entrada
    datos = pd.read_csv('archivos/' + p0_ind)

    # Convertir columna de fechas a datetime
    datos['DateTime'] = [datetime.strptime(datos['DateTime'][i], '%m/%d/%Y %H:%M:%S')
                         for i in range(0, len(datos['DateTime']))]

    # Ordernarlos de forma ascendente en el tiempo
    datos.sort_values(by=['DateTime'], inplace=True, ascending=True)
    datos = datos.reset_index(drop=True)

    # Agregar columna con numero de año y semana (Servira para empatar fecha de indicador con fecha de precio)
    datos['Year_Week'] = [datos.loc[i, 'DateTime'].strftime("%Y") + '_' +
                          datos.loc[i, 'DateTime'].strftime("%W") for i in range(0, len(datos['DateTime']))]

    # Solo tomar las columnas para el ejercicio
    datos = datos[['Year_Week', 'Actual']]

    # print(datos.head())

    return datos


# Leer todos los archivos y unir los DataFrames
dataframes = [f_datos_ce(p0_ind=archivos_ce[i]) for i in range(0, len(archivos_ce))]
datos_ce = reduce(lambda left, right: pd.merge(left, right, on=['Year_Week'], how='inner'), dataframes)

# Renombrar las columnas
variables_ce = ['x_' + str(i) for i in range(0, len(archivos_ce))]
datos_ce.columns = ['Year_Week'] + variables_ce

# -- ---------------------------------------------------------------------------------------------- Datos de OANDA -- #

# Generacion de variables explicativas
datos_fx = precios[['TimeStamp', 'Close', 'Open']]

# Convertir a valor tipo float
datos_fx.loc[:, 'Close'] = datos_fx.loc[:, 'Close'].astype(float)
datos_fx.loc[:, 'Open'] = datos_fx.loc[:, 'Open'].astype(float)

# Calcular el rendimiento logaritmico como variable a explicar Y
datos_fx.loc[:, 'log_ret'] = np.log(datos_fx.loc[:, 'Close']/datos_fx.loc[:, 'Close'].shift(1))

# Calcular la diferencia entre precio de cierre y apertura multiplicado por el multiplicador (PIP)
datos_fx.loc[:, 'pips_co'] = (datos_fx.loc[:, 'Close'] - datos_fx.loc[:, 'Open'])*10000

# Eliminar el NaN inicial
datos_fx = datos_fx.dropna()

# Resetear index de data frame
datos_fx = datos_fx.reset_index(drop=True)

# Convertir columna de fechas a datetime
datos_fx['TimeStamp'] = pd.to_datetime(datos_fx['TimeStamp'])

# Agregar columna de semana
# datos_fx['Semana'] = [datos_fx.loc[i, 'TimeStamp'].strftime("%W") for i in range(0, len(datos_fx['TimeStamp']))]
datos_fx['Year_Week'] = [datos_fx.loc[i, 'TimeStamp'].strftime("%Y") + '_' +
                         datos_fx.loc[i, 'TimeStamp'].strftime("%W") for i in range(0, len(datos_fx['TimeStamp']))]

# -- --------------------------------------------------------------------------- Generacion de dataset para modelo -- #

# unir los dos dataframes para obtener el dataframe a usar en el modelo
datos_md = pd.merge(datos_fx, datos_ce, on=['Year_Week'], how='inner')

# eliminar la columna Year_Week
datos_md = datos_md.drop(['Year_Week'], axis=1)

# -- --------------------------------------------------------------------------------------------------------- PCA -- #
pca = PCA(n_components=4)
datos_pca = datos_md.iloc[:, 5:]
pca.fit(datos_pca)
transformada = pca.transform(datos_pca)
# mglearn.discrete_scatter(transformada[:, 1], transformada[:, 2])
# plt.xlabel('PCA 1')
# plt.ylabel('PCA 2')
# plt.show()

# comprobar dimensiones maximas para reducir
w, v = np.linalg.eig(pca.get_covariance())  # Calcular los vectores y valores propios de la martiz de covarianza
indx = np.argsort(w)[::-1]  # ordenar los valores de mayor a menor
porcentaje = w[indx]/np.sum(w)  # calcular el procentaje de varianza en cada componente
porcent_acum = np.cumsum(porcentaje)  # calcular el porcentaje acumulado de los componentes
pca_90 = np.where(porcent_acum > 0.9)[0][0] + 1
pca_90

matrix_transform = pca.components_.T

plt.bar(np.arange(len(matrix_transform)), matrix_transform[:, 0])
plt.xlabel('Num variable real')
plt.ylabel('Magnitud vector asociado')
plt.show()
