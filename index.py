#loading all the needed libraries
import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# must add this line in order for the app to be deployed successfully on Heroku
# from app import server
from app import app
# import all pages in the app
from apps import world,home,compare,trends
server = app.server
# building the navigation bar
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("Powerful Nations", href="/world"),
        dbc.DropdownMenuItem("Trends(2005-2015)", href="/trends"),
        dbc.DropdownMenuItem("Compare", href="/compare"),
        
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
                        dbc.Col(html.Img(src="/assets/main_logo.png", height="80px",width="200px")),
                        dbc.Col(dbc.NavbarBrand("World Military Dashboard", className="ml-2")),
                        
                    ],
                    align="center",
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align for dropdown
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

#for dynamic functionality of the code
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/world':
        return world.layout
    elif pathname == '/compare':
        return compare.layout
    elif pathname == '/trends':
        return trends.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(port = 8079, debug=True)