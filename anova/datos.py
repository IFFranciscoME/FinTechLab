
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Aplicacion de ANOVA para finanzas bursatiles
# -- Codigo: datos.py
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import pandas as pd
import numpy as np

from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments

# -- --------------------------------------------------------------------------------- Datos: Calendario Economico -- #
# -- --------------------------------------------------------------------------------------- --------------------- -- #

df_ce = pd.read_csv(filepath_or_buffer='archivos/calendario_economico.csv')

# -- Elegir datos de indicador
indicador = 'ISM Manufacturing PMI'
df_ice = df_ce.iloc[np.where(df_ce['Name'] == indicador)[0], :]

# resetear index en dataframe resultante porque guarda los indices del dataframe pasado
df_ice = df_ice.reset_index(drop=True)

# -- criterio para rellenar datos faltantes 'nan'
# cuando falta en consensus
nan_consensus = df_ice.index[np.isnan(df_ice['Consensus'])].tolist()

# asignarle a consensus lo que tiene previous
df_ice['Consensus'][nan_consensus] = df_ice['Previous'][nan_consensus]

# -- escenarios A, B, C, D, E, F, G, H
df_ice['escenario'] = ''

# -- -- A: Actual >= Previous & Actual >= Consensus & Consensus >= Previous
df_ice['escenario'][((df_ice['Actual'] >= df_ice['Previous']) & (df_ice['Actual'] >= df_ice['Consensus']) &
                    (df_ice['Consensus'] >= df_ice['Previous']))] = 'A'

# -- -- B: Actual >= Previous & Actual >= Consensus & Consensus < Precious
df_ice['escenario'][((df_ice['Actual'] >= df_ice['Previous']) & (df_ice['Actual'] >= df_ice['Consensus']) &
                    (df_ice['Consensus'] < df_ice['Previous']))] = 'B'

# -- -- C: Actual >= Previous & Actual < Consensus & Consensus >= Previous
df_ice['escenario'][((df_ice['Actual'] >= df_ice['Previous']) & (df_ice['Actual'] < df_ice['Consensus']) &
                    (df_ice['Consensus'] >= df_ice['Previous']))] = 'C'

# -- -- D: Actual >= Previous & Actual < Consensus & Consensus < Previous
df_ice['escenario'][((df_ice['Actual'] >= df_ice['Previous']) & (df_ice['Actual'] < df_ice['Consensus']) &
                    (df_ice['Consensus'] < df_ice['Previous']))] = 'D'

# -- -- E: Actual < Previous & Actual >= Consensus & Consensus >= Previous
df_ice['escenario'][((df_ice['Actual'] < df_ice['Previous']) & (df_ice['Actual'] >= df_ice['Consensus']) &
                    (df_ice['Consensus'] >= df_ice['Previous']))] = 'E'

# -- -- F: Actual < Previous & Actual >= Consensus & Consensus < Previous
df_ice['escenario'][((df_ice['Actual'] < df_ice['Previous']) & (df_ice['Actual'] >= df_ice['Consensus']) &
                    (df_ice['Consensus'] < df_ice['Previous']))] = 'F'

# -- -- G: Actual < Previous & Actual < Consensus & Consensus >= Previous
df_ice['escenario'][((df_ice['Actual'] < df_ice['Previous']) & (df_ice['Actual'] < df_ice['Consensus']) &
                    (df_ice['Consensus'] >= df_ice['Previous']))] = 'G'

# -- -- H: Actual < Previous & Actual < Consensus & Consensus < Previous
df_ice['escenario'][((df_ice['Actual'] < df_ice['Previous']) & (df_ice['Actual'] < df_ice['Consensus']) &
                    (df_ice['Consensus'] < df_ice['Previous']))] = 'H'

# -- ------------------------------------------------------------------------------------ Datos: Precios con OANDA -- #
# -- --------------------------------------------------------------------------------------- --------------------- -- #

A1_OA_Da = 16                      # Day Align
A1_OA_Ai = "101-004-2221697-001"   # Id de cuenta
A1_OA_At = "practice"              # Tipo de cuenta
A1_OA_In = "EUR_USD"               # Instrumento
A1_OA_Gn = "M5"                    # Granularidad de velas
FechaIni = "2009-01-02T00:00:00Z"  # Fecha inicial
FechaFin = "2019-09-30T00:00:00Z"  # Fecha final

# Token para API de OANDA
A1_OA_Ak = '7' + '9ae0a52f8e483facdd81f5b316a8ef8-99fb5554f4739c76535b209044f7de2' + '6'

# -- ------------------------------------------------------------------------------------ Inicializar API de OANDA -- #

api = API(access_token=A1_OA_Ak)

# -- ---------------------------------------------------------------------------------- Obtener precios historicos -- #

params = {"granularity": A1_OA_Gn, "price": "M", "dailyAlignment": A1_OA_Da, "from": FechaIni, "to": FechaFin}

A1_Req1 = instruments.InstrumentsCandles(instrument=A1_OA_In, params=params)
A1_Hist = api.request(A1_Req1)

lista = []
for i in range(len(A1_Hist['candles'])-1):
    lista.append({'TimeStamp': A1_Hist['candles'][i]['time'],
                  'Open': A1_Hist['candles'][i]['mid']['o'],
                  'High': A1_Hist['candles'][i]['mid']['h'],
                  'Low': A1_Hist['candles'][i]['mid']['l'],
                  'Close': A1_Hist['candles'][i]['mid']['c']})

# -- ------------------------------------------------------------------------------------------------ Salida final -- #

df_hist = pd.DataFrame(lista)
df_hist['TimeStamp'] = pd.to_datetime(df_hist['TimeStamp'])
df_hist = df_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
