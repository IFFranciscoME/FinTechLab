
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Aplicacion de ANOVA para finanzas bursatiles
# -- Codigo: visualizaciones.py
# -- Autor: Francisco ME
# -- Repositorio: https://github.com/IFFranciscoME/FinTechLab/blob/master/anova/visualizaciones.py
# -- ------------------------------------------------------------------------------------------------------------- -- #

import plotly.graph_objs as go

# para elegir el motor de renderizacion por default
import plotly.io as pio
pio.renderers.default = "browser"


# -- ----------------------------------------------------------------------------------------------------- ------- -- #
# -- ----------------------------------------------------------------------------------------------------- Grafica -- #
# -- Grafica de velas para visualizar drawdown

def g_velasdd(p0_de):
    """
    :param p0_de: data frame con datos a graficar
    :return fig:

    p0_de = datos_dd
    p1_pa = 'sell'
    datos_dd = pd.DataFrame({'timestamp': [], 'open': [], 'high': [], 'low': [], 'close': []}, index=[])
    """

    # p0_de['timestamp'] = [(pd.to_datetime(p0_de['timestamp']))[x].tz_localize('UTC')
    #                           for x in range(0, len(p0_de['timestamp']))]

    f_i = p0_de['timestamp'].loc[0]

    yini = p0_de['high'][0]
    yfin = max(p0_de['high'])
    fig = go.Figure(data=[go.Candlestick(x=p0_de['timestamp'],
                                         open=p0_de['open'], high=p0_de['high'],
                                         low=p0_de['low'], close=p0_de['close'])])

    lineas = [dict(x0=f_i, x1=f_i, xref='x', y0=yini, y1=yfin, yref='y', type='line',
                   line=dict(color='red', width=1.5, dash='dashdot'))]

    fig.update_layout(
        title=dict(x=0.5, text='Reacción del precio (intradía) ante el comunicado de un <b> indicador económico </b>'),
        xaxis=dict(title_text='Hora del dia'),  # Etiquetas de eje x
        yaxis=dict(title_text='Precio del EurUsd'),
        annotations=[go.layout.Annotation(x=f_i, y=1.025, xref="x", yref="paper", showarrow=False,
                                          text="Indicador Comunicado")],
        shapes=lineas)

    return fig


# -- ----------------------------------------------------------------------------------------------------- ------- -- #
# -- ----------------------------------------------------------------------------------------------------- Grafica -- #
# -- Grafica histogramas multiples

def g_hist_varios(p0_val, p1_colores, p2_etiquetas):
    """
    :param p2_etiquetas:
    :param p1_colores:
    :param p0_val:
    :return:

    p0_val = pd.DataFrame({'val_1': df_data_ce_c[df_data_ce_c['escenario'] == 'A']['ol'],
                           'val_2': df_data_ce_c[df_data_ce_c['escenario'] == 'B']['ol'],
                           'val_3': df_data_ce_c[df_data_ce_c['escenario'] == 'H']['ol']})

    p1_colores = {'serie_1': '#047CFB', 'serie_2': '#42c29b', 'serie_3': '#6B6B6B'}

    p2_etiquetas = {'titulo': '<b>Histograma de probabilidad </b>ol: (open - low)',
                    'ejex': 'valores en (pips)', 'ejey': 'probabilidad'}

    """

    # Inicializar un objeto tipo figura
    fig = go.Figure()

    # parametros adicionales
    p2_nombres = {'serie_1': 'A', 'serie_2': 'B', 'serie_3': 'H'}

    # Agregar un trazo tipo histograma 1
    fig.add_trace(go.Histogram(x=p0_val['val_1'], histnorm='probability',
                               name='Escenario ' + p2_nombres['serie_1'], marker_color=p1_colores['serie_1'],
                               hovertemplate='<i>Probabilidad</i>: %{y} <br><b>Rango de pips 1</b>: %{x} <br>'))

    # Agregar un trazo tipo histograma 2
    fig.add_trace(go.Histogram(x=p0_val['val_2'], histnorm='probability',
                               name='Escenario ' + p2_nombres['serie_2'], marker_color=p1_colores['serie_2'],
                               hovertemplate='<i>Probabilidad</i>: %{y} <br><b>Rango de pips 2</b>: %{x} <br>'))

    # Agregar un trazo tipo histograma 3
    fig.add_trace(go.Histogram(x=p0_val['val_3'], histnorm='probability',
                               name='Escenario ' + p2_nombres['serie_3'], marker_color=p1_colores['serie_3'],
                               hovertemplate='<i>Probabilidad</i>: %{y} <br><b>Rango de pips 3</b>: %{x} <br>'))

    # Actualizar el layout de titulos y ejes
    fig.update_layout(title=dict(x=0.5, text=p2_etiquetas['titulo']),
                      xaxis=dict(title_text=p2_etiquetas['ejex']),
                      yaxis=dict(title_text=p2_etiquetas['ejey']),
                      bargap=0.01)

    # Al hacer hover o "mouse over" en las barras que se trunque a 2 decimales en los numeros y expersarlo en %
    fig.update_yaxes(hoverformat='%.2f')
    # Al hacer hover o "mouse over" en las barras que se trunque a 2 decimales en los numeros
    fig.update_xaxes(hoverformat=".2f")
    # Overlay both histograms
    fig.update_layout(barmode='relative')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.5)
    # mostrar plot
    # fig.show()

    return fig
