import pandas as pd
import streamlit as st
import pickle
import numpy as np
import base64
import os

# Load dataset
df = pd.read_csv("Flipkart_results(1).csv")

# Function to set background image and style elements
def set_background(image_path):
    """Set the background image and styles."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        /* Main heading styles */
        .title-text {{
            color: white !important;
            text-align: center;
            font-size: 48px; /* Increased size */
            font-weight: bold;
            padding: 10px;
        }}
        /* Main Subheading (Basic Info, Performance) */
        h2 {{
            color: white !important; /* White header */
            text-align: center;
            font-size: 28px !important;
        }}
        /* Sidebar Background */
        section[data-testid="stSidebar"] > div:first-child {{
            background: #FF8C00; /* Dark Orange */
            border-radius: 20px;
            padding: 15px;
        }}
        /* ✅ Sidebar Text, Radio Buttons, and Labels - WHITE */
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] p {{
            color: white !important;
        }}
        /* Make Sidebar Radio Buttons & Labels White */
        section[data-testid="stSidebar"] div[role="radiogroup"] label {{
            color: white !important;
            font-size: 18px !important;
            font-weight: bold !important;
        }}
        /* Fix radio button inner dot and circle to white */
        section[data-testid="stSidebar"] div[role="radiogroup"] div[data-testid="stRadio"] > div {{
            border-color: white !important;
            background-color: white !important;
        }}
        /* Inside Feature Labels to WHITE */
        label {{
            color: white !important;
            font-size: 18px !important;
            font-weight: bold !important;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    else:
        st.error(f"⚠️ Image file not found: {image_path}")

# Set the background image
set_background(r"C:/Users/91738/Desktop/Smartphone-Price-Predictions-master/phoneimage.jpg")

# Page Title without background box
st.markdown("<h1 class='title-text'>📱 MOBILE PRICE PREDICTION</h1>", unsafe_allow_html=True)

# --- Sidebar Setup ---
with st.sidebar:
    st.markdown("<h2 style='color: white; text-align: center;'>📢 Welcome to Mobile Price Prediction</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Explore the features and predict the price</p>", unsafe_allow_html=True)

    # Sidebar navigation with white-colored radio buttons
    category = st.radio("🎯 Select Feature Category", ["Basic Info", "Performance", "Display & Battery", "Predict Price"])

# Initialize session state for inputs if not already set
if "inputs" not in st.session_state:
    st.session_state.inputs = {
        "Model": df["Model"].unique()[0],
        "Stars": 0.0,
        "Num_of_Ratings": 0,
        "Reviews": 0,
        "RAM": df["Ram"].unique()[0],
        "Storage": df["Storage"].unique()[0],
        "Expandable": df["Expandable"].unique()[0],
        "Display": 6.5,
        "Camera": df["Camera"].unique()[0],
        "Battery": 4000,
        "Processor": df["Processor"].unique()[0],
    }

# --- Feature Selection Logic ---
# Basic Info Category
if category == "Basic Info":
    st.markdown("<h2>📌 Basic Information</h2>", unsafe_allow_html=True)

    st.session_state.inputs["Model"] = st.selectbox(
        "Select Model", df["Model"].unique(), index=list(df["Model"].unique()).index(st.session_state.inputs["Model"])
    )
    st.session_state.inputs["Stars"] = st.number_input(
        "Stars (Ratings)", min_value=0.0, max_value=5.0, step=0.1, value=st.session_state.inputs["Stars"]
    )
    st.session_state.inputs["Num_of_Ratings"] = st.number_input(
        "Number of Ratings", min_value=0, value=st.session_state.inputs["Num_of_Ratings"]
    )
    st.session_state.inputs["Reviews"] = st.number_input(
        "Number of Reviews", min_value=0, value=st.session_state.inputs["Reviews"]
    )

    st.sidebar.success("✅ Proceed to Performance Features")

# Performance Category
elif category == "Performance":
    st.markdown("<h2>⚡ Performance Features</h2>", unsafe_allow_html=True)

    ram_options = df["Ram"].unique()
    st.session_state.inputs["RAM"] = st.selectbox(
        "RAM (GB)", ram_options, index=list(ram_options).index(st.session_state.inputs["RAM"])
    )

    storage_options = df["Storage"].unique()
    st.session_state.inputs["Storage"] = st.selectbox(
        "Storage (GB)", storage_options, index=list(storage_options).index(st.session_state.inputs["Storage"])
    )

    st.session_state.inputs["Expandable"] = st.selectbox(
        "Expandable Storage", df["Expandable"].unique(), index=list(df["Expandable"].unique()).index(st.session_state.inputs["Expandable"])
    )

    st.sidebar.success("✅ Proceed to Display & Battery Features")

# Display & Battery Category
elif category == "Display & Battery":
    st.markdown("<h2>🔋 Display & Battery Features</h2>", unsafe_allow_html=True)

    st.session_state.inputs["Display"] = st.number_input(
        "Display Size (in inches)", min_value=0.0, step=0.1, value=st.session_state.inputs["Display"]
    )

    camera_options = df["Camera"].unique()
    default_camera = st.session_state.inputs["Camera"] if st.session_state.inputs["Camera"] in camera_options else camera_options[0]

    st.session_state.inputs["Camera"] = st.selectbox(
        "Camera (MP)", camera_options, index=list(camera_options).index(default_camera)
    )

    st.session_state.inputs["Battery"] = st.number_input(
        "Battery Capacity (mAh)", min_value=0, value=st.session_state.inputs["Battery"]
    )
    st.session_state.inputs["Processor"] = st.selectbox(
        "Processor Type", df["Processor"].unique(), index=list(df["Processor"].unique()).index(st.session_state.inputs["Processor"])
    )

    st.sidebar.success("✅ Proceed to Predict Price")

# Predict Price Category
elif category == "Predict Price":
    st.markdown("<h2>💰 Predict Mobile Price</h2>", unsafe_allow_html=True)

    if "Model" in st.session_state.inputs:
        # Prepare input array for prediction
        query = np.array([
            st.session_state.inputs["Stars"],
            st.session_state.inputs["Num_of_Ratings"],
            st.session_state.inputs["Reviews"],
            int(''.join(filter(str.isdigit, str(st.session_state.inputs["RAM"])))) or 0,
            int(''.join(filter(str.isdigit, str(st.session_state.inputs["Storage"])))) or 0,
            int(''.join(filter(str.isdigit, str(st.session_state.inputs["Expandable"])))) if any(
                x in str(st.session_state.inputs["Expandable"]) for x in ["GB", "TB"]
            )
            else 0,
            st.session_state.inputs["Display"],
            int(''.join(filter(str.isdigit, str(st.session_state.inputs["Camera"])))) or 0,
            st.session_state.inputs["Battery"],
        ]).reshape(1, -1)

        # Load the trained model
        try:
            with open("pipe.pkl", "rb") as model_file:
                pipe = pickle.load(model_file)
            predicted_price = int(np.round(pipe.predict(query)[0]))
            formatted_price = f"₹ {predicted_price:,}"
            st.markdown(
                f"<h1 class='title-text'>📢 Estimated Price of {st.session_state.inputs['Model']} is {formatted_price}</h1>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"⚠️ Error loading model: {str(e)}")
    else:
        st.warning("⚠️ Please complete all previous steps before predicting.")
