
##Libraries
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import os

##Import drive and set directory
from google.colab import drive
drive.mount('/content/drive')
shortcut_path = '/content/drive/MyDrive/Agglomeration'
os.chdir(shortcut_path)

output_dir = 'Code/output_data'
os.makedirs(output_dir, exist_ok=True)

# Set up the page layout
st.set_page_config(layout="wide")

# Step 1: Load data
@st.cache
def load_data():
    # Replace 'LAD_rankings.csv' with your file's path
    rankings = pd.read_csv('Code/output_data/Ranked_AllSIC_Agglomeration_Results.csv')
    
    # Replace with the actual GeoJSON URL or local path
    lad_boundaries = gpd.read_file(
        'Code/using_data/Local_Authority_Districts_December_2024_Boundaries_UK_BFC_-8514277369542505193.geojson'
    )
    return rankings, lad_boundaries

rankings, lad_boundaries = load_data()

# Step 2: Merge rankings with LAD boundaries
merged_data = lad_boundaries.merge(rankings, left_on="LAD24CD", right_on="LAD_Name")

# Step 3: Streamlit UI components
st.sidebar.header("Select Category (SIC 2 Digit)")
category = st.sidebar.selectbox(
    "Choose a performance category to display:", 
    [col for col in rankings.columns if col != "LAD_Name"]
)

st.sidebar.markdown("### About")
st.sidebar.info(
    "This application displays LAD performance rankings across various categories. "
    "Select a category from the dropdown to visualize the rankings as a heatmap."
)

# Step 4: Generate the map
st.title(f"Performance Heatmap for SIC code {category}")
st.write("This map displays LAD rankings (1 = highest, 318 = lowest) by deciles.")

fig = px.choropleth(
    merged_data,
    geojson=merged_data.geometry,
    locations=merged_data.index,
    color=category,
    color_continuous_scale="Viridis",
    range_color=(1, 318),
    title=f"LAD Rankings: {category}",
)
fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig, use_container_width=True)

# Optional: Add a data table
st.subheader("Data Table")
st.write(rankings)
