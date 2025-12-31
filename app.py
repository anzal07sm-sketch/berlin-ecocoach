import streamlit as st

st.set_page_config(page_title="Berlin EcoCoach AI", page_icon="🌍")

st.title("🌍 Berlin EcoCoach AI")
st.write("Free tool to check your daily carbon footprint & get easy green tips for Berlin life! 💚")

st.write("### Tell me your daily habits:")
transport = st.selectbox("Your main transport?", ["car", "bus", "train", "bike", "walk"])
distance = st.number_input("Daily distance (km)?", min_value=0.0, value=15.0)
electricity = st.number_input("Daily home electricity (kWh)?", min_value=0.0, value=8.0)

if st.button("Calculate my footprint! 🚀"):
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
    st.write("→ Turn off lights/TV/charger when not use!")
    
    st.write("Share with friends – make Berlin greener together! 🚲")
    st.balloons()
