
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Funcion para solicitar datos de Oanda
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

# Cargar librerias y dependencias
import pandas as pd
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments


# -- -------------------------------------------------------------------- Funcion: Obtencion de precios historicos -- #
# -- -------------------------------------------------------------------- ---------------------------------------- -- #

def f_precios(p_fuente, p_fini, p_ffin, p_ins, p_grn):
    """
    :param p_fuente: str : 'oanda' : nombre de la fuente para solicitar los precios historicos de Oanda
    :param p_fini: str : '2016-01-02T00:00:00Z' : fecha inicial para historicos, en formato especifico de Oanda
    :param p_ffin: str : '2016-01-02T00:00:00Z' : fecha inicial para historicos, en formato especifico de Oanda
    :param p_ins: str : 'EUR_USD' : nombre de instrumento para pedir precios, en formato especifico de Oanda
    :param p_grn: str : 'W' : granularidad de los precios OHLC, en formato especifico de Oanda

    :return: r_precios_hist : pd.DataFrame : con timestamp y precios OHLC
    """

    if p_fuente == 'oanda':

        # Parametros e inicializacion de API de OANDA
        oa_ak = '7' + '9ae0a52f8e483facdd81f5b316a8ef8-99fb5554f4739c76535b209044f7de2' + '6'  # Token de OANDA
        api = API(access_token=oa_ak)
        params = {"granularity": p_grn, "price": "M", "dailyAlignment": 16, "from": p_fini, "to": p_ffin}

        # Peticion a la API, a traves de la libreria, con los parametros deseados
        req1 = instruments.InstrumentsCandles(instrument=p_ins, params=params)
        hist = api.request(req1)

        # Proceso para convertir los datos resultado, pasarlos de listas a data frame.
        lista = []
        for i in range(len(hist['candles']) - 1):
            lista.append({'TimeStamp': hist['candles'][i]['time'],
                          'Open': hist['candles'][i]['mid']['o'], 'High': hist['candles'][i]['mid']['h'],
                          'Low': hist['candles'][i]['mid']['l'], 'Close': hist['candles'][i]['mid']['c']})
        # Conversion a DataFrame
        r_precios_hist = pd.DataFrame(lista)

        # Convertir columna de timestamp que es tipo str a tipo datetime.
        r_precios_hist['TimeStamp'] = pd.to_datetime(r_precios_hist['TimeStamp'])
        # Seleccionar solo las columnas de interes
        r_precios_hist = r_precios_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]

        # En caso de que haya sido seleccionada otra fuente, enviar mensaje de error.
    else:
        r_precios_hist = 'pendiente conexion a otra fuente'

    return r_precios_hist

# -- -------------------------------------------------------------------- Funcion: Obtencion de precios historicos -- #
# -- -------------------------------------------------------------------- ---------------------------------------- -- #
