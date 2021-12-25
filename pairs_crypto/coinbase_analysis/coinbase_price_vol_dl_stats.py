import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from coinbase_analysis.coinbase_extract_script import fetch_daily_data
from datetime import datetime


def import_crypto_ts(symbol):
    date = datetime.now().strftime("%Y%m%d")
    path = (
        "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//coinbase_data"
    )
    fetch_daily_data(symbol)
    df = pd.read_csv(
        os.path.join(
            path, f"Coinbase_%s_dailydata_{date}.csv" % symbol.replace("/", "")
        ),
        parse_dates=["date"],
    )
    # select columns of interest
    df = df[["date", "open", "close", "high", "low", "volume"]]
    # Add symbol column as identifier
    df["symbol"] = str(symbol)
    return df


def calc_returns_vols(input_df):
    output_df = input_df
    # Calculate daily returns from close data
    output_df["close_return"] = output_df.close.pct_change(1)
    # Calculate log returns from close daata
    output_df["close_log_return"] = np.log(output_df.close) - np.log(
        output_df.close.shift(1)
    )
    # Calculate 20 day Moving Average Price
    output_df["20_day_map"] = output_df.close.rolling(20).mean()
    # Calculate 20 day average daily volume
    output_df["20_day_adv"] = output_df.volume.rolling(20).mean()
    return output_df


def chart_price_vols(input_df, symbol):
    # Chart price and volume history and saves the file
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # init date
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//coinbase_outputs"
    fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8), sharex=True)
    fig.suptitle("Price and Volume Charts")
    ax1.plot(a["date"], a["close"], label="Close Price")
    ax2.plot(a["date"], a["volume"], label="Volume")
    plt.legend("Price and Volume History")
    plt.savefig(os.path.join(path, f"{symbol}_price_vol_{date}.png"))
    plt.close(fig)


if __name__ == "__main__":
    # we set which pair we want to retrieve data for
    print("\n")
    print(
        "Enter the Crypto symbol you want price and volume history for: BTC/USD; ETH/EUR etc"
    )
    print("\n")
    crypto_symbol = input()
    print("Fetching from Coinbase API...")
    a = calc_returns_vols(import_crypto_ts(crypto_symbol))
    print(a.tail(10))
    print("done...")
    print("\n")
    print("Charting Prices and Volumes")
    chart_price_vols(a, crypto_symbol.replace("/", ""))
    print("All done...")
