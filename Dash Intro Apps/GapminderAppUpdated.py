#import packages to create app
import dash
import dash_html_components as html
import dash_core_components as dcc
#from dash.dependencies import Input, Output

from gapminder import gapminder

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# Create figure to add to app
fig = px.scatter(data_frame=gapminder, x="gdpPercap", y="lifeExp",
                size="pop", color="continent",hover_name="country", 
               #add frame by year to create animation grouped by country
               animation_frame="year",animation_group="country",
               #specify formating of markers and axes
               log_x = True, size_max=60, range_x=[100,100000], range_y=[28,92],
                # change labels
                labels={'pop':'Population','year':'Year','continent':'Continent',
                        'country':'Country','lifeExp':'Life Expectancy','gdpPercap':"GDP/Capita"})
# Change the axis titles and add background colour using rgb syntax
fig.update_layout({'xaxis': {'title': {'text': 'log(GDP Per Capita)'}},
                  'yaxis': {'title': {'text': 'Life Expectancy'}}}, 
                  plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

# Create the dash app
app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#e9eef5',
    'text': '#1c1cbd'
}

markdown_text = '''
### Dash and Markdown
Just adding a lot of text here to explain the Dash markdown components 
'''


app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('Gapminder',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #Add multiple line text 
    html.Div('''
        Life Expectancy vs GDP per Capita for all Countries from 1952 to 2007 
    ''', style={
        'textAlign': 'center',
        'color': colors['text']}
    ),

    
    dcc.Markdown(children='''
    ### Dash Components to add Interactivitiy'''),
    html.Div([
        html.Div([
            html.Label('Dropdown'),
            dcc.Dropdown(
                options=[
                    {'label': 'All Continents', 'value': 'All'},
                    {'label': 'Asia', 'value': 'Asia'},
                    {'label': 'Europe', 'value': 'Eur'},
                    {'label': 'Africa', 'value': 'Afr'},
                    {'label': 'Americas', 'value': 'Ams'},
                    {'label': 'Oceania', 'value': 'Oce'}
                ],
                value='All', #sets the value the page opens on 
            ),
            html.Label('Dropdown with Multiple Choice'),
            dcc.Dropdown(
                options=[
                    {'label': 'Asia', 'value': 'Asia'},
                    {'label': 'Europe', 'value': 'Eur'},
                    {'label': 'Africa', 'value': 'Afr'},
                    {'label': 'Americas', 'value': 'Ams'},
                    {'label': 'Oceania', 'value': 'Oce'}
                ],
                value=['Asia','Eur','Afr','Ams','Oce'],
                multi=True,
            ),
            ],
            style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Radio Buttons'),
            dcc.RadioItems(            
                options=[
                    {'label': 'All Continents', 'value': 'All'},
                    {'label': 'Asia', 'value': 'Asia'},
                    {'label': 'Europe', 'value': 'Eur'},
                    {'label': 'Africa', 'value': 'Afr'},
                    {'label': 'Americas', 'value': 'Ams'},
                    {'label': 'Oceania', 'value': 'Oce'}
                ],
                value='All'
            ),
            html.Label('Checkboxes'),
            dcc.Checklist(
                options=[
                    {'label': 'Asia', 'value': 'Asia'},
                    {'label': 'Europe', 'value': 'Eur'},
                    {'label': 'Africa', 'value': 'Afr'},
                    {'label': 'Americas', 'value': 'Ams'},
                    {'label': 'Oceania', 'value': 'Oce'}
                ],
                value=['Asia','Eur','Afr','Ams','Oce']
            ),
        ], 
        style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        html.Label('Slider'),
        dcc.Slider(
        min=1952,
        max=2007,
        step=5,
        marks={i: 'Year {}'.format(i) for i in [1952,1957,1962,1967,1972,1977,1982,1987,1992,1997,2002,2007]},
        value=1952
        ),
        html.Label('Text Box'),
        dcc.Input(value='All', type='text'),
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'padding': '10px 5px'
    }),

    dcc.Graph(
        id='example-graph',
        figure=fig 
    )

])

if __name__ == '__main__':
    app.run_server(port=8092,debug=True)
