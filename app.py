import streamlit as st

st.set_page_config(page_title="Berlin Eco-Coach AI", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #0d0216 !important;
        background-image: 
            linear-gradient(135deg, transparent 40%, #bf00ff1a 45%, #bf00ff1a 55%, transparent 60%),
            linear-gradient(45deg, transparent 40%, #00ffff1a 45%, #00ffff1a 55%, transparent 60%);
        background-size: cover;
        color: #FFFFFF !important;
    }

    header, footer, .stDeployButton { visibility: hidden !important; }
    
    .app-title {
        text-align: center;
        font-family: 'sans-serif';
        letter-spacing: 2px;
        font-size: 14px;
        margin-top: 10px;
        font-weight: bold;
        text-transform: uppercase;
    }

    .score-container {
        text-align: center;
        padding: 50px 0;
    }
    .main-score {
        font-size: 72px;
        font-weight: 800;
        margin: 0;
        line-height: 1;
    }
    .sub-score {
        color: #efefef;
        font-size: 18px;
        margin-top: 10px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(15px);
        border-radius: 18px;
        padding: 25px;
        height: 180px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .card-header { font-weight: bold; font-size: 18px; margin-bottom: 20px; color: #fff; }
    .label-dim { color: #888; font-size: 15px; margin-bottom: 5px; }
    .label-active { color: #00ffff; font-weight: bold; font-size: 15px; }
    .label-white { color: #ffffff; font-size: 15px; }

    /* Fix Streamlit Toggle Color to Neon Pink */
    .stCheckbox div[data-baseweb="checkbox"] div {
        background-color: #ff00ff !important;
    }

    div.stButton > button {
        background: #00ffff !important;
        color: #000 !important;
        border: none !important;
        width: 100%;
        border-radius: 50px !important;
        font-weight: 900 !important;
        letter-spacing: 1.5px;
        padding: 18px 0 !important;
        margin-top: 30px;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.5);
    }

    .social-footer {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 25px;
        margin-top: 40px;
        color: #00ffff;
        font-size: 22px;
    }
    
    .share-text {
        color: white;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 1px;
        margin-left: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="app-title">BERLIN ECO-COACH AI</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="score-container">
        <h1 class="main-score">1.2 kg CO2</h1>
        <p class="sub-score">0.3 Döners Saved 🥙</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="glass-card">
            <div class="card-header">Travel</div>
            <p class="label-dim">Transport</p>
            <p class="label-white">U-Bahn/S-Bahn</p>
        </div>
        """, unsafe_allow_html=True)
    st.toggle("U-Bahn", value=True, label_visibility="collapsed", key="t1")
    st.toggle("Active", value=True, label_visibility="collapsed", key="t2")

with col2:
    st.markdown("""
        <div class="glass-card">
            <div class="card-header">Food</div>
            <div style="font-size: 20px; margin-bottom: 10px;">🥗</div>
            <p class="label-active">Plant-Based</p>
            <p class="label-dim">Beef</p>
        </div>
        """, unsafe_allow_html=True)

st.button("GENERATE SCORE")

st.markdown("""
    <div class="social-footer">
        <span><i class="fa fa-whatsapp"></i>💬</span> 
        <span><i class="fa fa-twitter"></i>🐦</span> 
        <span><i class="fa fa-linkedin"></i>in</span>
        <span class="share-text">SHARE ⚑</span>
    </div>
    """, unsafe_allow_html=True)
