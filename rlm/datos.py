
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Funcion para solicitar datos de Oanda
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

# Cargar librerias y dependencias
import pandas as pd
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 1000)

# -- --------------------------------------------------------------------------------------- Parametros para OANDA -- #
# -- --------------------------------------------------------------------------------------- --------------------- -- #

A1_OA_Da = 17                     # Day Align
A1_OA_Ta = "America/Mexico_City"  # Time Align

A1_OA_Ai = "101-004-2221697-001"  # Id de cuenta
A1_OA_At = "practice"             # Tipo de cuenta

A1_OA_In = "USD_MXN"              # Instrumento
A1_OA_Gn = "D"                    # Granularidad de velas

A1_OA_Ak = '1' + '1faa346ad5346935919f18cb9ce1d51-0cf8129d81cfa85a1c53c3b57a04014' + '7'

FechaIni = "2019-01-07T00:00:00Z"
FechaFin = "2019-08-30T00:00:00Z"

# -- ------------------------------------------------------------------------------------ Inicializar API de OANDA -- #
# -- ------------------------------------------------------------------------------------ ------------------------ -- #

api = API(access_token=A1_OA_Ak)

# -- ---------------------------------------------------------------------------------- Obtener precios historicos -- #
# -- ---------------------------------------------------------------------------------- -------------------------- -- #

params = {"granularity": A1_OA_Gn, "price": "M", "dailyAlignment": A1_OA_Da,
          "alignmentTimezone": A1_OA_Ta, "from": FechaIni, "to": FechaFin}

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
# -- ------------------------------------------------------------------------------------------------ ------------ -- #

pd_hist = pd.DataFrame(lista)
pd_hist = pd_hist[['TimeStamp', 'Close']]
pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])
