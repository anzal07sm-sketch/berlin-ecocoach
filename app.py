import streamlit as st
import pandas as pd
from streamlit_share import display_share

# 1. PAGE CONFIG
st.set_page_config(page_title="Berlin Eco-Coach AI", layout="centered")

# 2. STATE PRESERVATION
if 'total_co2' not in st.session_state:
    st.session_state.total_co2 = 0.0
if 'doner_units' not in st.session_state:
    st.session_state.doner_units = 0.0

# 3. FORCED CYBERPUNK CSS 
st.markdown("""
    <style>
    /* Fixed Background - No more disappearing */
    .stApp {
        background: radial-gradient(circle at center, #2e0259 0%, #05010a 100%) !important;
        background-attachment: fixed !important;
    }

    /* Clean UI - Hide Streamlit junk */
    header, footer, .stDeployButton { visibility: hidden !important; }
    .block-container { padding-top: 2rem !important; }

    /* Title Styling */
    .app-title {
        text-align: center;
        letter-spacing: 2px;
        font-size: 14px;
        font-weight: bold;
        color: #ffffff;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    /* Score Display (The Big Neon Number) */
    .score-box {
        text-align: center;
        padding: 20px 0;
    }
    .main-val {
        font-size: 65px;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 0 25px rgba(0, 255, 255, 0.7);
        margin: 0;
    }
    .sub-val {
        color: #ff00ff;
        font-size: 18px;
        font-weight: bold;
        margin-top: -10px;
    }

    /* Floating Input Cards */
    div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }

    /* The 'GENERATE SCORE' Button */
    div.stButton > button {
        background: #00ffff !important;
        color: #000000 !important;
        border: none !important;
        width: 100%;
        border-radius: 50px !important;
        font-weight: 900 !important;
        padding: 15px 0 !important;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.5) !important;
        margin-top: 30px;
    }

    /* Labels */
    label { color: #00ffff !important; font-weight: bold !important; }

    /* Functional Share Bar */
    .share-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        margin-top: 40px;
        padding: 10px;
    }
    .share-link {
        color: #00ffff !important;
        text-decoration: none;
        font-size: 24px;
        transition: 0.3s;
    }
    .share-link:hover { text-shadow: 0 0 15px #00ffff; }
    </style>
    """, unsafe_allow_html=True)

# 4. LANGUAGE & TITLE
lang = st.selectbox("", ["English", "Deutsch"], key="lang_picker", label_visibility="collapsed")
st.markdown('<div class="app-title">BERLIN ECO-COACH AI</div>', unsafe_allow_html=True)

# 5. INPUT GRID
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚗 Travel")
    dist = st.number_input("Distance (km)", min_value=0.0, step=0.1, key="dist_in")
    mode = st.selectbox("Transport", ["U-Bahn / S-Bahn", "Car", "Bike", "Walking"], key="mode_in")

with col2:
    st.markdown("### 🍔 Food")
    food = st.selectbox("Your Meal", ["Vegan Döner", "Beef Döner", "Chicken Döner", "Currywurst", "Club Mate"], key="food_in")

# 6. CALCULATOR LOGIC
if st.button("GENERATE SCORE"):
    
    travel_map = {"Car": 0.2, "U-Bahn / S-Bahn": 0.03, "Bike": 0.0, "Walking": 0.0}
    food_map = {"Vegan Döner": 0.1, "Beef Döner": 4.5, "Chicken Döner": 2.2, "Currywurst": 2.1, "Club Mate": 0.1}
    
    st.session_state.total_co2 = (dist * travel_map[mode]) + food_map[food]
    st.session_state.doner_units = st.session_state.total_co2 / 4.5

# 7. DYNAMIC SCORE DISPLAY
st.markdown(f"""
    <div class="score-box">
        <h1 class="main-val">{st.session_state.total_co2:.1f} kg CO2</h1>
        <p class="sub-val">🥙 {st.session_state.doner_units:.1f} Döner Units Saved</p>
    </div>
    """, unsafe_allow_html=True)

# 8. THE FUNCTIONAL SHARE BUTTOwebN 

share_msg = f"My Berlin footprint is {st.session_state.total_co2:.1f}kg CO2! 🥙 Check yours at EcoCoach!"
whatsapp_link = f"https://wa.me/?text={share_msg}"
twitter_link = f"https://twitter.com/intent/tweet?text={share_msg}"

st.markdown(f"""
    <div class="share-container">
        <a href="{whatsapp_link}" target="_blank" class="share-link">💬</a>
        <a href="{twitter_link}" target="_blank" class="share-link">🐦</a>
        <a href="https://www.linkedin.com" target="_blank" class="share-link">in</a>
        <span style="color:white; font-size:12px; font-weight:bold; letter-spacing:1px; margin-left:10px;">SHARE ⚑</span>
    </div>
    """, unsafe_allow_html=True)
