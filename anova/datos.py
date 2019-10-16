
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

df_ce = pd.read_csv(filepath_or_buffer='archivos/calendario_economico.csv')

# -- Elegir datos de indicador
indicador = 'ISM Manufacturing PMI'
df_ice = df_ce.iloc[np.where(df_ce['Name'] == indicador)[0], :]

# cambiar nombre de 'datetime' a uno estandar que uso 'timestamp'
df_ice = df_ice.rename(columns={'DateTime': 'timestamp'})

# cambiar a minusculas los nombres de las columnas
columnas = list(df_ice.columns)
columnas = [i.lower() for i in columnas]
df_ice.rename(columns=dict(zip(df_ice.columns[1:], columnas)), inplace=True)

# resetear index en dataframe resultante porque guarda los indices del dataframe pasado
df_ice = df_ice.reset_index(drop=True)

# convertir columna a datetime
df_ice['DateTime'] = pd.to_datetime(df_ice['DateTime'])

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

# renombrar las columnas
df_ice = df_ice.rename(columns={'DateTime': 'TimesTamp'})

# -- ------------------------------------------------------------------------------------ Datos: Precios con OANDA -- #
# -- --------------------------------------------------------------------------------------- --------------------- -- #

OA_Da = 16                         # Day Align
OA_Ai = "101-004-2221697-001"      # Id de cuenta
OA_At = "practice"                 # Tipo de cuenta
OA_In = "EUR_USD"                  # Instrumento
OA_Gn = "M5"                        # Granularidad de velas
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
    final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

    return final


# -- -------------------------------------------------------------------------------- Proceso de descarga completo -- #
# -- -------------------------------------------------------------------------------- ---------------------------- -- #
# -- Solo correr esta parte si se quiere descargar todos los precios

# Descagar todos los precios necesarios
# df_precios = f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn, p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=5000)

# Resetear index
# df_precios = df_precios.reset_index(drop=True)

# Escribir dataframe en un archivo csv
# df_precios.to_csv(r"archivos/precios_historicos.csv")

# Leer archivo de precios historicos
df_precios = pd.read_csv("archivos/precios_historicos.csv")
