
# -- ------------------------------------------------------------------------------------------------------------- -- #
# -- Proyecto: Ejercicios de aplicaciones de modelos lineales (Regresion simple/multiple, anova, loglineal)
# -- Codigo: visualizaciones.py
# -- Autor: Francisco ME
# -- Repositorio: https://github.com/IFFranciscoME/FinTechLab/tree/master/varios/modelos_lineales
# -- ------------------------------------------------------------------------------------------------------------- -- #

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"


# -- ------------------------------------------------------------------------------ Mapa de calor de correlaciones -- #
# -- ------------------------------------------------------------------------------ ------------------------------ -- #

def g_heatmap_corr(p0_data):
    """
    :param p0_data: Data frame con los datos a graficar (valores numericos)
    :return: fig: figura para mostrar

    p0_data = pd.DataFrame({'Gasto': [0.43, 0.31, 0.32, 0.46, 1.25],
                            'Ingreso': [2.1, 1.1, 0.9, 0.6, 1.2],
                            'Tamaño': [1, 2, 5, 4, 5]})

    """

    # Inicializar un objeto tipo figura
    fig = go.Figure()

    fig.add_trace(go.Heatmap(z=p0_data.corr(method='pearson').values,
                             x=p0_data.columns, y=p0_data.columns,
                             colorbar=dict(title='Coeficiente <br> de pearson <br> <br>',
                                           xpad=1.8), colorscale='PuBu'))

    # actualizar layout
    fig.update_layout(title=dict(x=0.5, text='Matriz de correlación: <b> Todas las variables </b>'))

    # mostrar grafica
    # fig.show()

    return fig

# -- --------------------------------------------------------------------------- matrixz de graficas de dispersion -- #
# -- --------------------------------------------------------------------------- --------------------------------- -- #
# -- Matriz de graficas de dispersion


def g_matriz_disp(p0_data):
    """
    :param p0_data:
    :return:

    debugging
    p0_data = df_gasto
    """

    # Inicializar un objeto tipo figura
    # fig = go.Figure()

    # Agregar trazo de matriz de diagramas de dispersion
    # fig.add_trace(go.Splom(p0_data))

    fig = px.scatter_matrix(p0_data)

    return fig


# -- ---------------------------------------------------------------------------------- Boxplots de multivariables -- #
# -- ---------------------------------------------------------------------------------- -------------------------- -- #
# -- Matriz de graficas de dispersion

def g_boxplot_varios(p0_data):
    """
    :param p0_data:
    :return:

    debugging
    p0_data = df_gasto
    """

    x_data = list(p0_data.columns)
    y_data = [p0_data.iloc[:, i]/max(p0_data.iloc[:, i]) for i in range(0, len(list(p0_data.columns)))]

    fig = go.Figure()

    for xd, yd in zip(x_data, y_data):
        q1 = yd.quantile(0.25)
        q3 = yd.quantile(0.75)
        iqr = q3 - q1
        out_yd = list(yd[(yd < (q1 - 1.5 * iqr)) | (yd > (q3 + 1.5 * iqr))].index)

        fig.add_trace(go.Box(y=yd, name=xd, boxpoints='all', jitter=0.5, whiskerwidth=0.5, marker_size=7,
                             line_width=1, boxmean=True, selectedpoints=out_yd))

    fig.update_layout(title='Visualizacion de todas las variables (Normalizadas)',
                      yaxis=dict(autorange=True, showgrid=True, dtick=5,
                                 gridcolor='rgb(255, 255, 255)', gridwidth=1),
                      margin=dict(l=40, r=30, b=80, t=100),
                      showlegend=False)

    fig.update_yaxes(hoverformat='.2f')

    # Mostrar figura
    # fig.show()

    return fig
