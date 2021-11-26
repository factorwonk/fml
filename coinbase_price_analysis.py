import pandas as pd
import matplotlib.pyplot as plt

from coinbase_data.coinbase_extract_script import fetch_daily_data


def import_btc_usd(symbol):
    fetch_daily_data(symbol)
    df = pd.read_csv("Coinbase_BTCUSD_dailydata.csv")
    # select columns of interest
    df = df[["date", "open", "close", "high", "low", "volume"]]
    return df


if __name__ == "__main__":
    # we set which pair we want to retrieve data for
    print("starting...")
    print("\n")
    a = import_btc_usd("BTC/USD")
    print(a.head())
    print("\n")
    a.plot.line(x="date", y="close")
    plt.show()
    plt.legend("BTC/USD Close Price")
    print("\n")
    print("done...")
