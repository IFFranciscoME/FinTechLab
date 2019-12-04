
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Modelo 1 - RLM con variables endogenas.
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import funciones as fn

# -- datos de entrada
df_precios = fn.f_precios(p_fuente='oanda', p_ins='EUR_USD', p_grn='W',
                          p_fini='2013-01-01T00:00:00Z', p_ffin='2019-11-29T00:00:00Z')

# -- generacion de variables endogenas
df_datos = fn.f_feature_eng(p_datos=df_precios, p_ohlc=True, p_ntiempo=55)
