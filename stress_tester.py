'''
File: stess_tester.py
Purpose: Source for steamlit web app meant to test stock portfolio resiliency
Author: Devin Lepur
Date: June 21, 2025
'''


import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

import data_manipulation as dm
import simulation_algs as sa

st.title("Stock Portfolio Stress Tester")

# Allow user to enter stock
ticker_input = st.text_input("Enter the tickers of your holdings a list. Example: \"TSLA, AAPL, MSFT\"", key="ticker")

# TODO: Allow user to upload downloaded holdings from brokerage

# TODO: Encapsulate pieces into functions into methods

# Remove extra info and prepare for ticker use
ticker_input = ticker_input.replace(' ', '')
ticker_input = ticker_input.upper()

# If there is input, parse the data
if ticker_input.strip():
    tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
    #Create data frame and allow editing
    df = pd.DataFrame({"Tickers": tickers, "No. Shares held": [0.0]*len(tickers)})
    input_data = st.data_editor(df, num_rows="fixed", use_container_width=True)


    total_value = 0
    st.markdown("## Estimated Current Value")
    st.write("(Based on last market close)")


# TODO: Combine the two following for loops and just have the first loop pull from the selected data

    # For each row, get price and determine value of shares held
    for i, row in input_data.iterrows():
        ticker_symbol = row['Tickers']
        shares_held = row['No. Shares held']

        try:
            data = yf.Ticker(ticker_symbol).history(period="1d", interval="1d")
            if data.empty:
                st.warning(f"Unable to fetch data from Yahoo Finance for {ticker_symbol}.")
            
            # Get total value of shares for last market close
            current_price = data['Close'].iloc[-1]
            holding_value = current_price * shares_held
            total_value += holding_value

            st.write(f"**{ticker_symbol}**: {shares_held} shares x \\${round(current_price,2):,} = \\${round(holding_value, 2):,}")

        except Exception as e:
            st.warning(f"Unable to fetch data for \"{ticker_symbol}\". Check to make sure you entered the tickers correctly.")

    st.markdown(f"#### Total Portfolio Value: ${round(total_value, 2):,}")



    # Dynamic line graph of portfolio value over time
    st.markdown("## Portfolio value over time")

    # Drop down for time frame, 1 year default selection
    graph_time_period = st.selectbox("Select time frame", options = ["1mo", "6mo", "1y", "5y", "10y", "Max"], index=2)
    if graph_time_period == "Max":
        graph_time_period = "300y"

    portfolio_timeline = pd.DataFrame(columns = ["Date", "Close"])
    for i, row in input_data.iterrows():
        # Pull ticker history
        ticker_timeline = yf.Ticker(row["Tickers"]).history(period=graph_time_period, interval="1d")
        ticker_timeline = ticker_timeline.reset_index()     # Remove index classification from Date column

        # For first iteration set portfolio date column
        if i == 0:
            portfolio_timeline["Date"] = ticker_timeline["Date"]
            portfolio_timeline["Close"] = 0.0
        
        # Adjust for shares held and add to portfolio
        ticker_timeline["Close"] = ticker_timeline["Close"] * row["No. Shares held"]
        portfolio_timeline["Close"] = portfolio_timeline["Close"] + ticker_timeline["Close"]

    # Possible TODO: Show the value of each stock on the graph to show it's effect on portfolio value

    st.line_chart(portfolio_timeline, x="Date", y="Close")
    st.markdown("**Note this chart assumes you've held all these shares the whole period*")


    # TODO: Only show graph if valid selection

    # Display histogram of daily returns
    percent_returns = dm.get_percent_returns(data=portfolio_timeline)["Percent_return"]
    
    fig, ax = plt.subplots()
    ax.hist(percent_returns, bins=30, edgecolor="black")
    ax.set_title("Histogram of Daily Percent Returns")
    ax.set_xlabel("Daily Percent Return (%)")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

    monte_sim_results = sa.sim_monte_carlo(portfolio_timeline)
    st.line_chart(monte_sim_results)

else:
    st.info("Please enter at least one ticker to get started")


