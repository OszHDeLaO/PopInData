import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
import re
from geopy.geocoders import Nominatim
import os

# Define the default CSV filename
DEFAULT_FILENAME = "MeetUpPopIn_Event.csv"

# Check if the default file exists
if os.path.exists(DEFAULT_FILENAME):
    try:
        df = pd.read_csv(DEFAULT_FILENAME)
        st.write(f"Using default data file: {DEFAULT_FILENAME}")
    except FileNotFoundError:
        st.error(f"Error: Default file '{DEFAULT_FILENAME}' not found.")
        df = None  # Set df to None to prevent further execution
    except pd.errors.ParserError:
        st.error(f"Error: Could not parse CSV file '{DEFAULT_FILENAME}'. Please check the format.")
        df = None
    except Exception as e: # Catch any other potential errors during file reading
        st.error(f"An unexpected error occurred while reading the file: {e}")
        df = None


else:
    df = None  # Initialize df to None if the file doesn't exist


# File uploader (runs only if the default file *doesn't* exist, or the user wants to override)
if df is None: # Only show the uploader if the default file wasn't loaded
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except pd.errors.ParserError:
            st.error("Error: Could not parse uploaded CSV file. Please check the format.")
            df = None
        except Exception as e:
            st.error(f"An unexpected error occurred while reading the uploaded file: {e}")
            df = None
    else:
        st.write("No data loaded. Please upload a CSV file or ensure the default file exists.")



if df is not None:  # Proceed only if a DataFrame was successfully loaded
    # ... (rest of the code - event type classification, geocoding, metrics, visualization, map)

    # ... (Event Type Classification, Geocoding, etc. - same as before)

    # Handle missing coordinates
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Metrics Calculation (same as before)

    # Metrics DataFrame (same as before)
    st.write("## Event Metrics")
    st.dataframe(results_df)

    # Visualization (Combined Bar Plot for Comparison)
    st.write("## Event Metrics Comparison")
    fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Event Type', y='value', hue='metric', data=pd.melt(results_df, id_vars=['Event Type'], var_name='metric', value_name='value'), ax=ax_bar)
    st.pyplot(fig_bar)


    # Map Creation (same as before)
    st.write("## Toronto Events Map")
    toronto_map = folium.Map(location=[43.6532, -79.3832], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(toronto_map)

    for index, row in df.iterrows():
        latitude, longitude = row['Latitude'], row['Longitude']
        if pd.notna(latitude) and pd.notna(longitude):
            total_attendees = row['Attendees']
            location_name = row['Cleaned Location']

            popup_text = f"Location: {location_name}<br>Total Attendees: {total_attendees}"
            folium.Marker(
                location=[latitude, longitude],
                popup=popup_text
            ).add_to(marker_cluster)

    st.components.v1.html(toronto_map._repr_html(), height=600)
