
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Aplicacion de ANOVA para finanzas bursatiles
# -- Codigo: modelo.py
# -- Autor: Francisco ME
# -- Repositorio: https://github.com/IFFranciscoME/FinTechLab/blob/master/anova/modelo.py
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
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas de un dataframe
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso de indexacion

# -- ------------------------------------------------------------------------------------ adecuaciones adicionales -- #
# duplicar objetos para conservar los originales
df_data_pe = df_pe
df_data_ce = df_ce

# cantidad de precios a futuro a considerar
psiguiente = 7

# convertir a datetime columna de fechas a los datos de precios
df_data_pe['timestamp'] = pd.to_datetime(df_data_pe['timestamp'])
df_data_pe['timestamp'] = df_data_pe['timestamp'].dt.tz_localize('UTC')

# convertir a datetime columna de fechas a los datos del calendario economico
df_data_ce['timestamp'] = pd.to_datetime(df_data_ce['timestamp'])
df_data_ce['timestamp'] = df_data_ce['timestamp'].dt.tz_localize('UTC')

# escenarios para clasificar los eventos
escenarios = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# reaccion del precio para cada escenario
d_reaccion = [fn.f_reaccion(p0_i=i, p1_ad=psiguiente, p2_pe=df_data_pe, p3_ce=df_data_ce)
              for i in range(0, len(df_ce['timestamp']))]

# acomodar resultados en columnas
df_data_ce['ho'] = [d_reaccion[j]['ho'] for j in range(0, len(df_data_ce['timestamp']))]
df_data_ce['ol'] = [d_reaccion[j]['ol'] for j in range(0, len(df_data_ce['timestamp']))]

# elegir a los que tengan > n
n = 30
elegidos = [escenarios[i] if len(df_data_ce[df_ce['escenario'] == escenarios[i]]) >= n else 'nan'
            for i in range(0, len(escenarios))]
l_elegidos = [x for x in elegidos if str(x) != 'nan']

# tomar las n ocurrencias mas recientes de los que hayan quedado
df_data_ce_c = pd.concat([df_data_ce[df_data_ce['escenario'] == l_elegidos[i]].sort_values(by='timestamp').tail(n)
                          for i in range(0, len(l_elegidos))]).reset_index(drop=True)

# comprobar que se tienen los escenarios con las 20 muestras mas recientes
ocurrencias = dict(df_data_ce_c['escenario'].value_counts())

# -- -------------------------------------------------------------------------------------------- Visualizaciones -- #
# visualizar ejemplo de venta de precio
n_ejem = 7
indice_1 = np.where(df_data_pe['timestamp'] == df_data_ce_c['timestamp'][n_ejem])[0][0]
indice_2 = indice_1 + psiguiente
df_data_g1 = df_data_pe[indice_1:indice_2].reset_index(drop=True)
grafica1 = vs.g_velasdd(p0_de=df_data_g1)
grafica1.show()

# colores para distinguir cada histograma
colores2 = {'serie_1': '#047CFB', 'serie_2': '#42c29b', 'serie_3': '#6B6B6B'}

# etiquetas para titulo y ejes
etiquetas2 = {'titulo': '<b>Histograma de probabilidad </b>ol: (open - low)',
              'ejex': 'valores en (pips)', 'ejey': 'probabilidad'}

# acomodar datos para funcion de 3 histogramas
datos2 = pd.DataFrame({'val_1': df_data_ce_c[df_data_ce_c['escenario'] == 'A']['ol'],
                       'val_2': df_data_ce_c[df_data_ce_c['escenario'] == 'B']['ol'],
                       'val_3': df_data_ce_c[df_data_ce_c['escenario'] == 'H']['ol']})

# grafica de 3 histogramas
grafica2 = vs.g_hist_varios(p0_val=datos2, p1_colores=colores2, p2_etiquetas=etiquetas2)
grafica2.show()

# colores para distinguir cada histograma
colores3 = {'serie_1': '#047CFB', 'serie_2': '#42c29b', 'serie_3': '#6B6B6B'}

# etiquetas para titulo y ejes
etiquetas3 = {'titulo': '<b>Histograma de probabilidad </b>ho: (high - open)',
              'ejex': 'valores en (pips)', 'ejey': 'probabilidad'}

# acomodar datos para funcion de 3 histogramas
datos3 = pd.DataFrame({'val_1': df_data_ce_c[df_data_ce_c['escenario'] == 'A']['ho'],
                       'val_2': df_data_ce_c[df_data_ce_c['escenario'] == 'B']['ho'],
                       'val_3': df_data_ce_c[df_data_ce_c['escenario'] == 'H']['ho']})

# grafica de 3 histogramas
grafica3 = vs.g_hist_varios(p0_val=datos3, p1_colores=colores3, p2_etiquetas=etiquetas3)
grafica3.show()

# -- ------------------------------------------------------------------------------------------------ Modelo ANOVA -- #
# crear cuadro de datos para modelo ANOVA
df_data_anova = df_data_ce_c[['escenario', 'ol', 'ho']]

# ajustar modelo lineal para (high - open)
model_ho = ols('ho ~ C(escenario)', data=df_data_anova).fit()
model_ho.summary()

# ajustar modelo lineal para (open - low)
model_ol = ols('ol ~ C(escenario)', data=df_data_anova).fit()
model_ol.summary()

# tabla anova (high - open)
anova_table_ho = sm.stats.anova_lm(model_ho, typ=2)

# tabla anova (open - low)
anova_table_ol = sm.stats.anova_lm(model_ol, typ=2)

# comparacion con tukey
mc = MultiComparison(df_data_anova['ho'], df_data_anova['escenario'])
mc_results = mc.tukeyhsd()
print(mc_results)

# comparacion con tukey
mc = MultiComparison(df_data_anova['ol'], df_data_anova['escenario'])
mc_results = mc.tukeyhsd()
print(mc_results)
