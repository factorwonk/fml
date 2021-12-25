import os
import pandas as pd
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt

from datetime import datetime
from coinbase_analysis.coinbase_agg_crypto import crypto_wallet
from statsmodels.tsa.vector_ar.vecm import coint_johansen


def transform_crypto_wallet():
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//coinbase_outputs"
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # Get rid of index_col = 0 later on
    df = pd.read_csv(os.path.join(path, f"coinbase_merged_{date}.csv"), index_col=0)
    # Select either Ethereum or Bitcoin for now
    df = df.reset_index()
    # Pivot
    pivot_df = df.pivot(index="date", columns="symbol", values="close")
    df = pd.DataFrame(pivot_df.to_records()).set_index("date")
    # Forward fill values with linear extrapolation
    df = df.interpolate(method="linear", limit_area="inside")
    return df


def plot_crypto_prices(wallet_df):
    # Today's date
    date = datetime.now().strftime("%Y%m%d")
    # Output path
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//coinbase_outputs"
    # Standardize by dividing by the first available value of each Crypto price
    norm_prices = [
        wallet_df[col].divide(wallet_df[col].loc[~wallet_df[col].isnull()].iloc[0])
        for col in wallet_df.columns
    ]
    norm_prices = pd.DataFrame(norm_prices).transpose()
    fig, ax = plt.subplots(1, figsize=(10, 8))
    fig.suptitle("Performance of Cryptocurrencies")
    ax.plot(norm_prices)
    plt.xlabel("Days")
    plt.legend("Assets")
    plt.savefig(os.path.join(path, f"crypto_performance_{date}.png"))
    plt.close(fig)
    return norm_prices


def calc_coint_agg_series(wallet_df):
    """Engle-Granger Two Step Cointegration

    Args:
        wallet_df ([DataFrame]): [Cryto wallet with prices up to a particular day]
    """
    for a1 in wallet_df.columns:
        for a2 in wallet_df.columns:
            if a1 != a2:
                test_result = ts.coint(wallet_df[a1].fillna(0), wallet_df[a2].fillna(0))
                print(a1 + " and " + a2 + ": p-value = " + str(test_result[1]))


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


if __name__ == "__main__":
    print("\n")
    print("Importing currencies into today's crypto wallet")
    a = crypto_wallet()
    print(a)
    print("\n")
    print("Pivot data into usable format")
    b = transform_crypto_wallet()
    print(b)
    print("\n")
    print("Plot normalized Crypto prices")
    c = plot_crypto_prices(b)
    print(c)
    print("\n")
    print("Calculate Engle Granger cointegration for each crypto pair")
    calc_coint_agg_series(b)
    print("\n")
    print("Calculate Johansen Cointegration of all pairs")
    d = calc_joh_coint_agg_series(b)
    print("\n")
    print(d)
    print("\n")
    print("Done")
