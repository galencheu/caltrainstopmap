#imports
import time

import streamlit as st
import pandas as pd
import folium
import streamlit
from streamlit_folium import st_folium, folium_static
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster

# App title
st.set_page_config(page_title="Galen's Apps", layout="wide")

st.title("📚 Galen's App Library")

# Create three tabs
homepage_tab, app_tab1, app_tab2, app_tab3, about_tab = st.tabs(["🏠 Homepage", "🚇 Caltrain Stops", "⚠️ CA WARN", "🧮 My App3",  "ℹ️ About"])

# --- Homepage Tab ---
with homepage_tab:
    st.header("Welcome to My Streamlit Apps")
    st.write("""
    I create things that help me out.
    I was looking for apartments near Caltrain so I built the stop map and address locator.
    """)

# --- App1 ---
with app_tab1:
    st.header("Caltrain Stop App")
    
    # 💡 Paste your existing app logic here
    st.subheader("Locate Nearest Caltrain Stop to Location")

    # #Set up our app
    # st.set_page_config(page_title='Train Station Locator', layout = 'wide')
    # st.title('Where are Caltrain Stations?')
    # st.write('Stop looking for stops, start going to stops.')

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
        default_lat = 37.484668049999996 #1 Hacker Way, Menlo Park, CA
        default_lon = -122.1483654685629 #1 Hacker Way, Menlo Park, CA
        if len(address) < 4:
            time.sleep(2)
            st.write("Default Address Used")
            st.session_state.map = None #Reset the session map
            return default_lat, default_lon
        else:
            time.sleep(2)
            # Geocode an address
            location = geolocator.geocode(address_to_search)
            time.sleep(2)
            if location is None:
                st.write("Coordinates not found for location, default address used")
                st.session_state.map = None #Reset the session map
                return default_lat, default_lon
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

# --- App2 ---
with app_tab2:
    st.header("WARN Monitor")
    
    # 💡 Paste your existing app logic here
    st.subheader("CA WARN Notice Viewer")

    warn_df = pd.read_excel('https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn_report1.xlsx', sheet_name='Detailed WARN Report ')
    warn_df.columns = warn_df.iloc[0]  # Set the first row as the header
    warn_df = warn_df[1:]  # Remove the first row from the DataFrame
    warn_df.reset_index(drop=True, inplace=True)  # Reset the index if needed

    # Input text field for user to enter a name
    name = st.text_input("Enter company name to filter:")

    # Filter the DataFrame based on user input
    if name:
        filtered_df = warn_df[warn_df['Company'].str.contains(name, case=False, na=False)]
        # = filtered_df['No. Of\nEmployees'].sum()
        #st.write(f"Total of Number of Employees for filtered companies: {total_number}")
    else:
        filtered_df = warn_df.tail()  # Show the full DataFrame if no input

    # Display the filtered DataFrame
    st.write("Filtered Companies:")
    st.dataframe(filtered_df)


# --- App3 ---
with app_tab3:
    st.header("Place holder for app3")
    
    # 💡 Paste your existing app logic here
    st.subheader("Example: BMI Calculator")

    weight3 = st.number_input("Enter your weight (kg):", min_value=1.0, step=0.5, key=5)
    height3 = st.number_input("Enter your height (cm):", min_value=50.0, step=0.5, key=6)

    if weight3 and height3:
        bmi = weight3 / ((height3 / 100) ** 2)
        st.metric(label="Your BMI", value=round(bmi, 2))

# --- About Tab ---
with about_tab:
    st.header("About the Apps")
    st.markdown("""
    - **Built with**: Streamlit  
    - **Author**: Galen
    - **Purpose**: Apps that help out my everyday life 
    - **GitHub**: [My Github](https://github.com/galencheu)
    """)
