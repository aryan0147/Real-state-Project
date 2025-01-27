import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Introduction Section
st.title("🏠 Real Estate Analytics Dashboard")
st.subheader("Welcome to the Real Estate Analytics Module!")
st.markdown("""
Explore key insights into the real estate market with our interactive dashboard.  
Use the tools provided to:  
- 📊 **Analyze Property Trends**: Understand sector-wise pricing and availability.  
- 🏡 **Compare Property Types**: Flats vs. houses, price per square foot, and more.  
- 📈 **Visualize Distributions**: Explore built-up area ranges, bedroom configurations, and price trends.  
- 🔍 **Filter with Ease**: Find properties within your desired price range and preferences.  
""")

# Data

# Load Data
new_df = pd.read_csv("App\Dataset\data_viz1.csv")


# Ensure the relevant columns are numeric
new_df["price"] = pd.to_numeric(new_df["price"], errors="coerce")
new_df["price_per_sqft"] = pd.to_numeric(new_df["price_per_sqft"], errors="coerce")
new_df["built_up_area"] = pd.to_numeric(new_df["built_up_area"], errors="coerce")
new_df["latitude"] = pd.to_numeric(new_df["latitude"], errors="coerce")
new_df["longitude"] = pd.to_numeric(new_df["longitude"], errors="coerce")

# Group data and calculate mean
group_df = new_df.groupby("sector").mean(numeric_only=True)[
    ["price", "price_per_sqft", "built_up_area", "latitude", "longitude"]
]


# Sidebar Visualization Selector
st.sidebar.title("Choose Visualization")
visualization_options = sorted(
    [
        "Sector Price per Sqft Geomap",
        "Area Vs Price",
        "Bedroom Distribution",
        "Side by Side BHK Price Comparison",
        "Side by Side Distplot for Property Type",
        "Average Price by Bedroom Type",
        "Top Sectors by Average Price",
        "Price Distribution by Sector",
        "Total Properties in Each Sector",
        "Average Price per Sqft by Property Type",
        "Built-Up Area Distribution",
        "Price vs. Built-Up Area",
    ]
)

selected_visualization = st.sidebar.selectbox(
    "Select Visualization",
    visualization_options,
    index=visualization_options.index("Sector Price per Sqft Geomap"),
)

# Render Visualizations
if selected_visualization == "Sector Price per Sqft Geomap":
    st.header("Sector Price per Sqft Geomap")
    fig = px.scatter_mapbox(
        group_df,
        lat="latitude",
        lon="longitude",
        color="price_per_sqft",
        size="built_up_area",
        color_continuous_scale=px.colors.cyclical.IceFire,
        zoom=10,
        mapbox_style="open-street-map",
        width=1200,
        height=700,
        hover_name=group_df.index,
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_visualization == "Area Vs Price":
    st.header("Area Vs Price")
    property_type = st.selectbox("Select Property Type", ["flat", "house"])
    filtered_df = new_df[new_df["property_type"] == property_type]
    fig = px.scatter(
        filtered_df,
        x="built_up_area",
        y="price",
        color="bedRoom",
        title="Area Vs Price",
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_visualization == "Bedroom Distribution":
    st.header("Bedroom Distribution")
    sector_options = new_df["sector"].unique().tolist()
    sector_options.insert(0, "overall")
    selected_sector = st.selectbox("Select Sector", sector_options)
    filtered_df = (
        new_df
        if selected_sector == "overall"
        else new_df[new_df["sector"] == selected_sector]
    )
    fig = px.pie(filtered_df, names="bedRoom")
    st.plotly_chart(fig, use_container_width=True)

elif selected_visualization == "Side by Side BHK Price Comparison":
    st.header("Side by Side BHK Price Comparison")
    filtered_df = new_df[new_df["bedRoom"] <= 4]
    fig = px.box(
        filtered_df,
        x="bedRoom",
        y="price",
        title="BHK Price Range",
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_visualization == "Side by Side Distplot for Property Type":
    st.header("Side by Side Distplot for Property Type")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.distplot(
        new_df[new_df["property_type"] == "house"]["price"], label="house", ax=ax
    )
    sns.distplot(
        new_df[new_df["property_type"] == "flat"]["price"], label="flat", ax=ax
    )
    ax.legend()
    st.pyplot(fig)

elif selected_visualization == "Average Price by Bedroom Type":
    st.header("Average Price by Bedroom Type")
    avg_price_bedroom = new_df.groupby("bedRoom")["price"].mean().reset_index()
    fig = px.bar(
        avg_price_bedroom,
        x="bedRoom",
        y="price",
        color="bedRoom",
        title="Average Price by Bedroom Type",
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_visualization == "Top Sectors by Average Price":
    st.header("Top Sectors by Average Price")
    top_sectors = (
        new_df.groupby("sector")["price"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig = px.bar(
        top_sectors,
        x="sector",
        y="price",
        color="price",
        title="Top Sectors by Average Price",
        labels={"price": "Average Price", "sector": "Sector"},
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_visualization == "Price Distribution by Sector":
    st.header("Price Distribution by Sector")
    selected_sector = st.selectbox("Select Sector", new_df["sector"].unique().tolist())
    filtered_df = (
        new_df
        if selected_sector == "overall"
        else new_df[new_df["sector"] == selected_sector]
    )
    fig = px.violin(
        filtered_df,
        x="sector",
        y="price",
        color="sector",
        box=True,
        points="all",
        title=f"Price Distribution for {selected_sector}",
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_visualization == "Total Properties in Each Sector":
    st.header("Total Properties in Each Sector")
    sector_count = new_df["sector"].value_counts().reset_index()
    sector_count.columns = ["sector", "total_properties"]
    fig = px.bar(
        sector_count,
        x="sector",
        y="total_properties",
        color="total_properties",
        title="Total Properties in Each Sector",
        labels={"total_properties": "Number of Properties", "sector": "Sector"},
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_visualization == "Average Price per Sqft by Property Type":
    st.header("Average Price per Sqft by Property Type")
    avg_price_per_sqft = (
        new_df.groupby("property_type")["price_per_sqft"].mean().reset_index()
    )
    fig = px.bar(
        avg_price_per_sqft,
        x="property_type",
        y="price_per_sqft",
        color="property_type",
        title="Average Price per Sqft by Property Type",
        labels={
            "price_per_sqft": "Price per Sqft",
            "property_type": "Property Type",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_visualization == "Built-Up Area Distribution":
    st.header("Built-Up Area Distribution")
    fig = px.histogram(
        new_df,
        x="built_up_area",
        nbins=30,
        title="Built-Up Area Distribution",
        labels={"built_up_area": "Built-Up Area (sqft)"},
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_visualization == "Price vs. Built-Up Area":
    st.header("Price vs. Built-Up Area")
    fig = px.scatter(
        new_df,
        x="built_up_area",
        y="price",
        color="sector",
        title="Price vs. Built-Up Area",
        labels={"built_up_area": "Built-Up Area (sqft)", "price": "Price (\u20b9)"},
    )
    st.plotly_chart(fig, use_container_width=True)

st.header("End of Dashboard. Explore the insights and take action!")
