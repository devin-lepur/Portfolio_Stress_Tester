'''
File: data_manipulation.py
Purpose: Functions for altering and manipulating data
Author: Devin Lepur
Date: June 30, 2025
'''

import pandas as pd

def get_percent_returns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates percent return for DataFrame
    
    Args:
        data (pd.DataFrame): pandas data frame holding data with "Date", and "Close" columns.
    
    Returns:
        pandas DataFrame: Time frame adjusted daily percent returns.
    """


    # % return = (close value - previous close value) / previous close value * 100
    data["Percent_return"] = 0

    for i, row in data.iterrows():
        if i == 0:      # Skip return for the oldest date
            continue
        curr_price = row["Close"]
        prev_price = data["Close"].iloc[i-1]
        
        data.at[i, "Percent_return"] = (curr_price - prev_price) / prev_price * 100.0

    return data