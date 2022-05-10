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
df = pd.read_csv('cleaned.csv')
cols = list(df.columns)
loc_cols = list(df['continent'].unique())
from app import app
nuclear.sort_values(by=['total'],inplace = True,ascending=False)
nuclear['total'] = nuclear['total'].astype(str)
fig= px.choropleth(nuclear,locations="iso", color="total",hover_name="country",hover_data=['total','type'],color_continuous_scale='Viridis',labels={'total':'Nuclear Weapons'},title=' Nuclear powers in the world by 2022 (Wikipedia)',height=400)
fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

head = df.sort_values(['available_manpower'],ascending = False).head(10)
head.sort_values(['available_manpower'],ascending = False,inplace=True)
hist = px.histogram(head, y="available_manpower",x='country',title='  Top 10 countries in Man power by year 2022',height=400).update_yaxes(categoryorder='total descending')
hist.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

colors = {
    'background': '#e9eef5',
    'text': '#1c1cbd'
}

layout = html.Div(style={'backgroundColor': 'white'},children=[
    dbc.Container([
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            dbc.Col(html.H3("Nuclear Powers and Top countries with Manpower", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='nuclear',
                    figure=fig
                )
            ],style={'width': '49%', 'display': 'inline-block','backgroundColor':'gray','size':150}),
        html.Div([
            dcc.Graph(
                id='manpower',
                figure = hist
            )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block','backgroundColor':'gray'}),
        ])
        
    ]),
        dbc.Row([html.H2("Airports and populations filter by continent",className="text-center")])
        ,
    html.Div([
        html.Div([
            html.Label('Select Continent'),
            dcc.Dropdown(id='continents_dropdown',
                        options=[{'label': i, 'value': i}
                                for i in loc_cols],
                        value=loc_cols,
                        multi=True
            )
        ],style={'width': '47%', 'display': 'inline-block','margin-left':'2%'}),
        html.Div([
            html.Label('Select Variable to display on the Graphs'),
            dcc.Dropdown(id='features_dropdown',
                options=[                    
                    {'label': 'Airports', 'value': 'airport_totals'},
                    {'label': 'Man Power', 'value': 'available_manpower'},
                    {'label': 'Population', 'value': 'total_population'}],
                value='airport_totals',
            )
        ],style={'width': '47%', 'float': 'right', 'display': 'inline-block'}),
    ]),
    html.Div([
        dcc.Graph(
            id='barcharts'
        ),
        ],style={'width': '80%', 'margin-left': '10%','display': 'inline-block','size':100}),
])

@app.callback(
    Output(component_id='barcharts', component_property='figure'),
    [Input(component_id='continents_dropdown', component_property='value'),
    Input(component_id='features_dropdown', component_property='value'),])

def update_graphs(cont,val):
    if not (cont or val):
        return dash.no_update
    data = []
    for j in cont:
            data.append(df[df['continent'] == j])
    
    dc = pd.DataFrame(np.concatenate(data), columns=cols)
    dc = dc.infer_objects()
    
    dc.sort_values(by = val,ascending=False,inplace=True)
    top = dc.head(20)
    barfig = px.bar(top, y=val, x='country',
             text=val, color='country', 
             hover_data=['available_manpower','airport_totals','total_population'])
    barfig.update_traces(texttemplate='%{text:.2s}')
    #update text to be font size 8 and hide if text can not stay with the uniform size
    barfig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
        plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
        showlegend=False, margin=dict( b=200),xaxis_title="")    
    
    return barfig