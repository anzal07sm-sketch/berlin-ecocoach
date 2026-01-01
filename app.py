import streamlit as st
st.markdown(
    """
    /* This changes the main title size */
    h1 {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5); /* Makes it pop! */
    }
    
    /* This changes the "Tell me your daily habits" size */
    h2, h3 {
        font-size: 1.8rem !important;
        margin-top: 20px !important;
    }
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
        url("https://images.unsplash.com/photo-1560969184-10fe8719e047");
        background-size: cover;
        background-attachment: fixed;
    }
    /* This part makes your text easier to read on a photo */
    .stMarkdown, .stHeader, p, h1, h2, h3 {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.set_page_config(page_title="Berlin EcoCoach AI", page_icon="🌿")

st.title("🌍 Berlin EcoCoach AI")
st.write(" New Year, Same BVG? Stop guessing if your ride home from the Berghain queue was a carbon sin. Let's check your green street-cred in 5 seconds flat and start 2026 as a climate loving legend! 💚")

st.write("### Tell me your daily habits:")
transport = st.selectbox("Your main transport?", ["car", "bus", "train", "bike", "walk"])
distance = st.number_input("Daily distance (km)?", min_value=0.0, value=0.0)
electricity = st.number_input("Daily home electricity (kWh)?", min_value=0.0, value=0.0)

if st.button("Calculate my footprint! ⚡"):
    co2_per_km = {"car": 0.17, "bus": 0.05, "train": 0.03, "bike": 0.00, "walk": 0.00}
    
    transport_co2 = co2_per_km.get(transport, 0.10) * distance
    elec_co2 = electricity * 0.38
    total = transport_co2 + elec_co2
    
    st.write("### 🌍 Your daily carbon footprint:")
    st.write(f"🚗 Transport ({transport}): **{transport_co2:.2f} kg CO2**")
    st.write(f"🏠 Electricity: **{elec_co2:.2f} kg CO2**")
    st.write(f"**TOTAL: {total:.2f} kg CO2 per day**")
    
    st.write("### 💡 Easy tips to save:")
    if transport in ["car", "bus"]:
        st.write("→ Try bike or walk – save a lot!")
    if transport == "car":
        save = (0.17 - 0.03) * distance
        st.write(f"→ Take train/U-Bahn: Save **{save:.2f} kg** today!")
    st.write("→ Turn off lights/TV/charger when not in use!")
    
    st.write("Share with friends – make Berlin greener together! 🚲")
    st.balloons()
