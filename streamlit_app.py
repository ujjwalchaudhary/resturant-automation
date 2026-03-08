import streamlit as st
import datetime
import requests
import qrcode
from io import BytesIO

# 1. Page Configuration & UI Styling
st.set_page_config(page_title="Spice Bistro | Smart Table", page_icon="🌶️")

st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; font-weight: bold; }
    .stTextInput>div>div>input { text-align: center; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Auto-Detect Live URL for QR Generation
try:
    host = st.context.headers.get("host")
    base_url = f"https://{host}/"
except:
    base_url = "https://resturant-automation-zbwvcoadgdhtzcajjydhe.streamlit.app/"

# 3. Capture Table ID from URL (?table=05)
query_params = st.query_params
table_id = query_params.get("table", "Walk-in")

# 4. Admin Sidebar: Table QR Generator
with st.sidebar:
    st.header("Admin: Print Table QRs")
    new_table = st.text_input("Enter Table Number", value="05")
    target_url = f"{base_url}?table={new_table}"
    
    qr = qrcode.make(target_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf, caption=f"Scan for Table {new_table}")
    st.code(target_url)

# 5. Customer Interface
st.title("Spice Bistro 🌶️")
st.subheader(f"Table: {table_id}")

st.write("Enter your WhatsApp number to view our **Digital Menu** and get an instant **10% Discount**.")

phone_number = st.text_input("WhatsApp Number", placeholder="91XXXXXXXXXX")

if st.button("View Menu & Get Discount"):
    if len(phone_number) >= 10:
        # --- THE AUTOMATION TRIGGER ---
        # Update this with your Make.com Webhook URL
        WEBHOOK_URL = "https://hook.eu1.make.com/4evyx4mx86pchmttab891addwpael1sk" 
        
        # Update with actual Restaurant Details
        RESTAURANT_UPI = "9958193633@ptsbi" # Example UPI ID
        RESTAURANT_NAME = "Spice Bistro"

        # Constructing the Payload with Payment Link
        payload = {
            "phone": phone_number,
            "table": table_id,
            "timestamp": str(datetime.datetime.now()),
            "status": "intent_captured",
            "upi_link": f"upi://pay?pa={RESTAURANT_UPI}&pn={RESTAURANT_NAME}&am=0&cu=INR&tn=Table_{table_id}"
        }
        
        try:
            # Send data to Make.com Agent
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
            st.success("✅ Access Granted! Check WhatsApp for your Menu & Payment Link.")
        except:
            st.warning("Connecting to Automation... Opening Menu now.")

        st.info("Opening Digital Menu...")
        # Replace with the actual URL of your Menu (PDF/Image)
        st.markdown("[👉 Click here to open Digital Menu](https://your-menu-link.com)")
    else:
        st.error("Please enter a valid 10-digit phone number.")
