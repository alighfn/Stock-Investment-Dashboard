import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import warnings

from utility.charts import chart_sunburst_all

warnings.filterwarnings('ignore')
CHART_THEME = 'seaborn'
dash.register_page(__name__, path='/sunburst')

main_chart, current_ptfvalue = chart_sunburst_all()

sunburstpage = [
    dbc.Row(dbc.Col(html.H2('SUNBURST VIEW', className='text-center mb-3 p-3'))),
    dbc.Row([
        dbc.Col([
            html.H5('Explore your portfolio interactively',
                    className='text-left'),
            html.Div(
                children=f"Portfolio Value: {current_ptfvalue}", className='text-left'),
            html.Hr(),
            dcc.Graph(id='chrt-sunburstpage',
                      figure=main_chart,
                      style={'height': 800}),
            html.Hr(),

        ],
            width={'size': 12, 'offset': 0, 'order': 1}),
    ]),
]

layout = sunburstpage
