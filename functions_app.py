import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import folium_static
import folium
import io
from PIL import Image
import os
from ipywebrtc import WidgetStream, ImageRecorder
from ipywidgets.embed import embed_minimal_html
import branca


def get_data(file):
    
    return pd.read_csv(file)

def clean_col(col: pd.Series, replace = 'Unknown') -> pd.Series:
    
    """This function replaces NaN values by 'Unknown' (by default), and then capitalizes the first letter of each word. The specified column (a Series) thus has to be a string column."""
    
    return pd.Series(np.where(col.isna(), replace, col)).str.title()

def get_var(df, var) -> list:
    
    return sorted(list(df[var].unique()))

def popup_html(shape, duration, date):
    html = """<!DOCTYPE html>
    <html>
        <head>
            <style>
                p {{
                  background-color: #00a0a0;
                  padding: 10px 10px 10px 10px;
                  border: 2px solid #101357;
                  border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <p>
                <strong>Shape:</strong>&nbsp;{shape}
                <br>
                <strong>Duration:</strong>&nbsp;{duration}&nbsp;seconds
                <br>
                <strong>Date:</strong>&nbsp;{date}
            </p>
        </body>
    </html>""".format(**locals())
    return html

def create_map(df: pd.DataFrame) -> folium.Map():
    
    
    location = df['latitude'].mean(), df['longitude'].mean()
    m = folium.Map(location=location, zoom_start=4)
  
    for lat, lon, city, shape, duration, date in zip(
        df['latitude'],
        df['longitude'],
        df['city'],
        df['shape'],
        df['duration_seconds'],
        df['datetime']
    ):
        #Creating the tooltip
        tooltip = f"<strong>{city}</strong><br>"
        #Creating the popup
        html = popup_html(shape=shape, duration=duration, date=date)
        iframe = branca.element.IFrame(html=html)
        popup = folium.Popup(folium.Html(html, script=True), parse_html=True)
        #Creating "eye-open" icon, from Bootstrap (https://getbootstrap.com/docs/3.3/components/)
        icon = 'eye-open'
        #Creating the marker
        folium.Marker(
            #Coordinates of the country
            location = [lat, lon],
            #Popup that shows up if click the marker
            popup = popup,
            tooltip = tooltip,
            icon = folium.Icon(color='darkred', icon=icon)
        ).add_to(m)
        
    return m
      
def create_multiselect(df: pd.DataFrame, col: str) -> st.multiselect:
    return st.sidebar.multiselect(
        "",
        get_var(df, col),
        label_visibility="collapsed"
    )

def create_select_slider(df: pd.DataFrame, col: str, measure: str, select_range: list) -> st.select_slider:
    return st.sidebar.select_slider(
        f"Choose a {measure} range",
        options=select_range,
        value=(min(df[col].unique()),
               max(df[col].unique())),
        label_visibility="collapsed"
    )

#def map_to_png(folium_map, file: str):
    #return folium_map.save(file)

def UFOs_UI(df: pd.DataFrame):
    
    df_selected = df.copy()
    
    r1 = st.sidebar.radio("Country:", ["All Countries", "Select specific countries"])
    
    if r1 == "Select specific countries":
        countries = create_multiselect(df=df_selected, col="country")
        
        if countries is not None:
            df_selected = df_selected.query('(country in @countries)')
    
    r2 = st.sidebar.radio("City:", ["All Cities", "Select specific cities"])
    
    if r2 == "Select specific cities":
        cities = create_multiselect(df=df_selected, col="city")

        if cities is not None:
            df_selected = df_selected.query('(city in @cities)')

    r3 = st.sidebar.radio("UFO shape:", ["All Shapes", "Select specific shapes"])

    if r3 == "Select specific shapes":
        shapes = create_multiselect(df=df_selected, col="shape")

        if shapes is not None:
            df_selected = df_selected.query('(shape in @shapes)')

    select_range_duration = sorted(df_selected['duration_seconds'].unique())       
    r4 = st.sidebar.radio("Duration of the episode (in seconds):", ["All Durations", "Select a specific duration"])
    
    if r4 == "Select a specific duration":
        if min(df_selected['duration_seconds'].unique()) == max(df_selected['duration_seconds'].unique()):
            
            durations = st.sidebar.markdown(f"UFOs sightings reports based on your filters contains a single duration only **{set(df_selected['duration_seconds'])}**.")
            df_selected = df_selected.query("duration_seconds == @durations")

        else:
            start_duration, end_duration = create_select_slider(df=df_selected, col="duration_seconds", measure="duration", select_range=select_range_duration)
            df_selected = df_selected.query("@start_duration <= duration_seconds <= @end_duration")
    
    select_range_date = sorted(df_selected['year_UFO'].unique())
    r5 = st.sidebar.radio("Period:", ["All Time", "Select a specific period of time"])
    
    if r5 == "Select a specific period of time":
        if min(df_selected['year_UFO'].unique()) == max(df_selected['year_UFO'].unique()):
            
            date = st.sidebar.markdown(f"UFOs sightings reports based on your filters were made during a single year only **{set(df_selected['year_UFO'])}**.")
            df_selected = df_selected.query("year_UFO == @date")
            
        else:
            start_date, end_date = create_select_slider(df=df_selected, col="year_UFO", measure="date range", select_range=select_range_date)
            df_selected = df_selected.query("@start_date <= year_UFO <= @end_date")
            
    main_button = st.sidebar.button("Submit here 👈")
    if not main_button:       
        st.image("pictures/warning_ufo.jpeg", width = 500)

    if main_button:
        #st.balloons()
    
        with st.container():
            m=create_map(df=df_selected)
            folium_static(m)
            
            st.info('You can click on a marker to see more details about the corresponding UFO sighting report!', icon="ℹ️")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("And you, have you ever seen a UFO? 🧐" )
        with c2:
            st.image("pictures/et.jpeg", width = 100)
        
        
        #img_data = m._to_png(5)
        #img = Image.open(io.BytesIO(img_data))
        #img.save('image.png')
        #widget_stream = WidgetStream(widget=m, readout_format='')
        #image_recorder = ImageRecorder(stream=widget_stream)
        #display(image_recorder)

        st.download_button("Export Map", data=m, file_name=("map.html"))

        #if downlo:
            #with open('map.png', 'wb') as f:
                #f.write(image_recorder.image.value)
        #with open("flower.png", "rb") as file:
     
            #btn = st.download_button(
                #label="Download image",
                #data=file.write(image_recorder.image.value),
                #file_name="flower.png",
                #mime="image/png"
              #)
           
        #map_to_png(folium_map=m, file="map.png")
        #if export_as_png:
            #mapFname = "output.html"
            #m.save(os.path.join(os.getcwd(), mapFname))
            
        #st.write(f"{type(m)}")
        #text_contents = '''This is some text'''
        #st.download_button('Download some text', text_contents)
        #map_to_png(folium_map=m, file="map.png)
        
            #download_map(folium_map=m)
        
        df_selected = df
