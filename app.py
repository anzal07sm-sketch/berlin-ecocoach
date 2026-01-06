import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Berlin Eco-Coach AI", layout="centered")

# 2. SESSION MEMORY 
if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []

# 3. PERFECT ALIGNMENT & CLUB BACKGROUND CSS
st.markdown("""
    <style>
    /* Full Page Background */
    .stApp {
        background: radial-gradient(circle at center, #1b0238 0%, #05010a 100%) !important;
        background-attachment: fixed;
        color: #FFFFFF !important;
    }

    /* Hide Streamlit default clutter */
    header, footer, .stDeployButton { visibility: hidden !important; }
    .block-container { padding-top: 1.5rem !important; }
    
    /* Neon Header Styling */
    .app-title {
        text-align: center;
        letter-spacing: 2px;
        font-size: 14px;
        font-weight: bold;
        text-transform: uppercase;
        color: rgba(0, 255, 204, 0.8);
        margin-bottom: 30px;
    }

    /* Big Neon Score */
    .score-container {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    .main-score {
        font-size: 68px;
        font-weight: 800;
        margin: 0;
        color: #ffffff;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.8);
    }
    .sub-score {
        color: #ff00ff;
        font-size: 20px;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
    }

    /* Clean Card Styling for Inputs */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }

    /* The 'Generate' Button */
    div.stButton > button {
        background: linear-gradient(90deg, #00ffff, #00d4ff) !important;
        color: #000 !important;
        border: none !important;
        width: 100%;
        border-radius: 50px !important;
        font-weight: 900 !important;
        padding: 15px 0 !important;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
        margin-top: 40px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 40px rgba(0, 255, 255, 0.7);
    }

    /* Social Bar */
    .social-footer {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 25px;
        margin-top: 40px;
        color: #00ffff;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. TOP NAV (Language)
lang = st.selectbox("Language / Sprache", ["English", "Deutsch"], label_visibility="collapsed")

st.markdown('<div class="app-title">BERLIN ECO-COACH AI</div>', unsafe_allow_html=True)

# 5. INPUT GRID 
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚗 Travel")
    dist = st.number_input("Distance (km)", min_value=0.0, step=0.1, key="dist_final")
    mode = st.selectbox("Transport", ["U-Bahn / S-Bahn", "Car", "Bike", "Walking"], key="mode_final")

with col2:
    st.markdown("### 🍔 Food")
    food_item = st.selectbox("Your Meal", [
        "Vegan Döner", 
        "Chicken Döner", 
        "Beef Döner", 
        "Currywurst", 
        "Beef Burger", 
        "Halloumi Burger"
    ], key="food_final")
    st.markdown("<br>", unsafe_allow_html=True) 

# 6. ACTION BUTTON
calculate = st.button("GENERATE SCORE")

# 7. LOGIC & RESULT RENDERING

res_co2 = 0.0
doner_val = 0.0

if calculate:
    # Calculations
    travel_map = {"Car": 0.2, "U-Bahn / S-Bahn": 0.03, "Bike": 0.0, "Walking": 0.0}
    food_map = {
        "Vegan Döner": 0.1, "Chicken Döner": 2.2, "Beef Döner": 4.5,
        "Currywurst": 2.1, "Beef Burger": 3.8, "Halloumi Burger": 1.2
    }
    
    res_co2 = (dist * travel_map[mode]) + food_map[food_item]
    doner_val = res_co2 / 4.5 # 1 Beef Doner = 4.5kg CO2
    
    # Save to history
    st.session_state.trip_history.append({
        "Mode": mode, 
        "Food": food_item, 
        "CO2": round(res_co2, 2),
        "Döner Units": round(doner_val, 2)
    })

# THE HERO DISPLAY
st.markdown(f"""
    <div class="score-container">
        <h1 class="main-score">{res_co2:.1f} kg CO2</h1>
        <p class="sub-score">🥙 {doner_val:.1f} Döner Units</p>
    </div>
    """, unsafe_allow_html=True)

# 8. SOCIAL FOOTER
st.markdown("""
    <div class="social-footer">
        <span>💬</span> <span>🐦</span> <span>in</span>
        <span style="font-size:12px; color:white; font-weight:bold; letter-spacing:1px; margin-left:10px;">SHARE ⚑</span>
    </div>
    """, unsafe_allow_html=True)

# 9. ANALYTICS 
if st.session_state.trip_history:
    with st.expander("View Daily History"):
        st.table(pd.DataFrame(st.session_state.trip_history))
