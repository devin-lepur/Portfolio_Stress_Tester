'''
File: data_manipulation.py
Purpose: Functions for altering and manipulating data
Author: Devin Lepur
Date: June 30, 2025
'''

import pandas as pd
import numpy as np

def get_percent_returns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates percent return for DataFrame
    
    Args:
        data (pd.DataFrame): pandas data frame holding data with "Date", and "Close" columns.
    
    Returns:
        pandas DataFrame: Time frame adjusted daily percent returns.
    """



    data["Percent_return"] = data["Close"].pct_change() * 100

    return data