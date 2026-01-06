import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Berlin EcoCoach AI", page_icon="🌿", layout="centered")

# 2. SESSION MEMORY
if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []

# 3. ADVANCED CLUB-MODE CSS (No ghost bars, Neon Glow)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* HIDE GHOST LABELS & FIX PADDING */
    label { display: none !important; }
    .block-container { padding-top: 1.5rem !important; }

    /* DASHBOARD CARDS */
    .main-card {
        background: #1A1C23;
        border-radius: 15px;
        padding: 25px;
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
    }

    /* THE GREEN CALCULATE BUTTON (From IMG_7132) */
    .stButton>button {
        background-color: #66BB6A !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 14px !important;
        font-weight: bold !important;
        width: 100%;
        font-size: 1.1rem;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #81C784 !important;
        box-shadow: 0 0 15px #66BB6A;
    }

    /* RESULT HERO BOX */
    .hero-box {
        border: 2px solid #FF00FF;
        border-radius: 15px;
        padding: 20px;
        background: rgba(255, 0, 255, 0.05);
        text-align: center;
        margin-bottom: 20px;
    }

    /* SOCIAL BUTTONS */
    .social-link {
        display: inline-block;
        background: #FFFFFF;
        color: #000000 !important;
        padding: 8px 15px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.8rem;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR SETTINGS
with st.sidebar:
    st.header("VibG Settings 2026")
    lang = st.selectbox("Language", ["English", "Deutsch"])

# 5. HEADER
st.markdown('<h1 class="neon-header">Berlin EcoCoach AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>New Year, Same VibG🌿 2026 Climate Legends</p>", unsafe_allow_html=True)

# 6. INPUT DASHBOARD (Travel & Food)
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.write("### 🏎️ 1. Travel Details")
st.write("<small>Distance (km)</small>", unsafe_allow_html=True)
dist = st.number_input("Dist", min_value=0.0, step=0.1, key="dist_final", label_visibility="collapsed")
mode = st.selectbox("Mode", ["Techno-Train (S-Bahn/U-Bahn)", "Car / Auto", "Bike / Fahrrad"], key="mode_final", label_visibility="collapsed")

st.write("### 🥙 2. Food Choice")
st.write("<small>Carbon footprint of your lunch?</small>", unsafe_allow_html=True)
food_item = st.selectbox("Food", ["Vegan Döner", "Chicken Döner", "Beef Döner", "No Food"], key="food_final", label_visibility="collapsed")

calculate = st.button("Calculate button")
st.markdown('</div>', unsafe_allow_html=True)

# 7. LOGIC & DÖNER COMPARISON
if calculate:
    # Calculations
    travel_map = {"Car / Auto": 0.2, "Techno-Train (S-Bahn)": 0.03, "Bike / Fahrrad": 0.0}
    food_map = {"Vegan Döner": 0.5, "Chicken Döner": 2.2, "Beef Döner": 4.5, "No Food": 0.0}
    
    trip_co2 = (dist * travel_map[mode]) + food_map[food_item]
    # 1 Döner Unit = 4.5kg CO2
    doner_units = trip_co2 / 4.5

    # Append to History
    st.session_state.trip_history.append({
        "Mode": mode, 
        "Food": food_item, 
        "CO2 (kg)": round(trip_co2, 2),
        "Döner Units": round(doner_units, 2)
    })

    # RESULT HERO BOX 
    st.markdown(f"""
        <div class="hero-box">
            <h3 style="color:#FF00FF; margin:0;">✅ Berlin Eco-Hero! 😂</h3>
            <p style="margin:10px; font-size:1.2rem;">Impact: <b>{trip_co2:.2f} kg CO2</b></p>
            <p style="color:#FFD700; font-size:1.5rem; font-weight:bold;">🥙 {doner_units:.2f} Döner Units</p>
            <hr style="border:0.5px solid #30363D;">
            <a class="social-link" href="#">Write on WhatsApp</a>
            <a class="social-link" href="#">Share on Twitter</a>
        </div>
    """, unsafe_allow_html=True)
    
    if trip_co2 < 1.0: st.balloons()

# 8. ANALYTICS DASHBOARD (The Data Table)
if st.session_state.trip_history:
    df = pd.DataFrame(st.session_state.trip_history)
    
    # FIXED ERROR HERE: Checking if column exists before summing
    total_co2 = df["CO2 (kg)"].sum()
    total_doners = df["Döner Units"].sum() if "Döner Units" in df.columns else 0

    st.markdown(f"""
        <div style="background:#00FFCC; color:black; padding:20px; border-radius:15px; text-align:center; margin-top:20px;">
            <p style="margin:0; font-weight:bold; text-transform:uppercase;">Your Daily Bass-print</p>
            <h1 style="margin:0; font-size:3.5rem;">{total_co2:.2f} kg</h1>
            <h3 style="margin:0;">≈ {total_doners:.1f} Döners of CO2</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("### 📈 Trip History")
    st.dataframe(df, use_container_width=True)
