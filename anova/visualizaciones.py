
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

def g_histograma(p0_val, p1_nbins, p2_color, p3_etiquetas):
    """
    :param p3_etiquetas:
    :param p2_color:
    :param p1_nbins:
    :param p0_val:
    :return:

    p3_etiquetas = {'titulo': 'titulo', 'ejex': 'ejex', 'ejey': 'ejey'}

    """

    bins_size = (max(p0_val) - min(p0_val)) / p1_nbins  # Calculo para distribuir valores en numero de bins elegido

    # Inicializar un objeto tipo figura
    fig = go.Figure()

    # Agregar un trazo tipo histograma
    fig.add_trace(go.Histogram(x=p0_val,  # Valores
                               histnorm='probability',  # Tipo de histograma
                               name='Pips descontados',  # Nombre para identificar el trazo
                               xbins=dict(start=min(p0_val), end=max(p0_val), size=bins_size),  # Info para bins
                               marker_color=p2_color,  # Color del marcador, en este caso las barras
                               opacity=0.75,  # Opacidad de los elementos del trazo, en este caso las barras
                               # Constructor de mensaje en HTML
                               hovertemplate='<i>Probabilidad</i>: %{y} <br><b>Rango de pips</b>: %{x} <br>'))

    # Actualizar el layout de titulos y ejes
    fig.update_layout(
        title=dict(x=0.5, text=p3_etiquetas['titulo']),
        xaxis=dict(title_text=p3_etiquetas['ejex']),  # Etiquetas de eje x
        yaxis=dict(title_text=p3_etiquetas['ejey']),  # Etiquetas de eje y
        bargap=0.01  # Espacio entre las barras
    )

    # Al hacer hover o "mouse over" en las barras que se trunque a 2 decimales en los numeros y expersarlo en %
    fig.update_yaxes(hoverformat='%.2f')

    # Al hacer hover o "mouse over" en las barras que se trunque a 2 decimales en los numeros
    fig.update_xaxes(hoverformat=".2f")

    # Mostrar grafica fuera de plotly
    # fig.show()

    return fig
