
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Aplicacion de ANOVA para finanzas bursatiles
# -- Codigo: modelo.py
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import pandas as pd
import numpy as np
import statsmodels.api as sm

from statsmodels.stats.multicomp import MultiComparison
from statsmodels.formula.api import ols
from datos import df_ce, df_pe

pd.set_option('display.max_rows', None)                   # sin limite de renglones maximos para mostrar pandas
pd.set_option('display.max_columns', None)                # sin limite de columnas maximas para mostrar pandas
pd.set_option('display.width', None)                      # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas de un pandas dataframe
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso de indexacion

# -- ------------------------------------------------------------------------------------ adecuaciones adicionales -- #
# ambas fechas, tanto del calendario economico como de los precios estan en Huso horario GMT
# duplicar objetos para conservar los originales
df_data_pe = df_pe
df_data_ce = df_ce

# convertir a datetime columna de fechas
df_data_pe['timestamp'] = pd.to_datetime(df_data_pe['timestamp'])

# escenarios para clasificar los eventos
escenarios = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


# -- ---------------------------------------------------------------------------------------- definir metrica base -- #
# -- ---------------------------------------------------------------------------------------- -------------------- -- #

# se define como tiempo inicial como aquel en el que se comunico el indicador
# proposito del ejercicio: probar si estadisticamente existe diferencia significativa en la media de las
# reacciones del precio ante 8 diferentes escenarios de salida de un indicador economico

# whether there is a statistically significant difference in mean systolic blood pressures among the four groups
# h0 = todas las 'reacciones' del precio, ante la comunicacion de un mismo indicador economico, son iguales.

def f_reaccion(p0_i, p1_ad):
    """
    :param p0_i: indexador
    :param p1_ad: cantidad de precios hacia adelante que se considera la ventana

    :return: resultado: diccionario con resultado final con 3 elementos como resultado

    # debugging
    p0_i = 1
    p0_ad = 3
    """

    indice_1 = np.where(df_pe['timestamp'] == df_ce['timestamp'][p0_i])[0][0]
    indice_2 = indice_1 + p1_ad
    ho = round((max(df_pe['high'][indice_1:indice_2]) - df_pe['open'][indice_1])*10000, 2)
    ol = round((df_pe['open'][indice_1] - min(df_pe['low'][indice_1:indice_2]))*10000, 2)
    hl = round((max(df_pe['high'][indice_1:indice_2]) - min(df_pe['low'][indice_1:indice_2]))*10000, 2)

    # diccionario con resultado final
    resultado = {'ho': ho, 'ol': ol, 'hl': hl}

    return resultado


# reaccion del precio para cada escenario
d_reaccion = [f_reaccion(p0_i=i, p1_ad=3) for i in range(0, len(df_ce['timestamp']))]

# acomodar resultados en columnas
df_data_ce['ho'] = [d_reaccion[j]['ho'] for j in range(0, len(df_data_ce['timestamp']))]
df_data_ce['ol'] = [d_reaccion[j]['ol'] for j in range(0, len(df_data_ce['timestamp']))]
df_data_ce['hl'] = [d_reaccion[j]['hl'] for j in range(0, len(df_data_ce['timestamp']))]

# Escenarios que si ocurrieron
esc_reales = list(set(df_data_ce['escenario']))

# Elegir a escenarios con mayor similitud entre muestras
ocurrencias = dict(df_data_ce['escenario'].value_counts())

# ajustar modelo lineal
model = ols('ol ~ escenario', data=df_data_ce).fit()

# tabla anova
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

# comparacion con tukey
mc = MultiComparison(df_data_ce['hl'], df_data_ce['escenario'])
mc_results = mc.tukeyhsd()
print(mc_results)
