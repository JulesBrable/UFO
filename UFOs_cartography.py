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

#def df_multiselect_query(df: pd.DataFrame) -> pd.DataFrame:

def UFOs_UI(df: pd.DataFrame):
    
    df_selected = df.copy()
    
    with header:
        st.header(f"Mapping of UFO sightings reports from {min(df['year_UFO'])} to {max(df['year_UFO'])}")

    r1 = st.sidebar.radio("Country:", ["All Countries", "Select specific countries"])
    if r1 == "Select specific countries":
        
        countries = st.sidebar.multiselect(
            "",
            get_var(df_selected,"country"),
            label_visibility="collapsed"
        )
        
        if countries is not None:
            
            df_selected = df_selected.query('(country in @countries)')
    
    r2 = st.sidebar.radio("City:", ["All Cities", "Select specific cities"])
    if r2 == "Select specific cities":
        
        cities = st.sidebar.multiselect(
            "",
            get_var(df_selected, "city"),
            label_visibility="collapsed"
        )
        
        if cities is not None:
            
            df_selected = df_selected.query('(city in @cities)')

    r3 = st.sidebar.radio("UFO shape:", ["All Shapes", "Select specific shapes"])
    if r3 == "Select specific shapes":
        
        shapes = st.sidebar.multiselect(
            "",
            get_var(df_selected, "shape"),
            key = "key1",
            label_visibility="collapsed"
        )
        
        if shapes is not None:
            
            df_selected = df_selected.query('(shape in @shapes)')

    select_range_duration = sorted(df_selected['duration_seconds'].unique())       
    r4 = st.sidebar.radio("Duration of the episode (in seconds):", ["All Durations", "Select a specific duration"])
    if r4 == "Select a specific duration":
        
        if min(df_selected['duration_seconds'].unique()) == max(df_selected['duration_seconds'].unique()):
            
            durations = st.sidebar.markdown(f"UFOs sightings reports based on your filters contains a single duration only **{set(df_selected['duration_seconds'])}**.")
            df_selected = df_selected.query("duration_seconds == @durations")

        else:
            start_duration, end_duration = st.sidebar.select_slider(
                "Choose a duration range",
                options=select_range_duration,
                value=(min(df_selected['duration_seconds'].unique()),
                       max(df_selected['duration_seconds'].unique())),
                label_visibility="collapsed"
            )
            df_selected = df_selected.query("@start_duration <= duration_seconds <= @end_duration")

        #durations = st.sidebar.multiselect(
            #"",
            #get_var(df_selected, "duration (seconds)"),
            #key = "key2",
            #label_visibility="collapsed"
        #)
        
        #if durations is not None:
            
            #df_selected = df_selected[df_selected.isin(durations)]
    
    select_range_date = sorted(df_selected['year_UFO'].unique())
    r5 = st.sidebar.radio("Period:", ["All Time", "Select a specific period of time"])
    if r5 == "Select a specific period of time":
        
        if min(df_selected['year_UFO'].unique()) == max(df_selected['year_UFO'].unique()):
            
            date = st.sidebar.markdown(f"UFOs sightings reports based on your filters were made during a single year only **{set(df_selected['year_UFO'])}**.")
            df_selected = df_selected.query("year_UFO == @date")
            
        else:
            start_date, end_date = st.sidebar.select_slider(
                "Choose a date range",
                options=select_range_date,
                value=(min(df_selected['year_UFO'].unique()),
                       max(df_selected['year_UFO'].unique())),
                label_visibility="collapsed"
            )
            
            df_selected = df_selected.query("@start_date <= year_UFO <= @end_date")


    if st.sidebar.button("Submit here 👈"):
        
        #st.balloons()
    
        with visualization:

            m = folium.Map()

            for lat, lon, name in zip(df_selected['latitude'],
                                      df_selected['longitude'],
                                      df_selected['city']):
                #Creating the marker
                folium.Marker(
                    #Coordinates of the country
                    location = [lat, lon],
                    #Popup that shows up if click the marker
                    popup = name
                ).add_to(m)
                
            folium_static(m)


        st.subheader("And you, have you ever seen a UFO? 🧐" )
        df_selected = df

if __name__ == '__main__':
    UFOs_UI(df = df)