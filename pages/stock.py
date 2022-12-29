import dash
from dash import dcc, html, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
import warnings
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utility.read_data import read_current_position, read_trading_data, read_ohlcv
from utility.charts import chart_ohlcv
from utility.process_data import calculate_table_dict

warnings.filterwarnings('ignore')
CHART_THEME = 'seaborn'
dash.register_page(__name__, path='/stock')

current_positions_df = read_current_position()
trading_df = read_trading_data()
table_dict = calculate_table_dict()

ticker_dict = [{'label': current_positions_df.company[i], 'value': current_positions_df.ticker[i]}
               for i in range(current_positions_df.shape[0])]
first_stock = current_positions_df.ticker[0]

stock_page = [
    dbc.Row(dbc.Col(html.H2('STOCK PRICE', className='text-center mb-3 p-3'))),
    dbc.Row([
        dbc.Col([
            html.H5('Candlestick chart', className='text-center'),
            dcc.Dropdown(
                id='ticker-selector',
                options=ticker_dict,
                value=first_stock,
                clearable=False,
            ),
            dcc.Graph(id='chrt-ticker-main',
                      figure=chart_ohlcv(ticker_name=first_stock),
                      style={'height': 920},
                      className='shadow-lg'),
            html.Hr(),

        ],
            width={'size': 9, 'offset': 0, 'order': 1}),
        dbc.Col([
            #             html.H5('Metrics', className='text-center'),
            dash_table.DataTable(id='first-table',
                                 columns=[],
                                 data=[],
                                 style_header={'display': 'none'},
                                 style_data={'whiteSpace': 'normal',
                                             'height': 'auto',
                                             'lineHeight': '15px',
                                             'border': 'none',
                                             'color': 'black'
                                             #                                                'textAlign': 'center'
                                             },
                                 style_cell_conditional=[
                                    {'if': {'column_id': 'indicator'},
                                     'width': '40%',
                                     'textAlign': 'left',
                                     'fontWeight': 'bold'
                                     },
                                 ]),
            html.Hr(),
            dash_table.DataTable(id='second-table',
                                 columns=[],
                                 data=[],
                                 style_header={'display': 'none'},
                                 style_data={'whiteSpace': 'normal',
                                             'height': 'auto',
                                             'lineHeight': '15px',
                                             'border': 'none',
                                             'color': 'black'
                                             #                                                'textAlign': 'center'
                                             },
                                 style_cell_conditional=[
                                     {
                                         'if': {'column_id': 'indicator'},
                                         'width': '40%',
                                         'textAlign': 'left',
                                         'fontWeight': 'bold'
                                     }]
                                 ),
            html.Hr(),
            dash_table.DataTable(id='third-table',
                                 columns=[],
                                 data=[],
                                 style_header={'display': 'none'},
                                 style_data={'whiteSpace': 'normal',
                                             'height': 'auto',
                                             'lineHeight': '15px',
                                             'border': 'none',
                                             'color': 'black'
                                             #                                                'textAlign': 'center'
                                             },
                                 style_cell_conditional=[
                                     {
                                         'if': {'column_id': 'indicator'},
                                         'width': '40%',
                                         'textAlign': 'left',
                                         'fontWeight': 'bold'
                                     }]
                                 ),
            html.Hr(),
        ],
            width={'size': 3, 'offset': 0, 'order': 2}),
    ])
]


@callback(
    [Output("chrt-ticker-main", "figure"),
     Output("first-table", "columns"), Output("first-table", "data"),
     Output("second-table", "columns"), Output("second-table", "data"),
     Output("third-table", "columns"), Output("third-table", "data")
     ],
    [Input("ticker-selector", "value")])
def render_tickerchart(value):
    t_candles = read_ohlcv(ticker_name=value)
    fig_main = make_subplots(rows=2, cols=1, shared_xaxes=True,
                             vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'),
                             row_width=[0.2, 0.7])

    # Plot OHLC on 1st row
    fig_main.add_trace(go.Candlestick(x=t_candles["date"], open=t_candles["open"], high=t_candles["high"],
                                      low=t_candles['low'], close=t_candles['close'], name="OHLC", showlegend=False),
                       row=1, col=1
                       )
    avg_price_df = current_positions_df.set_index('ticker')
    avg_price = avg_price_df.loc[value].avg_price
    res = round((avg_price_df.loc[value].price / avg_price - 1) * 100, 2)
    fig_main.update_layout(
        yaxis_title='Price $',
        shapes=[dict(
            x0=0, x1=1, y0=avg_price, y1=avg_price, xref='paper', yref='y', line_width=1)],
        annotations=[dict(
            x=0.05, y=avg_price * 0.90, xref='paper', yref='y',
            showarrow=False, xanchor='left', bgcolor="black",
            opacity=0.35, text='Average Price: $ {}<br>Result: {} %'.format(avg_price, res), font={'size': 12})]
    )

    # Bar trace for volumes on 2nd row without legend
    fig_main.add_trace(go.Bar(
        x=t_candles['date'], y=t_candles['volume'], showlegend=False), row=2, col=1)
    tx_df = trading_df[trading_df.ticker == value]
    fig_main.add_trace(go.Scatter(
        x=tx_df[tx_df.type == 'Buy'].date,
        y=tx_df[tx_df.type == 'Buy'].price,
        mode='markers',
        name='Buy Orders',
        marker=dict(
            color='rgba(200, 255, 75, 0.8)',
            size=12,
            line=dict(
                color='black',
                width=1
            )), showlegend=False))
    fig_main.add_trace(go.Scatter(
        x=tx_df[tx_df.type == 'Sell'].date,
        y=tx_df[tx_df.type == 'Sell'].price,
        mode='markers',
        name='Sell Orders',
        marker=dict(
            color='rgba(255, 20, 40, 0.9)',
            size=12,
            line=dict(
                color='red',
                width=1
            )), showlegend=False))

    # Do not show OHLC's rangeslider plot
    fig_main.update(layout_xaxis_rangeslider_visible=False)
    fig_main.update_layout(margin=dict(t=50, b=50, l=25, r=25))
    # fig_main.update_layout(paper_bgcolor="#272b30", plot_bgcolor='#272b30')
    fig_main.layout.template = CHART_THEME

    datatabletwo = table_dict[value][5:11].to_dict('records')
    datatable = table_dict[value].iloc[[0, 1, 2, 3, 34,
                                        35, 37, 31, 36, 39, 38, 33, 32],].to_dict('records')
    datatablethree = table_dict[value][18:25].to_dict('records')
    cols = [{"name": i, "id": i} for i in table_dict[value].columns]

    return fig_main, cols, datatable, cols, datatabletwo, cols, datatablethree


layout = stock_page
