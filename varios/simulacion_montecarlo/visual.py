

import plotly.graph_objects as go
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

    fig.add_trace(go.Heatmap(z=p0_data.corr(method='pearson').as_matrix(),
                             x=p0_data.columns, y=p0_data.columns,
                             colorbar=dict(title='Coeficiente <br> de pearson <br> <br>',
                                           xpad=1.8), colorscale='PuBu'))

    # actualizar layout
    fig.update_layout(title=dict(x=0.5, text='Matriz de correlación: <b> Todas las variables </b>'))

    # mostrar grafica
    # fig.show()

    return fig
