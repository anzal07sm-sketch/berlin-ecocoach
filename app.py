import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Berlin EcoCoach AI", page_icon="🥙", layout="centered")

# 2. SESSION MEMORY
if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []

# 3. CLUB-MODE CSS (Removing all ghost bars and labels)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* REMOVE GHOST BARS & LABELS */
    label { display: none !important; }
    .block-container { padding-top: 2rem !important; }

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

    /* GREEN CALCULATE BUTTON */
    .stButton>button {
        background-color: #66BB6A !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 14px !important;
        font-weight: bold !important;
        width: 100%;
        font-size: 1.1rem;
    }

    /* PINK RESULT BOX (HERO FEEDBACK) */
    .hero-box {
        border: 2px solid #FF00FF;
        border-radius: 15px;
        padding: 20px;
        background: rgba(255, 0, 255, 0.05);
        text-align: center;
        margin-bottom: 20px;
    }
    
    .doner-stat {
        color: #FFD700;
        font-size: 1.5rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. HEADER
st.markdown('<h1 class="neon-header">Berlin EcoCoach AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>New Year, Same VibG🌿 2026 Climate Legends</p>", unsafe_allow_html=True)

# 5. INPUT DASHBOARD
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# TRAVEL SECTION
st.write("### 🚗 1. Travel Details")
st.write("<small>Distance (km)</small>", unsafe_allow_html=True)
dist = st.number_input("Dist", min_value=0.0, step=0.1, key="dist_val", label_visibility="collapsed")
mode = st.selectbox("Mode", ["Techno-Train (S-Bahn)", "Car / Auto", "Bike / Fahrrad"], key="mode_val", label_visibility="collapsed")

# FOOD SECTION
st.write("### 🥙 2. Food Choice")
st.write("<small>What did you eat?</small>", unsafe_allow_html=True)
food_item = st.selectbox("Food", ["Vegan Döner", "Chicken Döner", "Beef Döner", "No Food"], key="food_val", label_visibility="collapsed")

calculate = st.button("Calculate button")
st.markdown('</div>', unsafe_allow_html=True)

# 6. CALCULATION LOGIC (THE DÖNER UNIT)
if calculate:
    # Math Factors
    travel_map = {"Car / Auto": 0.2, "Techno-Train (S-Bahn)": 0.03, "Bike / Fahrrad": 0.0}
    food_map = {"Vegan Döner": 0.5, "Chicken Döner": 2.2, "Beef Döner": 4.5, "No Food": 0.0}
    
    # Total CO2 calculation
    res_co2 = (dist * travel_map[mode]) + food_map[food_item]
    
    # Döner Comparison (1 Beef Döner = 4.5kg CO2)
    # This shows how many "Döners" your trip is worth
    doner_equiv = res_co2 / 4.5 

    st.session_state.trip_history.append({
        "Mode": mode, 
        "Food": food_item, 
        "CO2 (kg)": round(res_co2, 2),
        "Döner Units": round(doner_equiv, 2)
    })

    # 7. PINK HERO BOX RESULT
    st.markdown(f"""
        <div class="hero-box">
            <h3 style="color:#FF00FF; margin:0;">✅ Berlin Eco-Hero! 😂</h3>
            <p style="margin:10px; font-size:1.2rem;">Impact: <b>{res_co2:.2f} kg CO2</b></p>
            <div class="doner-stat">🥙 {doner_equiv:.2f} Döner Units</div>
            <p style="font-size:0.9rem; color:#aaa;">(1 Unit = 4.5kg CO2 footprint of 1 Beef Döner)</p>
            <hr style="border:0.5px solid #30363D;">
            <p style="font-size:0.8rem; color:#888;">#BerlinEcoCoach #DönerComparison</p>
        </div>
    """, unsafe_allow_html=True)
    
    if res_co2 < 1.0:
        st.balloons()

# 8. ANALYTICS DASHBOARD
if st.session_state.trip_history:
    df = pd.DataFrame(st.session_state.trip_history)
    total_co2 = df["CO2 (kg)"].sum()
    total_doners = df["Döner Units"].sum()

    st.markdown(f"""
        <div style="background:#00FFCC; color:black; padding:20px; border-radius:15px; text-align:center; margin-top:20px;">
            <p style="margin:0; font-weight:bold;">YOUR TOTAL DAILY IMPACT</p>
            <h1 style="margin:0; font-size:3rem;">{total_co2:.2f} kg CO2</h1>
            <h2 style="margin:0; color:#050505;">≈ {total_doners:.1f} Döners worth</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("### History Log")
    st.dataframe(df, use_container_width=True)
