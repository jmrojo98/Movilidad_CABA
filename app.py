
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
import plotly.graph_objects as go

barrios_estaciones = pd.read_csv('https://raw.githubusercontent.com/jmrojo98/Movilidad_CABA/main/assets/barrios2.csv')
barrios_estaciones.drop('Unnamed: 0',axis=1,inplace=True)
todos=pd.read_csv('https://raw.githubusercontent.com/jmrojo98/Movilidad_CABA/main/assets/ubicacion_movilidad.csv',usecols=['lat','long','tipo'])
colores_transporte={'subte':'red', 'bicicleta':'yellow', 'colectivo':'orange', 'tren':'blue'}

mapa=folium.Map(location=[-34.603722,-58.381592],zoom_start=12,min_zoom=12)
Paradas_transportes=FeatureGroup(name='Paradas_transportes')


for i in range(0,todos.shape[0]):
  lat=todos.loc[i,'lat']
  lon=todos.loc[i,'long']
  color_tipo=colores_transporte[str(todos.loc[i,'tipo'])]
  folium.CircleMarker([lat,lon],radius=2,color=color_tipo).add_to(Paradas_transportes) 


Paradas_transportes.add_to(mapa)

LayerControl().add_to(mapa)
mapa.save('mapa_de_barrios.html')

fig = px.bar(barrios_estaciones, y="barrio", x=["colectivos","subte","trenes","bicis"], title="Wide-Form Input")


#App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)



#Layout
app.layout = html.Div([
    html.H1('Movilidad CABA',style={'text-align':'center'}), 
    html.P('Accesibilidad por barrio analizando paradas de transportes publicos: Subte - Tren - Colectivo - EcoBicis'),
    dcc.Tabs([
        dcc.Tab(id='Tab1', label='Mapa de paradas',  children=[
            html.Div([
                      dcc.Dropdown(id='drop_medios_transpote',options=[{'label':'Subtes','value':'subte'},
                                               {'label':'Colectivos','value':'colectivo'},
                                               {'label':'Trenes','value':'tren'},
                                               {'label':'Bicicletas','value':'bicicleta'}],
                                   multi=True,value=['subte','colectivo','tren','bicicleta']),
                      dcc.RadioItems(id='radio_1', #punto para marcar
                options=[
                    {'label':'Scatter','value':'scatter'},
                    {'label':'Heat','value':'heat'}]
                 ,value= 'scatter' #valor por defecto
                 ),  
    html.Br(),
    html.Div([
              html.Iframe(id='mapa',srcDoc= open('mapa_de_barrios.html','r').read(),width='100%',height='500'),
              
    ])
                    ])
                ]),
        dcc.Tab(id='Tab2', label='Paradas por barrio',  children=[
            html.Div([
                      dcc.Graph(figure=fig,)
                    ])
                ])
            ])
])

@app.callback(
    Output(component_id='mapa', component_property='srcDoc'),
    [Input(component_id='drop_medios_transpote', component_property='value'),
     Input(component_id='radio_1', component_property='value')]
)

def update_mapa(transporte_seleccionado,mapa_seleccionado):

  todos_dash=todos.loc[todos.tipo.isin(transporte_seleccionado)]
  todos_dash=todos_dash.reset_index()

  if mapa_seleccionado == 'heat':
    heat=folium.Map(location=[-34.603722,-58.381592],zoom_start=12,min_zoom=12)
    Heatmap=FeatureGroup(name='Heatmap')
    HeatMap(data=todos_dash[['lat', 'long']].groupby(['lat', 'long']).sum().reset_index().values.tolist(), radius=15, max_val=50,).add_to(Heatmap)
    Heatmap.add_to(heat)
    LayerControl().add_to(heat)
    
    heat.save('mapa_de_barrios.html')

  else:
    m=folium.Map(location=[-34.603722,-58.381592],zoom_start=12,min_zoom=12)
    Subtes=FeatureGroup(name='Subtes')

    for i in range(0,todos_dash.shape[0]):
      lat=todos_dash.loc[i,'lat']
      lon=todos_dash.loc[i,'long']
      color_tipo=colores_transporte[str(todos_dash.loc[i,'tipo'])]
      folium.CircleMarker([lat,lon],radius=2,color=color_tipo).add_to(Subtes) #Cada  capa necesita un ciclo para marcar todos los puntos

    Subtes.add_to(m)
    m.save('mapa_de_barrios.html')

  return open('mapa_de_barrios.html','r').read()


#Ejecutar
if __name__ == '__main__':
    app.run_server()


