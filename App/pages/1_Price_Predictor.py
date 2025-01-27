import streamlit as st
import pickle
import pandas as pd
import numpy as np


# Page Configuration
st.set_page_config(page_title="Real Estate Price Predictor")

# Load df.pkl file

with open("App\Models\df.pkl", "rb") as file:
    df = pickle.load(file)

with open("App\Models\pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)


# App Title
st.markdown("# 🏡 **Real Estate Price Predictor**")
st.subheader("Welcome to the Price Prediction Module!")
st.markdown(
    """
Take the guesswork out of real estate pricing with our AI-powered price prediction tool.  
This module helps you:  

- 🤔 **Estimate Property Prices**: Predict property prices based on key features like area, location, bedrooms, and more.  
- 📍 **Sector-Specific Insights**: Tailor predictions to different sectors and property types.  
- 💡 **Make Data-Driven Decisions**: Leverage predictions to negotiate smarter and invest wisely.  

### **How It Works**  
1. Enter details about the property, such as **location**, **built-up area**, and **number of bedrooms**.  
2. Hit the **Predict** button to see the estimated price.  
3. Use the prediction to plan your next big move in the real estate market!  

Start below and let our AI guide your real estate journey.
"""
)

# Create two columns for input
col1, col2 = st.columns([1, 1])

# Column 1: First set of inputs
with col1:
    property_type = st.selectbox("Property Type", ["flat", "house"])
    sector = st.selectbox("Sector", sorted(df["sector"].unique().tolist()))
    bedrooms = float(
        st.selectbox("Number of Bedroom", sorted(df["bedRoom"].unique().tolist()))
    )
    bathroom = float(
        st.selectbox("Number of Bathrooms", sorted(df["bathroom"].unique().tolist()))
    )
    balcony = st.selectbox("Balconies", sorted(df["balcony"].unique().tolist()))
    property_age = st.selectbox(
        "Property Age", sorted(df["agePossession"].unique().tolist())
    )

# Column 2: Second set of inputs
with col2:
    built_up_area = float(st.number_input("Built Up Area", min_value=1.0, value=100.0))
    servant_room = float(st.selectbox("Servant Room", [0.0, 1.0]))
    store_room = float(st.selectbox("Store Room", [0.0, 1.0]))
    furnishing_type = st.selectbox(
        "Furnishing Type", sorted(df["furnishing_type"].unique().tolist())
    )
    luxury_category = st.selectbox(
        "Luxury Category", sorted(df["luxury_category"].unique().tolist())
    )
    floor_category = st.selectbox(
        "Floor Category", sorted(df["floor_category"].unique().tolist())
    )

# When Predict button is pressed
if st.button("Predict"):
    # Prepare the data for prediction
    data = [
        [
            property_type,
            sector,
            bedrooms,
            bathroom,
            balcony,
            property_age,
            built_up_area,
            servant_room,
            store_room,
            furnishing_type,
            luxury_category,
            floor_category,
        ]
    ]
    columns = [
        "property_type",
        "sector",
        "bedRoom",
        "bathroom",
        "balcony",
        "agePossession",
        "built_up_area",
        "servant room",
        "store room",
        "furnishing_type",
        "luxury_category",
        "floor_category",
    ]

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    try:
        # Predict the base price using the model pipeline
        base_price = np.expm1(pipeline.predict(one_df))[0]

        # Calculate price range dynamically (e.g., ±10% of base price)
        price_margin = 0.10  # 10% margin
        low = base_price * (1 - price_margin)
        high = base_price * (1 + price_margin)

        # Display the predicted price range
        st.success(
            "The price of the property is between {:.2f} Cr and {:.2f} Cr".format(
                round(low, 2), round(high, 2)
            )
        )
    except Exception as e:
        st.error(f"Error during prediction: {e}")
