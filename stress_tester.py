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
import numpy as np

import data_manipulation as dm
import simulation_algs as sa

st.title("Stock Portfolio Stress Tester")

# Allow user to enter stock
ticker_input = st.text_input("Enter the tickers of your holdings a list. Example: \"SPY, AAPL, MSFT\"", key="ticker")

# TODO: Allow user to upload downloaded holdings from brokerage

# TODO: Encapsulate pieces into functions into methods

# Remove extra info and prepare for ticker use
ticker_input = ticker_input.replace(' ', '')
ticker_input = ticker_input.upper()

# If there is input, parse the data
if ticker_input.strip():
    tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
    #Create data frame and allow editing

    st.write('Use the "No. Shares held" column to manually enter how many shares you hold.')
    df = pd.DataFrame({"Tickers": tickers, "No. Shares held": [0.0]*len(tickers)})
    input_data = st.data_editor(df, num_rows="fixed", use_container_width=True)


    total_value = 0
    st.markdown("## Current Value of Your Portfolio")


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

    st.markdown(f"#### Total Portfolio Value: ${round(total_value, 2):,}*")
    st.write("*Based on last market close.")





    # Dynamic line graph of portfolio value over time
    st.markdown("## Portfolio Value Over Time")
    st.write("*How has your portfolio performed historically?* Below is a representation of your portfolio " \
    "performance throughout time. *Note this assumes you've held the same portfolio the entire time period.")

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


    # TODO: Only show graph if valid selection


    try:
        st.markdown("## Day-To-Day Performance")
        st.write("*How does your portfolio perform each day?* Below we can see a breakdown " \
        "of the percent return your portfolio provides. The height of each column indicates how often " \
        "a return of that much occurs.")

        # Display histogram of daily returns
        percent_returns = dm.get_percent_returns(data=portfolio_timeline)["Percent_return"]
        
        fig, ax = plt.subplots()
        ax.hist(percent_returns, bins=30, edgecolor="black")
        ax.set_title("Histogram of Daily Percent Returns")
        ax.set_xlabel("Daily Percent Return (%)")
        ax.set_ylabel("Frequency")

        st.pyplot(fig)



        # Monte Carlo Simulation
        st.markdown("## Possible Future Performance")
        st.write("*Where can we expect to see your portfolio in the future?* Below is a statisical " \
        "representaion of where your portfolio could be given random returns on each day.")

        monte_carlo_period = st.selectbox("Select time frame for Monte Carlo Simulation", options = ["1mo", "6mo", "1y", "5y", "10y", "20y", "40y"], index=2)
    
        monte_sim_results = sa.sim_monte_carlo(portfolio_timeline, time_period=monte_carlo_period)

        percentiles_to_use = [5, 10, 25, 50, 75, 90, 95]
        monte_percentiles_df = monte_sim_results.apply(lambda row: np.percentile(row, percentiles_to_use), axis=1)

        # This gives a DataFrame of shape (NUM_DAYS, len(percentiles_to_use))
        # Now convert it to a proper DataFrame with named columns
        monte_percentiles_df = pd.DataFrame(
            monte_percentiles_df.tolist(),
            columns=[f"{p}th Pctl" for p in percentiles_to_use]
        )

        
        st.line_chart(monte_percentiles_df)

        st.write("*How does the above simulation work?* The simulation used here is called a Monte Carlo " \
        "Simulation. To do this simulation, we take historical daily returns of your portfolio and use them" \
        " as possible returns on any given day. For every day of the time period you select, we randomly determine" \
        " the return on that day and continue until we reach the period. This process is repeated 200 times and " \
        "we select a few of the possible returns (here we choose these percentiles) and graph those.")

        st.write("*How do I interpret this graph?* Each line represented is an important percentile of the " \
        "data generated in the simulation. For example, the \"10th Pctl\" line means, \"10% of all the " \
        "simulations ended below this line\". Additionally the \"75th Pctl\" line means 75% all simulations" \
        " ended below this line.")

        st.write("*Important note:* This simulation is based purely on random chance and is not representative" \
        " of your actual portfolio over time. The simulation does not take into account various economic, " \
        "political, or global conditions.")

    except:
        pass

else:
    st.info("Please enter at least one ticker to get started")


