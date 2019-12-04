
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Modelo 1 - RLM con variables endogenas.
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import funciones as fn

# -- Generacion de variables
df_precios = fn.f_precios(p_fuente='oanda', p_ins='EUR_USD', p_grn='W',
                          p_fini='2016-01-01T00:00:00Z', p_ffin='2019-09-30T00:00:00Z')
