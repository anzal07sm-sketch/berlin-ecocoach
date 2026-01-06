import streamlit as st
import pandas as pd

st.set_page_config(page_title="EcoCoach Berlin", page_icon="🌿", layout="centered")

if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #1b2735 0%, #050505 100%);
        color: #FFFFFF;
    }
    .block-container {
        padding-top: 2rem !important;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(0, 255, 204, 0.3);
    }
    h1, h2 {
        color: #00FFCC !important;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.6);
    }
    .stButton>button {
        background: linear-gradient(90deg, #00FFCC 0%, #0099FF 100%);
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    /* This part hides the empty label space */
    label { display: none !important; }
    .stNumberInput label, .stSelectbox label { display: block !important; color: #00FFCC !important; }
    </style>
    """, unsafe_allow_html=True)

texts = {
    "English": {
        "title": "EcoCoach Berlin",
        "sub": "Track your carbon footprint in Berlin.",
        "dist": "Distance traveled (km)",
        "mode": "Transport Mode",
        "btn": "LOG TRIP",
        "reset": "CLEAR HISTORY",
        "total": "Total Carbon Footprint:"
    },
    "Deutsch": {
        "title": "EcoCoach Berlin",
        "sub": "Verfolge deinen CO2-Fußabdruck in Berlin.",
        "dist": "Reisestrecke (km)",
        "mode": "Verkehrsmittel",
        "btn": "TRIP LOGGEN",
        "reset": "HISTORIE LÖSCHEN",
        "total": "Gesamt CO2-Fußabdruck:"
    }
}

with st.sidebar:
    lang = st.selectbox("Language / Sprache", ["English", "Deutsch"])

t = texts[lang]

st.title(f"🌿 {t['title']}")

st.markdown('<div class="main-card">', unsafe_allow_html=True)
dist = st.number_input(t["dist"], min_value=0.0, step=0.1)
mode = st.selectbox(t["mode"], ["U-Bahn / S-Bahn", "Car / Auto", "Bike / Fahrrad", "Walking / Laufen"])

c1, c2 = st.columns(2)
with c1:
    calculate = st.button(t["btn"], use_container_width=True)
with c2:
    if st.button(t["reset"], use_container_width=True):
        st.session_state.trip_history = []
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if calculate:
    factors = {"Car / Auto": 0.2, "U-Bahn / S-Bahn": 0.03, "Bike / Fahrrad": 0.0, "Walking / Laufen": 0.0}
    co2 = dist * factors[mode]
    st.session_state.trip_history.append({"Mode": mode, "Distance": dist, "CO2 (kg)": round(co2, 2)})
    if co2 == 0: st.balloons()

if st.session_state.trip_history:
    df = pd.DataFrame(st.session_state.trip_history)
    total = df["CO2 (kg)"].sum()
    st.markdown(f"""
        <div style="background: rgba(0, 255, 204, 0.15); padding: 20px; border-radius: 15px; border-left: 5px solid #00FFCC; margin-top: 20px;">
            <p style="margin:0; color: #FFFFFF; font-size: 1.1rem;">{t['total']}</p>
            <h1 style="margin:0; color: #00FFCC; font-size: 3rem;">{total:.2f} kg</h1>
        </div>
    """, unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
