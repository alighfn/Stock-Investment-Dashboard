import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import warnings

from utility.charts import chart_portfolio_value, chart_sunburst_all, chart_portfolio_kpi
from utility.charts import chart_sp500_kpi, chart_drawdown, chart_cashflow, chart_sunburst_small

warnings.filterwarnings('ignore')
dash.register_page(__name__, path='/overview')

sunburst_all_chart, current_ptfvalue = chart_sunburst_all()

overview = [
    dbc.Row(dbc.Col(html.H2('PORTFOLIO OVERVIEW', className='text-center mb-3 p-3'))),
    dbc.Row([
        dbc.Col([
            html.H5('Portfolio Value vs Net Invested ($USD)',
                    className='text-center'),
            html.Div(
                children=f"Portfolio Value: {current_ptfvalue}", className='text-left mb-2'),
            dcc.Graph(id='chrt-portfolio-main',
                      figure=chart_portfolio_value(),
                      style={'height': 450},
                      className='shadow-lg'
                      ),
            html.Hr(),

        ],
            width={'size': 8, 'offset': 0, 'order': 1}),
        dbc.Col([
                html.H5('Portfolio', className='text-center'),
                html.Div(children="KPI's", className='text-center fs-4'),
                dcc.Graph(id='indicators-ptf',
                          figure=chart_portfolio_kpi(),
                          style={'height': 450},
                          className='shadow-lg'),
                html.Hr()
                ],
                width={'size': 2, 'offset': 0, 'order': 2}),
        dbc.Col([
                html.H5('S&P500', className='text-center'),
                html.Div(children="KPI's", className='text-center fs-4'),
                dcc.Graph(id='indicators-sp',
                          figure=chart_sp500_kpi(),
                          style={'height': 450},
                          className='shadow-lg'),
                html.Hr()
                ],
                width={'size': 2, 'offset': 0, 'order': 3}),
    ]),  # end of second row
    dbc.Row([
            dbc.Col([
                dcc.Graph(id='chrt-portfolio-secondary',
                          figure=chart_drawdown(),
                          style={'height': 300},
                          className='shadow-lg'),
                html.Hr(),
                dcc.Graph(id='chrt-portfolio-third',
                          figure=chart_cashflow(),
                          style={'height': 300},
                          className='shadow-lg'),
            ],
                width={'size': 8, 'offset': 0, 'order': 1}),
            dbc.Col([
                dcc.Graph(id='pie-top15',
                          figure=chart_sunburst_small(),
                          style={'height': 630},
                          className='shadow-lg'),
            ],
                width={'size': 4, 'offset': 0, 'order': 2}),
            ])

]

layout = overview
