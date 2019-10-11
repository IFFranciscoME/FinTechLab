
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Funcion para solicitar datos de Oanda
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

# Cargar librerias y dependencias
import pandas as pd
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments

# -- --------------------------------------------------------------------------------------- Parametros para OANDA -- #
# -- --------------------------------------------------------------------------------------- --------------------- -- #

A1_OA_Da = 16                      # Day Align
A1_OA_Ai = "101-004-2221697-001"   # Id de cuenta
A1_OA_At = "practice"              # Tipo de cuenta
A1_OA_In = "USD_MXN"               # Instrumento
A1_OA_Gn = "W"                     # Granularidad de velas
FechaIni = "2018-08-30T00:00:00Z"  # Fecha inicial
FechaFin = "2019-08-30T00:00:00Z"  # Fecha final

A1_OA_Ak = '7' + '9ae0a52f8e483facdd81f5b316a8ef8-99fb5554f4739c76535b209044f7de2' + '6'  # Token para API de OANDA

# -- ------------------------------------------------------------------------------------ Inicializar API de OANDA -- #
# -- ------------------------------------------------------------------------------------ ------------------------ -- #

api = API(access_token=A1_OA_Ak)

# -- ---------------------------------------------------------------------------------- Obtener precios historicos -- #
# -- ---------------------------------------------------------------------------------- -------------------------- -- #

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
# -- ------------------------------------------------------------------------------------------------ ------------ -- #

pd_hist = pd.DataFrame(lista)
pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])
pd_hist = pd_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
