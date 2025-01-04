#imports
import time

import streamlit as st
import pandas as pd
import folium
import streamlit
from streamlit_folium import st_folium, folium_static
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster

DEFAULT_LAT = 37.484668049999996 #1 Hacker Way, Menlo Park, CA
DEFAULT_LON = -122.1483654685629 #1 Hacker Way, Menlo Park, CA

#Set up our app
st.set_page_config(page_title='Train Station Locator', layout = 'wide')
st.title('Where are Caltrain Stations?')
st.write('Stop looking for stops, start going to stops.')


def get_caltrain_stns():
    """
    Reads the ods file with Caltrain stops and info
    Returns:
        caltrainfile: dataframe cleaned
        colors: color coding for type of stop
    """
    caltrain_file = pd.read_excel("CalTrainStops.ods", engine="odf")
    #clean non-breaking space
    caltrain_file["Address"] = caltrain_file["Address"].str.replace(u'\xa0', u' ')
    caltrain_file["zone_str"] = caltrain_file["Zone"].astype("str")
    caltrain_file["popupinfo"] = caltrain_file["Code"] + " " +  caltrain_file["Station"]
    colors = {"Express" : "red",
                "Limited" : "orange",
                "Local" : "blue",
                "Weekends" : "green",
                "Football Games" : "green",
                "2x Daily": "Green",
                "South County" : "Green"}
    return caltrain_file, colors

def get_address_coords(address_to_search):
    """
    Geocodes a user input address
    """
    geolocator = Nominatim(user_agent="my_geocoder")

    if len(address) < 4:
        time.sleep(2)
        st.write("Default Address Used")
        st.session_state.map = None #Reset the session map
        return DEFAULT_LAT, DEFAULT_LON
    else:
        time.sleep(2)
        # Geocode an address
        location = geolocator.geocode(address_to_search)
        time.sleep(2)
        if location is None:
            st.write("Coordinates not found for location, default address used")
            st.session_state.map = None #Reset the session map
            return DEFAULT_LAT, DEFAULT_LON
        else:
            st.write(location.latitude, location.longitude)
            st.session_state.map = None #Reset the session map
            return location.latitude, location.longitude

"""
Here are all the Caltrain Stations.
"""
#with st.echo():

def create_map(address, caltrain_df, stop_colors, lat, lon):
    """
    Create a folium map based around caltrain stations
    
    Returns:
        Folium map
    """
    if 'map' not in st.session_state or st.session_state.map is None:
        m = folium.Map(location=[lat, lon], zoom_start=12)
        marker_cluster = MarkerCluster().add_to(m)
        folium.Marker(location=[lat, lon], popup=str(address)).add_to(marker_cluster)
        caltrain_df.apply(lambda row:folium.CircleMarker(location=[row["Lat"], row["Long"]], 
                                                    radius=5, fill_color=stop_colors[row["Stops"]],
                                                    popup=row['popupinfo'], weight = 1,
                                                    fill_opacity = 5)
                                                    .add_to(m), axis=1)        
        st.session_state.map = m  # Save the map in the session state
    return st.session_state.map

def show_map(address, stops, colors, lat, lon):
    """
    Show map based around the Lat Long
    """
    m = create_map(address, stops, colors, lat, lon)  # Get or create the map
    folium_static(m, width=1000)

######MAIN########
## Create form to get location address
form = st.form(key="form_settings")
address = ''
address = form.text_input(
    "Location address",
    key="address",
)
form.form_submit_button(label="Submit")

caltrain_df, stop_colors = get_caltrain_stns()
lat, lon = get_address_coords(address)
show_map(address, caltrain_df, stop_colors, lat, lon)
