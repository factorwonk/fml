import pandas as pd

from coinbase_data.coinbase_extract_script import fetch_daily_data


def import_btc_usd():
    df = pd.read_csv("Coinbase_BTCUSD_dailydata.csv")
    return df


if __name__ == "__main__":
    # we set which pair we want to retrieve data for
    print("starting...")
    fetch_daily_data("BTC/USD")
    a = import_btc_usd()
    print(a.head())
    print("done...")
