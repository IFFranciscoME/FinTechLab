
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Proyecto final de materia Análisis Estadístico Multivariado                               -- #
# -- Codigo: funciones.py - codigo con funciones de modelos y operaciones complejas                      -- #
# -- Repositorio: https://github.com/IFFranciscoME/FinTechLab/tree/master/MCD-ITESO/AEM/aem_proyecto     -- #
# -- Autor: Francisco ME                                                                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #

import numpy as np                                     # funciones numericas
import pandas as pd                                    # dataframes y utilidades
from statsmodels.tsa.api import acf, pacf              # funciones de econometria

from sklearn.preprocessing import StandardScaler       # estandarizacion de variables
from sklearn.decomposition import PCA                  # analisis de componentes principales (PCA)
import statsmodels.api as sm                           # utilidades para modelo regresion lineal
from sklearn.model_selection import train_test_split   # separacion de conjunto de entrenamiento y prueba

pd.set_option('display.max_rows', None)                # sin limite de renglones maximos para mostrar pandas
pd.set_option('display.max_columns', None)             # sin limite de columnas maximas para mostrar pandas
pd.set_option('display.width', None)                   # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)      # visualizar todas las columnas de un dataframe
pd.options.mode.chained_assignment = None              # para evitar el warning enfadoso de indexacion


# -- ---------------------------------------- FUNCION: Generacion de variables EXOGENAS series de tiempo -- #
# -- ------------------------------------------------------------------------------------ Version manual -- #

def f_anova(p_datos_ce, p_datos_ph):
    """
    :param p_datos_ph:
    :param p_datos_ce:
    :return:

    p_datos_ce = df_ce_w
    p_datos_ph = df_precios_m5
    """

    def f_reaccion(p0_i, p1_ad, p2_pe, p3_ce):
        """
        :param p0_i: int : indexador para iterar en los datos de entrada
        :param p1_ad: int : cantidad de precios futuros que se considera la ventana (t + p1_ad)
        :param p2_pe: DataFrame : precios en OHLC con columnas: timestamp, open, high, low, close
        :param p3_ce: DataFrame : calendario economico con columnas: timestamp, name,
                                                                     actual, consensus, previous

        :return: resultado: diccionario con resultado final con 3 elementos como resultado

        # debugging
        p0_i = 16
        p0_ad = 5
        p2_pe = pd.DataFrame({'timestamp': 2009-01-06 05:00:00,
                              'open': 1.3556, 'high': 1.3586, 'low': 1.3516, 'close': 1.3543})
        p3_ce = pd.DataFrame({})
        """
        print(p0_i)
        # Encontrar indice donde el timestamp sea igual al
        indice_1 = np.where(p2_pe['timestamp'] == p3_ce['timestamp'][p0_i])[0][0]
        indice_2 = indice_1 + p1_ad
        ho = round((max(p2_pe['high'][indice_1:indice_2]) - p2_pe['open'][indice_1]) * 10000, 2)
        ol = round((p2_pe['open'][indice_1] - min(p2_pe['low'][indice_1:indice_2])) * 10000, 2)

        # diccionario con resultado final
        resultado = {'ho': ho, 'ol': ol}

        return resultado

    # datos de calendario economico
    p_datos_ce['timestamp'] = pd.to_datetime(p_datos_ce['timestamp']).dt.floor('Min')
    p_datos_ce['timestamp'] = p_datos_ce['timestamp'].dt.tz_localize('UTC')

    # datos de precios historicos
    p_datos_ph['timestamp'] = pd.to_datetime(p_datos_ph['timestamp']).dt.floor('Min')
    p_datos_ph['timestamp'] = p_datos_ph['timestamp'].dt.tz_localize('UTC')

    # cantidad de precios a futuro a considerar
    psiguiente = 7

    # escenarios para clasificar los eventos
    escenarios = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    # reaccion del precio para cada escenario
    d_reaccion = [f_reaccion(p0_i=i, p1_ad=psiguiente, p2_pe=p_datos_ph, p3_ce=p_datos_ce)
                  for i in range(0, len(p_datos_ce['timestamp']))]

    # acomodar resultados en columnas
    p_datos_ce['ho'] = [d_reaccion[j]['ho'] for j in range(0, len(p_datos_ce['timestamp']))]
    p_datos_ce['ol'] = [d_reaccion[j]['ol'] for j in range(0, len(p_datos_ce['timestamp']))]

    return p_datos_ce


# -- --------------------------------------- FUNCION: Generacion de variables ENDOGENAS series de tiempo -- #
# -- ------------------------------------------------------------------------------------ Version manual -- #

def f_features_end(p_datos):
    """
    :param p_datos: pd.DataFrae : dataframe con 5 columnas 'timestamp', 'open', 'high', 'low', 'close'
        :return: r_features : dataframe con 5 columnas, nombres cohercionados + Features generados

    # Debuging
    p_datos = df_precios
    p_datos = pd.DataFrame({''timestamp': {}, 'open': np.random.normal(1.1400, 0.0050, 20).
                                              'high': np.random.normal(1.1400, 0.0050, 20),
                                              'low': np.random.normal(1.1400, 0.0050, 20),
                                              'close': np.random.normal(1.1400, 0.0050, 20)})
    """

    datos = p_datos
    datos.columns = ['timestamp', 'open', 'high', 'low', 'close']

    cols = list(datos.columns)[1:]
    datos[cols] = datos[cols].apply(pd.to_numeric, errors='coerce')

    # formato columna timestamp como 'datetime'
    datos['timestamp'] = pd.to_datetime(datos['timestamp'])
    # datos['timestamp'] = datos['timestamp'].dt.tz_localize('UTC')

    # rendimiento logaritmico de ventana 1
    datos['logrend'] = np.log(datos['close']/datos['close'].shift(1)).dropna()

    # pips descontados al cierre
    datos['co'] = (datos['close']-datos['open'])*10000

    # pips descontados alcistas
    datos['ho'] = (datos['high'] - datos['open'])*10000

    # pips descontados bajistas
    datos['ol'] = (datos['open'] - datos['low'])*10000

    # pips descontados en total (medida de volatilidad)
    datos['hl'] = (datos['high'] - datos['low'])*10000

    # funciones de ACF y PACF para determinar ancho de ventana historica
    data_acf = acf(datos['logrend'].dropna(), nlags=12, fft=True)
    data_pac = pacf(datos['logrend'].dropna(), nlags=12)
    sig = round(1.96/np.sqrt(len(datos['logrend'])), 4)

    # componentes AR y MA
    maxs = list(set(list(np.where((data_pac > sig) | (data_pac < -sig))[0]) +
                    list(np.where((data_acf > sig) | (data_acf < -sig))[0])))
    # encontrar la componente maxima como indicativo de informacion historica autorelacionada
    max_n = maxs[np.argmax(maxs)]

    # condicion arbitraria: 5 resagos minimos para calcular variables moviles
    if max_n <= 2:
        max_n = 5

    # ciclo para calcular N features con logica de "Ventanas de tamaño n"
    for n in range(0, max_n):

        # resago n de ho
        datos['lag_ho_' + str(n + 1)] = np.log(datos['ho'].shift(n + 1))

        # resago n de ol
        datos['lag_ol_' + str(n + 1)] = np.log(datos['ol'].shift(n + 1))

        # promedio movil de ventana n
        datos['ma_ol_' + str(n + 2)] = datos['ol'].rolling(n + 2).mean()

        # promedio movil de ventana n
        datos['ma_ho_' + str(n + 2)] = datos['ho'].rolling(n + 2).mean()

    # asignar timestamp como index
    datos.index = pd.to_datetime(datos['timestamp'])
    # quitar columnas no necesarias para modelos de ML
    datos = datos.drop(['timestamp', 'open', 'high', 'low', 'close', 'hl', 'logrend'], axis=1)
    # borrar columnas donde exista solo NAs
    r_features = datos.dropna(axis='columns', how='all')
    # borrar renglones donde exista algun NA
    r_features = r_features.dropna(axis='rows')
    # convertir a numeros tipo float las columnas
    r_features.iloc[:, 1:] = r_features.iloc[:, 1:].astype(float)
    # estandarizacion de todas las variables independientes
    lista = r_features[list(r_features.columns[1:])]
    r_features[list(r_features.columns[1:])] = StandardScaler().fit_transform(lista)

    return r_features


# -- ---------------------------------------------------------------------- FUNCION: Ajustar RLM a datos -- #
# -- ---------------------------------------------------------------------- ---------------------------- -- #

def f_rlm(p_datos, p_y):
    """
    :param p_datos: pd.DataFrame : DataFrame con variable "y" (1era col), y n variables "x_n" (2:n)
    :param p_y : str : nombre de la columna a elegir como variable dependiente Y
    :return:
    p_datos = df_datos
    """

    datos = p_datos

    # Reacomodar los datos como arreglos
    y_multiple = np.array(datos[p_y])
    x_multiple = np.array(datos.iloc[:, 1:])

    # datos para entrenamiento y prueba
    train_x, test_x, train_y, test_y = train_test_split(x_multiple, y_multiple,
                                                        test_size=0.8, shuffle=False)

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
    r_df_train = pd.DataFrame({'df_params': ['intercepto'] + list(datos.columns[1:]),
                               'm_params': r_train_modelo.model.data.param_names,
                               'pv_params': r_train_modelo.pvalues})
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
    r_df_test = pd.DataFrame({'df_params': ['intercepto'] + list(datos.columns[1:]),
                              'm_params': r_test_modelo.model.data.param_names,
                              'pv_params': r_test_modelo.pvalues})
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


# -- ---------------------------------------------------------------------- FUNCION: Aplicar PCA a datos -- #
# -- ---------------------------------------------------------------------- ---------------------------- -- #

def f_pca(p_datos, p_exp):
    """
    :param p_datos:
    :param p_exp:
    :return:

    p_datos = df_datos
    p_exp = .90
    """
    datos = p_datos

    pca = PCA(n_components=10)
    datos_pca = datos.iloc[:, 1:]
    pca.fit(datos_pca)
    # Calcular los vectores y valores propios de la martiz de covarianza
    w, v = np.linalg.eig(pca.get_covariance())
    # ordenar los valores de mayor a menor
    indx = np.argsort(w)[::-1]
    # calcular el procentaje de varianza en cada componente
    porcentaje = w[indx] / np.sum(w)
    # calcular el porcentaje acumulado de los componentes
    porcent_acum = np.cumsum(porcentaje)
    # encontrar las componentes necesarias para lograr explicar el 90% de variabilidad
    pca_90 = np.where(porcent_acum > p_exp)[0][0] + 1

    pca = PCA(n_components=pca_90)
    datos_pca = datos.iloc[:, 1:]
    df1 = datos.iloc[:, 0]
    pca.fit(datos_pca)
    df2 = pd.DataFrame(pca.transform(datos_pca))

    df1.reset_index(drop=True, inplace=True)
    df2.reset_index(drop=True, inplace=True)

    r_datos_pca = pd.concat([df1, df2], axis=1)
    r_datos_pca.index = datos_pca.index

    # Renombrar columnas
    r_datos_pca.columns = ['pca_y'] + ['pca_x_' + str(i) for i in range(0, pca_90)]

    return r_datos_pca


# -- ---------------------------------------------------------------------- FUNCION: Desempeño de modelo -- #
# -- ---------------------------------------------------------------------- ---------------------------- -- #

def f_analisis_mod(p_datos):
    """
    :param p_datos
    :return:
    p_datos = df_datos
    """

    # from statsmodels.stats.outliers_influence import variance_inflation_factor
    # from patsy import dmatrices
    # p_datos.index = [np.arange(len(p_datos))]
    # features = " + ".join(list(p_datos.columns[1:]))
    # y, X = dmatrices('co ~' + features, p_datos, return_type='dataframe')
    # vif = pd.DataFrame()
    # vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    # vif["features"] = X.columns

    return p_datos


# -- ------------------------------------------------------------------- FUNCION: Seleccion de variables -- #
# -- -------------------------------------------------------------------- ------------------------------ -- #

def f_feature_importance(p_datos):
    """
    :param p_datos:
    :return:
    p_datos = df_datos
    """

    # np.corrcoef()

    return p_datos
