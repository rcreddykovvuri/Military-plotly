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
#for results please change the path
os.chdir('D://DKIT//sem2//data_visualisation//dash//assignment2//MultipageApp//datasets//')
df = pd.read_csv('cleaned.csv')
loc_cols=list(df.columns)
from app import app
country_names = df['country'].unique()
colors = {
    'background': '#e9eef5',
    'text': '#1c1cbd'
}


layout = html.Div(style={'backgroundColor': 'white'},children=[
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
    ),dbc.Row([
        html.Label('*For better comparison you can select max 4 countries:'),
        dcc.Dropdown(id='country_drop_down',
                       options=[{'label': i, 'value': i}
                                for i in country_names],
                       value=['United States','Russia'],
                        multi=True,
placeholder="Select 2 countries for comparison")
            
        ],style={'width': '45%', 'display': 'inline-block','float':'left','margin-left':'2%','backgroundColor':'rgb(233, 238, 245)'}),
        dbc.Row([
            html.Div([
                dcc.Graph(
                    id='country_chart'
                ),
                ],style={'width': '100%','display': 'inline-block','backgroundColor':'white','height':'300px','margin-right':'2%'})
            ],style={'backgroundColor':'white'}),
        html.Div([
            html.Div([
                html.A('The comparision Table:'),
                dcc.Graph(
                    id='table_comp'
                ),
                ],style={'width': '75%', 'margin-left': '12%','display': 'inline-block','backgroundColor':'white'}),
            ])
        
        ])

@app.callback([Output(component_id='country_chart', component_property='figure'),
               Output(component_id='table_comp', component_property='figure')],
              [Input(component_id='country_drop_down', component_property='value')])

def update_graphs(selected_count):
    if len(selected_count) == 0:
        time.sleep(10)
    if len(selected_count) >= 5:
        selected_count = selected_count[0:4]
    data=[]
    for j in selected_count:
            data.append(df[df['country'] == j])
    d = pd.DataFrame(np.concatenate(data),columns=loc_cols)
    d=d.infer_objects()
    
    mapfig= px.choropleth(d,locations="iso",color='country',
            hover_name="country",hover_data=['total_population','available_manpower','airport_totals'],title='selected countries Geolocation',height=300)
    mapfig.update_layout(plot_bgcolor='white',paper_bgcolor='rgb(233, 238, 245)')
    mapfig.update_geos(fitbounds="locations")
    mapfig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    tab = d.copy()
    tab.rename(columns= {'country':'Index'},inplace=True)
    tab.set_index(['Index'],inplace=True)
    tab = tab.transpose()
    tab.reset_index(inplace=True)
    tabfig =  ff.create_table(tab)
    
    return [mapfig, tabfig]