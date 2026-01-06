import streamlit as st
import pandas as pd
import urllib.parse

# 1. PAGE CONFIG
st.set_page_config(page_title="Berlin Eco-Coach AI", layout="centered")

# 2. STATE MEMORY
if 'total_co2' not in st.session_state:
    st.session_state.total_co2 = 0.0
if 'doner_units' not in st.session_state:
    st.session_state.doner_units = 0.0
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. FORCED CYBERPUNK CSS (Forcing the IMG_7136 Look)
st.markdown("""
    <style>
    /* Full Page Background */
    .stApp {
        background: radial-gradient(circle at center, #2e0259 0%, #05010a 100%) !important;
        background-attachment: fixed !important;
    }

    /* Hide Headers */
    header, footer, .stDeployButton { visibility: hidden !important; }
    
    /* App Title */
    .app-title {
        text-align: center;
        letter-spacing: 2px;
        font-size: 14px;
        font-weight: bold;
        color: #ffffff;
        text-transform: uppercase;
        margin-top: 10px;
    }

    /* Score Box Area */
    .score-box {
        text-align: center;
        padding: 40px 0;
    }
    .main-val {
        font-size: 72px;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.8);
        margin: 0;
    }
    .sub-val {
        color: #ff00ff;
        font-size: 20px;
        font-weight: bold;
    }

    /* Floating Glass Cards */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 25px !important;
    }

    /* Neon Action Button */
    div.stButton > button {
        background: linear-gradient(90deg, #00ffff, #00d4ff) !important;
        color: #000000 !important;
        border: none !important;
        width: 100%;
        border-radius: 50px !important;
        font-weight: 900 !important;
        padding: 18px 0 !important;
        box-shadow: 0 0 35px rgba(0, 255, 255, 0.6) !important;
        margin-top: 20px;
        text-transform: uppercase;
    }

    /* Share Icons */
    .social-bar {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 40px;
        font-size: 28px;
    }
    .social-bar a { text-decoration: none; color: #00ffff !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. LANGUAGE SELECTOR
lang = st.selectbox("", ["English", "Deutsch"], label_visibility="collapsed")

st.markdown('<div class="app-title">BERLIN ECO-COACH AI</div>', unsafe_allow_html=True)

# 5. INPUT GRID (Aligned as requested)
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚗 Travel")
    dist = st.number_input("Distance (km)", min_value=0.0, step=0.1, key="dist")
    mode = st.selectbox("Transport", ["S-Bahn/U-Bahn", "Car", "Bike", "Walking"], key="mode")

with col2:
    st.markdown("### 🍔 Food")
    food = st.selectbox("Your Meal", ["Vegan Döner", "Beef Döner", "Chicken Döner", "Currywurst", "Halloumi Burger"], key="food")

# 6. CALCULATION LOGIC
if st.button("GENERATE SCORE"):
    t_map = {"Car": 0.2, "S-Bahn/U-Bahn": 0.03, "Bike": 0.0, "Walking": 0.0}
    f_map = {"Vegan Döner": 0.1, "Beef Döner": 4.5, "Chicken Döner": 2.2, "Currywurst": 2.1, "Halloumi Burger": 1.2}
    
    st.session_state.total_co2 = (dist * t_map[mode]) + f_map[food]
    st.session_state.doner_units = st.session_state.total_co2 / 4.5
    st.session_state.history.append({"Mode": mode, "Food": food, "CO2": st.session_state.total_co2})

# 7. MAIN DISPLAY
st.markdown(f"""
    <div class="score-box">
        <h1 class="main-val">{st.session_state.total_co2:.1f} kg CO2</h1>
        <p class="sub-val">🥙 {st.session_state.doner_units:.1f} Döner Units Saved</p>
    </div>
    """, unsafe_allow_html=True)

# 8. FUNCTIONAL SHARE BAR (No special modules needed)
msg = urllib.parse.quote(f"My Berlin Eco-Score is {st.session_state.total_co2:.1f}kg CO2! Check yours on EcoCoach!")
st.markdown(f"""
    <div class="social-bar">
        <a href="https://wa.me/?text={msg}" target="_blank">💬</a>
        <a href="https://twitter.com/intent/tweet?text={msg}" target="_blank">🐦</a>
        <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://ecocoach.berlin" target="_blank">in</a>
        <span style="color:white; font-size:12px; font-weight:bold; letter-spacing:1px; margin-left:15px;">SHARE ⚑</span>
    </div>
    """, unsafe_allow_html=True)

# 9. HISTORY DRAWER
if st.session_state.history:
    with st.expander("📊 Analytics History"):
        st.table(pd.DataFrame(st.session_state.history))
