import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap

header = st.container()
visualization = st.container()

@st.cache # for improved performance in (re-)loading data
def get_data(file):
    
    return pd.read_csv(file)

df = get_data("data/ufo_sightings_clean.csv")

def get_shape(df, var):
    
    return list(df[var].unique())

def get_city(df, var):
    
    return list(df[var].unique())

def UFOs_UI(df: pd.DataFrame):
    
    with header:
        st.header("Mapping of UFO sightings reports from 1940 to 2014")

    #country = st.sidebar.selectbox('Country',get_country(cat,"Country"))
    list_city = st.sidebar.selectbox("City", get_city(df, "city"))
    list_shape = st.sidebar.selectbox("UFO shape", get_shape(df, "shape"))
    
    df_selected = df.query('city in @list_city and shape in @list_shape')

    if st.sidebar.button("Submit here 👈"):
        
        st.balloons()
    
        with visualization:

            m = folium.Map()

            for lat, lon, name in zip(df_selected['latitude'],
                                      df_selected['longitude'],
                                      df_selected['city']):
                #Creating the marker
                folium.Marker(
                    #Coordinate of the country$
                    location = [lat, lon],
                    #The popup that show up if click the marker
                    popup = name
                ).add_to(m)
                #heat_data = [df['latitude'],df['longitude']]
                #HeatMap(heat_data).add_to(m)
                
            folium_static(m)


        st.subheader("And you, have you ever seen a UFO? 🧐" )

if __name__ == '__main__':
    UFOs_UI(df = df)