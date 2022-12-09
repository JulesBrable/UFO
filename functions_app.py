import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static
import folium
import branca
from wc_functions import mywc, display_wc
from wordcloud import ImageColorGenerator
from PIL import Image
import io

def get_data(file):
    
    return pd.read_csv(file)

def clean_col(col: pd.Series, replace = 'Unknown') -> pd.Series:
    
    """This function replaces NaN values by 'Unknown' (by default), and then capitalizes the first letter of each word. The specified column (a Series) thus has to be a string column."""
    
    return pd.Series(np.where(col.isna(), replace, col)).str.title()

def get_var(df, var) -> list:
    """Get each unique element of a dataframe column, and return it as a list."""
    return sorted(list(df[var].unique()))

def create_multiselect(df: pd.DataFrame, col: str) -> st.multiselect:
    
    return st.sidebar.multiselect(
        "",
        get_var(df, col),
        label_visibility="collapsed" # removing label and the space above the widget
    )

def create_select_slider(df: pd.DataFrame, col: str, measure: str, select_range: list) -> st.select_slider:
    
    """When generating the slider input, the idea is to create a range: we take the min and max values of the targeted feature."""
    
    return st.sidebar.select_slider(
        f"Choose a {measure} range",
        options=select_range,
        value=(min(df[col].unique()),
               max(df[col].unique())),
        label_visibility="collapsed"
    )

#def map_to_png(folium_map, file: str):
    #return folium_map.save(file)

def create_radio_feature(df: pd.DataFrame, label: str, feature: str, col: str, feature_type: str) -> pd.DataFrame:
    
    # creating a radio button in the sidebar: choose btw all values or specific values
    r = st.sidebar.radio(label,
                         [f"All {feature.capitalize()}",
                          f"Select specific {feature}"])
    
    # if selected specific values, then create a multiselect container or a select slider, depending on the type of the feature
    if r == f"Select specific {feature}":
        
        ## first case: categorical feature (city, shape) ##
        if feature_type == "Categorical":
            
            list_selected = create_multiselect(df=df, col=col)
            
            # if the selector is not empty (ie, the user made a choice), then do filter the df accordingly to this choice
            if list_selected is not None:
                return df.loc[df[col].isin(list_selected)]
            
            #if not, the return the df without any changes
            else:
                return df
        
        ## second case: time/date feature (duration, year)##
        # -> same idea as before, but with a different selector 
        elif feature_type == "Time/date":
            
            select_range = sorted(df[col].unique())
            
            if min(df[col].unique()) == max(df[col].unique()):
            
                list_selected = st.sidebar.markdown(f"UFOs sightings reports based on your filters contains a single {feature} only **{set(df[col])}**.")
                return df.loc[df[col] == list_selected]

            else:
                start, end = create_select_slider(df=df, col=col, measure=feature, select_range=select_range)
                return df.loc[(df[col] >= start) & (df[col] <= end)]
            
        ## else, return an error ## 
        else:
            raise TypeError("Unknown feature type, please choose either 'Categorical' or 'Time/date'")
        
    else:
        return df

def popup_html(shape, duration, date):
    
    """Creates a beautiful popup for the folium map, using a bit of HTML and CSS style. It allows to give more sepcific information about a given point of the map."""
    
    html = """<!DOCTYPE html>
    <html>
        <head>
            <style>
                p {{
                  background-color: #00a0a0;
                  color: white;
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
    
    """Creates of folium map with a given dataframe (filtered or not). Also creates personalized markers for each point of the map"""
    
    # setting default view of the map: mean location and zoom
    location = df['latitude'].mean(), df['longitude'].mean()
    m = folium.Map(location=location, zoom_start=4)

    # adding a personalized appearance for each point of the map
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

def hist_chart(df, col, label, orientation = "v", sort_hist = False, rotate = 0):
    
    """Display charts for the section "data visualization" of the webapp. The histogram can be oriented either vertically or horizontally, sorted or not."""
    
    fig = plt.figure(figsize=(10, 4))
    
    if orientation == "v": #vertically
        fig = px.histogram(df, x=col,
                           color_discrete_sequence=px.colors.diverging.Spectral,
                           title=f"Count of UFO sightings by {label}:")
        
        fig.update_yaxes(title_text="") #removing y axis label
        
        if sort_hist == True:
            fig.update_xaxes(title_text=f"label",
                             tickangle=rotate,
                             categoryorder="total descending")
        else:
            fig.update_xaxes(title_text=f"{label}", tickangle=rotate)
            
    else: #horizontally
        fig = px.histogram(df, y=col,
                           color_discrete_sequence=px.colors.diverging.Spectral,
                           title=f"Count of UFO sightings by {label}:")
        
        fig.update_xaxes(tickangle=rotate, title_text="")
        
        if sort_hist == True:
            fig.update_yaxes(title_text=f"{label}", categoryorder="total descending")
            
        else:
            fig.update_yaxes(title_text=f"{label}")
        
    fig.update_layout(bargap=0.2) # add a little gap between bars of the histogram
    
    return fig
              
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
