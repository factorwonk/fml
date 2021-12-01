import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from coinbase_data.coinbase_extract_script import fetch_daily_data
from coinbase_price_vol_dl_stats import import_crypto_ts


def crypto_wallet():
    # This depends on data availabilty
    crypto_array = ["BTC/USD", "ETH/USD", "DOGE/USD", "SOL/USD"]
    wallet_df = pd.DataFrame()
    # wallet_df = [wallet_df.append(import_crypto_ts(c)) for c in crypto_array]
    for c in crypto_array:
        wallet_df = wallet_df.append(import_crypto_ts(c))
    return wallet_df


if __name__ == "__main__":
    # Loop through and extract price data for various crypto currencies
    print("start...")
    print("\n")
    print("Extract historical price and volume data from Coinbase for listed Cryptos.")
    a = crypto_wallet()
    print(a.tail(10))
    print("\n")
    print("done...")
