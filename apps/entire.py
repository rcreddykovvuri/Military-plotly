import dash
from dash import dcc
import os
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
#for results please change the path
os.chdir('D://DKIT//sem2//data_visualisation//dash//assignment2//MultipageApp//datasets//')
nuclear = pd.read_csv('nuclear.csv')
from app import app
nuclear.sort_values(by=['total'],inplace = True,ascending=False)
nuclear['total'] = nuclear['total'].astype(str)
fig= px.choropleth(nuclear,locations="iso", color="total",hover_name="country",hover_data=['total','type'],color_continuous_scale='Viridis',labels={'total':'Nuclear Weapons'},title='Nuclear powers in the world by 2022 (Wikipedia)',height=400)
fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

colors = {
    'background': '#e9eef5',
    'text': '#1c1cbd'
}

layout = html.Div(style={'backgroundColor': 'white'},children=[
    dbc.Container([
        html.Div([
            html.Div([
                dcc.Graph(
                    id='LifeExp',
                    figure=fig
                )
            ],style={'width': '49%', 'display': 'inline-block','backgroundColor':'gray','size':150}),
        ])
        
    ])
])
