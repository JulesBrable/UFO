import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap

header = st.container()
visualization = st.container()

@st.cache(allow_output_mutation=True) # for improved performance in (re-)loading data
def get_data(file):
    
    return pd.read_csv(file)

df = get_data("data/ufo_sightings_clean.csv")

def clean_col(col: pd.Series, replace = 'Unknown') -> pd.Series:
    
    """This function replaces NaN values by 'Unknown' (by default), and then capitalizes the first letter of each word. The specified column (a Series) thus has to be a string column."""
    
    return pd.Series(np.where(col.isna(), replace, col)).str.title()

cols_list = ['country', 'city', 'shape']
df[cols_list] = df[cols_list].apply(clean_col)

def get_var(df, var) -> list:
    
    return sorted(list(df[var].unique()))

format='%Y-%m-%d %H:%M:%S'
df['year_UFO'] = pd.DatetimeIndex(pd.to_datetime(df['datetime'], format=format)).year
select_range = sorted(df['year_UFO'].unique())

#def df_multiselect_query(df: pd.DataFrame) -> pd.DataFrame:

def UFOs_UI(df: pd.DataFrame):
    
    with header:
        st.header(f"Mapping of UFO sightings reports from {min(df['year_UFO'])} to {max(df['year_UFO'])}")

    r1 = st.sidebar.radio("Country:", ["All Countries", "Select specific countries"])
    if r1 == "Select specific countries":
        
        countries = st.sidebar.multiselect("", get_var(df,"country"), label_visibility="collapsed")
        
        if countries is not None:
            
            df = df.query('(country in @countries)')
    
    r2 = st.sidebar.radio("City:", ["All Cities", "Select specific cities"])
    if r2 == "Select specific cities":
        
        cities = st.sidebar.multiselect("", get_var(df, "city"), label_visibility="collapsed")
        
        if cities is not None:
            
            df = df.query('(city in @cities)')

    r3 = st.sidebar.radio("UFO shape:", ["All Shapes", "Select specific shapes"])
    if r3 == "Select specific shapes":
        
        shapes = st.sidebar.multiselect("", get_var(df, "shape"), key = "key1", label_visibility="collapsed")
        
        if shapes is not None:
            
            df = df.query('(shape in @shapes)')

    r4 = st.sidebar.radio("Period:", ["All Time", "Select a specific period of time"])
    
    if r4 == "Select a specific period of time":
        
        if min(df['year_UFO'].unique()) == max(df['year_UFO'].unique()):
            
            date = st.sidebar.markdown(f"UFOs sightings reports based on your filters were made during a single year only **{set(df['year_UFO'])}**.")
            
        else:
            start_date, end_date = st.sidebar.select_slider("Choose a date range",
                                                            options=select_range,
                                                            value=(min(df['year_UFO'].unique()),
                                                                   max(df['year_UFO'].unique())),
                                                           label_visibility="collapsed")

    if st.sidebar.button("Submit here 👈"):
        
        st.balloons()
    
        with visualization:

            m = folium.Map()

            for lat, lon, name in zip(df['latitude'],
                                      df['longitude'],
                                      df['city']):
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