import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

# Set Streamlit page layout
st.set_page_config(layout="wide")

# Load the data
@st.cache
def load_data():
    # Load rankings data from CSV
    rankings = pd.read_csv("LAD_rankings.csv")
    
    # Load LAD boundaries from GeoJSON
    lad_boundaries = gpd.read_file("LAD_boundaries.geojson")
    
    return rankings, lad_boundaries

# Load and process the data
rankings, lad_boundaries = load_data()

# Merge the rankings with LAD boundaries
merged_data = lad_boundaries.merge(rankings, left_on="LAD_Code", right_on="LAD_Code")

# Sidebar for category selection
st.sidebar.header("Select Category")
category = st.sidebar.selectbox(
    "Choose a performance category to display:",
    [col for col in rankings.columns if col != "LAD_Code"]
)

# Main app title
st.title(f"Performance Heatmap for {category}")
st.write("This map displays LAD rankings (1 = highest, 360 = lowest).")

# Create the map using Plotly
fig = px.choropleth(
    merged_data,
    geojson=merged_data.geometry,
    locations=merged_data.index,
    color=category,
    color_continuous_scale="Viridis",
    range_color=(1, 360),
    title=f"LAD Rankings: {category}",
)
fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig, use_container_width=True)

# Display the data table
st.subheader("Data Table")
st.write(rankings)
