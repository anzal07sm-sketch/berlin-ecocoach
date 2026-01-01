import streamlit as st

st.set_page_config(page_title="Berlin EcoCoach AI", page_icon="🌿")

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
    h2, h3, p, label {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Berlin EcoCoach AI")