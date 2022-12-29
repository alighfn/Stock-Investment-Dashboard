import dash
from dash import html, dash_table
import dash_bootstrap_components as dbc
import warnings

from utility.process_data import calculate_datatable

warnings.filterwarnings('ignore')
CHART_THEME = 'seaborn'
dash.register_page(__name__, path='/table')

datatabletotal, cols_total = calculate_datatable()
tableview_table = dash_table.DataTable(
    id='total-table',
    columns=cols_total,
    data=datatabletotal,
    filter_action="native",
    sort_action="native",
    fixed_columns={
        'headers': True,
        'data': 2
    },
    style_table={
        'minWidth': '100%',
        'overflowX': 'auto'
    },
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(80, 80, 80)',
        },
        {
            'if': {'column_id': 'Ticker'},
            'width': '25px',
            'textAlign': 'left',
            'fontWeight': 'bold'
        },
        {
            'if': {'column_id': 'Company'},
            'width': '140px',
            'textAlign': 'left',
        }
    ],
)

# Tables
tablepage = [
    dbc.Row(dbc.Col(html.H2('FULL TABLE VIEW', className='text-center mb-3 p-3'))),
    dbc.Row([
        dbc.Col([
            html.H5('Detailed view about every stock', className='text-left'),
            html.Hr(),
            tableview_table,
            html.Hr(),

        ],
            width={'size': 12, 'offset': 0, 'order': 1}),
    ]),
]

layout = tablepage
