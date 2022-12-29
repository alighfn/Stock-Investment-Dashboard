import pandas as pd
from dash import dash_table, html, dcc, Input, Output
import dash
import dash_bootstrap_components as dbc


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Dashboards", header=True),
                dbc.DropdownMenuItem("Overview", href="/overview"),
                dbc.DropdownMenuItem("Stock Price", href="/stock"),
                dbc.DropdownMenuItem("Portfolio", href="/sunburst"),
                dbc.DropdownMenuItem("Stock Table", href="/table"),
            ],
            nav=True,
            in_navbar=True,
            label="Dashboard Pages",
        ),
    ],
    brand="Stock Trading Dashboard v 1.0",
    brand_href="https://github.com/alighfn",
    color="primary",
    dark=True,
)

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.SKETCHY], use_pages=True, suppress_callback_exceptions=True)

app.layout = html.Div([
    navbar,
    dash.page_container,
])


if __name__ == "__main__":
    app.run_server(debug=True)
