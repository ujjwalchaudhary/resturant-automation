import streamlit as st
import datetime

# 1. Capture Table ID from URL (e.g., ?table=05)
query_params = st.query_params
table_id = query_params.get("table", "Walk-in")

st.set_page_config(page_title="Welcome to Spice Bistro", page_icon="🍽️")

# Custom CSS for a premium "App-like" feel
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("Spice Bistro 🌶️")
st.subheader(f"Table: {table_id}")

st.write("Enter your WhatsApp number to view our **Digital Menu** and get an instant **10% Discount Coupon**.")

# 2. Collect User Information
phone_number = st.text_input("WhatsApp Number", placeholder="91XXXXXXXXXX")

if st.button("View Menu & Get Discount"):
    if len(phone_number) >= 10:
        # 3. Log the Data (For now, we display it. In production, send to Google Sheets)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.success("✅ Access Granted! Your discount is applied.")
        
        # This is where you'd trigger your 'Intent' Agent
        # Example: requests.post(WEBHOOK_URL, data={'phone': phone_number, 'table': table_id})
        
        st.info("The menu is loading... Check your WhatsApp for your coupon!")
        
        # Link to the actual PDF or Image of the Menu
        st.markdown("[Click here to open Digital Menu](https://your-menu-link.com)")
        
    else:
        st.error("Please enter a valid 10-digit phone number.")
      
