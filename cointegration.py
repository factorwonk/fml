import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

from statsmodels.tsa.stattools import coint
from statsmodels.tsa.stattools import adfuller
from datetime import datetime


def transform_data():
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//coinbase_outputs"
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # Get rid of index_col = 0 later on
    df = pd.read_csv(os.path.join(path, f"coinbase_merged_{date}.csv"), index_col=0)
    # Select either Ethereum or Bitcoin for now
    df = df[(df.symbol == "ETH/USD") | (df.symbol == "BTC/USD")].reset_index()
    # Pivot
    pivot_df = df.pivot(index="date", columns="symbol", values="close")
    df = pd.DataFrame(pivot_df.to_records()).set_index("date")

    return df


def cointegrate_series(df):
    x = df["BTC/USD"]
    y = df["ETH/USD"]
    X1 = sm.add_constant(x)

    ols1 = sm.OLS(y, X1).fit()
    resid1 = ols1.resid
    # test for the unit roots in residuals (null hypothesis)
    aeg_test = adfuller(resid1, regression="n", autolag="AIC", store=True)
    aeg_test
    print(aeg_test[-1].resols.summary())


if __name__ == "__main__":
    print("Going to extract and transform the data from csv...")
    print("\n")
    a = transform_data()
    print(a)
    print("\n")
    print("Going to return Engle-Granger Cointegration of series...")
    b = cointegrate_series(a)
    print(b)
    print("\n")
    print("Done!")
