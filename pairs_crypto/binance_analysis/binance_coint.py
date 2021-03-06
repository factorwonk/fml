from cgi import test
import os
import pandas as pd
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt

from datetime import datetime
from binance_utilities import load_binance_wallet, pivot_binance_wallet
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.stattools import adfuller


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
    """
    Takes in the minute-wise binance tick data and returns resampled, end-of-day data

    Args:
        wallet_df (_type_): _description_
    """
    eod_wallet_df = minute_wallet_df
    # convert index to datetime
    eod_wallet_df.index = pd.to_datetime(eod_wallet_df.index)
    eod_wallet_df = eod_wallet_df.resample("1D", closed="right").first()
    return eod_wallet_df


def calc_adf_agg_series(wallet_df):
    """_summary_

    Args:
        wallet_df (_type_): _description_

    Returns:
        _type_: _description_
    """
    adf_pairs = []
    for c1 in wallet_df.columns:
        test_result = ts.adfuller(wallet_df[c1].dropna())
        adf_pairs.append([c1, test_result[1]])
    return adf_pairs
    # return c1, test_result


def calc_coint_agg_series(wallet_df):
    """
    Engle-Granger Two Step Cointegration method. Runs quickly with daily data and slowly with hourly data

    Args:
        wallet_df ([DataFrame]): [Crypto wallet with end-of hour or end of day prices]
    """
    list_pairs = []
    for a1 in wallet_df.columns:
        for a2 in wallet_df.columns:
            if a1 != a2:
                test_result = ts.coint(wallet_df[a1].fillna(0), wallet_df[a2].fillna(0))
                list_pairs.append([a1, a2, test_result[1]])
    # print(list_pairs)
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
    return [x for x in list_pairs if x[2] <= 0.01]


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
    # This does not have a set time index
    print("\n Loading in the entire Binance Crypto Wallet as of", today)
    print("\n")
    a = load_binance_wallet(crypto_array)
    print(a)
    print("Pivot data into usable format")
    b = pivot_binance_wallet()
    # To check rebalancing function
    # print(b.head(61))
    print(b)
    # print("Resampling to hourly data")
    # c = resample_min_to_hourly(b)
    # print(c)
    # Not much value from looking at intraday data at this stage.
    print("Resampling to daily data")
    d = resample_min_to_daily(b)
    print(d)
    print("\n")
    print("Count NaNs")
    print(d.isna().sum())
    print("\n")
    # print("ADF Test of Stationary for each crypto pair\n")
    # x = calc_adf_agg_series(d)
    # print(x)
    print("Engle Granger cointegration using daily data for crypto pairs\n")
    e = calc_coint_agg_series(d)
    print(e)
    print("\n Daily trading pairs signifcant at the 0.01 level\n")
    f = identify_significant_pairs(e)
    print(f)
    # This takes a while. Go make a cup of coffee.
    # print("\n Calculate Engle Granger cointegration using hourly data\n")
    # print("This takes a while. Go get a coffee\n")
    # g = calc_coint_agg_series(c)
    # print(g)
    # print("\n Hourly trading pairs signifcant at the 0.01 level\n")
    # h = identify_significant_pairs(g)
    # print(h)
    print("\n Done")
