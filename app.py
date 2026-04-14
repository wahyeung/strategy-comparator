import streamlit as st
import yfinance as yf
import pandas as pd
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator

# Page configuration
st.set_page_config(page_title="Strategy Comparator", layout="wide")

# Sidebar for user inputs
st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Enter Ticker", value="AAPL").upper()
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))

st.sidebar.subheader("SMA Strategy Params")
sma_fast = st.sidebar.number_input("Fast SMA", value=20)
sma_slow = st.sidebar.number_input("Slow SMA", value=50)

st.sidebar.subheader("RSI Strategy Params")
rsi_period = st.sidebar.number_input("RSI Period", value=14)
rsi_overbought = st.sidebar.slider("Overbought", 50, 90, 70)
rsi_oversold = st.sidebar.slider("Oversold", 10, 50, 30)

# Data Fetching
@st.cache_data
def load_data(symbol, start):
    # Fetch data using yfinance
    if not symbol:
        return pd.DataFrame()
    df = yf.download(symbol, start=start)
    if df.empty:
        return df
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.index = pd.to_datetime(df.index)
    return df

data = load_data(ticker, start_date)

if not data.empty:
    # --- Strategy 1: SMA Crossover ---
    # Calculate SMA technical indicators using 'ta' library
    close_prices = data['Close'].squeeze()
    data['SMA_Fast'] = SMAIndicator(close=close_prices, window=sma_fast).sma_indicator()
    data['SMA_Slow'] = SMAIndicator(close=close_prices, window=sma_slow).sma_indicator()

    # Generate signals: 1 when fast SMA is above slow SMA, else 0
    data['SMA_Signal'] = 0
    data.loc[data['SMA_Fast'] > data['SMA_Slow'], 'SMA_Signal'] = 1
    # Calculate daily strategy returns
    data['SMA_Returns'] = data['SMA_Signal'].shift(1) * close_prices.pct_change()
    # Calculate cumulative returns
    data['Cum_SMA'] = (1 + data['SMA_Returns'].fillna(0)).cumprod()

    # --- Strategy 2: RSI Based ---
    # Calculate RSI technical indicator
    data['RSI'] = RSIIndicator(close=close_prices, window=rsi_period).rsi()

    
    # Generate signals: 1 for oversold (buy), -1 for overbought (sell)
    data['RSI_Signal'] = 0
    data.loc[data['RSI'] < rsi_oversold, 'RSI_Signal'] = 1
    data.loc[data['RSI'] > rsi_overbought, 'RSI_Signal'] = -1
    
    # Avoid future warnings for ffill
    pd.set_option('future.no_silent_downcasting', True)
    data['RSI_Signal'] = data['RSI_Signal'].replace(0, pd.NA).ffill().fillna(0).infer_objects(copy=False)
    
    data['RSI_Returns'] = data['RSI_Signal'].shift(1) * close_prices.pct_change()
    data['Cum_RSI'] = (1 + data['RSI_Returns'].fillna(0)).cumprod()

    # 3. Before plotting, make sure to drop any potential MultiIndex leftovers
    plot_data = data[['Cum_SMA', 'Cum_RSI']].copy()
    
    # Display Chart
    st.line_chart(plot_data)

    # --- UI Layout ---
    st.title(f"Strategy Comparison: {ticker}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cumulative Returns")
        # Display comparison chart
        st.line_chart(data[['Cum_SMA', 'Cum_RSI']])
    
    with col2:
        st.subheader("Metric Summary")
        # Calculate final percentage returns
        total_sma = (data['Cum_SMA'].iloc[-1] - 1) * 100
        total_rsi = (data['Cum_RSI'].iloc[-1] - 1) * 100
        st.metric("SMA Return", f"{total_sma:.2f}%")
        st.metric("RSI Return", f"{total_rsi:.2f}%")

    st.subheader("Latest Price Data & Signals")
    st.dataframe(data.tail(10))
else:
    st.error("No data found for the given ticker. Please check the ticker symbol.")