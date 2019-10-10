
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Regresion Lineal Multiple
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

# Cargar librerias y dependencias
import numpy as np
import pandas as pd
# import statsmodels.api as sm
# import visualizaciones as vs
# from sklearn import linear_model
from numpy import arange, array, ones
from scipy import stats
from datos import pd_hist as precios

# para visualizar data frames en consola
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 100)

# Generacion de variables explicativas
datos = precios[['TimeStamp', 'Close']]

# Convertir a valor tipo float
datos['Close'] = datos['Close'].astype(float)

# Calcular el rendimiento logaritmico como variable a explicar Y
datos['log_ret'] = np.log(datos['Close']/datos['Close'].shift(1))

# Calcular las diferencias de 1 hasta 99 periodos
n_diffs = 5
datos = pd.concat([datos, pd.DataFrame({'log_ret_d_' + str(i): datos['log_ret'].diff(i)
                                        for i in range(1, n_diffs)})], axis=1)
# Eliminar el NaN inicial
datos = datos.dropna()

# datos para entrenamiento y prueba
train_set, test_set = np.split(datos, [int(.6 * len(datos))])
train_set_x = train_set.iloc[:, 3:]
train_set_y = train_set.iloc[:, 2]
test_set_x = test_set.iloc[:, 3:]
test_set_y = test_set.iloc[:, 2]

# Exploraciones iniciales con visualizaciones

# Scientific libraries
xi = arange(0, 9)
A = array([xi, ones(9)])
y = [19, 20, 20.5, 21.5, 22, 23, 23, 25.5, 24]

# Generated linear fit
slope, intercept, r_value, p_value, std_err = stats.linregress(xi, y)
line = slope*xi + intercept
