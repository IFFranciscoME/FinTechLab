
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Regresion Lineal Multiple
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np                                        # tratamiento cientifico de numeros
import pandas as pd                                       # dataframes
import statsmodels.api as sm                              # modelos estadisticos
from datetime import datetime                             # tratamiento de datetime

from sklearn import linear_model                          # modelo lineal
from rlm.datos import pd_hist as precios                  # importar precios
from sklearn.model_selection import train_test_split      # separacion de conjunto de entrenamiento y prueba

# Para visualizar data frames en consola
pd.set_option('display.max_rows', None)                   # Sin limite de renglones maximos para mostrar pandas
pd.set_option('display.max_columns', None)                # Sin limite de columnas maximas para mostrar pandas
pd.set_option('display.width', None)                      # Sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)         # Visualizar todas las columnas de un pandas dataframe
pd.options.mode.chained_assignment = None                 # Para evitar el warning enfadoso

# -- ------------------------------------------------------------------------------- Datos de CALENDARIO ECONOMICO -- #

# Datos de entrada
datos_ce = pd.read_csv('rlm/archivos/calendario_economico.csv')

# Convertir columna de fechas a datetime
datos_ce['DateTime'] = [datetime.strptime(datos_ce['DateTime'][i], '%m/%d/%Y %H:%M:%S')
                        for i in range(0, len(datos_ce['DateTime']))]

# Lista de indicadores economicos a utilizar
indicadores = ['Continuing Jobless Claims', 'Initial Jobless Claims', '4-Week Bill Auction',
               'CFTC USD NC Net Positions', 'CFTC Oil NC Net Positions']

# Obtener los datos exclusivamente del indicador seleccionado
prueba = datos_ce.loc[np.where(datos_ce.loc[:, 'Name'] == indicadores[0])]

# Resetear el index de los datos encontrados
prueba = prueba.reset_index(drop=True)

# Agregar columna con numero de semana (Servira para empatar fecha de indicador con fecha de precio)
prueba['semana'] = [prueba.loc[i, 'DateTime'].strftime("%W") for i in range(0, len(prueba['DateTime']))]


# acomodar verticalmente los datos encontrados, que queden ordenados por fecha
# -- --- Union de dataframes por fechas : crear un data frame donde esten empatados los datos por fechas

# -- ---------------------------------------------------------------------------------------------- Datos de OANDA -- #

# Generacion de variables explicativas
datos_fx = precios[['TimeStamp', 'Close']]

# Convertir a valor tipo float
datos_fx.loc[:, 'Close'] = datos_fx.loc[:, 'Close'].astype(float)

# Calcular el rendimiento logaritmico como variable a explicar Y
datos_fx.loc[:, 'log_ret'] = np.log(datos_fx.loc[:, 'Close']/datos_fx.loc[:, 'Close'].shift(1))

# Calcular las diferencias de 1 hasta 5 periodos
n_diffs = 5
datos_fx = pd.concat([datos_fx, pd.DataFrame({'log_ret_d_' + str(i): datos_fx.loc[:, 'log_ret'].diff(i)
                                              for i in range(1, n_diffs)})], axis=1)
# Eliminar el NaN inicial
datos_fx = datos_fx.dropna()

# Resetear index de data frame
datos_fx = datos_fx.reset_index(drop=True)

# Convertir columna de fechas a datetime
datos_fx['TimeStamp'] = pd.to_datetime(datos_fx['TimeStamp'])

# Agregar columna de semana
datos_fx['Semana'] = [datos_fx.loc[i, 'TimeStamp'].strftime("%W") for i in range(0, len(datos_fx['TimeStamp']))]

# -- --------------------------------------------------------------------------- Generacion de dataset para modelo -- #

# Reacomodar los datos como arreglos
y_multiple = np.array(datos_fx.iloc[:, 2])
x_multiple = np.array(datos_fx.iloc[:, 3:])

# datos para entrenamiento y prueba
train_x, test_x, train_y, test_y = train_test_split(x_multiple, y_multiple, test_size=0.2, shuffle=False)

# # # Variable tipo modelo lineal
modelo_rlm = linear_model.LinearRegression()
modelo_rlm.fit(train_x, train_y)

# Extraer coeficiente de modelo
Bo = modelo_rlm.intercept_
Bi = modelo_rlm.coef_

# reconvertir a un array
# y_multiple = np.reshape(y_multiple, (len(y_multiple), 1))
# Varianza de la variable a explicar
var_y = y_multiple.var()

# Q = (x_multiple.T*x_multiple).I
# Q2 = var_y*(x_multiple.T*x_multiple).I

# Revisar ajuste de modelo a datos de entrenamiento
Y_ajuste_multiple = modelo_rlm.predict(test_x)

# Agregar interceptos a X en entrenamiento y prueba
train_x_betha = sm.add_constant(train_x)
test_x_betha = sm.add_constant(test_x)

# Modelo ajustado
modelo = sm.OLS(train_y, train_x_betha)
# Resultados de ajuste de modelo
resultados = modelo.fit()
# Resultados de predicciones de modelo
Yhat = modelo.predict(test_x_betha).fit()

print(resultados.summary())
print('Parameters: ', resultados.params)
print('Standard errors: ', resultados.bse)
print('Predicted values: ', resultados.predict())
