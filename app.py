import streamlit as st
import pandas as pd

# 1. PAGE CONFIG
st.set_page_config(page_title="Berlin EcoCoach AI", page_icon="🌿", layout="centered")

# 2. SESSION MEMORY
if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []

# 3. THE "CLUB MODE" ULTIMATE CSS
# This fixes the background, removes the empty bars, and creates the neon glow
st.markdown("""
    <style>
    /* 1. Immersive Club Background */
    .stApp {
        background: radial-gradient(circle at top, #1b2735 0%, #050505 100%) !important;
        color: #FFFFFF !important;
    }
    
    /* 2. Remove all ghost bars, headers, and empty space */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    .block-container { padding-top: 1rem !important; }
    label { display: none !important; }
    [data-testid="stVerticalBlock"] > div:empty { display: none !important; }
    
    /* 3. Neon Header Styling */
    .neon-header {
        color: #00FFCC;
        text-shadow: 0 0 20px #00FFCC;
        font-weight: bold;
        font-size: 2.8rem;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-text {
        text-align: center;
        color: #888;
        font-style: italic;
        margin-bottom: 25px;
    }

    /* 4. Glassmorphism Card (The Dashboard) */
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(0, 255, 204, 0.2);
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
    }

    /* 5. The Emerald Green Calculate Button */
    .stButton>button {
        background: linear-gradient(90deg, #66BB6A 0%, #43A047 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 15px !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        width: 100%;
        box-shadow: 0 0 15px rgba(102, 187, 106, 0.4);
    }

    /* 6. Neon Pink Hero Result Box */
    .hero-box {
        border: 2px solid #FF00FF;
        border-radius: 20px;
        padding: 20px;
        background: rgba(255, 0, 255, 0.08);
        text-align: center;
        margin-top: 25px;
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
    }

    /* 7. Social Button Styling */
    .social-btn {
        background: #FFFFFF;
        color: #000000 !important;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
        margin: 5px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. LANGUAGE SELECTOR 
lang = st.selectbox("", ["English", "Deutsch"], key="lang_select")

# 5. TRANSLATIONS
texts = {
    "English": {
        "title": "Berlin EcoCoach AI",
        "sub": "New Year, Same VibG🌿 2026 for Climate Legends!",
        "dist": "Distance traveled (km)",
        "food": "Berlin Food Choice",
        "btn": "Calculate button",
        "total": "Your Daily Bass-print"
    },
    "Deutsch": {
        "title": "Berlin EcoCoach AI",
        "sub": "Neues Jahr, gleicher VibG🌿 2026 für Klima-Legenden!",
        "dist": "Reisestrecke (km)",
        "food": "Berlin Food Choice",
        "btn": "Berechnen",
        "total": "Dein täglicher Impact"
    }
}
t = texts[lang]

# 6. APP HEADER
st.markdown(f'<h1 class="neon-header">{t["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-text">{t["sub"]}</p>', unsafe_allow_html=True)

# 7. MAIN INPUT DASHBOARD
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.write("### 🚗 1. Travel Details")
st.write(f"<small>{t['dist']}</small>", unsafe_allow_html=True)
dist = st.number_input("", min_value=0.0, step=0.1, key="d_input", label_visibility="collapsed")
mode = st.selectbox("", ["Techno-Train (S-Bahn/U-Bahn)", "Car / Auto", "Bike / Fahrrad", "Walking"], key="m_input", label_visibility="collapsed")

st.write(f"### 🍔 2. {t['food']}")
food_item = st.selectbox("", [
    "Vegan Döner (0.1kg)", 
    "Chicken Döner (2.2kg)", 
    "Beef Döner (4.5kg)", 
    "Currywurst (2.1kg)",
    "Beef Burger (3.5kg)",
    "Vegan Burger (0.6kg)",
    "Club Mate (0.1kg)",
    "No Food Today"
], key="f_input", label_visibility="collapsed")

calculate = st.button(t["btn"])
st.markdown('</div>', unsafe_allow_html=True)

# 8. LOGIC & RESULTS
if calculate:
    # Impact Mapping
    travel_map = {"Car / Auto": 0.2, "Techno-Train (S-Bahn/U-Bahn)": 0.03, "Bike / Fahrrad": 0.0, "Walking": 0.0}
    food_map = {
        "Vegan Döner (0.1kg)": 0.1, "Chicken Döner (2.2kg)": 2.2, "Beef Döner (4.5kg)": 4.5,
        "Currywurst (2.1kg)": 2.1, "Beef Burger (3.5kg)": 3.5, "Vegan Burger (0.6kg)": 0.6,
        "Club Mate (0.1kg)": 0.1, "No Food Today": 0.0
    }
    
    trip_co2 = (dist * travel_map[mode]) + food_map[food_item]
    # Döner Conversion (1 Beef Döner = 4.5kg CO2)
    doner_conv = trip_co2 / 4.5

    # Safe History Log
    st.session_state.trip_history.append({
        "Mode": mode, 
        "Food": food_item.split(" (")[0], 
        "CO2 (kg)": round(trip_co2, 2),
        "Döner Units": round(doner_conv, 2)
    })

    # HERO BOX RESULT 
    st.markdown(f"""
        <div class="hero-box">
            <h3 style="color:#FF00FF; margin:0;">✅ Berlin Eco-Hero! 😂</h3>
            <p style="margin:10px; font-size:1.2rem;">Impact: <b>{trip_co2:.2f} kg CO2</b></p>
            <p style="color:#FFD700; font-size:1.6rem; font-weight:bold;">🥙 {doner_conv:.2f} Döner Units</p>
            <div style="display:flex; justify-content:center; gap:10px; margin-top:10px;">
                <a class="social-btn" href="#">Write on WhatsApp</a>
                <a class="social-btn" href="#">Share on Twitter</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 9. HISTORY DASHBOARD
if st.session_state.trip_history:
    df = pd.DataFrame(st.session_state.trip_history)
    total_co2 = df["CO2 (kg)"].sum()
    
    st.markdown(f"""
        <div style="background: linear-gradient(90deg, #00FFCC 0%, #0099FF 100%); color:black; padding:20px; border-radius:15px; text-align:center; margin-top:30px;">
            <p style="margin:0; font-weight:bold; letter-spacing:1px;">{t['total'].upper()}</p>
            <h1 style="margin:0; font-size:3.5rem;">{total_co2:.2f} kg</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("### 📊 Analytics Dashboard")
    st.dataframe(df, use_container_width=True)
