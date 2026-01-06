import streamlit as st
import pandas as pd

# 1. PAGE SETUP WITH 🌿 ICON
st.set_page_config(
    page_title="Berlin EcoCoach AI", 
    page_icon="🌿", 
    layout="centered"
)

# 2. STATE MANAGEMENT (Prevents KeyErrors)
if 'total_co2' not in st.session_state:
    st.session_state.total_co2 = 0.0
if 'doner_units' not in st.session_state:
    st.session_state.doner_units = 0.0

# 3. BERLIN VIBES 2026 CSS
st.markdown("""
    <style>
    /* Fixed Berlin Skyline Background with Dark Overlay */
    .stApp {
        background: linear-gradient(rgba(15, 1, 26, 0.85), rgba(5, 1, 10, 0.95)), 
                    url('https://images.unsplash.com/photo-1560969184-10fe8719e047?q=80&w=2070&auto=format&fit=crop');
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    header, footer, .stDeployButton { visibility: hidden !important; }
    
    /* Neon Text Header */
    .app-title {
        text-align: center;
        letter-spacing: 4px;
        font-size: 24px;
        font-weight: 900;
        color: #00ffcc;
        text-shadow: 0 0 20px #00ffcc;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    
    .app-subtitle {
        text-align: center;
        color: white;
        font-size: 14px;
        margin-bottom: 30px;
        opacity: 0.8;
    }

    /* Score Display (The Big Neon Numbers) */
    .score-box {
        text-align: center;
        padding: 40px 0;
        border-radius: 30px;
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 204, 0.3);
        margin: 20px 0;
    }
    
    .main-val {
        font-size: 80px;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 35px rgba(0, 255, 204, 0.9);
        margin: 0;
    }
    
    .sub-val {
        color: #ff00ff;
        font-size: 22px;
        font-weight: bold;
        text-shadow: 0 0 10px #ff00ff;
    }

    /* Input Card Containers */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }

    /* Neon Action Button */
    div.stButton > button {
        background: linear-gradient(90deg, #00ffcc, #00d4ff) !important;
        color: #000000 !important;
        border: none !important;
        width: 100%;
        border-radius: 50px !important;
        font-weight: 900 !important;
        padding: 18px 0 !important;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.5) !important;
        font-size: 18px !important;
        margin-top: 10px;
        text-transform: uppercase;
    }
    
    label { color: #00ffcc !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. LANGUAGE SELECTOR
lang = st.selectbox("", ["English", "Deutsch"], key="lang_final", label_visibility="collapsed")

ui = {
    "English": {
        "title": "Berlin EcoCoach AI", 
        "sub": "New Year, Same VibG 🌿 2026 is for Climate Legends!", 
        "travel": "🚗 Travel", 
        "food": "🍔 Berlin Food Choice", 
        "dist": "Distance (km)", 
        "btn": "GENERATE SCORE", 
        "unit": "Döner Units Saved",
        "qty": "How many? (Count)"
    },
    "Deutsch": {
        "title": "Berlin EcoCoach AI", 
        "sub": "Neues Jahr, gleicher VibG 🌿 2026 für Klima-Legenden!", 
        "travel": "🚗 Reise", 
        "food": "🍔 Berlin Food Auswahl", 
        "dist": "Entfernung (km)", 
        "btn": "PUNKTE GENERIEREN", 
        "unit": "Döner-Einheiten gespart",
        "qty": "Anzahl? (Count)"
    }
}[lang]

st.markdown(f'<div class="app-title">{ui["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="app-subtitle">{ui["sub"]}</div>', unsafe_allow_html=True)

# 5. INPUT GRID
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {ui['travel']}")
    distance = st.number_input(ui["dist"], min_value=0.0, step=1.0, key="distance_input")
    transport = st.selectbox("Transport Mode", ["U-Bahn / S-Bahn", "Car (Petrol)", "Car (Electric)", "Bike", "Walking"], key="transport_input")

with col2:
    st.markdown(f"### {ui['food']}")
    meal = st.selectbox("Your Meal", [
        "Vegan Döner (0.1kg)", "Chicken Döner (2.2kg)", "Beef Döner (4.5kg)", 
        "Beef Burger (3.8kg)", "Veggie Burger (1.2kg)", "Currywurst (2.1kg)", "Club Mate (0.1kg)"
    ], key="food_input")
    quantity = st.number_input(ui["qty"], min_value=1, step=1, key="count_input")

# 6. CALCULATION LOGIC
if st.button(ui["btn"]):
    t_map = {"Car (Petrol)": 0.2, "Car (Electric)": 0.05, "U-Bahn / S-Bahn": 0.03, "Bike": 0.0, "Walking": 0.0}
    f_map = {
        "Vegan Döner (0.1kg)": 0.1, "Chicken Döner (2.2kg)": 2.2, "Beef Döner (4.5kg)": 4.5,
        "Beef Burger (3.8kg)": 3.8, "Veggie Burger (1.2kg)": 1.2, "Currywurst (2.1kg)": 2.1, "Club Mate (0.1kg)": 0.1
    }
    
    # Logic: (Dist * Transport) + (Meal Value * Quantity)
    calc_co2 = (distance * t_map[transport]) + (f_map[meal] * quantity)
    st.session_state.total_co2 = calc_co2
    st.session_state.doner_units = calc_co2 / 4.5

# 7. HERO RESULT DISPLAY
st.markdown(f"""
    <div class="score-box">
        <h1 class="main-val">{st.session_state.total_co2:.1f} kg CO2</h1>
        <p class="sub-val">🥙 {st.session_state.doner_units:.1f} {ui['unit']}</p>
    </div>
    """, unsafe_allow_html=True)
