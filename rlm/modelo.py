
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Regresion Lineal Multiple
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np                                        # tratamiento cientifico de numeros
import pandas as pd                                       # dataframes
import statsmodels.api as sm                              # modelos estadisticos
from datetime import datetime                             # tratamiento de datetime
from functools import reduce                              # para la union de los dataframes
import visualizaciones as vs                              # script con funciones para visualizar
from os import listdir, getcwd                            # para leer todos los archivos de un folder
from os.path import isfile, join                          # encontrar y unir archivos en un folder

from sklearn import linear_model                          # modelo lineal
from datos import pd_hist as precios                      # importar precios
from sklearn.model_selection import train_test_split      # separacion de conjunto de entrenamiento y prueba
from statsmodels.formula.api import ols                   # ols

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


def f_datos_ce(p0_ind):

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

    print(datos.head())

    return datos


# Unir dataframes
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

# -- ------------------------------------------------------------------------------------ Exploracion de variables -- #

# Matriz de diagramas de dispersion
g1 = vs.explora(datos_md)

# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- ----------------------------------------------------------------------------------------- Modelo con: sklearn -- #

# Reacomodar los datos como arreglos
y_multiple = np.array(datos_md.iloc[:, 1])
x_multiple = np.array(datos_md.iloc[:, 3:])

# Varianza de la variable a explicar
var_y = y_multiple.var()

# datos para entrenamiento y prueba
train_x, test_x, train_y, test_y = train_test_split(x_multiple, y_multiple, test_size=0.2, shuffle=False)

# Variable tipo modelo lineal
modelo_rlm = linear_model.LinearRegression()
modelo_rlm.fit(train_x, train_y)
y_pred = modelo_rlm.predict(test_x)

# data frame con valor real y valor pronosticado
res = pd.DataFrame({'Close_Actual': test_y, 'Close_Predicted': y_pred, 'Errores': (test_y-y_pred)*10000})

# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- ------------------------------------------------------------------------------------- Modelo con: statsmodels -- #

str_modelo = 'Close ~ x_0 + x_2 + x_4 + x_5 + x_8 + x_10'

mod = ols(formula=str_modelo, data=datos_md)
resultado = mod.fit()
resumen = resultado.summary()
valores_p = resultado.pvalues

# # Agregar interceptos a X en entrenamiento y prueba
# train_x_betha = sm.add_constant(train_x)
# test_x_betha = sm.add_constant(test_x)

# # Modelo ajustado
# modelo = sm.OLS(train_y, train_x_betha)
# # Resultados de ajuste de modelo
# resultados = modelo.fit()
# # Resultados de predicciones de modelo
# # Yhat = modelo.predict(train_x).fit()
#
# print(resultados.summary())
# print('Parameters: ', resultados.params)
# print('Standard errors: ', resultados.bse)
# print('Predicted values: ', resultados.predict())
