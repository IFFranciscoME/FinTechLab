
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Funcion para solicitar datos de Oanda
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

# Cargar librerias y dependencias
import pandas as pd
import numpy as np

from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments

pd.set_option('display.max_rows', None)                   # sin limite de renglones maximos para mostrar pandas
pd.set_option('display.max_columns', None)                # sin limite de columnas maximas para mostrar pandas
pd.set_option('display.width', None)                      # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas de un dataframe
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso de indexacion


# -- -------------------------------------------------------------------- FUNCION: Obtencion de precios historicos -- #
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
        precios_hist = pd.DataFrame(lista)

        # Convertir columna de timestamp que es tipo str a tipo datetime.
        precios_hist['TimeStamp'] = pd.to_datetime(precios_hist['TimeStamp'])
        # Seleccionar solo las columnas de interes
        r_precios_hist = precios_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
        # cohercionar los nombres de columnas a minusculas
        r_precios_hist.columns = [r_precios_hist.columns[i].lower() for i in range(0, len(r_precios_hist.columns))]

        # En caso de que haya sido seleccionada otra fuente, enviar mensaje de error.
    else:
        r_precios_hist = 'pendiente conexion a otra fuente'

    return r_precios_hist


# -- ------------------------------------------------------- FUNCION: Ingenieria de features para series de tiempo -- #
# -- ------------------------------------------------------- ----------------------------------------------------- -- #

def f_feature_eng(p_datos, p_ohlc, p_ntiempo):
    """
    :param p_datos: pd.DataFrae : dataframe con 5 columnas 'timestamp', 'open', 'high', 'low', 'close'
    :param p_ohlc: bool : True si son datos con columnas 'timestamp', 'open', 'high', 'low', 'close', False otro caso
    :param p_ntiempo: int : cantidad de periodos de historia para calcular features
    :return: r_features : dataframe con 5 columnas originales, nombres cohercionados. + Features generados

    # Debuging
    p_datos = pd.DataFrame({''timestamp': {}, 'open': np.random.normal(1.1400, 0.0050, 20).
                                              'high': np.random.normal(1.1400, 0.0050, 20),
                                              'low': np.random.normal(1.1400, 0.0050, 20),
                                              'close': np.random.normal(1.1400, 0.0050, 20)})
    p_ohlc = True
    p_ntiempo = 100
    """

    datos = p_datos

    if not p_ohlc:
        datos.columns = ['timestamp', 'open', 'high', 'low', 'close']

    cols = list(datos.columns)[1:]
    datos[cols] = datos[cols].apply(pd.to_numeric, errors='coerce')

    # formato columna timestamp como 'datetime'
    datos['timestamp'] = pd.to_datetime(datos['timestamp'])
    # datos['timestamp'] = datos['timestamp'].dt.tz_localize('UTC')

    # rendimiento logaritmico de ventana 1
    datos['logrend'] = np.log(datos['close']/datos['close'].shift(1))

    # diferencia de high - low como medida de "volatilidad"
    datos['hl'] = datos['high'] - datos['low']

    # ciclo para calcular features en "ventanas"
    for n in range(0, p_ntiempo):

        # resago n de log rendimiento
        datos['lag_logrend_' + str(n)] = datos['logrend'].shift(n)

        # diferencia n de log rendimiento
        datos['dif_logrend_' + str(n+1)] = datos['logrend'].diff(n)

        # promedio movil de ventana n con log rendimiento
        datos['ma_logrend_' + str(n+1)] = datos['logrend'].rolling(n).mean()

        # log rendimiento de ventana n
        datos['logrend_' + str(n)] = np.log(datos['close']/datos['close'].shift(n))

        # resago n de high - low
        datos['lag_hl_' + str(n)] = datos['hl'].shift(n)

        # diferencia n de high - low
        datos['dif_hl_' + str(n + 1)] = datos['hl'].diff(n)

        # promedio movil de ventana n con high - low
        datos['ma_hl_' + str(n + 1)] = datos['hl'].rolling(n).mean()

    datos.dropna(axis='columns')

    r_features = datos

    return r_features
