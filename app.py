import streamlit as st
import pandas as pd

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="EcoCoach Berlin", page_icon="🌱", layout="centered")

# 2. SESSION STATE (Memory)
# This keeps your trip history from disappearing when you click buttons
if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []

# 3. NEON UI DESIGN
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. TRANSLATION DICTIONARY
texts = {
    "English": {
        "title": "🌱 EcoCoach Berlin",
        "sub": "Track your carbon footprint & save the planet.",
        "dist": "Distance traveled (km)",
        "mode": "Transport Mode",
        "btn": "LOG TRIP",
        "reset": "CLEAR HISTORY",
        "result": "Trip Impact:",
        "history_title": "📊 Your Trip History",
        "total_saved": "Total CO2 tracked so far:"
    },
    "Deutsch": {
        "title": "🌱 EcoCoach Berlin",
        "sub": "Verfolge deinen CO2-Fußabdruck und rette den Planeten.",
        "dist": "Reisestrecke (km)",
        "mode": "Verkehrsmittel",
        "btn": "TRIP LOGGEN",
        "reset": "HISTORIE LÖSCHEN",
        "result": "Trip Impact:",
        "history_title": "📊 Deine Reise-Historie",
        "total_saved": "Gesamt CO2 getrackt:"
    }
}

# 5. SIDEBAR
lang = st.sidebar.selectbox("Language / Sprache", ["English", "Deutsch"])
t = texts[lang]

# 6. MAIN UI
st.title(t["title"])
st.write(t["sub"])

with st.container():
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

# 7. LOGIC & DATA STORAGE
if calculate:
    # Calculation Logic
    if mode == "Car / Auto":
        co2 = dist * 0.2
    elif mode == "Bike / Fahrrad" or mode == "Walking / Laufen":
        co2 = 0.0  # Zero emissions!
    else:
        co2 = dist * 0.03
    
    # Save trip to session memory
    new_trip = {"Mode": mode, "Distance (km)": dist, "CO2 (kg)": round(co2, 2)}
    st.session_state.trip_history.append(new_trip)
    
    # Results Display
    st.subheader(t["result"])
    st.metric("Current Trip CO2", f"{co2:.2f} kg")

    # Ranking Logic
    if co2 == 0:
        rank, color = "ECO HERO 🌿", "#00FFCC"
        st.balloons()
    elif co2 < 2.0:
        rank, color = "GREEN TRAVELLER 🚲", "#FFD700"
    else:
        rank, color = "HEAVY FOOTPRINT 🚗", "#FF0055"
        
    st.markdown(f"""
        <div style="padding:20px; border:2px solid {color}; border-radius:10px; text-align:center;">
            <h2 style="color:{color}; margin:0;">{rank}</h2>
        </div>
    """, unsafe_allow_html=True)

# 8. DATA ANALYTICS TABLE (Intermediate Level)
if st.session_state.trip_history:
    st.divider()
    st.subheader(t["history_title"])
    
    # Convert list to Pandas DataFrame
    df_history = pd.DataFrame(st.session_state.trip_history)
    
    # Show total summary
    total_co2 = df_history["CO2 (kg)"].sum()
    st.info(f"{t['total_saved']} **{total_co2:.2f} kg**")
    
    # Display the table
    st.dataframe(df_history, use_container_width=True)
