
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Proyecto:
# -- Codigo:
# -- Autor: Francisco ME
# -- --------------------------------------------------------------------------------------------------- -- #

import numpy as np                                        # funciones numericas
import pandas as pd                                       # dataframes y utilidades
from datetime import timedelta                            # diferencia entre datos tipo tiempo
from oandapyV20 import API                                # conexion con broker para informacion historica
import oandapyV20.endpoints.instruments as instruments    # informacion de precios historicos

# -- ----------------------------------------------------------------- Solo cargar datos pre-descargados -- #
# leer archivo de precios historicos ya descargados previamente
df_pe_m5 = pd.read_csv("archivos/Eur_Usd_M5.csv")
df_pe_w = pd.read_csv("archivos/Eur_Usd_W.csv")
df_ce = pd.read_csv("archivos/Calendario_Economico.csv")

# seleccionar indicadores que hayan sido publicados 4 veces en cada mes (semanales)
df_ce = df_ce.iloc[np.where(df_ce['timestamp'] == '01/04/2016 19:30:00')[0][0]:len(df_ce['timestamp'])]
df_ce = df_ce.reset_index(drop=True)
df_ce['mes'] = [pd.to_datetime(df_ce['timestamp'][i]).strftime('%m')
                for i in range(0, len(df_ce['timestamp']))]
unicos = list(set(df_ce['Name']))
longitudes = [len(df_ce[df_ce['Name'] == unicos[i]]) for i in range(0, len(unicos))]
res = [idx for idx, val in enumerate(longitudes) if val > 12*3.5*4]
ind_semanales = [unicos[i] for i in res]

# funcion wow
df_ce_w = df_ce[df_ce['Name'].isin(ind_semanales)]
df_ce_w = df_ce_w.reset_index(drop=True)

# -- -------------------------------------------------------------------- Para descargar todos los datos -- #
# Token para API de OANDA
OA_Ak = '7' + '9ae0a52f8e483facdd81f5b316a8ef8-99fb5554f4739c76535b209044f7de2' + '6'
OA_In = "EUR_USD"                  # Instrumento
OA_Gn = "M5"                        # Granularidad de velas
fini = pd.to_datetime("2009-01-06 00:00:00").tz_localize('GMT')  # Fecha inicial
ffin = pd.to_datetime("2019-12-06 00:00:00").tz_localize('GMT')  # Fecha final

pd.set_option('display.max_rows', None)             # sin limite de renglones maximos para mostrar pandas
pd.set_option('display.max_columns', None)          # sin limite de columnas maximas para mostrar pandas
pd.set_option('display.width', None)                # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)   # visualizar todas las columnas de un dataframe
pd.options.mode.chained_assignment = None           # para evitar el warning enfadoso de indexacion


# -- ---------------------------------------------------------- FUNCION: Obtencion de precios historicos -- #
# -- ---------------------------------------------------------- ---------------------------------------- -- #

def f_precios_masivos(p0_fini, p1_ffin, p2_gran, p3_inst, p4_oatk, p5_ginc):
    """
    :param p0_fini: str : fecha inicial para pedir precios : "2009-01-06 00:00:00"
    :param p1_ffin: str : fecha final para pedir precios : "2019-12-01 00:00:00"
    :param p2_gran: str : granularidad para pedir precios : S5, S10, S30, M1, M5, M15, M30, H1, H4, H8, D, W
    :param p3_inst: str : instrumento sobre el cual peedir precios (Acorde a nomenclatura OANDA) : EUR_USD
    :param p4_oatk: str : llave privada de oanda para peticiones con api : alfanumerica
    :param p5_ginc: int : numero limite de datos historicos a pedir segun Oanda : 5000

    :return: r_df_final: pd.DataFrame : dataframe final con todos los precios historicos
    """

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

    # inicializar api de OANDA
    api = API(access_token=p4_oatk)

    gn = {'S30': 30, 'S10': 10, 'S5': 5, 'M1': 60, 'M5': 60*5, 'M15': 60*15, 'M30': 60*30,
          'H1': 60*60, 'H4': 60*60*4, 'H8': 60*60*8, 'D': 60*60*24, 'W': 60*60*24*7, 'M': 60*60*24*7*4}

    # -- para el caso donde con 1 peticion se cubran las 2 fechas
    if int((p1_ffin - p0_fini).total_seconds() / gn[p2_gran]) < 5000:

        # Fecha inicial y fecha final
        f1 = p0_fini.strftime('%Y-%m-%dT%H:%M:%S')
        f2 = p1_ffin.strftime('%Y-%m-%dT%H:%M:%S')

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
        r_df_final = pd.DataFrame(lista)
        r_df_final = r_df_final[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
        r_df_final['TimeStamp'] = pd.to_datetime(r_df_final['TimeStamp'])

        return r_df_final

    # -- para el caso donde se construyen fechas secuenciales
    else:

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
            print(f1 + ' y ' + f2)
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
        r_df_final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

        columns = list(r_df_final.columns)
        columns = [i.lower() for i in columns]

        # Renombrar todas las columnas del dataframe con una lista de nombres
        r_df_final.rename(columns=dict(zip(r_df_final.columns[0:], columns)), inplace=True)

        # resetear index en dataframe resultante porque guarda los indices del dataframe pasado
        r_df_final = r_df_final.reset_index(drop=True)

        return r_df_final


print('Fin proceso cargar datos')

# -- ---------------------------------------------------------------------- Proceso de descarga completo -- #
# -- ---------------------------------------------------------------------- ---------------------------- -- #
# -- Solo correr esta parte si se quiere descargar todos los precios

# Descagar todos los precios necesarios (descomentar la linea de import funciones as fn)
# df_pe = f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,
#                           p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=5000)

# Escribir dataframe en un archivo csv
# df_pe.to_csv(r"archivos/Eur_Usd_M5.csv", index=False)
