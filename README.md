# 📈 Financial Strategy Comparator

A lightweight interactive dashboard to evaluate and compare two classic trading strategies using historical market data.

## 🛠 Features
- **SMA Crossover Strategy:** Compare Fast and Slow Simple Moving Averages.
- **RSI Momentum Strategy:** Test Overbought/Oversold thresholds.
- **Real-time Visualization:** Built with Streamlit for seamless parameter tuning.
- **Data Sourcing:** Live data fetching via `yfinance`.

## 🚀 Quick Start
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/wahyeung/strategy-comparator.git](https://github.com/wahyeung/strategy-comparator.git)
   cd strategy-comparator
   ```
2. **Environment Setup:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. **Launch the App:**
   ```bash
   python3 -m streamlit run app.py
   ```

## 📝 Tech Stack
- **Frontend/App Framework:** Streamlit
- **Data Analysis:** Pandas
- **Financial Indicators:** `ta` library
- **Data Source:** Yahoo Finance API


