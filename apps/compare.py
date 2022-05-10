#importing all the libraries needed for this layout
import dash
from dash import dcc
import time
import os
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
#reading csv
df = pd.read_csv('cleaned.csv')
#taking loc_cols to a list
loc_cols=list(df.columns)
from app import app
#taking unique column values
country_names = df['country'].unique()
colors = {
    'background': '#e9eef5',
    'text': '#1c1cbd'
}


layout = html.Div(style={'backgroundColor': 'white'},children=[
 #code for title
    html.H2('You can compare military strengths here',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),html.H4('Currently this app support comparision of 115 countries.',
        style={
            'textAlign': 'center',
            'color': colors['text']
        },
        #building a dropdown
    ),dbc.Row([
        html.Label('*You can select max 4 countries for better comparison :'),
        dcc.Dropdown(id='country_drop_down',
                       options=[{'label': i, 'value': i}
                                for i in country_names],
                       value=['United States','Russia'],
                        multi=True,
placeholder="Select 2 countries for comparison")
            
        ],style={'width': '45%', 'display': 'inline-block','float':'left','margin-left':'2%','backgroundColor':'rgb(233, 238, 245)'}),
       #code to recieve the map and display it
        dbc.Row([
            html.Div([
                dcc.Graph(
                    id='country_chart'
                ),
                ],style={'width': '100%','display': 'inline-block','backgroundColor':'white','height':'300px','margin-right':'2%'})
            ],style={'backgroundColor':'white'}),
       #code for receiving the table and display it
        html.Div([
            html.Div([
                html.A('The comparision Table:'),
                dcc.Graph(
                    id='table_comp'
                ),
                ],style={'width': '75%', 'margin-left': '12%','display': 'inline-block','backgroundColor':'white'}),
            ])
        
        ])
#this block takes input and gives updated graphs 1 input and 2 outputs
@app.callback([Output(component_id='country_chart', component_property='figure'),
               Output(component_id='table_comp', component_property='figure')],
              [Input(component_id='country_drop_down', component_property='value')])
#code to take input and update the data
def update_graphs(selected_count):
    #if no input then wait for input
    if len(selected_count) == 0:
        time.sleep(10)
        #only consider 1st 4 inputs because the limit is 4
    if len(selected_count) >= 5:
        selected_count = selected_count[0:4]
    data=[]
    #slicing the data according to input
    for j in selected_count:
            data.append(df[df['country'] == j])
    d = pd.DataFrame(np.concatenate(data),columns=loc_cols)
    d=d.infer_objects()
    #code for building map
    mapfig= px.choropleth(d,locations="iso",color='country',
            hover_name="country",hover_data=['total_population','available_manpower','airport_totals'],title='selected countries Geolocation',height=300)
    mapfig.update_layout(plot_bgcolor='white',paper_bgcolor='rgb(233, 238, 245)')
    mapfig.update_geos(fitbounds="locations")
    mapfig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    #code for building table
    tab = d.copy()
    tab.rename(columns= {'country':'Index'},inplace=True)
    tab.set_index(['Index'],inplace=True)
    tab = tab.transpose()
    tab.reset_index(inplace=True)
    tabfig =  ff.create_table(tab)
    #return the values
    return [mapfig, tabfig]