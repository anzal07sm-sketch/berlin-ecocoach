import streamlit as st
import pandas as pd

st.set_page_config(page_title="EcoCoach Berlin", page_icon="🌱", layout="centered")

if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #1b2735 0%, #050505 100%);
        color: #FFFFFF;
    }
    
    .main-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(0, 255, 204, 0.3);
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.1);
        margin-bottom: 25px;
    }

    h1, h2, h3 {
        color: #00FFCC !important;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.6);
    }

    [data-testid="stMetricValue"] {
        color: #00FFCC !important;
    }

    .stButton>button {
        background: linear-gradient(90deg, #00FFCC 0%, #0099FF 100%);
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.8);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

texts = {
    "English": {
        "title": "🌱 EcoCoach Berlin",
        "sub": "Track your carbon footprint in Berlin's true currency.",
        "dist": "Distance traveled (km)",
        "mode": "Transport Mode",
        "btn": "LOG TRIP",
        "reset": "CLEAR HISTORY",
        "result": "Trip Impact",
        "history_title": "📊 Analytics Dashboard",
        "total_saved": "Total Carbon Footprint:"
    },
    "Deutsch": {
        "title": "🌱 EcoCoach Berlin",
        "sub": "Verfolge deinen CO2-Fußabdruck in Berlin.",
        "dist": "Reisestrecke (km)",
        "mode": "Verkehrsmittel",
        "btn": "TRIP LOGGEN",
        "reset": "HISTORIE LÖSCHEN",
        "result": "Trip Impact",
        "history_title": "📊 Analytics Dashboard",
        "total_saved": "Gesamt CO2-Fußabdruck:"
    }
}

lang = st.sidebar.selectbox("Language / Sprache", ["English", "Deutsch"])
t = texts[lang]

st.title(t["title"])
st.write(f"*{t['sub']}*")

st.markdown('<div class="main-card">', unsafe_allow_html=True)
dist = st.number_input(t["dist"], min_value=0.0, step=0.1)
mode = st.selectbox(t["mode"], ["U-Bahn / S-Bahn", "Car / Auto", "Bike / Fahrrad", "Walking / Laufen"])

col1, col2 = st.columns(2)
with col1:
    calculate = st.button(t["btn"], use_container_width=True)
with col2:
    if st.button(t["reset"], use_container_width=True):
        st.session_state.trip_history = []
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if calculate:
    if mode == "Car / Auto":
        co2 = dist * 0.2
    elif mode == "Bike / Fahrrad" or mode == "Walking / Laufen":
        co2 = 0.0
    else:
        co2 = dist * 0.03
    
    new_trip = {"Mode": mode, "Distance": dist, "CO2 (kg)": round(co2, 2)}
    st.session_state.trip_history.append(new_trip)
    
    st.markdown(f"### {t['result']}")
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("Trip CO2", f"{co2:.2f} kg")
    
    if co2 == 0:
        rank, color = "ECO HERO 👑", "#00FFCC"
        st.balloons()
    elif co2 < 2.0:
        rank, color = "CITY SURVIVOR 🚲", "#FFD700"
    else:
        rank, color = "CO2 GIANT 🚗", "#FF0055"
        
    st.markdown(f"""
        <div style="padding:15px; border:2px solid {color}; border-radius:10px; text-align:center; background: rgba(0,0,0,0.3);">
            <h2 style="color:{color}; margin:0;">{rank}</h2>
        </div>
    """, unsafe_allow_html=True)

if st.session_state.trip_history:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader(t["history_title"])
    
    df_history = pd.DataFrame(st.session_state.trip_history)
    total_co2 = df_history["CO2 (kg)"].sum()
    
    st.markdown(f"""
        <div style="background: rgba(0, 255, 204, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #00FFCC; margin-bottom: 20px;">
            <p style="margin:0; font-size: 0.9rem; color: #FFFFFF;">{t['total_saved']}</p>
            <h2 style="margin:0; color: #00FFCC;">{total_co2:.2f} kg</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df_history, use_container_width=True)
