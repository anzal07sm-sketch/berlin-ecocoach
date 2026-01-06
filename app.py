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

# 3. VIBRANT BERLIN CSS
st.markdown("""
    <style>
    /* Brighter Berlin Skyline Background */
    .stApp {
        background: linear-gradient(rgba(15, 1, 26, 0.2), rgba(5, 1, 10, 0.3)), 
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
    
    .app-subtitle {
        text-align: center;
        color: #ffffff;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 30px;
        text-shadow: 1px 1px 10px #000;
    }

    /* Score Display Box */
    .score-box {
        text-align: center;
        padding: 40px 0;
        border-radius: 30px;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        border: 2px solid rgba(0, 255, 204, 0.5);
        margin: 20px 0;
    }
    
    .main-val {
        font-size: 85px;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 30px rgba(0, 255, 204, 1);
        margin: 0;
    }
    
    .sub-val {
        color: #ff00ff;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 0 0 10px #ff00ff;
    }

    /* Input Card Containers */
    [data-testid="column"] {
        background: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }

    /* CENTERED NEON BUTTON LOGIC */
    .stButton {
        display: flex;
        justify-content: center;
        width: 95%;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #00ffcc, #00d4ff) !important;
        color: #000000 !important;
        border: none !important;
        width: 100% !important; 
        border-radius: 50px !important;
        font-weight: 900 !important;
        padding: 15px 0 !important;
        box-shadow: 0 0 35px rgba(0, 255, 204, 0.8) !important;
        font-size: 18px !important;
        text-transform: uppercase;
        transition: 0.3s ease;
        margin-top: 25px;
    }

    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 50px rgba(0, 255, 204, 1) !important;
    }
    
    label { color: #00ffcc !important; font-weight: bold !important; font-size: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. LANGUAGE SELECTOR
lang = st.selectbox("", ["English", "Deutsch"], key="lang_final", label_visibility="collapsed")

ui = {
    "English": {
        "title": "Berlin EcoCoach AI", 
        "sub": "New Year, Same VibG 🌿 2026 for Climate Legends!", 
        "travel": "🚕 Travel Details", 
        "food": "🍔 Food Choice",
        "dist": "Distance (km)", 
        "btn": "GENERATE SCORE", 
        "unit": "Döner Units Saved",
        "qty": "Quantity",
        "mode": "Transport Mode",
        "meal": "Meal Name"
    },
    "Deutsch": {
        "title": "Berlin EcoCoach AI", 
        "sub": "Neues Jahr, gleicher VibG 🌿 2026 für Klima-Legenden!", 
        "travel": "🚕 Reise Details", 
        "food": "🍔 Essen Auswahl",
        "dist": "Strecke (km)", 
        "btn": "PUNKTE GENERIEREN", 
        "unit": "Döner-Einheiten gespart",
        "qty": "Anzahl",
        "mode": "Verkehrsmittel",
        "meal": "Essen Name"
    }
}[lang]

st.markdown(f'<div class="app-title">{ui["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="app-subtitle">{ui["sub"]}</div>', unsafe_allow_html=True)

# 5. INPUT GRID 
col_top_left, col_top_right = st.columns(2)
with col_top_left:
    st.markdown(f"### {ui['travel']}")
    transport = st.selectbox(ui["mode"], ["U-Bahn / S-Bahn", "Car (Petrol)", "Car (Electric)", "Bike", "Walking"], key="t_mode")
with col_top_right:
    st.markdown(f"### {ui['food']}")
    meal = st.selectbox(ui["meal"], ["Vegan Döner", "Chicken Döner", "Beef Döner", "Beef Burger", "Veggie Burger", "Currywurst", "Club Mate"], key="m_choice")

# 6. CENTERED ROW (Distance - Button - Quantity)

col_dist, col_btn, col_qty = st.columns([1, 1.2, 1])

with col_dist:
    distance = st.number_input(ui["dist"], min_value=0.0, step=1.0, key="d_val")

with col_btn:
    
    if st.button(ui["btn"]):
        t_map = {"Car (Petrol)": 0.2, "Car (Electric)": 0.05, "U-Bahn / S-Bahn": 0.03, "Bike": 0.0, "Walking": 0.0}
        f_map = {"Vegan Döner": 0.1, "Chicken Döner": 2.2, "Beef Döner": 4.5, "Beef Burger": 3.8, "Veggie Burger": 1.2, "Currywurst": 2.1, "Club Mate": 0.1}
        

        
        pass

with col_qty:
    quantity = st.number_input(ui["qty"], min_value=0, step=1, value=0, key="q_val")

# 7. CALCULATION 
t_map = {"Car (Petrol)": 0.2, "Car (Electric)": 0.05, "U-Bahn / S-Bahn": 0.03, "Bike": 0.0, "Walking": 0.0}
f_map = {"Vegan Döner": 0.1, "Chicken Döner": 2.2, "Beef Döner": 4.5, "Beef Burger": 3.8, "Veggie Burger": 1.2, "Currywurst": 2.1, "Club Mate": 0.1}
        
total = (distance * t_map[transport]) + (f_map[meal] * quantity)
st.session_state.total_co2 = total
st.session_state.doner_units = total / 4.5

# 8. RESULTS DISPLAY
st.markdown(f"""
    <div class="score-box">
        <h1 class="main-val">{st.session_state.total_co2:.1f} kg CO2</h1>
        <p class="sub-val">🥙 {st.session_state.doner_units:.1f} {ui['unit']}</p>
    </div>
    """, unsafe_allow_html=True)
