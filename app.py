
import pandas as pd
import numpy as np
import folium 
from folium import FeatureGroup, LayerControl, Map, Marker
from folium.plugins import HeatMap
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import dash_table
import plotly.express as px

#App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)


#Layout
app.layout = html.Div([
    html.H1('Movilidad CABA',className='twelve columns'),
    dcc.Dropdown(id='drop_medios_transpote',options=[{'label':'Subtes','value':'subte'},
                                               {'label':'Colectivos','value':'colectivo'},
                                               {'label':'Trenes','value':'tren'},
                                               {'label':'Bicicletas','value':'bicicleta'}],
                 multi=True,value=['subte','colectivo','tren','bicicleta']),
    html.Br()
  
])

@app.callback(
    Output(component_id='mapa', component_property='srcDoc'),
    [Input(component_id='drop_medios_transpote', component_property='value')]
)



#Ejecutar
if __name__ == '__main__':
    app.run_server()
