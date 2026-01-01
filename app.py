import streamlit as st

st.set_page_config(page_title="Berlin EcoCoach AI", page_icon="🌿")

# 1. Background and Font Styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url("https://images.unsplash.com/photo-1560969184-10fe8719e047?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    h1 {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    h2, h3, p, label, .stMarkdown {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. App Title and Inputs
st.title("Berlin EcoCoach AI")
st.write("New Year, Same BVG? Start 2026 as a climate loving legend🌿!")

transport = st.selectbox("Your main transport?", ["car", "bus", "train", "bike"])
distance = st.number_input("Daily distance (km)?", min_value=0.0, value=0.0)
electricity = st.number_input("Daily home electricity (kWh)?", min_value=0.0, value=0.0)

# 3. The Calculations (The part that was missing!)
if st.button("Calculate my footprint!"):
    co2_per_km = {"car": 0.17, "bus": 0.03, "train": 0.02, "bike": 0.0}
    transport_co2 = co2_per_km.get(transport, 0) * distance
    elec_co2 = electricity * 0.38
    total = transport_co2 + elec_co2
    
    st.subheader(f"Your daily footprint: {total:.2f} kg CO2")
    if total < 5:
        st.success("Berlin loves you! You're a green hero. 🌍")
    else:
        st.warning("A bit high! Try taking the S-Bahn more often. 🚄")