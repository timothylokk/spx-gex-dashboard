import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image

# 1. Dashboard Config
st.set_page_config(page_title="0DTE GEX Analyzer", layout="wide")
st.title("🎯 0DTE SPX GEX Dashboard")

# 2. Live SPX Price Section
spx = yf.Ticker("^SPX")
current_price = spx.history(period="1d")['Close'].iloc[-1]
st.metric(label="Live SPX Spot Price", value=f"{current_price:,.2f}")

# 3. Sidebar for Screenshot Upload
st.sidebar.header("Data Upload")
uploaded_file = st.sidebar.file_uploader("Upload Barchart/Quantwheel Screenshot", type=['png', 'jpg', 'jpeg'])

# 4. Analysis Logic (The "Brain")
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Current GEX Data Source", use_container_width=True)
    
    st.header("⚡ Trade Setup Analysis")
    st.info("Manual Input needed until OCR is connected: Enter the 'Call Wall' and 'Put Wall' from your image below.")
    
    col1, col2 = st.columns(2)
    call_wall = col1.number_input("Call Wall (Highest GEX)", value=5100)
    put_wall = col2.number_input("Put Wall (Lowest GEX)", value=5000)

    # 5. Automated Recommendation logic
    dist_to_call = call_wall - current_price
    dist_to_put = current_price - put_wall

    if dist_to_call < 5:
        st.warning(f"⚠️ PIN ALERT: SPX is at the Call Wall ({call_wall}). Expect resistance or a 'pin' for expiration.")
    elif dist_to_put < 5:
        st.error(f"⚠️ SQUEEZE ALERT: SPX is at the Put Wall ({put_wall}). If this breaks, volatility could spike.")
    else:
        st.success("✅ Neutral Zone: Price is trading between major walls. Trend following is viable.")
else:
    st.write("Please upload a screenshot to begin the GEX analysis.")
