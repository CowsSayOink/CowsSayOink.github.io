import folium
import pandas as pd
import webbrowser
import gpxpy
import os
import xml.etree.ElementTree as ET


# create map and load the background tile
map = folium.Map(location=[44.035507,-35.930348], tiles=None, zoom_start=3)
folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}.png', name='Map', attr='Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community').add_to(map)

# city feature group
fg_city = folium.FeatureGroup(name='Travel').add_to(map)

# add legend in top right corner
map.add_child(folium.LayerControl(position='topright', collapsed=False, autoZIndex=True))


# add city locations
#import csv file

#travel = pd.read_csv(r"C:\Users\Lilly\Documents\venv\Travel - Sheet1.csv").to_dict(orient="records")
travel = pd.read_csv(r"C:\Users\felix\PycharmProjects\CowsSayOink.github.io\Python\Travel - Sheet1.csv").to_dict(orient="records")


# create marker and add it to biking feature group
for city in travel:
    folium_marker = folium.Marker(location=[city['Latitude'], city['Longitude']], tooltip=city['Name'], icon=folium.Icon(icon="",color='orange'))
    folium_marker.add_to(fg_city)


map.save('travel_map.html')
webbrowser.open('../travel_map.html')
