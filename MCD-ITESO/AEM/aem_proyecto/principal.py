
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Modelo 1 - RLM con variables endogenas.
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import funciones as fn

# -- datos de entrada
df_precios = fn.f_precios(p_fuente='oanda', p_ins='EUR_USD', p_grn='W',
                          p_fini='2010-01-01T00:00:00Z', p_ffin='2019-10-31T00:00:00Z')


# -- generacion de variables endogenas
df_datos = fn.f_feature_eng(p_datos=df_precios)

# -- ajute de modelo 1: RLM con variables endogenas (Sin tratamiento)
res1 = fn.f_rlm(p_datos=df_datos, p_y='co')
print(res1['train']['summary'])
# print(res1['test']['summary'])

# -- Utilizar PCA para reducir dimensionalidad de modelo 1
df_pca = fn.f_pca(p_datos=df_datos, p_exp=0.95)

# -- ajuste de modelo 2: RLM con variables endogenas (Reducido con PCA)
res2 = fn.f_rlm(p_datos=df_pca, p_y='pca_y')
print(res2['train']['summary'])
# print(res2['test']['summary'])

# -- estrategia de trading con modelo

# -- clustering de resultados de estrategia de trading

# -- clustering secuencial como modelo 3: Uso de algoritmo MASS para series de tiempo financieras

# -- estrategia de trading

# -- comparacion de 2 estrategias (RLM con PCA Vs MASS)
