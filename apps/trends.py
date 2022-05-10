import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import os
os.chdir('D://DKIT//sem2//data_visualisation//dash//assignment2//MultipageApp//datasets//')
trends = pd.read_csv('trend.csv')


cont_names = trends['continent'].unique()
cols=list(trends.columns)
#data for the region plot
colors = {
    #background to rgb(233, 238, 245)
    'background': '#e9eef5',
    'text': '#1c1cbd'
}

from app import app


color_discrete_map = {'Asia': 'red', 'Africa': 'blue', 'South America': 'green','Europe': 'cyan','North America':'purple','Oceania': 'indigo'}

layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('Trends in military from 2005 to 2016',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div([
        html.Div([
            
            html.Label('Select Continent/Continents:'),

            dcc.Dropdown(id='cont_bub',
                        options=[{'label': i, 'value': i}
                                for i in cont_names],
                        value=['Asia','Europe','Africa','South America','Oceania','North America'],
                        multi=True
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Select Population Range'),
                dcc.RangeSlider(id='popul',
                    min=7000000,
                    max=1403500000,
                    value=[7000000,1403500000],
                    step= 1,
                    marks={
                        7000000: '7M',
                        250000000: '250M',
                        500000000: '500M',
                        750000000:'750M',
                        1000000000:'1B',
                        1403500000: '1.4B'
                    }
                    
                )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ]),
    dcc.Graph(
        
        id='population'
    ),
    html.Label('Select Variable to display on Graphs'),
        dcc.Dropdown(id='multi_select',
                     
            options=[                    
                {'label': 'Military Expenditure', 'value': 'military_exp'},
                {'label': 'Military Personnnel', 'value': 'military_personnel'},
                {'label': 'Total Population', 'value': 'total_population'}],
            value='military_exp',
            style={'width':'50%'}
    ),
    html.Div([
        html.Div([
            dcc.Graph(
                id='multi_graph'
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='lines_graph',
            )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ])

])


@app.callback(
    Output(component_id='population', component_property='figure'),
    [Input(component_id='cont_bub', component_property='value'),
    Input(component_id='popul', component_property='value')]
)

def update_graph(cont_bub,popul):
    if not cont_bub:
        return dash.no_update
    data =[]
    d = trends[(trends['total_population'] >= popul[0]) & (trends['total_population'] <= popul[1])]
    for j in cont_bub:
            data.append(d[d['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    scat_fig = px.scatter(data_frame=df, x="total_population", y="military_personnel",
                color="continent",hover_name="country",size='total_population',
                # different colour for each country
                color_discrete_map=color_discrete_map, 
               #add frame by year to create animation grouped by country
               animation_frame="year",animation_group="country",
               #specify formating of markers and axes
               log_x = True, size_max=60,range_x=[6000000,1700000000])
    # Change the axis titles and add background colour using rgb syntax
    scat_fig.update_layout({'xaxis': {'title': {'text': 'Total Population'}},
                  'yaxis': {'title': {'text': 'Military Personnal'}}}, 
                  plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    return scat_fig

@app.callback(
    [Output(component_id='multi_graph', component_property='figure'),
    Output(component_id='lines_graph', component_property='figure')],
    [Input(component_id='cont_bub', component_property='value'),
    Input(component_id='popul', component_property='value'),
    Input(component_id='multi_select', component_property='value')]
)
def update_map(cont,value,col):
    if not (cont or value or col):
        return dash.no_update
    d = trends[(trends['total_population'] >= value[0]) & (trends['total_population'] <= value[1])]
    data =[]
    for j in cont:
            data.append(d[d['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    map_fig= px.choropleth(df,locations="iso", color=df[col],
            hover_name="country",hover_data=['continent','total_population'],animation_frame="year",    
            color_continuous_scale='Turbo',range_color=[df[col].min(), df[col].max()],
            labels={'total_population':'Population','year':'Year','continent':'Continent',
                'country':'Country','military_expenditure':'Defence_budjet','military_personnel':'Personnel'})
    map_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    line_fig = px.line(data_frame=df, 
                x="year",  y = df[col] , color='continent',line_group="country", 
                hover_data=['total_population','year'],
                  hover_name='country',color_discrete_map=color_discrete_map,
                 # change labels
                 labels={'total_population':'Population','year':'Year','continent':'Continent',
                     'country':'Country','military_expenditure':'Defence_budjet','military_personnel':'Personnel'})
    line_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',
        paper_bgcolor='rgb(233, 238, 245)')
        
    return [map_fig, line_fig]