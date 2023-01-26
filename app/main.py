import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import folium_static
import folium
from st_utils import get_data, get_var, clean_col, create_multiselect, create_select_slider, create_radio_feature, popup_html, create_map, hist_chart
from wordcloud import ImageColorGenerator
from PIL import Image
import io
import sys
sys.path.append('../')
from UFO.scripts.viz import mywc, display_wc



def UFOs_UI(df: pd.DataFrame):
    
    # creation of different tabs for the different corresponding sections
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Information", "Data Visualization", "Interactive Map", "Word Cloud"])
    
    df_selected = df.copy()
    
    # select country
    df_selected = create_radio_feature(df=df_selected, label="🌍 Country of sighting:", feature="countries", feature_type="Categorical", col="country")
    
    # specific case for the USA: if it is the only country selected, then show an additional filter: the state
    if ("United States Of America (The)" in get_var(df_selected, "country")) & (len(get_var(df_selected, "country"))==1):
        
        df_selected = create_radio_feature(df=df_selected, label="🇺🇸 State of sighting:", feature="states", feature_type="Categorical", col="state")
     
    # select city
    df_selected = create_radio_feature(df=df_selected, label="🌃 City of sighting:", feature="cities", feature_type="Categorical", col="city")
    
    # select shape
    df_selected = create_radio_feature(df=df_selected, label="🛸 Shape of the UFO:", feature="shapes", feature_type="Categorical", col="shape")
    
    # select duration
    df_selected = create_radio_feature(df=df_selected, label="⏱ Duration of the episode (in seconds):", feature="durations", feature_type="Time/date", col="duration_seconds")
    
    # select duration
    
    df_selected = create_radio_feature(df=df_selected, label="🗓 Year/period of sighting:", feature="periods of time", feature_type="Time/date", col="year_UFO")
    
    main_button = st.sidebar.button("Submit here 👈")
    
    with tab1:
        st.markdown(
            f"This app allows you to visualize UFO sightings reports from all over the world, from {min(df['year_UFO'])} to {max(df['year_UFO'])}. With this application, you can view the data according to a filter you may want to select. Within the two following sections (tabs), you can either:"
        )
            
        st.markdown("- View and interact with a personalized map;")
        st.markdown("- Have access to some summary statistics and graphs, which will also be modified according to your filters;")
        st.markdown("- Finally, you can generate a wordcloud based on your filters.")
        st.markdown("You may also want to download the data that you have just filtered (here is a glance at these data :")
        
        cols = ['datetime', 'city', 'country', 'shape', 'duration_seconds', 'comments']
        df_to_export = df_selected[cols].reset_index(drop = True)
        st.dataframe(df_to_export)
        
        #@st.cache
        csv = df_to_export.to_csv().encode('utf-8')
        
        # possibility for the user to download data, based on his filters, as a .csv
        d1 = st.download_button(
            label="📊 Export selected data as CSV",
            data=csv,
            file_name='selected_data.csv',
            mime='text/csv',
        )
        
    with tab2: # data viz
        
        col1, col2 = st.columns(2)
        
        with col1: # display histograms
            
            fig1 = hist_chart(df_selected, "year_UFO", "Year", rotate = 45)
            st.plotly_chart(fig1)
            
            fig2 = hist_chart(df_selected, "shape", "Shape", orientation = "h", sort_hist = True)
            st.plotly_chart(fig2)
        
        with col2: # summary stat for "duration"
            
            # It is relevant to visualize duration values with statistical summary, so we will generate a streamlit table:
            
            st.text("")
            st.text("")
            st.markdown("Summary statistics of sightings duration:")

            desc_duration = pd.DataFrame(
                df_selected["duration_seconds"].describe().rename_axis('Statistics').reset_index()
            ) #summary statistics
            
            # using CSS to hide dataframe index
            hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            
            st.table(desc_duration.drop(desc_duration.index[0]).rename(columns={"duration_seconds": "Duration (seconds)"})) # streamlit table
                                
    with tab3: # map
        
        if not main_button:
            st.info("Please submit your choices within the sidebar panel so as to view the corresponding interactive map 🥶")
            st.image("pictures/warning_ufo.jpeg", width = 500)

        if main_button:
            with st.container():
                m=create_map(df=df_selected)
                folium_static(m)

                st.info('You can click on a marker to see more details about the corresponding UFO sighting report!', icon="ℹ️")

            c1, c2 = st.columns([2, 1])
            with c1:
                st.subheader("And you, have you ever seen a UFO? 🧐" )
            with c2:
                st.image("pictures/et.jpeg", width = 100)
            
    with tab4: # wordcloud
        st.markdown("**Word cloud of all comments corresponding to UFO sightings according to your filters:**")
        
        ufo_mask = np.array(Image.open("pictures/ufo_coloring.jpeg"))
        colors = ImageColorGenerator(ufo_mask)
        
        wordcloud = mywc(df=df_selected,
                         col="comments",
                         words_update=['39s', 'quot'],
                         background="gray",
                         mask=ufo_mask,
                         colors=colors)
        
        fig, ax = display_wc(wordcloud=wordcloud)
        st.pyplot(fig) # display the wordcloud using streamlit
        
        st.info("ℹ️ When a person reports a UFO sighting, they may briefly describe what they saw in their own words. Hence, this word cloud represents the most relevant and most used words by people who have witnessed UFO sightings.")
        
        # possibility for the user to download wordcloud based on his filters
        img = io.BytesIO() # create  BytesIO object
        plt.savefig(img, format='png') #create memory space
        
        # download wordcloud as a .png
        d2 = st.download_button(
           label="🌩 Download Wordcloud 🌩",
           data=img,
           file_name='ufo_wordcloud.png',
           mime="image/png"
        )
        
    df_selected = df



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