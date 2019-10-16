
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Aplicacion de ANOVA para finanzas bursatiles
# -- Codigo: modelo.py
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import pandas as pd
from datos import df_ice, df_hist

pd.set_option('display.max_rows', None)                   # sin limite de renglones maximos para mostrar pandas
pd.set_option('display.max_columns', None)                # sin limite de columnas maximas para mostrar pandas
pd.set_option('display.width', None)                      # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas de un pandas dataframe
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso de indexacion

print(df_hist)
print(df_ice)
