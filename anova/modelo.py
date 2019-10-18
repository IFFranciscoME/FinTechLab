
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Aplicacion de ANOVA para finanzas bursatiles
# -- Codigo: modelo.py
# -- Autor: Francisco ME
# -- Repositorio:
# -- ------------------------------------------------------------------------------------------------------------- -- #

import pandas as pd                                       # dataframes y utilidades
import numpy as np                                        # operaciones matematicas
import statsmodels.api as sm                              # modelos estadisticos: anova
import funciones as fn                                    # importar funciones desde otro script
import visualizaciones as vs                              # importar visualizaciones desde otro script

from statsmodels.stats.multicomp import MultiComparison   # herramientas estadisticas: multicomparacion
from statsmodels.formula.api import ols                   # herramientas estadisticas: modelo lineal con ols
from datos import df_ce, df_pe                            # importar datos internamente de otro script

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

# cantidad de precios a futuro a considerar
psiguiente = 7

# convertir a datetime columna de fechas
df_data_pe['timestamp'] = pd.to_datetime(df_data_pe['timestamp'])

# escenarios para clasificar los eventos
escenarios = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# reaccion del precio para cada escenario
d_reaccion = [fn.f_reaccion(p0_i=i, p1_ad=psiguiente, p2_pe=df_data_pe, p3_ce=df_data_ce)
              for i in range(0, len(df_ce['timestamp']))]

# acomodar resultados en columnas
df_data_ce['ho'] = [d_reaccion[j]['ho'] for j in range(0, len(df_data_ce['timestamp']))]
df_data_ce['ol'] = [d_reaccion[j]['ol'] for j in range(0, len(df_data_ce['timestamp']))]
df_data_ce['hl'] = [d_reaccion[j]['hl'] for j in range(0, len(df_data_ce['timestamp']))]

# visualizar ejemplo de venta de precio
indice_1 = np.where(df_data_pe['timestamp'] == df_data_ce['timestamp'][6])[0][0]
indice_2 = indice_1 + psiguiente
df_data_g1 = df_data_pe[indice_1:indice_2].reset_index(drop=True)
grafica1 = vs.g_velasdd(p0_de=df_data_g1)
grafica1.show()

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
