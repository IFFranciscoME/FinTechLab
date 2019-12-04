
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Funcion para solicitar datos de Oanda
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

# Cargar librerias y dependencias
import pandas as pd
import numpy as np
from statsmodels.tsa.api import acf, pacf

from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments

import statsmodels.api as sm                              # utilidades para modelo regresion lineal
from sklearn.model_selection import train_test_split      # separacion de conjunto de entrenamiento y prueba

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
# -- --------------------------------------- ------------------------------------------------------ Version manual -- #

def f_feature_eng(p_datos, p_ohlc):
    """
    :param p_datos: pd.DataFrae : dataframe con 5 columnas 'timestamp', 'open', 'high', 'low', 'close'
    :param p_ohlc: bool : True si son datos con columnas 'timestamp', 'open', 'high', 'low', 'close', False otro caso
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
    datos['logrend'] = np.log(datos['close']/datos['close'].shift(1)).dropna()
    # signo del rendimiento para indicar "alcista = 1" o "bajista = 0"
    datos['logrend_c'] = [1 if datos['logrend'][i] > 0 else -1 for i in range(0, len(datos['logrend']))]

    # diferencia de high - low como medida de "volatilidad"
    datos['hl'] = (datos['high'] - datos['low'])*10000

    # funciones de ACF y PACF para determinar ancho de ventana historica
    data_acf = acf(datos['logrend'].dropna(), nlags=52, fft=True)
    data_pac = pacf(datos['logrend'].dropna(), nlags=52)
    # componentes AR y MA
    maxs = list(set(list(np.where((data_pac > 0.122) | (data_pac < -0.122))[0]) +
                    list(np.where((data_acf > 0.122) | (data_acf < -0.122))[0])))
    # encontrar la componente maxima como indicativo de informacion historica autorelacionada
    max_n = maxs[np.argmax(maxs)]

    # ciclo para calcular N features con logica de "Ventanas de tamaño n"
    for n in range(0, max_n):

        # resago n de log rendimiento
        datos['lag_logrend_' + str(n+1)] = datos['logrend'].shift(n+1)

        # diferencia n de log rendimiento
        datos['dif_logrend_' + str(n+1)] = datos['logrend'].diff(n+1)

        # promedio movil de ventana n con log rendimiento
        datos['ma_logrend_' + str(n+2)] = datos['logrend'].rolling(n+2).mean()

        # resago n de high - low
        datos['lag_hl_' + str(n+1)] = datos['hl'].shift(n+1)

        # diferencia n de high - low
        datos['dif_hl_' + str(n+1)] = datos['hl'].diff(n+1)

        # promedio movil de ventana n con high - low
        datos['ma_hl_' + str(n+2)] = datos['hl'].rolling(n+2).mean()

    # asignar timestamp como index
    datos.index = datos['timestamp']
    # quitar columnas no necesarias para modelos de ML
    datos = datos.drop(['timestamp', 'open', 'high', 'low', 'close', 'hl'], axis=1)
    # borrar columnas donde exista solo NAs
    r_features = datos.dropna(axis='columns', how='all')
    # borrar renglones donde exista algun NA
    r_features = r_features.dropna(axis='rows')
    # resetear index de dataframe
    r_features = r_features.reset_index(drop=True)

    return r_features


# -- ----------------------------------------------------------------------------- FUNCION: Seleccion de variables -- #
# -- ------------------------------------------------------------------------------ ------------------------------ -- #

def f_feature_importance(p_datos):
    """
    :param p_datos:
    :return:
    p_datos = df_datos
    """

    # np.corrcoef()

    return 1


# -- -------------------------------------------------------------------------------- FUNCION: Ajustar RLM a datos -- #
# -- -------------------------------------------------------------------------------- ---------------------------- -- #

def f_rlm(p_datos):
    """
    :param p_datos: pd.DataFrame : DataFrame con variable "y" (1era col), y n variables "x_n" (2:n)
    :return:
    p_datos = df_datos
    """

    datos = p_datos

    # Reacomodar los datos como arreglos
    y_multiple = np.array(datos.iloc[:, 1])
    x_multiple = np.array(datos.iloc[:, 2:])

    # datos para entrenamiento y prueba
    train_x, test_x, train_y, test_y = train_test_split(x_multiple, y_multiple, test_size=0.8, shuffle=False)

    # Agregar interceptos a X en entrenamiento y prueba
    train_x_betha = sm.add_constant(train_x)
    test_x_betha = sm.add_constant(test_x)

    # Modelo ajustado (entrenamiento)
    modelo_train = sm.OLS(train_y, train_x_betha)
    # Resultados de ajuste de modelo (entrenamiento)
    modelo_fit_train = modelo_train.fit()

    # Modelo ajustado (prueba)
    modelo_test = sm.OLS(test_y, test_x_betha)
    # Resultados de ajuste de modelo (prueba)
    modelo_fit_test = modelo_test.fit()

    # -- Con datos de ENTRENAMIENTO
    # modelo completo resultante
    r_train_modelo = modelo_fit_train
    # summary de resultados del modelo
    r_train_summary = r_train_modelo.summary()
    # DataFrame con nombre de parametros segun dataset, nombre de parametros y pvalues segun modelo
    r_df_train = pd.DataFrame({'df_params': ['intercepto'] + list(datos.columns[2:]),
                               'm_params': r_train_modelo.model.data.param_names, 'pv_params': r_train_modelo.pvalues})
    # valor de AIC del modelo
    r_train_aic = r_train_modelo.aic
    # valor de BIC del modelo
    r_train_bic = r_train_modelo.bic

    # -- Con datos de PRUEBA
    # modelo completo resultante
    r_test_modelo = modelo_fit_test
    # summary de resultados del modelo
    r_test_summary = r_test_modelo.summary()
    # DataFrame con nombre de parametros segun dataset, nombre de parametros y pvalues segun modelo
    r_df_test = pd.DataFrame({'df_params': ['intercepto'] + list(datos.columns[2:]),
                              'm_params': r_test_modelo.model.data.param_names, 'pv_params': r_test_modelo.pvalues})
    # valor de AIC del modelo
    r_test_aic = r_test_modelo.aic
    # valor de BIC del modelo
    r_test_bic = r_test_modelo.bic

    # tabla de resultados periodo de entrenamiento
    r_df_pred_train = pd.DataFrame({'y': train_y, 'y_ajustada': modelo_fit_train.predict()})
    # tabla de resultados periodo de prueba
    r_df_pred_test = pd.DataFrame({'y': test_y, 'y_ajustada': modelo_fit_test.predict()})

    r_d_modelo = {'train': {'modelo': r_train_modelo, 'summary': r_train_summary, 'parametros': r_df_train,
                            'resultado': r_df_pred_train, 'aic': r_train_aic, 'bic': r_train_bic},
                  'test': {'modelo': r_test_modelo, 'summary': r_test_summary, 'parametros': r_df_test,
                            'resultado': r_df_pred_test, 'aic': r_test_aic, 'bic': r_test_bic}}

    return r_d_modelo
