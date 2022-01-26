import os
import pandas as pd


def load_binance_data():
    # display all columns in output
    pd.set_option("display.max_columns", None)
    # Hardcode path for binance data
    path = (
        "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_data//"
    )
    df = pd.read_parquet(os.path.join(path, "BTC-USDT.parquet"))
    select_cols = ["close", "volume", "number_of_trades"]
    df = df[select_cols]
    return df


if __name__ == "__main__":
    print("Start loading Binance Data\n")
    print("\nBTC_USDT pair\n")
    a = load_binance_data()
    print(a)
    print("\nEnd\n")
