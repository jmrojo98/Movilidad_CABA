import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

barrios_estaciones = pd.read_csv('https://raw.githubusercontent.com/jmrojo98/Movilidad_CABA/main/assets/barrios2.csv')
barrios_estaciones.drop('Unnamed: 0',axis=1,inplace=True)
todos=pd.read_csv('https://raw.githubusercontent.com/jmrojo98/Movilidad_CABA/main/assets/ubicacion_movilidad.csv',usecols=['lat','long','tipo'])
colores_transporte={'subte':'red', 'bicicleta':'yellow', 'colectivo':'orange', 'tren':'blue'}

colors = {
    'background': '#808080',
    'text': '#F8F8FF'
}
stylex={'color': colors['text'],'background-color':colors['background']}

fig = px.bar(barrios_estaciones, y="barrio", x=["colectivos","subte","trenes","bicis"], title="Wide-Form Input")


#App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)

theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

#Layout
app.layout = html.Div([
    html.H1('Movilidad CABA',style={'text-align':'center'}), 
    html.P('Accesibilidad por barrio analizando paradas de transportes publicos: Subte - Tren - Colectivo - EcoBicis'),
    dcc.Tabs([
        dcc.Tab(id='Tab1', label='Mapa de paradas',  children=[
            
            html.Div([
                      html.Br(),
                      html.H3('Medios de transporte',style={'text-align':'left'}),
                      dcc.Dropdown(id='drop_medios_transpote',options=[{'label':'Subtes','value':'subte'},
                                               {'label':'Colectivos','value':'colectivo'},
                                               {'label':'Trenes','value':'tren'},
                                               {'label':'Bicicletas','value':'bicicleta'}],
                                   multi=True,value=['subte','colectivo','tren','bicicleta']),
                      
                      html.H3('Tipo de Mapa',style={'text-align':'left'}),
                      dcc.RadioItems(id='radio_1', #punto para marcar
                options=[
                    {'label':'Scatter','value':'scatter'},
                    {'label':'Heat','value':'heat'}]
                 ,value= 'scatter' #valor por defecto
                 )
            ],className="three columns"),  

    html.Div([
              dcc.Graph(id='mapbox',config={'displayModeBar':False})
              
    ],className="nine columns")
                    ])
                ,
        dcc.Tab(id='Tab2', label='Paradas por barrio',  children=[
            html.Div([
                      dcc.Graph(figure=fig,)
                    ])
                ])
            ])
])

                          


@app.callback(
    Output(component_id='mapbox', component_property='figure'),
    [Input(component_id='drop_medios_transpote', component_property='value')]
)

def update_mapa(transporte_seleccionado):

  todos_dash=todos.loc[todos.tipo.isin(transporte_seleccionado)]
  todos_dash=todos_dash.reset_index()
    
  mapa=px.scatter_mapbox(todos,
                    lat='lat',
                    lon='long',  
                    mapbox_style='open-street-map',
                        zoom=11,width=950, height=650)
  mapa=px.scatter_mapbox(todos_dash,
                    lat='lat',
                    lon='long',  
                    mapbox_style='open-street-map',
                    color_discrete_map=colores_transporte,
                    color='tipo',
                  
                    zoom=11,
                    width=950, 
                    height=650).update_yaxes(automargin=True)

#.update_layout(template='plotly_dark')

  return mapa


#Ejecutar
if __name__ == '__main__':
    app.run_server()


