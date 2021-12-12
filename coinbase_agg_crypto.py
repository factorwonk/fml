import os
import pandas as pd

from coinbase_price_vol_dl_stats import import_crypto_ts
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
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//coinbase_outputs"
    # init empty df
    wallet_df = pd.DataFrame()
    # Appending dataframes this way is not efficient. Append to a list first, then convert to DF
    for c in crypto_array:
        wallet_df = wallet_df.append(import_crypto_ts(c))
    wallet_df.to_csv(os.path.join(path, f"coinbase_merged_{date}.csv"), index=False)
    return wallet_df


if __name__ == "__main__":
    # Loop through and extract price data for various crypto currencies
    print("start...")
    print("\n")
    print("Extracting historical price and volume data from Coinbase...")
    a = crypto_wallet()
    print(a.tail(10))
    print("\n")
    print("Saving to output folder...")
    print("done...")
