import streamlit as st

# 1. PAGE SETUP WITH 🌿 ICON
st.set_page_config(
    page_title="Berlin EcoCoach AI", 
    page_icon="🌿", 
    layout="centered"
)

# 2. STATE MANAGEMENT
if 'total_co2' not in st.session_state:
    st.session_state.total_co2 = 0.0
if 'doner_units' not in st.session_state:
    st.session_state.doner_units = 0.0

# 3. VIBRANT BERLIN CSS & MOBILE FIX
st.markdown("""
    <style>
    /* Brighter Berlin Skyline Background */
    .stApp {
        background: linear-gradient(rgba(15, 1, 26, 0.1), rgba(5, 1, 10, 0.2)), 
                    url('https://images.unsplash.com/photo-1560969184-10fe8719e047?q=80&w=2070&auto=format&fit=crop');
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    header, footer, .stDeployButton { visibility: hidden !important; }
    
    .app-title {
        text-align: center;
        letter-spacing: 4px;
        font-size: 26px;
        font-weight: 900;
        color: #00ffcc;
        text-shadow: 0 0 15px #00ffcc, 0 0 30px #00ffcc;
        margin-bottom: 5px;
        text-transform: uppercase;
    }

    /* THE MOBILE FIX: Force side-by-side layout */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: flex-end !important;
        gap: 0.1rem !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        min-width: 0px !important;
        flex: 1 1 auto !important;
        background: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 15px !important;
    }

    /* CENTERED NEON BUTTON ALIGNMENT */
    div.stButton > button {
        background: linear-gradient(90deg, #00ffcc, #00d4ff) !important;
        color: #000000 !important;
        border: none !important;
        width: 100% !important; 
        border-radius: 50px !important;
        font-weight: 900 !important;
        padding: 12px 0 !important;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.8) !important;
        font-size: 9px !important;
        text-transform: uppercase;
        margin-top: 27px !important; /* This aligns button with input boxes */
    }

    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 50px rgba(0, 255, 204, 1) !important;
    }
    
    label { color: #00ffcc !important; font-weight: bold !important; font-size: 13px !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. LANGUAGE SELECTOR
lang = st.selectbox("", ["English", "Deutsch"], key="lang_selector", label_visibility="collapsed")

ui = {
    "English": {
        "title": "Berlin EcoCoach AI", 
        "sub": "2026 is for Climate Legends! 🌿", 
        "travel": "🚕 Travel", 
        "food": "🍔 Food", 
        "dist": "Distance (km)", 
        "btn": "GENERATE SCORE", 
        "unit": "Döner Units Saved",
        "qty": "Quantity",
        "mode": "Transport Mode",
        "meal": "Meal Name"
    },
    "Deutsch": {
        "title": "Berlin EcoCoach AI", 
        "sub": "2026 ist für Klima-Legenden! 🌿", 
        "travel": "🚕 Reise", 
        "food": "🍔 Essen", 
        "dist": "Strecke (km)", 
        "btn": "BERECHNEN", 
        "unit": "Döner-Einheiten gespart",
        "qty": "Anzahl",
        "mode": "Verkehrsmittel",
        "meal": "Essen Name"
    }
}[lang]

st.markdown(f'<div class="app-title">{ui["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; color:white; margin-bottom:20px;">{ui["sub"]}</div>', unsafe_allow_html=True)

# 5. TOP ROW 
col_top_1, col_top_2 = st.columns(2)
with col_top_1:
    transport = st.selectbox(ui["mode"], ["U-Bahn / S-Bahn", "Car (Petrol)", "Car (Electric)", "Bike", "Walking"])
with col_top_2:
    meal = st.selectbox(ui["meal"], ["Vegan Döner", "Chicken Döner", "Beef Döner", "Beef Burger", "Veggie Burger", "Currywurst", "Club Mate"])

# 6. CENTERED ROW 
c1, c2, c3 = st.columns([1, 4, 1])
with c1:
    dist = st.number_input(ui["dist"], min_value=0.0, step=1.0, value=0.0)
with c2:
    
    generate = st.button(ui["btn"])
with c3:
    qty = st.number_input(ui["qty"], min_value=0, step=1, value=0)

# 7. LOGIC
if generate:
    t_map = {"Car (Petrol)": 0.2, "Car (Electric)": 0.05, "U-Bahn / S-Bahn": 0.03, "Bike": 0.0, "Walking": 0.0}
    f_map = {"Vegan Döner": 0.1, "Chicken Döner": 2.2, "Beef Döner": 4.5, "Beef Burger": 3.8, "Veggie Burger": 1.2, "Currywurst": 2.1, "Club Mate": 0.1}
    
    total_val = (dist * t_map[transport]) + (f_map[meal] * qty)
    st.session_state.total_co2 = total_val
    st.session_state.doner_units = total_val / 4.5

# 8. RESULTS DISPLAY
st.markdown(f"""
    <div style="text-align: center; background: rgba(0,0,0,0.6); padding: 35px; border-radius: 25px; border: 2px solid #00ffcc; margin-top: 30px;">
        <h1 style="color: white; font-size: 55px; margin: 0; text-shadow: 0 0 20px #00ffcc;">{st.session_state.total_co2:.1f} kg CO2</h1>
        <p style="color: #ff00ff; font-weight: bold; font-size: 22px; margin: 0;">🥙 {st.session_state.doner_units:.1f} {ui['unit']}</p>
    </div>
    """, unsafe_allow_html=True)
