import streamlit as st
import pandas as pd

# 1. PAGE CONFIG
st.set_page_config(page_title="Berlin EcoCoach AI", page_icon="🌿", layout="centered")

# 2. SESSION MEMORY
if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []

# 3. THE "PERFECT LOOK" CSS
# This removes all ghost bars and matches the neon aesthetic
st.markdown("""
    <style>
    /* Dark Theme */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* 100% REMOVE GHOST BARS AND LABELS */
    label, [data-testid="stSidebarNav"] { display: none !important; }
    header {visibility: hidden;}
    .block-container { padding-top: 1rem !important; }
    [data-testid="stVerticalBlock"] > div:empty { display: none !important; }

    /* DASHBOARD CARD */
    .main-card {
        background: #1A1C23;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #30363D;
        margin-bottom: 20px;
    }

    /* NEON TITLES */
    .neon-header {
        color: #00FFCC;
        text-shadow: 0 0 10px #00FFCC;
        font-weight: bold;
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 0px;
    }

    /* THE GREEN BUTTON FROM YOUR FOTO */
    .stButton>button {
        background-color: #66BB6A !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        width: 100%;
        margin-top: 10px;
    }

    /* PINK RESULT BOX (HERO BOX) */
    .hero-box {
        border: 2px solid #FF00FF;
        border-radius: 15px;
        padding: 15px;
        background: rgba(255, 0, 255, 0.05);
        text-align: center;
    }

    /* SOCIAL LINKS */
    .social-btn {
        background: #FFFFFF;
        color: #000000 !important;
        padding: 5px 12px;
        border-radius: 5px;
        text-decoration: none;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. CONTENT HEADERS
st.markdown('<h1 class="neon-header">Berlin EcoCoach AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>New Year, Same VibG🌿 2026 for Climate Legends!</p>", unsafe_allow_html=True)

# 5. INPUT DASHBOARD
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Section 1: Travel
st.write("### 🚗 1. Travel Details")
st.write("<small>Distance (km)</small>", unsafe_allow_html=True)
dist = st.number_input("d", min_value=0.0, step=0.1, key="d_val", label_visibility="collapsed")
mode = st.selectbox("m", ["Techno-Train (S-Bahn/U-Bahn)", "Car / Auto", "Bike / Fahrrad"], key="m_val", label_visibility="collapsed")

# Section 2: Food
st.write("### 🥙 2. Food Choice")
st.write("<small>Carbon footprint of your lunch?</small>", unsafe_allow_html=True)
food_item = st.selectbox("f", ["Vegan Döner", "Chicken Döner (Basic)", "Beef Döner", "No Food Today"], key="f_val", label_visibility="collapsed")

calculate = st.button("Calculate button")
st.markdown('</div>', unsafe_allow_html=True)

# 6. CALCULATIONS
if calculate:
    # Math Factors
    travel_map = {"Car / Auto": 0.2, "Techno-Train (S-Bahn/U-Bahn)": 0.03, "Bike / Fahrrad": 0.0}
    food_map = {"Vegan Döner": 0.1, "Chicken Döner (Basic)": 4.5, "Beef Döner": 4.5, "No Food Today": 0.0}
    
    trip_co2 = (dist * travel_map[mode]) + food_map[food_item]
    # Döner Comparison (Based on Beef Döner = 4.5kg)
    doner_val = trip_co2 / 4.5

    # Store in history
    st.session_state.trip_history.append({
        "Mode": mode, 
        "Food": food_item, 
        "CO2 (kg)": round(trip_co2, 2),
        "Döner Units": round(doner_val, 2)
    })

    # RESULT PINK BOX (Matches IMG_7132)
    st.markdown(f"""
        <div class="hero-box">
            <h3 style="color:#FF00FF; margin:0;">✅ Berlin Eco-Hero! 😂</h3>
            <p style="margin:10px;">Impact: <b>{trip_co2:.2f} kg CO2</b></p>
            <p style="color:#FFD700; font-size:1.4rem;">🥙 <b>{doner_val:.2f} Döners</b></p>
            <div style="display:flex; justify-content:center; gap:5px;">
                <a class="social-btn" href="#">Write on WhatsApp</a>
                <a class="social-btn" href="#">Share on Twitter</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 7. ANALYTICS (Bottom Table)
if st.session_state.trip_history:
    df = pd.DataFrame(st.session_state.trip_history)
    total_co2 = df["CO2 (kg)"].sum()
    
    st.markdown(f"""
        <div style="background:#00FFCC; color:black; padding:15px; border-radius:10px; text-align:center; margin-top:20px;">
            <p style="margin:0; font-weight:bold;">YOUR TOTAL BASS-PRINT</p>
            <h1 style="margin:0;">{total_co2:.2f} kg</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df, use_container_width=True)
