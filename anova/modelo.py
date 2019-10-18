
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
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas de un pandas dataframe
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso de indexacion

# -- ------------------------------------------------------------------------------------ adecuaciones adicionales -- #
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

# escenarios que si ocurrieron
esc_reales = list(set(df_data_ce['escenario']))

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

# visualizar ejemplo de venta de precio
n_ejem = 7
indice_1 = np.where(df_data_pe['timestamp'] == df_data_ce_c['timestamp'][n_ejem])[0][0]
indice_2 = indice_1 + psiguiente
df_data_g1 = df_data_pe[indice_1:indice_2].reset_index(drop=True)
grafica1 = vs.g_velasdd(p0_de=df_data_g1)
grafica1.show()

# visualizar valores de ol: (open - low)
grafica3 = vs.g_histograma(p0_val=df_data_ce_c[df_data_ce_c['escenario'] == 'A']['ol'],
                           p1_nbins=10, p2_color='#047CFB',
                           p3_etiquetas={'titulo': '<b>Histograma de probabilidad </b>ol: (open - low)',
                                         'ejex': 'valores en (pips)', 'ejey': 'probabilidad'})
grafica3.show()

# visualizar valores de ho: (high - open)
grafica4 = vs.g_histograma(p0_val=df_data_ce_c[df_data_ce_c['escenario'] == 'A']['ho'],
                           p1_nbins=10, p2_color='#047CFB',
                           p3_etiquetas={'titulo': '<b>Histograma de probabilidad </b>ho: (high - open)',
                                         'ejex': 'valores en (pips)', 'ejey': 'probabilidad'})
grafica4.show()

# crear cuadro de datos para modelo ANOVA
df_data_anova = df_data_ce_c[['escenario', 'ol', 'ho']]

# ajustar modelo lineal
model = ols('ho ~ C(escenario)', data=df_data_anova).fit()
model.summary()

# tabla anova
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

# comparacion con tukey
mc = MultiComparison(df_data_anova['hl'], df_data_anova['escenario'])
mc_results = mc.tukeyhsd()
print(mc_results)
