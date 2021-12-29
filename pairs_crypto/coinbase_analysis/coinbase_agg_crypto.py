import os
import pandas as pd

from coinbase_analysis.coinbase_price_vol_dl_stats import import_crypto_ts
from datetime import datetime


def crypto_wallet():
    # This depends on data availabilty from Coinbase
    crypto_array = [
        "BTC/USD",
        "ETH/USD",
        "DOGE/USD",
        "SOL/USD",
        "LTC/USD",
        "ZEC/USD",
        "ADA/USD",
        "DAI/USD",
        "SHIB/USD",
        "MATIC/USD",
    ]
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # init path
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//coinbase_outputs"
    # init empty df
    wallet_df = pd.DataFrame()
    # Appending dataframes this way is not efficient. Append to a list first, then convert to DF
    for c in crypto_array:
        wallet_df = wallet_df.append(import_crypto_ts(c))
    wallet_df.to_csv(os.path.join(path, f"coinbase_merged_{date}.csv"), index=False)
    return wallet_df


def transform_crypto_wallet():
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//coinbase_outputs"
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # Get rid of index_col = 0 later on
    df = pd.read_csv(
        os.path.join(path, f"coinbase_merged_{date}.csv"), index_col=0
    ).reset_index()
    # Pivot
    pivot_df = df.pivot(index="date", columns="symbol", values="close")
    output_df = pd.DataFrame(pivot_df.to_records()).set_index("date")
    # Forward fill values with linear extrapolation
    output_df = output_df.interpolate(method="linear", limit_area="inside")
    # Don't backfill missing values with zero just yet.
    # output_df = output_df.fillna(0)
    return output_df


if __name__ == "__main__":
    # Loop through and extract price data for various crypto currencies
    print("start...")
    print("\n")
    print("Extracting historical price and volume data from Coinbase...\n")
    a = crypto_wallet()
    print(a.head(10))
    print("\n")
    print("Pivot crypto wallet...\n")
    b = transform_crypto_wallet()
    print(b.head(10))
    print("\n")
    print("See the tail of this crypto wallet\n")
    print(b.tail(10))
    print("\nDone...")
