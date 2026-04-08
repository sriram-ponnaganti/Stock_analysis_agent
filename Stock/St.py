import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd  # Add this line
from datetime import datetime, timedelta

# Page Config
st.set_page_config(page_title="AI Stock Analyst", layout="wide")
st.title("📈 Real-Time Stock Market Analysis")

# Sidebar for User Input
st.sidebar.header("User Settings")
stock_name = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, GOOGL)", "AAPL")
days_to_plot = st.sidebar.slider("Number of Days for Chart", min_value=1, max_value=365, value=30)

def get_data(ticker, days):
    start_date = datetime.now() - timedelta(days=days)
    # Fetch data
    data = yf.download(ticker, start=start_date, end=datetime.now(), interval='1h')
    
    # FIX: Flatten MultiIndex columns if they exist
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
        
    return data

if stock_name:
    try:
        with st.spinner(f'Fetching data for {stock_name}...'):
            df = get_data(stock_name, days_to_plot)
            
        if not df.empty:
            # Now that columns are flattened, this is safe and simple:
            last_price = float(df['Close'].iloc[-1])
            open_price = float(df['Open'].iloc[0])
            change = last_price - open_price
            
            col1, col2 = st.columns(2)
            col1.metric("Current Price", f"${last_price:,.2f}", f"{change:,.2f}")
            col2.metric("Highest in Period", f"${float(df['High'].max()):,.2f}")

            # The rest of your Plotly code stays the same...

            # Interactive Candlestick Chart
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name="Price"
            )])
            
            fig.update_layout(
                title=f"{stock_name} Price Action (Last {days_to_plot} Days)",
                yaxis_title="Price (USD)",
                template="plotly_dark",
                xaxis_rangeslider_visible=False
            )
            
            st.plotly_chart(fig, use_container_width=True)

            # Data Table
            with st.expander("View Raw Data"):
                st.write(df.tail(10))
        else:
            st.error("No data found. Please check the ticker symbol.")
            
    except Exception as e:
        st.error(f"Error: {e}")

st.info("Tip: Use Indian tickers by adding '.NS' (e.g., RELIANCE.NS)")