import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap

@st.cache # for improved performance in (re-)loading data
def get_data(file):
    
    return pd.read_csv(file)

df = get_data("data/ufo_sightings_clean.csv")

def get_shape(df, var):
    
    return df[var].unique().tolist()

def get_city(df, var):
    
    return list(df[var].unique())

def main():
    
    st.sidebar.header("Mapping of UFO sightings reports from 1940 to 2014")
    #country = st.sidebar.selectbox('Country',get_country(cat,"Country"))
    city = st.sidebar.selectbox("City", get_city(df, "city"))
    shape = st.sidebar.selectbox("UFO shape", get_shape(df, "shape"))
    #bedtype = st.sidebar.selectbox("Bed Type", get_cat(df,"Bed Type"))
    #roomtype=st.sidebar.selectbox("Room Type", get_cat(cat,"Room Type"))
    #bedrooms=st.sidebar.slider("Bedrooms",0,15,key=0)
    #bathrooms=st.sidebar.slider("Bathrooms", 0,15,key=1)
    #beds=st.sidebar.slider("Beds", 0,15,key=2)
    #min_nights=st.sidebar.selectbox("Minimum Nights", get_cat(cat,"Minimum Nights"))
    #max_nights=st.sidebar.selectbox("Maximum Nights", get_cat(cat,"Maximum Nights"))
    #cancel=st.sidebar.selectbox("Cancellation policy", get_cat(cat,"Cancellation Policy"))
    #amenities=st.sidebar.multiselect("Amenities",['pets allowed','long term stays allowed','air conditioning', 'elevator in building','suitable for events','bathtub', 'essentials','gym','baby-friendly','security', 'secure_access', 'outdoor','bathroom_essentials','heating', 'pool_jacuzzi','clothes_stuff','not specified','kitchen','cooking basics','tv','family/kid friendly', 'internet','easy_to_check_in','free parking', 'laptop friendly workspace','old_handicap_people_friendly'])
    #amenities = ' '.join([str(elem) for elem in amenities])
    #host=st.sidebar.multiselect("host",["has profile pic","is superhost","identity verified","location exact","instant bookable","require guest phone verification","require guest profile picture","no specified","requires license"])
    #host= ' '.join([str(elem) for elem in host])
    m = folium.Map()
    
    for lat, lon, name in zip(df['latitude'], df['longitude'], df['city']):
        #Creating the marker
        folium.Marker(
            #Coordinate of the country$
            location = [lat, lon],
            #The popup that show up if click the marker
            popup = name
        ).add_to(m)
        
    #heat_data = [df['latitude'],df['longitude']]
    #HeatMap(heat_data).add_to(m)
    m
    
    st.subheader("And you, have you ever seen a UFO? 🧐" )
    #feat=Image.open("feature_importance.png")
    #rmse= Image.open("RMSE.png") 
    #pred=Image.open("predvsreal.png")
    #st.image(feat) 
    #st.image(rmse) 
    #st.image(pred) 
    


    if st.sidebar.button("Submit here 👈"):
        st.balloons()

if __name__ == '__main__':
    main()