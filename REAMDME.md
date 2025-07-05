
# Stock Portfolio Stress Tester
[Try the Portfolio Stress Tester for yourself!](https://portfolio-stress-tester.streamlit.app/)


This project is a web-based application built with Streamlit that allows users to test the resiliency of their stock portfolios under different historical and simulated conditions. It is designed for individual investors who want a better understanding of how their holdings would perform over time and under random market fluctuations. The app enables users to input their stock tickers and the number of shares they hold to visualize historical portfolio value, analyze daily return distributions, and simulate possible future performance using Monte Carlo techniques.

Once the user enters a list of ticker symbols, the app retrieves real-time and historical stock price data using the Yahoo Finance API. It calculates the current value of each holding based on the latest closing prices and outputs the total value of the portfolio. Users are also able to select a time window (e.g., 1 month, 6 months, 1 year, etc.) to see how their portfolio would have performed historically if they had held the same assets during that entire time period. This is visualized through a dynamic line chart.

The app then computes the daily percent returns of the portfolio and displays a histogram that shows how frequently certain return levels have occurred. This helps users understand the day-to-day volatility of their investments. For forward-looking analysis, the app runs a Monte Carlo simulation based on historical returns. It randomly samples daily returns over a user-selected time frame and performs 200 simulations to generate a range of possible future portfolio values. The results are presented as a series of percentile lines (e.g., 10th, 50th, 90th percentiles) to show expected distributions of outcomes.

The simulation works by:

Calculating daily returns from the historical portfolio timeline.

Sampling those returns at random for each day in the simulated time period.

Repeating the simulation process 200 times to produce a wide distribution of possible outcomes.

Aggregating the results into percentile summaries for display.

The price data and historical time series used in this application are sourced via the yfinance Python library, which pulls data directly from Yahoo Finance. This allows the app to remain lightweight and requires no user authentication or financial data storage.
