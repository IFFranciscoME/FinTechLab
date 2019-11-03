
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Examen parcial 2
# -- Codigo: examen.py
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import pandas as pd                                       # dataframes y utilidades
import numpy as np                                        # operaciones matematicas
import statsmodels.api as sm                              # modelos estadisticos: anova
import visualizaciones as vs                              # importar visualizaciones desde otro script
from sklearn.model_selection import train_test_split      # separar conjunto de entrenamiento y prueba
from statsmodels.stats.multicomp import MultiComparison   # herramientas estadisticas: multicomparacion
from statsmodels.formula.api import ols                   # herramientas estadisticas: modelo lineal con ols

pd.set_option('display.max_rows', None)                   # sin limite de renglones maximos para mostrar pandas
pd.set_option('display.max_columns', None)                # sin limite de columnas maximas para mostrar pandas
pd.set_option('display.width', None)                      # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas de un dataframe
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso de indexacion


#  Ejercicio 1, A y B
df_datos = pd.read_excel('datos/AirQuality.xlsx')

x_train, x_test, y_train, y_test = train_test_split(df_datos.loc[:, 'T'],
                                                    df_datos.loc[:, 'CO(GT)'],
                                                    test_size=0.20, random_state=0, shuffle=False)

# Agregar interceptos a X en entrenamiento y prueba
x_train_betha = sm.add_constant(x_train)
x_test_betha = sm.add_constant(x_test)
modelo = sm.OLS(y_train, x_train_betha, hasconst=False)
resultados_a = modelo.fit()
print(resultados_a.summary())
