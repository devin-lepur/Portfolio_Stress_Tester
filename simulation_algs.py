'''
File: simulation_algs.py
Purpose: Algorithms for simulating potential economic events
Author: Devin Lepur
Date: June 24, 2025
'''

import numpy as np
import pandas as pd

# TODO: Value at Risk Estimator (VaR)


# TODO: Historical crash simulation (Dot Com bubble, Housing Crisis, COVID-19)


# TODO: allow for dynamic number of days simulated
def sim_monte_carlo(data):

    NUM_SIMULATIONS = 50
    NUM_DAYS = 360

    log_return = np.log(1+data["Close"].pct_change())
    log_return = log_return[1:]

    daily_volatility = np.std(log_return)


    last_price = data["Close"].iloc[-1]
    simulation_results = []

    for i in range(NUM_SIMULATIONS):
        price_series = [last_price]

        for j in range(1, NUM_DAYS):
            price = price_series[-1] * (1 + np.random.normal(0, daily_volatility))
            price_series.append(price)

        simulation_results.append(price_series)

    simulation_df = pd.DataFrame(simulation_results).transpose()

    return simulation_df