
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Aplicacion de ANOVA para finanzas bursatiles
# -- Codigo: modelo.py
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import pandas as pd
from datos import df_ice, df_precios

pd.set_option('display.max_rows', None)                   # sin limite de renglones maximos para mostrar pandas
pd.set_option('display.max_columns', None)                # sin limite de columnas maximas para mostrar pandas
pd.set_option('display.width', None)                      # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas de un pandas dataframe
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso de indexacion


# -- ---------------------------------------------------------------------------------------- definir metrica base -- #
# -- ---------------------------------------------------------------------------------------- -------------------- -- #

# -- Ambas fechas, tanto del calendario economico como de los precios estan en Huso horario GMT

# se define como tiempo inicial como aquel en el que se comunico el indicador

# se define como precio inicial el precio de apertura en el tiempo inicial

# para cada evento del indicador se hace una ventana de T tiempo con todos los precios OHLC

# hacer el calculo de (high - precio inicial) y (precio inicial - low) con los precios de la ventana de T tiempo
# hacer calculo de amplitud de movimiento entre precio inicial y high y low durante la ventana

# High - Open  (a 10 minutos despues)
# Open - High  (a 10 minutos despues)

# print(df_precios)
# print(df_ice)
