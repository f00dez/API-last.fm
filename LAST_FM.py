import numpy as np
import pandas as pd

from time import sleep
from time import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from pprint import pprint

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sn
import folium
import jenkspy

from IPython.display import clear_output

import ast

top_artistas = pd.read_csv("ARTISTAS_TOP.csv")

df_paises = pd.read_csv("paises_geo.csv").iloc[16:]

top_artistas["SIMILARES"] = top_artistas["SIMILARES"].apply(lambda x : ast.literal_eval(x) if type(x) != type(np.nan) else x)
top_artistas["ETIQUETAS"] = top_artistas["ETIQUETAS"].apply(lambda x : ast.literal_eval(x) if type(x) != type(np.nan) else x)
top_artistas["CANCIONES TOP"] = top_artistas["CANCIONES TOP"].apply(lambda x : ast.literal_eval(x) if type(x) != type(np.nan) else x)
top_artistas["DISCOS TOP"] = top_artistas["DISCOS TOP"].apply(lambda x : ast.literal_eval(x) if type(x) != type(np.nan) else x)

paises = top_artistas["PAIS"].unique().tolist()

nan = np.nan

countries = ['United Kingdom', 'France', 'Canada', 'USA', nan, 'Australia', 'Ireland', 'Barbados', 'Spain', 'Colombia', 'Sweden', 'Germany', 'Jamaica', 'New Zealand', 'Iceland', 'Austria', 'Italy', 'Norway', 'Netherlands', 'Puerto Rico', 'Belgium', 'Denmark', 'Myanmar (Burma)', 'Argentina', 'Mexico', 'Cuba', 'Russian Federation', 'Greece', 'Uruguay', 'Trinidad and Tobago', 'Panama', 'South Africa', 'Brazil', 'Haiti', 'Japan', 'Czech Republic', 'Finland', 'Estonia', 'Peru', 'Chili', 'Romania', 'Swiss', 'Dominican Republic', 'Morocco', 'Israel', 'Nigeria', 'Costa Rica', 'Philippines', 'Lebanon', 'Mali', 'Slovenia', 'Poland', 'Lithuania', 'Albania']

traduccion = dict()

for i, j in zip(paises, countries):
    traduccion[i] = j

retraduccion= {'Myanmar (Burma)' : 'Myanmar', 
               'Russian Federation': 'Russia', 
               'Chili' : 'Chile', 
               'Swiss' : 'Switzerland', 
               'Türkiye' : 'Turkey', 
               'Bahamas' : 'The Bahamas', 
               'United Kingdom' : 'United Kingdom of Great Britain and Northern Ireland', 
               'USA' : 'United States of America'}

top_artistas['PAIS TRADUCCION'] = top_artistas["PAIS"].replace(traduccion)
top_artistas['PAIS TRADUCCION'] = top_artistas["PAIS TRADUCCION"].replace(retraduccion)

def intro(): ### MAPA MUNDIAL DE TODOS LOS ARTISTAS CON CLOROPLETH ###
        
    print("\033[1m¡BIENVENIDOS A LA BASE DE DATOS DE LAST FM!\033[0m")
    
    print("\033[1mMapa mundial con los artistas más escuchados del país:\033[0m")
    
    paises = pd.DataFrame(top_artistas["PAIS TRADUCCION"].value_counts()).reset_index()

    world_geo = "world_countries.json"

    world_map = folium.Map(location = [0, 0], zoom_start = 2, tiles = "CartoDB Dark_Matter")

    folium.Choropleth(geo_data     = "world_countries.json",
                      data         = paises,
                      columns      = ["index", 'PAIS TRADUCCION'],
                      key_on       = "feature.properties.name",
                      fill_color   = "BrBG", 
                      fill_opacity = 0.7, 
                      line_opacity = 0.2,
                      use_jenks    = True,
                      legend_name  = "ARTISTAS").add_to(world_map)

    display(world_map)
    
    print("\033[1mTop 50 artistas más escuchados en Last FM:\033[0m")
    
    top_100_artistas = top_artistas.sort_values("REPRODUCCIONES", ascending = False).iloc[:50]
    
    top_100_artistas = top_100_artistas.sort_values("ARTISTA", ascending = False)

    fig = px.scatter(data_frame  = top_100_artistas,
                     x           = "ARTISTA",
                     y           = "REPRODUCCIONES",
                     color       = "ARTISTA",
                     hover_name  = "ARTISTA",
                     opacity     = 0.5,
                     size        = "OYENTES",
                     template    = "plotly_dark")
    fig.show()
    
    sleep(3)

def data_management():

    top_artistas = pd.read_csv("ARTISTAS_TOP.csv")
    
    df_paises = pd.read_csv("paises_geo.csv").iloc[16:]

    top_artistas["SIMILARES"] = top_artistas["SIMILARES"].apply(lambda x : ast.literal_eval(x) if type(x) != type(np.nan) else x)
    top_artistas["ETIQUETAS"] = top_artistas["ETIQUETAS"].apply(lambda x : ast.literal_eval(x) if type(x) != type(np.nan) else x)
    top_artistas["CANCIONES TOP"] = top_artistas["CANCIONES TOP"].apply(lambda x : ast.literal_eval(x) if type(x) != type(np.nan) else x)
    top_artistas["DISCOS TOP"] = top_artistas["DISCOS TOP"].apply(lambda x : ast.literal_eval(x) if type(x) != type(np.nan) else x)
        
    paises = top_artistas["PAIS"].unique().tolist()

    nan = np.nan

    countries = ['United Kingdom', 'France', 'Canada', 'USA', nan, 'Australia', 'Ireland', 'Barbados', 'Spain', 'Colombia', 'Sweden', 'Germany', 'Jamaica', 'New Zealand', 'Iceland', 'Austria', 'Italy', 'Norway', 'Netherlands', 'Puerto Rico', 'Belgium', 'Denmark', 'Myanmar (Burma)', 'Argentina', 'Mexico', 'Cuba', 'Russian Federation', 'Greece', 'Uruguay', 'Trinidad and Tobago', 'Panama', 'South Africa', 'Brazil', 'Haiti', 'Japan', 'Czech Republic', 'Finland', 'Estonia', 'Peru', 'Chili', 'Romania', 'Swiss', 'Dominican Republic', 'Morocco', 'Israel', 'Nigeria', 'Costa Rica', 'Philippines', 'Lebanon', 'Mali', 'Slovenia', 'Poland', 'Lithuania', 'Albania']

    traduccion = dict()

    for i, j in zip(paises, countries):
        traduccion[i] = j

    retraduccion= {'Myanmar (Burma)' : 'Myanmar', 
                   'Russian Federation': 'Russia', 
                   'Chili' : 'Chile', 
                   'Swiss' : 'Switzerland', 
                   'Türkiye' : 'Turkey', 
                   'Bahamas' : 'The Bahamas', 
                   'United Kingdom' : 'United Kingdom of Great Britain and Northern Ireland', 
                   'USA' : 'United States of America'}

    top_artistas['PAIS TRADUCCION'] = top_artistas["PAIS"].replace(traduccion)
    top_artistas['PAIS TRADUCCION'] = top_artistas["PAIS TRADUCCION"].replace(retraduccion)
    
    return top_artistas, df_paises    
        

class InfoArtista:
    
    def __init__(self, name): ### INICIALIZAMOS ATRIBUTOS ###
        self.name = name.title()
        self.listeners = top_artistas["OYENTES"][top_artistas["ARTISTA"] == self.name].tolist()[0]
        self.bio = "".join(top_artistas["BIOGRAFIA"][top_artistas["ARTISTA"] == self.name].to_list())
        self.country = top_artistas["PAIS"][top_artistas["ARTISTA"] == self.name].tolist()[0]
        self.genre = ", ".join(top_artistas["ETIQUETAS"][top_artistas["ARTISTA"] == self.name].tolist()[0])
        self.similar = top_artistas["SIMILARES"][top_artistas["ARTISTA"] == self.name].tolist()[0]
        self.url = top_artistas["URL ARTISTA"][top_artistas["ARTISTA"] == self.name]
            
    def info_artist(self): ### BREVE INFORMACIÓN DEL ARTISTA ###
        print("Artista: ", self.name)
        print("Enlace: ", self.url)
        
        if type(self.country) == type(np.nan):
            print("País: No consta en la base de datos.") 
        else:
            print("País: ", self.country)
            
        world_map = folium.Map(location = [0, 0], 
                       zoom_start = 2, 
                       tiles = "CartoDB Dark_Matter")

        localizaciones = folium.map.FeatureGroup()

        for lat, lng, label in zip(df_paises["latitud"], df_paises["longitud"], df_paises["etiqueta"]):

            if top_artistas[top_artistas['ARTISTA'] == self.name]['PAIS'].tolist()[0] == label:
                localizaciones.add_child(folium.Marker(location = [lat, lng],
                                                       popup    = f"{label}", 
                                                       tooltip = f"Pais de procedencia: {self.country}"))
        world_map.add_child(localizaciones)
        display(world_map)
            
    def listeners_artist(self): ### OYENTES MENSUALES DEL ARTISTA ###
        print(f"Los oyentes mensuales de {self.name} son:", self.listeners)
        
    def bio_artist(self): ### BIOGRAFÍA COMPLETA DEL ARTISTA ###
        print(f"Biografía detallada de {self.name}: ", self.bio)
        
    def top_songs_artist(self): ### TOP 15 CANCIONES DEL ARTISTA ###
    
        grafica = pd.DataFrame()
        
        if len(top_artistas[top_artistas["ARTISTA"] == self.name]["CANCIONES TOP"].tolist()[0]) >= 15:
            lista_df = top_artistas["CANCIONES TOP"][top_artistas["ARTISTA"] == self.name].tolist()[0][0:15]
        else:
            lista_df = top_artistas["CANCIONES TOP"][top_artistas["ARTISTA"] == self.name].tolist()[0]

        dict_df = dict()

        for dic in lista_df:
            for key, value in dic.items():
                dict_df.setdefault(key, []).append(value)

        keys = dict_df["track"]
        values = dict_df["reproducciones"]

        grafica["track"] = keys
        grafica["reproducciones"] = values
        grafica["reproducciones"] = grafica["reproducciones"].astype('int32')


        fig = px.bar(data_frame = grafica,
                      y          = "track",
                      x          = "reproducciones",
                      hover_data = ["track"],
                      color      = "track",
                      orientation = 'h',
                      template = "plotly_dark")
        
        print(f"El top 15 canciones de {self.name} son:", ", ".join(dict_df["track"]))
        fig.show()
             
    def top_albums(self): ### TOP 5 ÁLBUMES(SI CONSTAN) DEL ARTISTA CON SUS RESPECTIVAS CANCIONES ###
        
        nan = np.nan

        lista_df = top_artistas["DISCOS TOP"][top_artistas["ARTISTA"] == self.name].tolist()[0]

        dict_df = dict()

        for dic in lista_df:
            for key, value in dic.items():
                dict_df.setdefault(key, []).append(value)
        
        print(f"El top álbumes de {self.name} son: ", ", ".join(dict_df["album"]))
        
        df = pd.DataFrame()

        albumes = []
        canciones = []
        duraciones = []

        for i in range(len(top_artistas["DISCOS TOP"][top_artistas["ARTISTA"] == self.name].tolist()[0])):
            for j in range(len(top_artistas["DISCOS TOP"][top_artistas["ARTISTA"] == self.name].tolist()[0][i]['tracks'])):
                
                album = top_artistas["DISCOS TOP"].iloc[top_artistas['ARTISTA'].tolist().index(self.name)][i]['album']
                
                if top_artistas["DISCOS TOP"][top_artistas["ARTISTA"] == self.name].tolist()[0][i]['tracks'][j]['titulo'] != '':
                    cancion = top_artistas["DISCOS TOP"][top_artistas["ARTISTA"] == self.name].tolist()[0][i]['tracks'][j]['titulo']
                else: 
                    cancion = top_artistas["DISCOS TOP"].iloc[top_artistas['ARTISTA'].tolist().index(self.name)][i]['album']
                
                if top_artistas["DISCOS TOP"][top_artistas["ARTISTA"] == self.name].tolist()[0][i]['tracks'][j]['duracion'] != '':
                    duracion = top_artistas["DISCOS TOP"][top_artistas["ARTISTA"] == self.name].tolist()[0][i]['tracks'][j]['duracion']
                else:
                    duracion = 3
                    
                albumes.append(album)
                canciones.append(cancion)
                duraciones.append(duracion)

        df['album'] = albumes
        df['cancion'] = canciones
        df['duracion'] = duraciones
        df['duracion'] = df['duracion'].replace("", np.nan)
        df['duracion'] = df['duracion'].astype('float')
        
        fig = px.treemap(data_frame = df,
           values     = "duracion",
           path       = ["album", "cancion"],
           hover_name = "cancion",
           color      = "album", 
           template   = "plotly_dark")

        fig.update_traces(marker=dict(cornerradius=5))
        fig.show()
        
    def genre_artist(self): ### GÉNEROS MUSICALES QUE ABARCA EL ARTISTA ###
        
        etiquetas = list()
        
        for i in range(len(top_artistas["DISCOS TOP"].iloc[top_artistas['ARTISTA'].tolist().index(self.name)])):
            for j in range(len(top_artistas["DISCOS TOP"].iloc[top_artistas['ARTISTA'].tolist().index(self.name)][i]['tags'])):

                etiqueta = top_artistas["DISCOS TOP"].iloc[top_artistas['ARTISTA'].tolist().index(self.name)][i]['tags'][j]

                etiquetas.append(etiqueta)

        etiqueta = pd.DataFrame()
        etiqueta['etiquetas'] = etiquetas

        etiqueta = pd.DataFrame({'Etiqueta': etiqueta['etiquetas'].value_counts().index, 'Frecuencia': etiqueta['etiquetas'].value_counts().values})

        fig = px.pie(data_frame = etiqueta,
                     names      = "Etiqueta",
                     values     = "Frecuencia",
                     hole       = 0.5, 
                     template   = "plotly_dark",
                     hover_name = "Etiqueta", 
                     title = f'Etiquetas relacionadas con {self.name}:')

        print(f"Los géneros que abarca/abarcan {self.name}:", self.genre)
        
        fig.show()
        
    def similar_artist(self): ### ARTISTAS RECOMENDADOS/SIMILARES AL ARTISTA ###
        if type(self.similar) == float:
            print(f"Artistas similares a {self.name} no constan en la base de datos.")
        else:
            print(f"Artistas similares a {self.name}:", ", ".join(self.similar))

def accion(infoartista, opcion): ### DEFINIMOS LAS ACCIONES SEGÚN LOS MÉTODOS CREADOS ###
    
    while opcion != "0":

        clear_output(wait = True)

        if opcion == "1":
            print("\n\033[1mINFORMACIÓN BREVE\033[0m\n")
            infoartista.info_artist()
            print("--"*60)
            print("\n\033[1mOYENTES\033[0m\n")
            infoartista.listeners_artist()
            print("--"*60)
            print("\n\033[1mBIOGRAFÍA\033[0m\n")
            infoartista.bio_artist()
            print("--"*60)
            print("\n\033[1mTOP 15 CANCIONES\033[0m\n")
            infoartista.top_songs_artist()
            print("--"*60)
            print("\n\033[1mGÉNEROS\033[0m\n")
            infoartista.genre_artist()
            print("--"*60)
            print("\n\033[1mARTISTAS SIMILARES\033[0m\n")
            infoartista.similar_artist()
            print("--"*60)
            print("\n\033[1mTOP ÁLBUMES\033[0m\n")
            infoartista.top_albums()
            print("--"*60)
            sleep(3)
        elif opcion == "2":
            clear_output(wait = True)
            artista = input("Ingrese el nombre de un artista: ")
            while artista.title() not in top_artistas["ARTISTA"].tolist():
                print(f"\n{artista} no se encuentra en la base de datos.\n")
                artista = input("Ingrese el nombre de un artista: ")
            infoartista = InfoArtista(artista)
        elif opcion not in "12":
            print("Opción no válida.")
                
        opcion = menu(infoartista)
        
    clear_output(wait = True)

    print("\033[1m¡Gracias por utilizar nuestro programa!\033[0m")

def menu(infoartista): ### HACEMOS LA INTERFAZ PARA EL USUARIO ###

    print("""
    Pulse 1: Información detallada del artista.
    Pulse 2: Cambiar de artista.
    Pulse 0: Terminar programa.
    """)
    opcion = input()
    return opcion

def last_fm():
    
    intro() 

    artista = input("Ingrese el nombre de un artista: ")
    
    while artista.title() not in top_artistas["ARTISTA"].tolist():
        print(f"\n{artista} no se encuentra en la base de datos.\n")
        artista = input("Ingrese el nombre de un artista: ")
    
    infoartista = InfoArtista(artista)
    
    accion(infoartista, opcion = menu(infoartista))