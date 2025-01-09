import streamlit as st
import pandas as pd
import folium
from folium import Choropleth
from streamlit_folium import st_folium

# Load the LAD shapefile (GeoJSON)
@st.cache_data
def load_geojson():
    import requests
    url = "https://opendata.arcgis.com/datasets/fafd3d02c6c9431f812b154a14f98e09_0.geojson"  # Example LAD GeoJSON
    geojson_data = requests.get(url).json()
    return geojson_data

# Load the ranking data from GitHub
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/your-username/repository-name/branch-name/All_SIC_Agglomeration_Results.csv"
    df = pd.read_csv(url)
    return df

# Define function to create map
def create_map(data, geojson_data, sic_column):
    # Merge ranking data with GeoJSON
    data['decile'] = pd.qcut(data[sic_column], 10, labels=False)
    merged_data = {
        row['LAD_Name']: row['decile']
        for _, row in data.iterrows()
    }

    # Initialize Folium Map
    m = folium.Map(location=[52.3555, -1.1743], zoom_start=6)  # Approx center of England

    # Add Choropleth Layer
    Choropleth(
        geo_data=geojson_data,
        data=data,
        columns=["LAD_Name", sic_column],
        key_on="feature.properties.LAD21NM",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"{sic_column} Ranking by Decile",
        bins=10,
    ).add_to(m)

    return m

# Main app
def main():
    st.title("Interactive Map: LAD Rankings by SIC Code")
    st.write(
        "This app visualizes LAD rankings for various SIC codes. Select a SIC code to view the decile map."
    )

    geojson_data = load_geojson()
    data = load_data()

    if data is not None:
        # Select SIC code column
        sic_columns = [col for col in data.columns if col != "LAD_Name"]
        selected_sic = st.selectbox("Select SIC Code", options=sic_columns)

        # Create and display map
        map_object = create_map(data, geojson_data, selected_sic)
        st_folium(map_object, width=700, height=500)

if __name__ == "__main__":
    main()
