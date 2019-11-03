
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Aplicacion de ANOVA para finanzas bursatiles
# -- Codigo: funciones.py
# -- Autor: Francisco ME
# -- Repositorio: https://github.com/IFFranciscoME/FinTechLab/blob/master/anova/funciones.py
# -- ------------------------------------------------------------------------------------------------------------- -- #

import numpy as np                                        # operaciones matematicas
import pandas as pd                                       # dataframes y utilidades
from datetime import timedelta                            # diferencia entre datos tipo tiempo
from oandapyV20 import API                                # conexion con broker para informacion historica
import oandapyV20.endpoints.instruments as instruments    # informacion de precios historicos


# -- ---------------------------------------------------------------------------------------- definir metrica base -- #
# -- ---------------------------------------------------------------------------------------- -------------------- -- #

def f_reaccion(p0_i, p1_ad, p2_pe, p3_ce):
    """
    :param p0_i: indexador para iterar en los datos de entrada
    :param p1_ad: cantidad de precios futuros que se considera la ventana (t + p1_ad)
    :param p2_pe: precios en OHLC tipo dataframe con columnas: timestamp, open, high, low, close
    :param p3_ce: calendario economico en dataframe con columnas: timestamp, name, actual, consensus, previous

    :return: resultado: diccionario con resultado final con 3 elementos como resultado

    # debugging
    p0_i = 1
    p0_ad = 3
    p2_pe = pd.DataFrame({'timestamp': 2009-01-06 05:00:00,
                          'open': 1.3556, 'high': 1.3586, 'low': 1.3516, 'close': 1.3543})
    p3_ce = pd.DataFrame({})
    """

    # Encontrar indice donde el timestamp sea igual al
    indice_1 = np.where(p2_pe['timestamp'] == p3_ce['timestamp'][p0_i])[0][0]
    indice_2 = indice_1 + p1_ad
    ho = round((max(p2_pe['high'][indice_1:indice_2]) - p2_pe['open'][indice_1])*10000, 2)
    ol = round((p2_pe['open'][indice_1] - min(p2_pe['low'][indice_1:indice_2]))*10000, 2)

    # diccionario con resultado final
    resultado = {'ho': ho, 'ol': ol}

    return resultado


# -- --------------------------------------------------------------------------------------------- rango de fechas -- #
# -- --------------------------------------------------------------------------------------------- --------------- -- #

def f_datetime_range_fx(start_datetime, end_datetime, increment, delta_period):
    """
    :param start_datetime:
    :param end_datetime:
    :param increment:
    :param delta_period:

    :return:
    """

    result = []
    nxt = start_datetime

    while nxt <= end_datetime:
        result.append(nxt)
        if delta_period == 'minutes':
            nxt += timedelta(minutes=increment)
        elif delta_period == 'hours':
            nxt += timedelta(hours=increment)
        elif delta_period == 'days':
            nxt += timedelta(days=increment)

    return result


# -- ------------------------------------------------------------------------- Descarga masiva de recios con OANDA -- #
# -- ------------------------------------------------------------------------- ----------------------------------- -- #

def f_precios_masivos(p0_fini, p1_ffin, p2_gran, p3_inst, p4_oatk, p5_ginc):
    """
    :param p0_fini: fecha inicial
    :param p1_ffin: fecha final
    :param p2_gran: granularidad de los precios
    :param p3_inst: instrumento
    :param p4_oatk: llave privada de oanda para peticiones con api
    :param p5_ginc: incremento de valor para fechas dinamicas

    :return: final: dataframe final con todos los precios historicos

    p0_fini = fini
    p1_ffin = ffin
    p2_gran = OA_Gn
    p3_inst = OA_In
    p4_oatk = OA_Ak
    p5_ginc = gn[OA_Gn]['in']

    """

    # inicializar api de OANDA
    api = API(access_token=p4_oatk)

    # hacer series de fechas e iteraciones para pedir todos los precios
    fechas = f_datetime_range_fx(start_datetime=p0_fini, end_datetime=p1_ffin, increment=p5_ginc,
                                 delta_period='minutes')

    # Lista para ir guardando los data frames
    lista_df = list()

    for n_fecha in range(0, len(fechas)-1):

        # Fecha inicial y fecha final
        f1 = fechas[n_fecha].strftime('%Y-%m-%dT%H:%M:%S')
        f2 = fechas[n_fecha+1].strftime('%Y-%m-%dT%H:%M:%S')

        # Parametros pra la peticion de precios
        params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1, "to": f2}

        # Ejecutar la peticion de precios
        a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
        a1_hist = api.request(a1_req1)

        # Para debuging
        # print(f1 + ' y ' + f2)
        lista = list()

        # Acomodar las llaves
        for i in range(len(a1_hist['candles']) - 1):
            lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                          'Open': a1_hist['candles'][i]['mid']['o'],
                          'High': a1_hist['candles'][i]['mid']['h'],
                          'Low': a1_hist['candles'][i]['mid']['l'],
                          'Close': a1_hist['candles'][i]['mid']['c']})

        # Acomodar en un data frame
        pd_hist = pd.DataFrame(lista)
        pd_hist = pd_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
        pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])

        # Ir guardando resultados en una lista
        lista_df.append(pd_hist)

    # Concatenar todas las listas
    df_final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

    columns = list(df_final.columns)
    columns = [i.lower() for i in columns]

    # Renombrar todas las columnas del dataframe con una lista de nombres
    df_final.rename(columns=dict(zip(df_final.columns[0:], columns)), inplace=True)

    # resetear index en dataframe resultante porque guarda los indices del dataframe pasado
    df_final = df_final.reset_index(drop=True)

    return df_final
