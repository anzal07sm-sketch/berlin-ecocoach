import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Berlin EcoCoach AI", page_icon="🌿", layout="centered")

# 2. SESSION MEMORY
if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []

# 3. ADVANCED "NO-GAP" CSS
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* REMOVES THE EMPTY BAR AND TOP SPACING */
    .block-container { padding-top: 1rem !important; }
    header { visibility: hidden; }
    label { display: none !important; }
    [data-testid="stVerticalBlock"] > div:empty { display: none !important; }

    /* NEON HEADER STYLING */
    .neon-header {
        color: #00FFCC;
        text-shadow: 0 0 15px #00FFCC;
        font-weight: bold;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: -10px;
    }
    .sub-text {
        text-align: center;
        color: #888;
        margin-bottom: 20px;
    }

    /* GLASS DASHBOARD CARD */
    .main-card {
        background: #1A1C23;
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #30363D;
        margin-bottom: 20px;
    }

    /* THE GREEN CALCULATE BUTTON */
    .stButton>button {
        background-color: #66BB6A !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        width: 100%;
        margin-top: 15px;
    }

    /* PINK RESULT BOX (FROM YOUR PHOTO) */
    .hero-box {
        border: 2px solid #FF00FF;
        border-radius: 15px;
        padding: 20px;
        background: rgba(255, 0, 255, 0.05);
        text-align: center;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);
    }
    
    .social-btn {
        background: #FFFFFF;
        color: #000000 !important;
        padding: 5px 12px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.8rem;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. LANGUAGE SELECTOR 
lang = st.selectbox("Language / Sprache", ["English", "Deutsch"], key="lang_select")

# 5. TRANSLATION LOGIC
texts = {
    "English": {
        "title": "Berlin EcoCoach AI",
        "sub": "New Year, Same VibG🌿 2026 for Climate Legends!",
        "dist": "Distance traveled (km)",
        "food": "What did you eat today?",
        "btn": "Calculate button",
        "total": "Your Daily Bass-print"
    },
    "Deutsch": {
        "title": "Berlin EcoCoach AI",
        "sub": "Neues Jahr, gleicher VibG🌿 2026 für Klima-Legenden!",
        "dist": "Reisestrecke (km)",
        "food": "Was hast du heute gegessen?",
        "btn": "Berechnen",
        "total": "Dein täglicher Impact"
    }
}
t = texts[lang]

# 6. HEADER
st.markdown(f'<h1 class="neon-header">{t["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-text">{t["sub"]}</p>', unsafe_allow_html=True)

# 7. INPUT DASHBOARD
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.write(f"### 🚗 1. Travel Details")
st.write(f"<small>{t['dist']}</small>", unsafe_allow_html=True)
dist = st.number_input("d", min_value=0.0, step=0.1, key="d_v", label_visibility="collapsed")
mode = st.selectbox("m", ["Techno-Train (S-Bahn/U-Bahn)", "Car / Auto", "Bike / Fahrrad", "Walking"], key="m_v", label_visibility="collapsed")

st.write(f"### 🍔 2. Berlin Food Choice")
st.write(f"<small>{t['food']}</small>", unsafe_allow_html=True)
food_item = st.selectbox("f", [
    "Vegan Döner (0.1kg)", 
    "Chicken Döner (2.2kg)", 
    "Beef Döner (4.5kg)", 
    "Currywurst (2.1kg)",
    "Beef Burger (3.8kg)",
    "Halloumi Burger (1.2kg)",
    "No Food Today"
], key="f_v", label_visibility="collapsed")

calculate = st.button(t["btn"])
st.markdown('</div>', unsafe_allow_html=True)

# 8. CALCULATION LOGIC
if calculate:
    # Math mapping
    travel_map = {"Car / Auto": 0.2, "Techno-Train (S-Bahn/U-Bahn)": 0.03, "Bike / Fahrrad": 0.0, "Walking": 0.0}
    food_map = {
        "Vegan Döner (0.1kg)": 0.1, "Chicken Döner (2.2kg)": 2.2, "Beef Döner (4.5kg)": 4.5,
        "Currywurst (2.1kg)": 2.1, "Beef Burger (3.8kg)": 3.8, "Halloumi Burger (1.2kg)": 1.2,
        "No Food Today": 0.0
    }
    
    trip_co2 = (dist * travel_map[mode]) + food_map[food_item]
    # Döner Conversion (Base: Beef Döner = 4.5kg)
    doner_units = trip_co2 / 4.5

    # Safe History Append
    st.session_state.trip_history.append({
        "Mode": mode, 
        "Food": food_item, 
        "CO2 (kg)": round(trip_co2, 2),
        "Döner Units": round(doner_units, 2)
    })

    # RESULT PINK BOX 
    st.markdown(f"""
        <div class="hero-box">
            <h3 style="color:#FF00FF; margin:0;">✅ Berlin Eco-Hero! 😂</h3>
            <p style="margin:10px;">Impact: <b>{trip_co2:.2f} kg CO2</b></p>
            <p style="color:#FFD700; font-size:1.5rem; font-weight:bold;">🥙 {doner_units:.2f} Döner Units</p>
            <div style="display:flex; justify-content:center; gap:5px;">
                <a class="social-btn" href="#">Write on WhatsApp</a>
                <a class="social-btn" href="#">Share on Twitter</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 9. ANALYTICS (SUMMARY)
if st.session_state.trip_history:
    df = pd.DataFrame(st.session_state.trip_history)
    total_co2 = df["CO2 (kg)"].sum()
    
    st.markdown(f"""
        <div style="background:#00FFCC; color:black; padding:15px; border-radius:10px; text-align:center; margin-top:20px;">
            <p style="margin:0; font-weight:bold;">{t['total']}</p>
            <h1 style="margin:0;">{total_co2:.2f} kg</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df, use_container_width=True)
