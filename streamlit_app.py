import streamlit as st
import datetime
import requests
import qrcode
from io import BytesIO

# 1. Setup & Custom Styling
st.set_page_config(page_title="Spice Bistro | Smart Table", page_icon="🌶️")

st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Dynamic URL & Table ID
try:
    host = st.context.headers.get("host")
    base_url = f"https://{host}/"
except:
    base_url = "https://resturant-automation-zbwvcoadgdhtzcajjydhe.streamlit.app/"

query_params = st.query_params
table_id = query_params.get("table", "Walk-in")

# 3. Admin Sidebar (QR Generator)
with st.sidebar:
    st.header("Admin: Print QRs")
    new_table = st.text_input("Table No.", value="05")
    target_url = f"{base_url}?table={new_table}"
    qr = qrcode.make(target_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf, caption=f"Scan for Table {new_table}")
    st.code(target_url)

# 4. Customer Interface
st.title("Spice Bistro 🌶️")
st.subheader(f"Table: {table_id}")

st.write("Enter WhatsApp number for **Digital Menu** & **10% Discount**.")
phone_number = st.text_input("WhatsApp Number", placeholder="91XXXXXXXXXX")

if st.button("View Menu & Get Discount"):
    if len(phone_number) >= 10:
        # THE BRAIN: Sending data to Make.com
        WEBHOOK_URL = "https://hook.eu1.make.com/4evyx4mx86pchmttab891addwpael1sk"
        
        # Replace with your actual UPI ID
        RESTAURANT_UPI = "9958193633@paytm" 
        
        payload = {
            "phone": phone_number,
            "table": table_id,
            "upi_link": f"upi://pay?pa={RESTAURANT_UPI}&pn=SpiceBistro&am=0&tn=Table_{table_id}",
            "timestamp": str(datetime.datetime.now())
        }
        
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
            st.success("✅ Access Granted! Check WhatsApp for your Menu & Pay Link.")
        except:
            st.warning("Automation Bridge Connecting...")

        st.info("Opening Digital Menu...")
        st.markdown("[👉 Click here to open Digital Menu](https://your-menu-link.com)")
    else:
        st.error("Please enter a valid 10-digit number.")
