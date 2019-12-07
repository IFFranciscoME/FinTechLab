
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Proyecto final de materia Análisis Estadístico Multivariado                               -- #
# -- Codigo: principal.py - codigo de flujo principal                                                    -- #
# -- Repositorio: https://github.com/IFFranciscoME/FinTechLab/tree/master/MCD-ITESO/AEM/aem_proyecto     -- #
# -- Autor: Francisco ME                                                                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #

import funciones as fn                          # Importar funcione especiales hechas para este proyecto
import visualizaciones as vs                    # Importar funciones para visualizaciones
from datos import df_pe_w as df_precios_w       # Importar los precios historicos semanales
from datos import df_ce_w as df_ce_w            # Importar los indicadores económicos historicos

# -- generacion de variables endogenas
df_datos_end = fn.f_features_end(p_datos=df_precios_w)

# -- visualizacion de precios semanales
grafica1 = vs.g_velas(p0_de=df_precios_w)

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
