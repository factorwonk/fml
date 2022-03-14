from cgi import test
import os
import pandas as pd
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt

from datetime import datetime
from binance_utilities import load_binance_wallet, pivot_binance_wallet
from statsmodels.tsa.vector_ar.vecm import coint_johansen


def calc_coint_agg_series(wallet_df):
    """Engle-Granger Two Step Cointegration method

    Args:
        wallet_df ([DataFrame]): [Crypto wallet with prices up to a particular day]
    """
    list_pairs = []
    for a1 in wallet_df.columns:
        for a2 in wallet_df.columns:
            if a1 != a2:
                test_result = ts.coint(wallet_df[1].fillna(0), wallet_df[a2].fillna(0))
                list_pairs.append([a1, a2, test_result[1]])
    print(list_pairs)
    return list_pairs


if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    crypto_array = [
        "ADA-USDT",
        "BTC-USDT",
        "DOGE-USDT",
        "ETH-USDT",
        "LTC-USDT",
        "MATIC-USDT",
        "SOL-USDT",
        "ZEC-USDT",
    ]
    print("\n Loading in the entire Binance Crypto Wallet on", today)
    print("\n")
    a = load_binance_wallet(crypto_array)
    print(a)
    print("Done")
