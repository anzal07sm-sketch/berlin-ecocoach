import streamlit as st
import pandas as pd

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Berlin Eco-Coach AI", layout="centered")

# 2. STATE PERSISTENCE (Crucial for language switching)
if 'total_co2' not in st.session_state:
    st.session_state.total_co2 = 0.0
if 'doner_units' not in st.session_state:
    st.session_state.doner_units = 0.0
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. BERLIN VIBES 2026 CSS
st.markdown("""
    <style>
    /* Obsidian & Purple Pulse Background */
    .stApp {
        background: linear-gradient(180deg, #0f011a 0%, #05010a 100%) !important;
        background-attachment: fixed !important;
    }

    /* Interface Cleanup */
    header, footer, .stDeployButton { visibility: hidden !important; }
    
    /* Neon Text Headers */
    .app-title {
        text-align: center;
        letter-spacing: 3px;
        font-size: 16px;
        font-weight: bold;
        color: #00ffcc;
        text-shadow: 0 0 10px #00ffcc;
        margin-bottom: 25px;
        text-transform: uppercase;
    }

    /* Score Display (Centerpiece) */
    .score-box {
        text-align: center;
        padding: 30px 0;
        border-radius: 30px;
        background: rgba(255, 255, 255, 0.03);
        margin: 20px 0;
    }
    .main-val {
        font-size: 80px;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 40px rgba(0, 255, 204, 0.6);
        margin: 0;
    }
    .sub-val {
        color: #ff00ff;
        font-size: 22px;
        font-weight: bold;
        text-shadow: 0 0 10px #ff00ff;
    }

    /* Input Card Styling */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 255, 204, 0.2) !important;
        border-radius: 25px !important;
        padding: 30px !important;
    }

    /* The "Calculate" Button */
    div.stButton > button {
        background: linear-gradient(90deg, #00ffcc, #0099ff) !important;
        color: #000000 !important;
        border: none !important;
        width: 100%;
        border-radius: 50px !important;
        font-weight: 900 !important;
        padding: 20px 0 !important;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.4) !important;
        font-size: 18px !important;
        margin-top: 15px;
    }
    
    /* Input Labels */
    label { color: #00ffcc !important; font-weight: bold !important; font-size: 14px !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. FIXED LANGUAGE LOGIC
# The selectbox is at the top; the app re-renders instantly on change.
lang_choice = st.selectbox("", ["English", "Deutsch"], key="lang_toggle", label_visibility="collapsed")

# Dictionary for multi-language support
ui = {
    "English": {
        "title": "Berlin Eco-Coach AI",
        "travel": "🚗 Travel Details",
        "food": "🍔 Food Choice",
        "dist": "Distance traveled (km)",
        "mode": "Transport Mode",
        "meal": "What did you eat today?",
        "btn": "GENERATE SCORE",
        "saved": "Döner Units Saved",
        "history": "Trip History"
    },
    "Deutsch": {
        "title": "Berlin Eco-Coach AI",
        "travel": "🚗 Reise-Details",
        "food": "🍔 Essen Auswahl",
        "dist": "Reisestrecke (km)",
        "mode": "Verkehrsmittel",
        "meal": "Was hast du heute gegessen?",
        "btn": "PUNKTE GENERIEREN",
        "saved": "Döner-Einheiten gespart",
        "history": "Verlauf"
    }
}[lang_choice]

st.markdown(f'<div class="app-title">{ui["title"]}</div>', unsafe_allow_html=True)

# 5. INPUT GRID (Restructured for symmetry)
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {ui['travel']}")
    distance = st.number_input(ui["dist"], min_value=0.0, step=0.1, key="dist_val")
    transport = st.selectbox(ui["mode"], ["U-Bahn / S-Bahn", "Car (Petrol)", "Car (Electric)", "Bike", "Walking"], key="trans_val")

with col2:
    st.markdown(f"### {ui['food']}")
    # Expanded Food List as requested
    meal = st.selectbox(ui["meal"], [
        "Vegan Döner (0.1kg)", 
        "Chicken Döner (2.2kg)", 
        "Beef Döner (4.5kg)", 
        "Beef Burger (3.8kg)",
        "Cheeseburger (4.2kg)",
        "Veggie Burger (1.2kg)",
        "Currywurst (2.1kg)",
        "Halloumi Burger (1.2kg)",
        "Club Mate (0.1kg)"
    ], key="meal_val")

# 6. CALCULATION ENGINE
if st.button(ui["btn"]):
    # Map transport to CO2 per km
    t_map = {"Car (Petrol)": 0.2, "Car (Electric)": 0.05, "U-Bahn / S-Bahn": 0.03, "Bike": 0.0, "Walking": 0.0}
    
    # Map meal to fixed CO2 values
    f_map = {
        "Vegan Döner (0.1kg)": 0.1, "Chicken Döner (2.2kg)": 2.2, "Beef Döner (4.5kg)": 4.5,
        "Beef Burger (3.8kg)": 3.8, "Cheeseburger (4.2kg)": 4.2, "Veggie Burger (1.2kg)": 1.2,
        "Currywurst (2.1kg)": 2.1, "Halloumi Burger (1.2kg)": 1.2, "Club Mate (0.1kg)": 0.1
    }
    
    # Update Session State
    st.session_state.total_co2 = (distance * t_map[transport]) + f_map[meal]
    st.session_state.doner_units = st.session_state.total_co2 / 4.5
    
    # Log to history
    st.session_state.history.append({
        "Mode": transport, 
        "Food": meal.split(" (")[0], 
        "CO2 (kg)": round(st.session_state.total_co2, 2)
    })

# 7. MAIN DISPLAY (Dynamic Neon Box)
st.markdown(f"""
    <div class="score-box">
        <h1 class="main-val">{st.session_state.total_co2:.1f} kg CO2</h1>
        <p class="sub-val">🥙 {st.session_state.doner_units:.1f} {ui['saved']}</p>
    </div>
    """, unsafe_allow_html=True)

# 8. ANALYTICS (Hidden by default in an expander)
if st.session_state.history:
    with st.expander(f"📊 {ui['history']}"):
        st.table(pd.DataFrame(st.session_state.history))
