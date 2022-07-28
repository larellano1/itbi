import plotly.express as px
import numpy as np
import pandas as pd

from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output

import folium
import geopandas as gpd
from geopy.geocoders import Nominatim
from shapely.geometry import Point, Polygon

def get_location_point(address):
    geolocator = Nominatim(user_agent='app_test')
    try:
      location = geolocator.geocode(address)
      return Point(location.point[0:2])
    except AttributeError:
      print(f"Erro, endereco {address} ano encontrado.")
      return None

def acerta_df(df):
    df['endereco_completo'] = df['Número'].astype(str) + ", " + df['Nome do Logradouro'] + ", " + "SAO PAULO"
    df['geometry'] = df['endereco_completo'].apply(get_location_point)
    df = gpd.GeoDataFrame(df, geometry=df.geometry)
    return df

def baixa_dados():
    URL = "https://www.prefeitura.sp.gov.br/cidade/secretarias/upload/fazenda/arquivos/itbi/ITBI2022_maio.xlsx"
    df = pd.read_excel(URL)
    USO = 20
    df = df[df['Uso (IPTU)'] == USO]
    return df[0:10]

def carrega_dados_uso():
    df = baixa_dados()
    df = acerta_df(df)
    return df

def cria_mapa(df):
    arquivo_distritos_sp = 'distritosSP_gps.geojson'
    distritos = gpd.read_file(arquivo_distritos_sp)
    map = folium.Map(tiles = "OpenStreetMap", zoom_start = 10, location=[df.geometry.x[0],df.geometry.y[0]])
    feat_distritos = folium.features.GeoJson(distritos)
    feat_distritos.add_to(map)
    for i in range(len(df)):
        try:
            map.add_child(folium.Marker(location=[df.geometry.x[i],df.geometry.y[i]]))
        except:
            print("Unable to mark {}".format(df.iloc[i]['endereco_completo']))
        return map