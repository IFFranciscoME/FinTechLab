
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Proyecto final de materia Análisis Estadístico Multivariado                               -- #
# -- Codigo: visualizaciones.py - codigos para generar visualizaciones para el proyecto                  -- #
# -- Repositorio: https://github.com/IFFranciscoME/FinTechLab/tree/master/MCD-ITESO/AEM/aem_proyecto     -- #
# -- Autor: Francisco ME                                                                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #

import plotly.graph_objs as go
# para elegir el motor de renderizacion por default
import plotly.io as pio
pio.renderers.default = "browser"


# -- ------------------------------------------------------------------------------------------- ------- -- #
# -- ------------------------------------------------------------------------------------------- Grafica -- #
# -- Grafica de velas para visualizar drawdown

def g_velas(p0_de):
    """
    :param p0_de: data frame con datos a graficar
    :return fig:

    p0_de = datos_dd
    p1_pa = 'sell'
    datos_dd = pd.DataFrame({'timestamp': [], 'open': [], 'high': [], 'low': [], 'close': []}, index=[])
    """

    p0_de.columns = [list(p0_de.columns)[i].lower() for i in range(0, len(p0_de.columns))]

    fig = go.Figure(data=[go.Candlestick(x=p0_de['timestamp'],
                                         open=p0_de['open'], high=p0_de['high'],
                                         low=p0_de['low'], close=p0_de['close'])])

    fig.update_layout(
        title=dict(x=0.5, text='Precios Historicos '),
        xaxis=dict(title_text='Hora del dia'),  # Etiquetas de eje x
        yaxis=dict(title_text='Precio del EurUsd'))

    return fig


# fig = plt.figure(figsize=(12, 8))
# ax1 = fig.add_subplot(211)
# fig = sm.graphics.tsa.plot_acf(p_datos['logrend'], lags=10, ax=ax1)
# ax2 = fig.add_subplot(212)
# fig = sm.graphics.tsa.plot_pacf(p_datos['logrend'], lags=10, ax=ax2)
