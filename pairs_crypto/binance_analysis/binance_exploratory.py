import os
import pandas as pd

import matplotlib.pyplot as plt

from datetime import datetime


def load_1min_binance_data():
    # display all columns in output
    pd.set_option("display.max_columns", None)
    # Hardcode path for binance data
    path = (
        "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_data//"
    )
    df = pd.read_parquet(os.path.join(path, "BTC-USDT.parquet"))
    # Filter down to columns of interest
    # Index is open time, hence use open prices
    select_cols = ["open", "volume", "number_of_trades"]
    df = df[select_cols].reset_index()
    return df


def chart_1min_binance_price_vols(input_df):
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # init path
    save_path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_outputs//"
    fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8), sharex=True)
    fig.suptitle("Close Price and Volume Charts")
    ax1.plot(a["open_time"], a["open"], label="Open Price")
    ax2.plot(a["open_time"], a["volume"], label="Volume")
    plt.legend("Price and Volume History")
    plt.savefig(os.path.join(save_path, f"BTC_USDT_price_vol_{date}.png"))
    plt.close(fig)


if __name__ == "__main__":
    print("Start loading 1 minute Binance Data\n")
    print("\nBTC_USDT pair\n")
    a = load_1min_binance_data()
    print(a)
    print("\nCharting the price and volume for BTC_USDT\n")
    chart_1min_binance_price_vols(a)
    print("\nEnd\n")
