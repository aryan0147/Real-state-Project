import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Set up Streamlit page configuration
st.set_page_config(page_title="Recommend Apartments", layout="wide")

# Load data
location_df = pickle.load(open("App\Models\location_distance.pkl", "rb"))
cosine_sim1 = pickle.load(open("App\Models\cosine_sim1.pkl", "rb"))
cosine_sim2 = pickle.load(open("App\Models\cosine_sim3.pkl", "rb"))
cosine_sim3 = pickle.load(open("App\Models\cosine_sim3.pkl", "rb"))


# Function to recommend properties without weights
def recommend_properties(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

    sim_scores = list(
        enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)])
    )
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1 : top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1 : top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()

    recommendations_df = pd.DataFrame(
        {"PropertyName": top_properties, "SimilarityScore": top_scores}
    )
    return recommendations_df


# Sidebar for navigation
st.sidebar.title("Navigation")
navigation = st.sidebar.radio(
    "Choose an option", ["Home", "Search Nearby Properties", "Recommend Apartments"]
)

# Header and Introduction
if navigation == "Home":
    st.title("🏠 Apartment Recommendation Hub")
    st.subheader("Welcome to the Apartment Recommendation Module!")
    st.markdown("""
    Find the best apartments based on your preferences with our intelligent recommendation system.  
    Use the tools provided to:  
    - 🔍 **Discover Similar Properties**: Get personalized suggestions based on the apartment you like.  
    - 🏙️ **Search by Location**: Explore properties within a specific radius from your selected location.  
    - ⚖️ **Adjust Recommendation Weights**: Fine-tune the recommendations by adjusting similarity factors like price, distance, and amenities.  
    - 📊 **View Property Details**: See key information such as distance, property names, and similarity scores for easier comparison.  
    """)

# Search Nearby Properties Section
elif navigation == "Search Nearby Properties":
    st.title("🔍 Search Nearby Properties")
    selected_location = st.selectbox(
        "Select Location:", sorted(location_df.columns.to_list())
    )

    # Input for radius with validation
    radius = st.slider(
        "Select Radius (in kilometers):", min_value=1, max_value=50, value=5, step=1
    )

    if selected_location and radius:
        if st.button("Search"):
            # Filter locations based on the radius
            result_ser = location_df[location_df[selected_location] < radius * 1000][
                selected_location
            ].sort_values()

            if result_ser.empty:
                st.error(
                    f"No properties found within {radius} km of {selected_location}. Try increasing the radius or choosing another location."
                )
            else:
                st.success(
                    f"Found {len(result_ser)} properties within {radius} km of {selected_location}:"
                )

                # Display the nearby locations and their distances
                result_df = pd.DataFrame(
                    {
                        "Property Name": result_ser.index,
                        "Distance (km)": result_ser.values
                        / 1000,  # Convert from meters to kilometers
                    }
                )
                st.dataframe(result_df)

# Recommend Apartments Section
elif navigation == "Recommend Apartments":
    st.title("🏠 Recommend Apartments")
    selected_apartment = st.selectbox(
        "Select an Apartment:", sorted(location_df.index.to_list())
    )

    if st.button("Recommend"):
        if not selected_apartment:
            st.error("Please select an apartment!")
        else:
            recommendation_df = recommend_properties(selected_apartment)
            if recommendation_df.empty:
                st.warning("No similar properties found.")
            else:
                st.success(f"Top {len(recommendation_df)} recommendations:")
                st.dataframe(recommendation_df)
