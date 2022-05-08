import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# must add this line in order for the app to be deployed successfully on Heroku
# from app import server
from app import app
# import all pages in the app
from apps import entire, Europe, home

# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("Global", href="/entire"),
        dbc.DropdownMenuItem("Europe", href="/Europe"),
    ],
    nav = True,
    in_navbar = True,
    label = "Goto Page",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # code for initial column in the navigation bar
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/logo.jpg", height="100px",width="200px")),
                        dbc.Col(dbc.NavbarBrand("World Military Dashboard", className="ml-2")),
                    ],
                    align="center",
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/entire':
        return entire.layout
    elif pathname == '/Europe':
        return Europe.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(port = 8079, debug=True)