#getting all the needed libraries
import dash
from dash import html
import dash_bootstrap_components as dbc

from app import app

# change to app.layout if running as single page app instead
layout = html.Div([
    #giving titles and content
    dbc.Container([
        dbc.Row([
            
            dbc.Col(html.H1("Welcome to the World Military dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='This app shows military strength of 115 countries and change in trends of more than 150 countries from 2005 to 2016. This is designed with the available information.'
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='Do you know, according to tradingeconomics.com: total armed forces personnel in the world on 2019 is 27.67 Million. Every country says about peace but they still invest and expand their military every year.')
                    , className="mb-5")
        ]),

        dbc.Row([
            #this code is for getting 2 blocks
            # code for block 1 
            dbc.Col(dbc.Card(children=[html.H3(children='Go to the original datasets for more information. Data is from many sources.',
                                               className="text-center"),
             #code for dropdown menu
                                       dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("2021 Army", href="https://www.kaggle.com/datasets/sleymanzeynul/military-strengths-of-countries-2021"),
        dbc.DropdownMenuItem("1990 to 2016", href="https://correlatesofwar.org/data-sets/national-material-capabilities"),
        dbc.DropdownMenuItem("Nuclear data", href="https://en.wikipedia.org/wiki/List_of_states_with_nuclear_weapons"),
        dbc.DropdownMenuItem("Images", href="https://pixabay.com/"),
    ],
    nav = True,
    in_navbar = True,
    style={'width':'30%','backgroundColor':'gray','height':'36px','float':'right','textColor':'white'},
    label = "Data Sources",
),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),
#code for 2nd block and button inside it
            dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
                                               className="text-center"),dbc.Button("GitHub",
                                                  href="https://github.com/rcreddykovvuri/Milatary-plotly.git",
                                                  style={'backgroundColor':'gray','float':'right'},
                                                  className="mt-3"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),

        ], className="mb-5"),
        #code for report used to display and its hyperlink
          html.Label(['According to statista.com - These are top 10 powerful countries as of 2022. For more details ', html.A("click here",href="https://www.statista.com/chart/20418/most-powerful-militaries/")]),
          html.A(
              # Use row and col to control vertical alignment of analysis brand
              dbc.Row(
                  [
                      dbc.Col(html.Img(src="/assets/20418.jpeg",width="300px",height="300px")),
                 ],
              style={'textAlign':'center'},)
          ),
    #code for ending slide
        dbc.Container([
                html.A(
                    # adding a row in the end to tell about developer
                    dbc.Row(
                        [
                            html.A(['This is developed only for educational purposes, not for any commercial use. For details contact rcreddy.kovvuri@gmail.com'])
                            ,
                        ],
                        
                
                    ),
                ),],style={'textAlign':'center','backgroundColor':'black','color': 'white','width':'150%'},)
        

    ])

])