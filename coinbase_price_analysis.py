import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from coinbase_data.coinbase_extract_script import fetch_daily_data


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
    df = df.set_index("date")
    return df


def calc_returns_vols(input_df):
    output_df = input_df
    # Calculate daily returns from close data
    output_df["close_return"] = output_df.close.pct_change(1)
    # Calculate log returns from close daata
    output_df["close_log_return"] = np.log(output_df.close) - np.log(
        output_df.close.shift(1)
    )
    # Calculate 20 day average daily volume
    output_df["20_day_adv"] = output_df.volume.rolling(20).sum() / 20.0
    return output_df


def chart_price_vols(input_df):
    fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8), sharex=True)
    fig.suptitle("Price and Volume Charts")
    ax1.plot(a["date"], a["close"], label="Close Price")
    ax2.plot(a["date"], a["volume"], label="Volume")
    plt.show()
    plt.legend("Close Price History")
    return 0


if __name__ == "__main__":
    # we set which pair we want to retrieve data for
    print("\n")
    print(
        "Enter the Crypto symbol you want price and volume history for e.g. BTC/USD, ETH/EUR etc"
    )
    print("\n")
    crypto_symbol = input()
    # a = import_crypto_ts("BTC/USD")
    print("Fetching...")
    a = calc_returns_vols(import_crypto_ts(crypto_symbol))
    print(a.tail(10))
    print("\n")
    print("done...")
