
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Ejercicios de aplicaciones de modelos lineales (Regresion simple/multiple, anova, loglineal)
# -- Codigo: ejercicios_varios.py
# -- Autor: Francisco ME
# -- Repositorio: https://github.com/IFFranciscoME/FinTechLab/tree/master/varios/modelos_lineales
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np                                        # funciones matematicas
import pandas as pd                                       # dataframes y utilidades
import visualizaciones as vs                              # funciones de visualizacion
import statsmodels.api as sm                              # modelos estadisticos
from statsmodels.formula.api import ols                   # herramientas estadisticas: modelo lineal con ols
from sklearn.model_selection import train_test_split      # para dividir conjuntos de entrenamiento y prueba
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso de indexacion

# -- -------------------------------------------------------------------------------------------- Regresion Lineal -- #

# -- Paso 1: Cargar y limpiar datos
df_gasto = pd.read_excel('archivos/datos_gastofamiliar.xlsx')

# -- Paso 2: Definir proposito
# explicar gastos de alimentacion con base a ingreso y tamaño por familia

# -- Paso 3: Definir Modelo y base inicial (Parametros, supuestos, consideraciones base)
# Regresion lineal multiple, variable dependiente: Gasto, variables independientes: Ingreso y tamaño por familia

# -- Paso 4: Explorar datos con base a orientacion de modelo
# Paso 4.1 : Grafica de Matriz de correlaciones entre variables
# -- Las variables independientes estan correlacionadas entre si?
# -- Cada variable independiente esta correlacionada con la dependiente

grafica_1 = vs.g_heatmap_corr(p0_data=df_gasto)

# Paso 4.2 : Grafica de cada combinacion de variable dependiente vs variable independiente
# -- Se muestra en cada grafica una linealidad de la relacion entre variable dependiente e independiente ?

grafica_2 = vs.g_matriz_disp(p0_data=df_gasto)

# Paso 4.3 : Grafica de boxplot para variables dependiente e independientes
# -- Presencia de atipicos

grafica_3 = vs.g_boxplot_varios(p0_data=df_gasto)

# Paso 5 : Ajustar modelo de regresion lineal simple
# Gasto mensual en funcion del ingreso
# Paso 5.1 : Preparar datos y dividirlos en entrenamiento, prueba y validacion
x_train, x_test, y_train, y_test = train_test_split(df_gasto.loc[:, ['Ingreso', 'Tamaño']],
                                                    df_gasto.loc[:, 'Gasto'],
                                                    test_size=0.20, random_state=0, shuffle=False)

# Agregar interceptos a X en entrenamiento y prueba
x_train_betha = sm.add_constant(x_train)
x_test_betha = sm.add_constant(x_test)
modelo = sm.OLS(np.array(y_train), np.array(x_train_betha), hasconst=False)
resultados = modelo.fit()
print(resultados.summary())

# predicciones con datos de prueba
resultados.predict(np.array(x_test_betha))

datos = pd.read_excel('archivos/datos_peces.xlsx', header=None)
datos.columns = ['grupo'] + ['pez_' + str(i) for i in range(1, len(datos.columns))]
datos = datos.melt(id_vars='grupo')
datos = datos[['grupo', 'value']]
datos = datos.sort_values(by=['grupo'])

# ajustar modelo lineal para (high - open)
modelo_peces = ols('value ~ C(grupo)', data=datos[['grupo', 'value']]).fit()
modelo_peces.summary()

# tabla anova
anova_table = sm.stats.anova_lm(modelo_peces, typ=2)
print(anova_table)

# -- Aspirina para el corazon
datos = pd.DataFrame({'Mortal': [18, 5], 'No mortal': [171, 99], 'No ataque': [10845, 10933],
                      'Total': [11034, 11037]}, index=['Placebo', 'Aspirina'])
