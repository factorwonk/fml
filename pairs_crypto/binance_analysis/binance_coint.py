from cgi import test
import os
import pandas as pd
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt

from datetime import datetime
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

