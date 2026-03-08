import streamlit as st
import datetime
import requests
import qrcode
from io import BytesIO
from PIL import Image

# 1. Page Configuration  & twilio  - 2JR5NYSGDALQQL9LNNBF7XV4
st.set_page_config(page_title="Spice Bistro | Smart Table", page_icon="🌶️")

# Custom CSS for Mobile UI
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; font-weight: bold; }
    .stTextInput>div>div>input { text-align: center; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Capture Table ID from URL (?table=05)
query_params = st.query_params
table_id = query_params.get("table", "Walk-in")

# 3. Sidebar for QR Generation (Your Internal Tool)
with st.sidebar:
    st.header("Admin: Generate Table QR")
    new_table = st.text_input("Enter Table Number", value="05")
    if st.button("Generate QR for Printing"):
        # Create URL for this specific table
        base_url = "https://resturant-automation-zbwvcoadgdhtzcajjjydhe.streamlit.app/" # UPDATE THIS TO YOUR LIVE URL
        target_url = f"{base_url}?table={new_table}"
        
        # Generate QR
        qr = qrcode.make(target_url)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf, caption=f"QR for Table {new_table}")
        st.write(f"URL: {target_url}")

# 4. Main Customer UI
st.title("Spice Bistro 🌶️")
st.subheader(f"Table: {table_id}")

st.write("Enter your WhatsApp number to view our **Digital Menu** and get an instant **10% Discount Coupon**.")

phone_number = st.text_input("WhatsApp Number", placeholder="91XXXXXXXXXX")

if st.button("View Menu & Get Discount"):
    if len(phone_number) >= 10:
        # --- THE AUTOMATION TRIGGER ---
        # Replace with your Make.com Webhook URL
        WEBHOOK_URL = "https://hook.eu1.make.com/4evyx4mx86pchmttab891addwpael1sk" 
        
        payload = {
            "phone": phone_number,
            "table": table_id,
            "timestamp": str(datetime.datetime.now()),
            "status": "intent_captured"
        }
        
        try:
            # This sends the data to your "Agent"
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
            st.success("✅ Access Granted! Check WhatsApp for your coupon.")
        except:
            # Fallback if webhook isn't set up yet
            st.warning("Connected! Menu loading...")

        st.info("Opening Digital Menu...")
        st.markdown("[👉 Click here to open Digital Menu](https://your-menu-link.com)")
    else:
        st.error("Please enter a valid 10-digit number.")
