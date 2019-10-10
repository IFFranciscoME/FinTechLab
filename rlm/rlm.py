
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Regresion Lineal Multiple
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np
import pandas as pd
import statsmodels.api as sm
from rlm.datos import pd_hist as precios
from sklearn import linear_model
import plotly.graph_objs as go
from numpy import arange, array, ones
from scipy import stats
import plotly.io as pio
pio.renderers.default = "browser"

# -- para visualizar data frames en consola
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
line = slope*xi+intercept

# Creating the dataset, and generating the plot
trace1 = go.Scatter(x=xi, y=y, mode='markers', marker=go.Marker(color='rgb(255, 127, 14)'), name='Data')
trace2 = go.Scatter(x=xi, y=line, mode='lines', marker=go.Marker(color='rgb(31, 119, 180)'), name='Fit')
# annotation = go.Annotation(x=3.5, y=23.5, showarrow=False, font=go.Font(size=16))

layout = go.Layout(title='Linear Fit in Python', plot_bgcolor='rgb(229, 229, 229)')

data = [trace1, trace2]
fig = go.Figure(data=data, layout=layout)

fig.show()

# Modelo
# lr_multiple = linear_model.LinearRegression()
# lr_multiple.fit(train_set_x, train_set_y)
#
# Bo = lr_multiple.intercept_
# Bi = lr_multiple.coef_
#
# # Realizo una predicción
# y_pred = lr_multiple.predict(train_set_x)
#
# # Hipótesis Lineal
# Betha0_train = sm.add_constant(train_set_x)
# Betha0_test = sm.add_constant(test_set_x)
#
# model = sm.OLS(train_set_y, Betha0_train).fit()
# print(model.summary())
# Yhat = model.predict(Betha0_test)
#
# print('DATOS DEL MODELO REGRESIÓN LINEAL MULTIPLE')
# print()
# print('Valor de las pendientes o coeficientes "Betha_i":')
# print(lr_multiple.coef_)
# print('Valor de la intersección o coeficiente "Betha_0":')
# print(lr_multiple.intercept_)
# print('Precisión del modelo:')
# print(lr_multiple.score(train_set_x, train_set_y))
