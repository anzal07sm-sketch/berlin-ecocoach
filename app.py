import streamlit as st
import pandas as pd
import urllib.parse

# 1. PAGE CONFIG
st.set_page_config(page_title="Berlin Eco-Coach AI", layout="centered")

# 2. SESSION STATE 
if 'history' not in st.session_state:
    st.session_state.history = []
if 'res_co2' not in st.session_state:
    st.session_state.res_co2 = 0.0
if 'doner_val' not in st.session_state:
    st.session_state.doner_val = 0.0

# 3. CSS
st.markdown("""
    <style>
    /* Full Page Immersive Background - Forced */
    .stApp {
        background: radial-gradient(circle at center, #1b0238 0%, #05010a 100%) !important;
        background-attachment: fixed !important;
        color: #FFFFFF !important;
    }

    /* Hide Headers & UI Clutter */
    header, footer, .stDeployButton { visibility: hidden !important; }
    .block-container { padding-top: 2rem !important; }
    
    /* Neon Text Styles */
    .app-title {
        text-align: center;
        letter-spacing: 3px;
        font-size: 16px;
        font-weight: bold;
        color: #00ffff;
        text-shadow: 0 0 10px #00ffff;
        margin-bottom: 30px;
    }

    .main-score {
        font-size: 72px;
        font-weight: 800;
        text-align: center;
        margin: 0;
        color: white;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.8);
    }

    .sub-score {
        text-align: center;
        color: #ff00ff;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 40px;
    }

    /* Card Alignment Fix */
    div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 25px !important;
    }

    /* Custom Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #00ffff, #0088ff) !important;
        color: black !important;
        border: none !important;
        width: 100%;
        border-radius: 50px !important;
        font-weight: 900 !important;
        padding: 20px 0 !important;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.5) !important;
        font-size: 18px !important;
    }
    
    /* Social Bar Styling */
    .social-bar {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 50px;
        font-size: 24px;
    }
    .social-bar a { text-decoration: none; color: #00ffff !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. LANGUAGE LOGIC
lang = st.selectbox("", ["English", "Deutsch"], key="lang_select", label_visibility="collapsed")

t = {
    "English": {
        "title": "BERLIN ECO-COACH AI",
        "travel": "🚗 Travel",
        "food": "🍔 Food",
        "dist": "Distance (km)",
        "mode": "Transport Mode",
        "meal": "Your Meal",
        "btn": "GENERATE SCORE",
        "share": "SHARE IT"
    },
    "Deutsch": {
        "title": "BERLIN ECO-COACH AI",
        "travel": "🚗 Reise",
        "food": "🍔 Essen",
        "dist": "Entfernung (km)",
        "mode": "Verkehrsmittel",
        "meal": "Deine Mahlzeit",
        "btn": "PUNKTE GENERIEREN",
        "share": "TEILEN"
    }
}[lang]

st.markdown(f'<div class="app-title">{t["title"]}</div>', unsafe_allow_html=True)

# 5. INPUT GRID 
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {t['travel']}")
    dist = st.number_input(t["dist"], min_value=0.0, step=0.1, key="d_val")
    mode = st.selectbox(t["mode"], ["U-Bahn / S-Bahn", "Car", "Bike", "Walking"], key="m_val")

with col2:
    st.markdown(f"### {t['food']}")
    food_item = st.selectbox(t["meal"], [
        "Vegan Döner", "Chicken Döner", "Beef Döner", 
        "Currywurst", "Beef Burger", "Halloumi Burger", "Club Mate"
    ], key="f_val")

# 6. CALCULATOR ENGINE
if st.button(t["btn"]):
    travel_map = {"Car": 0.2, "U-Bahn / S-Bahn": 0.03, "Bike": 0.0, "Walking": 0.0}
    food_map = {
        "Vegan Döner": 0.1, "Chicken Döner": 2.2, "Beef Döner": 4.5,
        "Currywurst": 2.1, "Beef Burger": 3.8, "Halloumi Burger": 1.2, "Club Mate": 0.1
    }
    
    st.session_state.res_co2 = (dist * travel_map[mode]) + food_map[food_item]
    st.session_state.doner_val = st.session_state.res_co2 / 4.5
    
    st.session_state.history.append({
        "Mode": mode, "Food": food_item, "CO2": st.session_state.res_co2
    })

# 7. DYNAMIC SCORE DISPLAY
st.markdown(f'<h1 class="main-score">{st.session_state.res_co2:.1f} kg CO2</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-score">🥙 {st.session_state.doner_val:.1f} Döner Units Saved</div>', unsafe_allow_html=True)

# 8. FUNCTIONAL SHARE BUTTONS
share_text = f"My Berlin Carbon Footprint is {st.session_state.res_co2:.1f}kg CO2! Check yours on Berlin EcoCoach!"
encoded_text = urllib.parse.quote(share_text)

whatsapp_url = f"https://wa.me/?text={encoded_text}"
twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"

st.markdown(f"""
    <div class="social-bar">
        <a href="{whatsapp_url}" target="_blank"></a>
        <a href="{twitter_url}" target="_blank"></a>
        <a href="#" style="font-size: 14px; font-weight: bold; margin-left: 20px;">{t['share']} ⚑</a>
    </div>
    """, unsafe_allow_html=True)

# 9. ANALYTICS DRAWER
if st.session_state.history:
    with st.expander("📊 Analytics History"):
        st.table(pd.DataFrame(st.session_state.history))
