import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

HOMEPAGE_STYLE = {
    'textAlign': 'center',
    'margin': '10% auto',
}

homepage = html.Div([
    html.H1('Welcome to Stock Trading Dashboard'),
    html.Br(),
    html.H2('The dashboard has been developed by:'),
    html.H3(html.A('Ali Ghaffarinejad', href='https://github.com/alighfn')),
    html.Br(),
    dcc.Link('Enter Dashboard', href='/overview', className='btn btn-primary')
], style=HOMEPAGE_STYLE)

layout = homepage
