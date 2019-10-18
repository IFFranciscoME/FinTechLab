
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Aplicacion de ANOVA para finanzas bursatiles
# -- Codigo: datos.py
# -- Autor: Francisco ME
# -- Repositorio: https://github.com/IFFranciscoME/FinTechLab/blob/master/anova/datos.py
# -- ------------------------------------------------------------------------------------------------------------- -- #

import pandas as pd                                       # dataframes y utilidades
import numpy as np                                        # operaciones matematicas
# import funciones as fn                                  # importar funciones internas desde otro script (precios)
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso de indexacion

# -- --------------------------------------------------------------------------------- Datos: Calendario Economico -- #

# Elegir datos de indicador
indicador = 'ISM Manufacturing PMI'

# leer archivo con informacion historica
df_ce_ini = pd.read_csv(filepath_or_buffer='archivos/calendario_economico.csv')
df_ce = df_ce_ini.iloc[np.where(df_ce_ini['Name'] == indicador)[0], :]

# cambiar a minusculas los nombres de las columnas
columnas = list(df_ce.columns)
columnas = [i.lower() for i in columnas]

# Renombrar todas las columnas del dataframe con una lista de nombres
df_ce.rename(columns=dict(zip(df_ce.columns[0:], columnas)), inplace=True)

# resetear index en dataframe resultante porque guarda los indices del dataframe pasado
df_ce = df_ce.reset_index(drop=True)

# convertir columna a datetime
df_ce['timestamp'] = pd.to_datetime(df_ce['timestamp'])

# escenarios para clasificar los eventos
escenarios = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# criterio para rellenar datos faltantes 'nan'
# cuando falta en consensus
nan_consensus = df_ce.index[np.isnan(df_ce['consensus'])].tolist()

# asignarle a consensus lo que tiene previous
df_ce['consensus'][nan_consensus] = df_ce['previous'][nan_consensus]

# inicializar la columna escenario, habra los siguientes: A, B, C, D, E, F, G, H
df_ce['escenario'] = ''

# -- -- A: actual >= previous & actual >= consensus & consensus >= previous
df_ce['escenario'][((df_ce['actual'] >= df_ce['previous']) & (df_ce['actual'] >= df_ce['consensus']) &
                    (df_ce['consensus'] >= df_ce['previous']))] = 'A'

# -- -- B: actual >= previous & actual >= consensus & consensus < Precious
df_ce['escenario'][((df_ce['actual'] >= df_ce['previous']) & (df_ce['actual'] >= df_ce['consensus']) &
                    (df_ce['consensus'] < df_ce['previous']))] = 'B'

# -- -- C: actual >= previous & actual < consensus & consensus >= previous
df_ce['escenario'][((df_ce['actual'] >= df_ce['previous']) & (df_ce['actual'] < df_ce['consensus']) &
                    (df_ce['consensus'] >= df_ce['previous']))] = 'C'

# -- -- D: actual >= previous & actual < consensus & consensus < previous
df_ce['escenario'][((df_ce['actual'] >= df_ce['previous']) & (df_ce['actual'] < df_ce['consensus']) &
                    (df_ce['consensus'] < df_ce['previous']))] = 'D'

# -- -- E: actual < previous & actual >= consensus & consensus >= previous
df_ce['escenario'][((df_ce['actual'] < df_ce['previous']) & (df_ce['actual'] >= df_ce['consensus']) &
                    (df_ce['consensus'] >= df_ce['previous']))] = 'E'

# -- -- F: actual < previous & actual >= consensus & consensus < previous
df_ce['escenario'][((df_ce['actual'] < df_ce['previous']) & (df_ce['actual'] >= df_ce['consensus']) &
                    (df_ce['consensus'] < df_ce['previous']))] = 'F'

# -- -- G: actual < previous & actual < consensus & consensus >= previous
df_ce['escenario'][((df_ce['actual'] < df_ce['previous']) & (df_ce['actual'] < df_ce['consensus']) &
                    (df_ce['consensus'] >= df_ce['previous']))] = 'G'

# -- -- H: actual < previous & actual < consensus & consensus < previous
df_ce['escenario'][((df_ce['actual'] < df_ce['previous']) & (df_ce['actual'] < df_ce['consensus']) &
                    (df_ce['consensus'] < df_ce['previous']))] = 'H'

# -- ------------------------------------------------------------------------------------ Datos: Precios con OANDA -- #

OA_Da = 16                         # Day Align
OA_Ai = "101-004-2221697-001"      # Id de cuenta
OA_At = "practice"                 # Tipo de cuenta
OA_In = "EUR_USD"                  # Instrumento
OA_Gn = "M5"                       # Granularidad de velas
FechaIni = "2009-01-06 00:00:00"   # Fecha inicial
FechaFin = "2019-09-27 00:00:00"   # Fecha final

# cohercionar las fechas a huso horario GMT
fini = pd.to_datetime(FechaIni).tz_localize('GMT')
ffin = pd.to_datetime(FechaFin).tz_localize('GMT')

# Token para API de OANDA
OA_Ak = '7' + '9ae0a52f8e483facdd81f5b316a8ef8-99fb5554f4739c76535b209044f7de2' + '6'

# Leer archivo de precios historicos
df_pe = pd.read_csv("archivos/precios_historicos.csv")

# -- -------------------------------------------------------------------------------- Proceso de descarga completo -- #
# -- -------------------------------------------------------------------------------- ---------------------------- -- #
# -- Solo correr esta parte si se quiere descargar todos los precios

# Descagar todos los precios necesarios (descomentar la linea de import funciones as fn)
# df_pe = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn, p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=5000)

# Escribir dataframe en un archivo csv
# df_pe.to_csv(r"archivos/precios_historicos.csv", index=False)
