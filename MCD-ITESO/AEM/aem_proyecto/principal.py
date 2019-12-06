
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Modelo 1 - RLM con variables endogenas.
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import funciones as fn
from datos import df_pe_m5 as df_precios_m5
from datos import df_pe_w as df_precios_w
from datos import df_ce_w as df_ce_w

# -- precios semanales

# -- generacion de variables endogenas
df_datos_end = fn.f_features_end(p_datos=df_precios_w)

# -- ajute de modelo 1A: RLM con variables endogenas (Sin tratamiento)
res1 = fn.f_rlm(p_datos=df_datos_end, p_y='co')

# -- utilizar PCA para reducir dimensionalidad de modelo 1
df_pca = fn.f_pca(p_datos=df_datos_end, p_exp=0.80)

# -- ajuste de modelo 1B: RLM con variables endogenas (Reducido con PCA)
res2 = fn.f_rlm(p_datos=df_pca, p_y='pca_y')

# -- generacion de variables exogenas
df_datos_exo = fn.f_features_exo(p_datos=df_ce_w)

# -- ajuste de modelo 2A: RLM con variables exogenas (sin tratamiento)
# -- utilizar PCA para reducir dimensionalidad de modelo 2
# -- ajuste de modelo 2B: RLM con variables exogenas (Reducido con PCA)

# -- STS Clustering
