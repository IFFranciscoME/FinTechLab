
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Regresion Lineal Multiple para Series de Tiempo
# -- Codigo: Funciones para generar viualizaciones de datos
# -- Autor: Francisco ME
# -- ------------------------------------------------------------------------------------------------------------- -- #

# Cargar librerias y dependencias
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

# para elegir el motor de renderizacion por default
import plotly.io as pio
pio.renderers.default = "browser"


# -- ----------------------------------------------------------------------------------------------------- ------- -- #
# -- ----------------------------------------------------------------------------------------------------- Grafica -- #
# -- Grafica de velas para visualizar drawdown

def g_velasdd(p0_de, p1_pa):
    """
    :param p0_de: data frame con datos a graficar
    :param p1_pa: parametro de si fue 'sell' o 'buy' para color de lineas
    :return fig:

    p0_de = datos
    p1_pa = 'sell'
    datos_dd = pd.DataFrame({'timestamp': [], 'open': [], 'high': [], 'low': [], 'close': []}, index=[])
    """

    # convertir a minusculas todos los nombres de columnas
    p0_de.columns = [p0_de.columns[i].lower() for i in range(0, len(p0_de.columns))]

    # p0_de['timestamp'] = [(pd.to_datetime(p0_de['timestamp']))[x].tz_localize('UTC')
    #                           for x in range(0, len(p0_de['timestamp']))]

    f_i = p0_de['timestamp'].loc[0]
    f_h = p0_de['timestamp'].loc[np.where(p0_de['high'] == max(p0_de['high']))[0][0]]
    f_l = p0_de['timestamp'].loc[np.where(p0_de['low'] == min(p0_de['low']))[0][0]]
    f_f = p0_de['timestamp'].loc[len(p0_de) - 1]

    p_o = p0_de['low'].loc[0]
    p_h = float(p0_de['high'].loc[np.where(p0_de['high'] == max(p0_de['high']))[0][0]])
    p_l = float(p0_de['low'].loc[np.where(p0_de['low'] == min(p0_de['low']))[0][0]])
    p_c = p0_de['low'].loc[len(p0_de) - 1]

    fig = go.Figure(data=[go.Candlestick(x=p0_de['timestamp'],
                                         open=p0_de['open'], high=p0_de['high'],
                                         low=p0_de['low'], close=p0_de['close'])])

    lineas = [dict(x0=f_i, x1=f_i, xref='x',
                   y0=p_l, y1=p_o, yref='y', type='line', line=dict(color='grey', width=1.25, dash='dot')),

              dict(x0=f_f, x1=f_f, xref='x',
                   y0=p_l, y1=p_c, yref='y', type='line', line=dict(color='grey', width=1.25, dash='dot')),

              dict(x0=f_i, x1=f_h, xref='x',
                   y0=p_h, y1=p_h, yref='y', type='line', line=dict(color='grey', width=1.25, dash='dot')),
              dict(x0=f_l, x1=f_f, xref='x',
                   y0=p_l, y1=p_l, yref='y', type='line', line=dict(color='grey', width=1.25, dash='dot')),

              dict(x0=f_i, x1=f_l, xref='x',
                   y0=p0_de['open'].loc[0], y1=p_l, yref='y', type='line',
                   line=dict(color='red' if p1_pa == 'buy' else 'blue', width=2)),

              dict(x0=f_i, x1=f_h, xref='x',
                   y0=p0_de['open'].loc[0], y1=p_h, yref='y', type='line',
                   line=dict(color='blue' if p1_pa == 'buy' else 'red', width=2))]

    fig.update_layout(xaxis_rangeslider_visible=False,
                      title='DrawDown y DrawUp de operacion: ' + p1_pa,
                      shapes=lineas)

    return fig

# -- ----------------------------------------------------------------------------------------------------- ------- -- #
# -- ----------------------------------------------------------------------------------------------------- Grafica -- #
# -- Matriz de graficas de dispersion


def explora(datos):

    fig = px.scatter_matrix(datos)

    return fig
