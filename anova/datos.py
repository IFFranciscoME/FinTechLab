
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Aplicacion de ANOVA para finanzas bursatiles
# -- Codigo: datos.py
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

import pandas as pd
import numpy as np
from datetime import timedelta

from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
pd.options.mode.chained_assignment = None                 # para evitar el warning enfadoso de indexacion

# -- --------------------------------------------------------------------------------- Datos: Calendario Economico -- #
# -- --------------------------------------------------------------------------------------- --------------------- -- #

# leer archivo con informacion historica
df_ce_ini = pd.read_csv(filepath_or_buffer='archivos/calendario_economico.csv')

# Elegir datos de indicador
indicador = 'ISM Manufacturing PMI'
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
# -- --------------------------------------------------------------------------------------- --------------------- -- #

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


# -- --------------------------------------------------------------------------------------------- rango de fechas -- #

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


# -- ---------------------------------------------------------------------------------- Obtener precios historicos -- #

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
        params = {"granularity": p2_gran, "price": "M", "dailyAlignment": OA_Da, "from": f1, "to": f2}

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


# -- -------------------------------------------------------------------------------- Proceso de descarga completo -- #
# -- -------------------------------------------------------------------------------- ---------------------------- -- #
# -- Solo correr esta parte si se quiere descargar todos los precios

# Descagar todos los precios necesarios
# df_pe = f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn, p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=5000)

# Escribir dataframe en un archivo csv
# df_pe.to_csv(r"archivos/precios_historicos.csv", index=False)

# Leer archivo de precios historicos
df_pe = pd.read_csv("archivos/precios_historicos.csv")
