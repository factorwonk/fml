import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

from statsmodels.tsa.stattools import coint
from statsmodels.tsa.stattools import adfuller
from datetime import datetime


def cointegrate_series():
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//coinbase_outputs"
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # Get rid of index_col = 0 later on
    df = pd.read_csv(os.path.join(path, f"coinbase_merged_{date}.csv"), index_col=0)
    # Select either Ethereum or Bitcoin for now
    df = df[(df.symbol == "ETH/USD") | (df.symbol == "BTC/USD")]
    return df


if __name__ == "__main__":
    print("Going to return Engle-Granger Cointegration of series...")
    print("\n")
    a = cointegrate_series()
    print(a.tail())
    print("Done!")

