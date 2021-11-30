import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from coinbase_data.coinbase_extract_script import fetch_daily_data

# from statsmodels.tsa.seasonal import seasonal_decompose, STL


def import_crypto_ts(symbol):
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//coinbase_data"
    fetch_daily_data(symbol)
    df = pd.read_csv(
        os.path.join(path, "Coinbase_%s_dailydata.csv" % symbol.replace("/", "")),
        parse_dates=["date"],
    )
    # df = pd.read_csv("Coinbase_BTCUSD_dailydata.csv", parse_dates=["date"])
    # select columns of interest
    df = df[["date", "open", "close", "high", "low", "volume"]]
    return df


def calc_return(input_df):
    output_df = input_df
    # Calculate daily returns from close data
    output_df["close_return"] = output_df.close.pct_change(1)
    # Calculate log returns from close daata
    output_df["close_log_return"] = np.log(output_df.close) - np.log(
        output_df.close.shift(1)
    )
    return output_df


if __name__ == "__main__":
    # we set which pair we want to retrieve data for
    print("\n")
    print("Enter the Crypto symbol you want price history for e.g. BTC/USD")
    print("\n")
    crypto_symbol = input()
    # a = import_crypto_ts("BTC/USD")
    print("Fetching...")
    a = import_crypto_ts(crypto_symbol)
    b = calc_return(a)
    print(b.tail())
    b.plot.line(x="date", y="close")
    plt.show()
    plt.legend("Close Price History")
    print("\n")
    print("done...")
