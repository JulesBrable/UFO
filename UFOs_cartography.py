import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static
import folium
from functions_app import get_data, clean_col, UFOs_UI
import branca

if __name__ == '__main__':
    
    st.set_page_config(
        page_title="UFOs Sightings Reports Map",
        page_icon="🛸", # this icon appears on the tab of the web page
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'Report a bug': "https://github.com/JulesBrable/UFO/issues/new",
            'About': """ 
            If you want to read more about the project, you would be interested in going to the corresponding
            [GitHub](https://github.com/JulesBrable/UFO) repository.
            
            Contributions:
            - [Jules Brablé⛑](linkedin.com/in/jbrable)
            - [Antonio Sasaki👑](https://www.linkedin.com/in/antoniosasaki)
            - Oumar Dione🎩
            We also want to thank our teachers of Python's class, L.Galiana and C.Laroche.
            
            The underlying data comes from a [public website](https://www.mavenanalytics.io/data-playground).
            """
        }
    ) 
    
    #@st.cache(allow_output_mutation=True) # for improved performance in (re-)loading data
    df = get_data("data/ufo_sightings_clean.csv")
    
    cols_list = ['country', 'city', 'shape', 'state']
    df[cols_list] = df[cols_list].apply(clean_col)
    
    df['year_UFO'] = pd.DatetimeIndex(df['datetime']).year
    
    st.sidebar.subheader(f"Please filter the desired features:")
        
    with st.container():
        st.header(
            f"Mapping of UFO sightings reports from {min(df['year_UFO'])} to {max(df['year_UFO'])}"
        )

    UFOs_UI(df=df)