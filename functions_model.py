import pandas as pd
import folium

def map_kmeans(df, col_state: str = "state", col_km: str = "group"):
    
    """Plot on a map the KMeans labels defined by our model"""
    
    # we get geojson in order to have the borders of the US states
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    state_geo = f'{url}/us-states.json'
    
    # init the map
    m = folium.Map(location=[48, -102], zoom_start=3)

    # we need to upper the first letter of each state name
    #in order to match the state name from those of the geojson
    df["state"] = df['state'].str.capitalize()
    
    # adding a layer to the map with choropleth (here the layer is the KMeans label for each US state)
    folium.Choropleth(
        geo_data=state_geo, # geojson
        name='choropleth',
        data=df,
        columns=[col_state, col_km], # columns we need to display on the map
        key_on='feature.properties.name', # where we can find the name of the states in the geojson
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='KMeans Label'
    ).add_to(m)
    
    return m
