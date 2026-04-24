import streamlit as st
import numpy as np
import pickle
import base64

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="House Price App", layout="wide")  # "wide" helps with top-left alignment

# -----------------------------

st.markdown("""
<style>
/* Labels for inputs */
label {
    font-size: 30px !important;   /* increase size */
    font-weight: 1000 !important;  /* bold */
    color: black !important;
}

/* Slider label */
div[data-testid="stSlider"] label {
    font-size: 30px !important;
    font-weight: 1000 !important;
}

/* Selectbox text */
div[data-testid="stSelectbox"] label {
    font-size: 30px !important;
    font-weight: 10000 !important;
}
</style>
""", unsafe_allow_html=True)




# Background Image
# -----------------------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        /* Make all labels black */
        label, .stMarkdown, .stTextInput label, .stNumberInput label,
        .stSelectbox label, .stSlider label {{
            color: black !important;
            font-weight: 600;
        }}

        /* Push buttons to top-left */
        .top-left-buttons {{
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1000;
        }}

        .top-left-buttons button {{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            margin-right: 5px;
            cursor: pointer;
            font-size: 14px;
            border-radius: 5px;
        }}

        .top-left-buttons button:hover {{
            background-color: #45a049;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("back.jfif")



# -----------------------------
# Reduce sidebar width
# -----------------------------
st.markdown("""
<style>
/* Sidebar width */
section[data-testid="stSidebar"] {
    width: 170px !important;      /* change this value */
    min-width: 170px !important;
}
</style>
""", unsafe_allow_html=True)
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("Navigation")

    if st.button("🏠 Home"):
        st.session_state["page"] = "home"

    if st.button("🔮 Prediction"):
        st.session_state["page"] = "prediction"

#with st.sidebar:
#    st.session_state["page"] = st.radio(
#        "Navigation",
#        ["home", "prediction"]
#    )
#"""
# -----------------------------
# Load model & scaler
# -----------------------------
@st.cache_resource
def load_model():
    with open("finalized_model.sav", "rb") as f:
        model = pickle.load(f)
    with open("scaler.sav", "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_model()

# =====================================================
# 🏠 HOME PAGE
# =====================================================
if st.session_state.page == "home":
    st.markdown("<h1></h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; font-size:60px; color:black;font-weight:bold; '>WELCOME  TO  THE  FRANCE  HOUSE  PRICE  PREDICTION  SYSTEM <br> DEVELOPED : BREEZY_YRN</p>",
        unsafe_allow_html=True
    )

# =====================================================
# 🔮 PREDICTION PAGE
# =====================================================

elif st.session_state.page == "prediction":

    st.markdown("""
    <div style="display:flex; justify-content:center; align-items:center; flex-direction:column;">
        <h1 style="color:black; text-align:center;">🔮 House Price Prediction</h1>
    </div>
    """, unsafe_allow_html=True)

   # Centered inputs using columns
    col1, col_center, col2 = st.columns([1, 2, 1])  # center column is wider
    with col_center:
         squareMeters = st.number_input("Square meters", 10, 1000, 100)
         numberOfRooms = st.number_input("Number of rooms", 1, 20, 3)
         hasYard = st.selectbox("Has yard?", ["No", "Yes"])
         hasPool = st.selectbox("Has pool?", ["No", "Yes"])
         floors = st.number_input("Floors", 1, 10, 1)
         cityCode = st.number_input(
             "City Code (e.g., 75001)", 
             min_value=10000, 
             max_value=99999, 
             value=75001, 
             step=1
    )
         cityPartRange = st.slider("Neighborhood range", 1, 10, 5)
         numPrevOwners = st.number_input("Previous owners", 0, 10, 1)
         isNewBuilt = st.selectbox("Newly built?", ["No", "Yes"])
         hasStormProtector = st.selectbox("Storm protector?", ["No", "Yes"])
         basement = st.number_input("Basement (sqm)", 0, 200, 0)
         attic = st.number_input("Attic (sqm)", 0, 200, 0)
         garage = st.number_input("Garage capacity", 0, 5, 1)
         hasStorageRoom = st.selectbox("Storage room?", ["No", "Yes"])
         hasGuestRoom = st.number_input("Guest rooms", 0, 5, 1)
         propertyAge = st.number_input("Property age (years)", 0, 200, 10)

         st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # Yes / No → 0 / 1
    # -----------------------------
    def yn(x): 
        return 1 if x == "Yes" else 0

    # -----------------------------
    # Prediction
    # -----------------------------
    if st.button("🔮 Predict Price"):
        input_data = np.array([[squareMeters, numberOfRooms, yn(hasYard),
                                yn(hasPool), floors, cityCode, cityPartRange,
                                numPrevOwners, yn(isNewBuilt),
                                yn(hasStormProtector), basement, attic,
                                garage, yn(hasStorageRoom),
                                hasGuestRoom, propertyAge]])

        input_scaled = scaler.transform(input_data)
        price = model.predict(input_scaled)

        st.success(f"💰 Estimated House Price: **€ {price[0]:,.2f}**")
