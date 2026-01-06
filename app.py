import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Berlin EcoCoach AI", layout="centered")

# 2. SESSION MEMORY
if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []

# 3. ULTIMATE CLUB UI CSS 
st.markdown("""
    <style>
    /* Dark Immersive Background */
    .stApp {
        background-color: #0d0216 !important;
        background-image: 
            linear-gradient(135deg, transparent 40%, #bf00ff1a 45%, #bf00ff1a 55%, transparent 60%),
            linear-gradient(45deg, transparent 40%, #00ffff1a 45%, #00ffff1a 55%, transparent 60%);
        background-size: cover;
        color: #FFFFFF !important;
    }

    /* Hide Streamlit elements that create 'empty bars' */
    header, footer, .stDeployButton { visibility: hidden !important; }
    [data-testid="stHeader"] {background: rgba(0,0,0,0) !important;}
    label { display: none !important; }

    .app-title {
        text-align: center;
        letter-spacing: 2px;
        font-size: 14px;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    /* The Score Display at the Top */
    .score-container {
        text-align: center;
        padding: 30px 0;
    }
    .main-score {
        font-size: 60px;
        font-weight: 800;
        margin: 0;
        background: -webkit-linear-gradient(#fff, #00ffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-score {
        color: #efefef;
        font-size: 18px;
        margin-top: 5px;
    }

    /* Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(15px);
        border-radius: 18px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }
    
    .card-header { font-weight: bold; font-size: 16px; margin-bottom: 10px; color: #00ffff; }

    /* The 'Generate Score' Button */
    div.stButton > button {
        background: linear-gradient(90deg, #00ffff, #0099ff) !important;
        color: #000 !important;
        border: none !important;
        width: 100%;
        border-radius: 50px !important;
        font-weight: 900 !important;
        letter-spacing: 1.5px;
        padding: 15px 0 !important;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.4);
        margin-top: 20px;
    }

    /* Social Icons */
    .social-footer {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 30px;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. LANGUAGE SELECTOR 
lang = st.selectbox("Language", ["English", "Deutsch"], key="lang")

# 5. UI CONTENT
st.markdown('<div class="app-title">BERLIN ECO-COACH AI</div>', unsafe_allow_html=True)

# 6. INPUT LOGIC
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass-card"><div class="card-header">Travel</div></div>', unsafe_allow_html=True)
    dist = st.number_input("Dist", min_value=0.0, step=0.1, key="d")
    mode = st.selectbox("Mode", ["S-Bahn/U-Bahn", "Car", "Bike", "Walking"], key="m")

with col2:
    st.markdown('<div class="glass-card"><div class="card-header">Food</div></div>', unsafe_allow_html=True)
    food_item = st.selectbox("Food", [
        "Vegan Döner", "Chicken Döner", "Beef Döner", 
        "Currywurst", "Beef Burger", "Halloumi Burger", "No Food"
    ], key="f")

generate = st.button("GENERATE SCORE")

# 7. CALCULATOR CALCULATION
if generate:
    # Math Factors
    travel_map = {"Car": 0.2, "S-Bahn/U-Bahn": 0.03, "Bike": 0.0, "Walking": 0.0}
    food_map = {
        "Vegan Döner": 0.1, "Chicken Döner": 2.2, "Beef Döner": 4.5,
        "Currywurst": 2.1, "Beef Burger": 3.8, "Halloumi Burger": 1.2, "No Food": 0.0
    }
    
    total_co2 = (dist * travel_map[mode]) + food_map[food_item]
    doners_saved = total_co2 / 4.5

    # Store in history
    st.session_state.trip_history.append({"CO2": total_co2, "Döner": doners_saved})

    # DISPLAY THE DYNAMIC SCORE 
    st.markdown(f"""
        <div class="score-container">
            <h1 class="main-score">{total_co2:.1f} kg CO2</h1>
            <p class="sub-score">{doners_saved:.1f} Döner Units Saved 🥙</p>
        </div>
        """, unsafe_allow_html=True)

# 8. SOCIAL FOOTER
st.markdown("""
    <div class="social-footer">
        <span>💬</span> <span>🐦</span> <span>in</span>
        <span style="font-size:12px; font-weight:bold; margin-left:10px;">SHARE ⚑</span>
    </div>
    """, unsafe_allow_html=True)

# 9. HISTORY 
if st.session_state.trip_history:
    st.markdown("---")
    st.write("### History Log")
    st.dataframe(pd.DataFrame(st.session_state.trip_history), use_container_width=True)
