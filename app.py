import streamlit as st
import pandas as pd

# 1. PAGE SETUP WITH 🌿 ICON
st.set_page_config(
    page_title="Berlin EcoCoach AI", 
    page_icon="🌿", 
    layout="centered"
)

# 2. STATE MANAGEMENT
if 'total_co2' not in st.session_state:
    st.session_state.total_co2 = 0.0
if 'doner_units' not in st.session_state:
    st.session_state.doner_units = 0.0

# 3. VIBRANT BERLIN CSS
st.markdown("""
    <style>
    /* Brighter Berlin Skyline Background */
    .stApp {
        background: linear-gradient(rgba(15, 1, 26, 0.2), rgba(5, 1, 10, 0.3)), 
                    url('https://images.unsplash.com/photo-1560969184-10fe8719e047?q=80&w=2070&auto=format&fit=crop');
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    header, footer, .stDeployButton { visibility: hidden !important; }
    
    .app-title {
        text-align: center;
        letter-spacing: 4px;
        font-size: 26px;
        font-weight: 900;
        color: #00ffcc;
        text-shadow: 0 0 15px #00ffcc, 0 0 30px #00ffcc;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    
    .app-subtitle {
        text-align: center;
        color: #ffffff;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 30px;
        text-shadow: 1px 1px 10px #000;
    }

    /* Score Display Box */
    .score-box {
        text-align: center;
        padding: 40px 0;
        border-radius: 30px;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        border: 2px solid rgba(0, 255, 204, 0.5);
        margin: 20px 0;
    }
    
    .main-val {
        font-size: 85px;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 30px rgba(0, 255, 204, 1);
        margin: 0;
    }
    
    .sub-val {
        color: #ff00ff;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 0 0 10px #ff00ff;
    }

    /* Input Card Containers */
    [data-testid="column"] {
        background: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 25px !important;
    }

    /* CENTERED NEON BUTTON */
    .stButton {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #00ffcc, #00d4ff) !important;
        color: #000000 !important;
        border: none !important;
        width: 100% !important; 
        border-radius: 50px !important;
        font-weight: 900 !important;
        padding: 20px 0 !important;
        box-shadow: 0 0 40px rgba(0, 255, 204, 0.8) !important;
        font-size: 20px !important;
        text-transform: uppercase;
        transition: 0.3s ease;
    }

    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 60px rgba(0, 255, 204, 1) !important;
    }
    
    label { color: #00ffcc !important; font-weight: bold !important; font-size: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. LANGUAGE SELECTOR
lang = st.selectbox("", ["English", "Deutsch"], key="lang_main", label_visibility="collapsed")

ui = {
    "English": {
        "title": "Berlin EcoCoach AI", 
        "sub": "New Year, Same VibG 🌿 2026 for Climate Legends!", 
        "travel_header": "🚕 Travel", 
        "food_header": "🍔 Food",
        "dist_lbl": "Distance (km)", 
        "btn": "GENERATE SCORE", 
        "unit": "Döner Units Saved",
        "qty_lbl": "Quantity",
        "mode_lbl": "Transport Mode",
        "meal_lbl": "Meal Selection"
    },
    "Deutsch": {
        "title": "Berlin EcoCoach AI", 
        "sub": "Neues Jahr, gleicher VibG 🌿 2026 für Klima-Legenden!", 
        "travel_header": "🚕 Reise", 
        "food_header": "🍔 Essen",
        "dist_lbl": "Strecke (km)", 
        "btn": "PUNKTE GENERIEREN", 
        "unit": "Döner-Einheiten gespart",
        "qty_lbl": "Anzahl",
        "mode_lbl": "Verkehrsmittel",
        "meal_lbl": "Essen Auswahl"
    }
}[lang]

st.markdown(f'<div class="app-title">{ui["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="app-subtitle">{ui["sub"]}</div>', unsafe_allow_html=True)

# 5. NEW GRID LAYOUT: Row 1 (Names/Modes) and Row 2 (Counts)
col_top_left, col_top_right = st.columns(2)

with col_top_left:
    st.markdown(f"### {ui['travel_header']}")
    transport = st.selectbox(ui["mode_lbl"], ["U-Bahn / S-Bahn", "Car (Petrol)", "Car (Electric)", "Bike", "Walking"], key="tr_in")

with col_top_right:
    st.markdown(f"### {ui['food_header']}")
    # Cleaned food list: removed weights from labels
    meal = st.selectbox(ui["meal_lbl"], [
        "Vegan Döner", "Chicken Döner", "Beef Döner", 
        "Beef Burger", "Veggie Burger", "Currywurst", "Club Mate"
    ], key="ml_in")

col_bot_left, col_bot_right = st.columns(2)

with col_bot_left:
    distance = st.number_input(ui["dist_lbl"], min_value=0.0, step=1.0, key="ds_in")

with col_bot_right:
    # Quantity now defaults to 0
    quantity = st.number_input(ui["qty_lbl"], min_value=0, step=1, value=0, key="qt_in")

# 6. CENTERED BUTTON
if st.button(ui["btn"]):
    t_map = {"Car (Petrol)": 0.2, "Car (Electric)": 0.05, "U-Bahn / S-Bahn": 0.03, "Bike": 0.0, "Walking": 0.0}
    # Calculation map remains the same in the background
    f_map = {
        "Vegan Döner": 0.1, "Chicken Döner": 2.2, "Beef Döner": 4.5,
        "Beef Burger": 3.8, "Veggie Burger": 1.2, "Currywurst": 2.1, "Club Mate": 0.1
    }
    
    total = (distance * t_map[transport]) + (f_map[meal] * quantity)
    st.session_state.total_co2 = total
    st.session_state.doner_units = total / 4.5

# 7. HERO RESULTS
st.markdown(f"""
    <div class="score-box">
        <h1 class="main-val">{st.session_state.total_co2:.1f} kg CO2</h1>
        <p class="sub-val">🥙 {st.session_state.doner_units:.1f} {ui['unit']}</p>
    </div>
    """, unsafe_allow_html=True)
