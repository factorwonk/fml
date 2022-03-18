import os
import pandas as pd
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt

from datetime import datetime
from binance_utilities import load_binance_wallet, pivot_binance_wallet
from statsmodels.tsa.vector_ar.vecm import coint_johansen


def resample_min_to_hourly(minute_wallet_df):
    """
        Takes in the minute-wise binance tick data and returns resampled, hourly data

    Args:
        minute_wallet_df (_type_): _description_
    """

    eoh_wallet_df = minute_wallet_df
    # convert index to datetime
    eoh_wallet_df.index = pd.to_datetime(eoh_wallet_df.index)
    eoh_wallet_df = eoh_wallet_df.resample("1H", closed="right").first()
    return eoh_wallet_df


def resample_min_to_daily(minute_wallet_df):
    """_summary_

    Args:
        wallet_df (_type_): _description_
    """
    eod_wallet_df = minute_wallet_df
    # convert index to datetime
    eod_wallet_df.index = pd.to_datetime(eod_wallet_df.index)
    eod_wallet_df = eod_wallet_df.resample("1D", closed="right").first()
    return eod_wallet_df


def calc_coint_agg_series(wallet_df):
    """Engle-Granger Two Step Cointegration method. This needs to be run on daily data

    Args:
        wallet_df ([DataFrame]): [Crypto wallet with end-of hour or end of day prices]
    """
    list_pairs = []
    for a1 in wallet_df.columns:
        for a2 in wallet_df.columns:
            if a1 != a2:
                test_result = ts.coint(wallet_df[a1].fillna(0), wallet_df[a2].fillna(0))
                list_pairs.append([a1, a2, test_result[1]])
    print(list_pairs)
    return list_pairs


def calc_joh_coint_agg_series(wallet_df):

    """
        Johansen cointegration test of the cointegration rank of a VECM
        Parameters
        ----------
        endog : array_like (nobs_tot x neqs)
            Data to test
        det_order : int
            * -1 - no deterministic terms - model1
            * 0 - constant term - model3
            * 1 - linear trend
        k_ar_diff : int, nonnegative
            Number of lagged differences in the model.
    """
    return coint_johansen(wallet_df.fillna(0), 0, 1).lr1


def identify_significant_pairs(list_pairs):
    """Takes in a a list of lists, which include the pairs and the third element of each list is L.O.S.

    Args:
        list_pairs (list of lists): First element is crypto pair 1, second element crypto pair 2 and third element is L.O.S.
    """
    return [x for x in list_pairs if x[2] <= 0.05]


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
    print("Pivot data into usable format")
    b = pivot_binance_wallet()
    # To check rebalancing function
    # print(b.head(61))
    print(b)
    print("Resample to hourly data")
    c = resample_min_to_hourly(b)
    print(c)
    print("Resample to daily data")
    d = resample_min_to_daily(b)
    print(d)
    # print("Calculate Engle Granger cointegration for each crypto pair")
    # calc_coint_agg_series(b)
    print("\n")
    print("Done")
