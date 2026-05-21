import folium
import pandas as pd
import webbrowser
import gpxpy
import os
import xml.etree.ElementTree as ET


# create map and load the background tile
map = folium.Map(location=[49.4891,8.46694], tiles=None, zoom_start=6)
folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}.png', name='Map', attr='Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community').add_to(map)

# add feature groups
fg_bike = folium.FeatureGroup(name='Biking').add_to(map)
fg_hike = folium.FeatureGroup(name='Hiking').add_to(map)
fg_run = folium.FeatureGroup(name='Running').add_to(map)


# add legend in top right corner
map.add_child(folium.LayerControl(position='topright', collapsed=False, autoZIndex=True))

# import gpx traces
gpx_folder = r"C:\Users\Lilly\Documents\venv\gpx"


for gpx_file in os.listdir(gpx_folder):
    file = os.path.join(gpx_folder,gpx_file)
    
    gpx = gpxpy.parse(open(file))
    track = gpx.tracks[0]
    segment = track.segments[0]

    # load coordinate points
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            step = 10
            for point in segment.points[::step]:
                points.append(tuple([point.latitude, point.longitude]))

    # Select colour and group

    tree = ET.parse(file)
    root = tree.getroot()
    namespace = {'ns': 'http://www.topografix.com/GPX/1/1'}
    value = root.findall('ns:trk', namespace)
    sport = value[0].find('ns:type', namespace).text
   
    colour_dict = {'cycling': 'red', 'walking': 'blue', 'hiking': 'blue', 'running': 'purple'}
    group_dict = {'cycling': fg_bike, 'walking': fg_hike, 'hiking': fg_hike, "running": fg_run}
    
    # add segments to the map
    folium_gpx = folium.PolyLine(points, color=colour_dict[sport], weight=3, opacity=0.85).add_to(map)

    # add the gpx trace to our marathon group
    folium_gpx.add_to(group_dict[sport])



map.save('adventures_map.html')
webbrowser.open('../adventures_map.html')
