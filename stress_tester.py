import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np

st.title("Stock Portfolio Stress Tester")

# Allow user to enter stock
ticker_input = st.text_input("Enter the tickers of your holdings a list. Example: \"TSLA,AAPL,MSFT\"", key="ticker")

# If there is input, parse the data
if ticker_input.strip():
    tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
    #Create data frame and allow editing
    df = pd.DataFrame({"Tickers": tickers, "No. Shares held": [0.0]*len(tickers)})
    input_data = st.data_editor(df, num_rows="fixed", use_container_width=True)


    total_value = 0
    st.markdown("## Estimated Current Value")
    st.write("(Based on last market close)")


    # For each row, get price and determine value of shares held
    for i, row in input_data.iterrows():
        ticker_symbol = row['Tickers']
        shares_held = row['No. Shares held']

        try:
            data = yf.Ticker(ticker_symbol).history(period="1d", interval="1m")
            if data.empty:
                raise ValueError("No data found.")
            
            # Get total value of shares for last market close
            current_price = data['Close'].iloc[-1]
            holding_value = current_price * shares_held
            total_value += holding_value

            st.write(f"**{ticker_symbol}**: {shares_held} shares x \\${round(current_price,2):,} = \\${round(holding_value, 2):,}")

        except Exception as e:
            st.warning(f"Unable to fetch data for \"{ticker_symbol}\". Check to make sure you entered the tickers correctly.")

    st.markdown(f"#### Total Portfolio Value: ${round(total_value, 2):,}")

else:
    st.info("Please enter at least one ticker to get started")
