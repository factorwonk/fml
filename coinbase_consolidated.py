from coinbase_agg_crypto import crypto_wallet, transform_crypto_wallet
from coinbase_agg_coint_test import (
    calc_joh_coint_agg_series,
    plot_crypto_prices,
    calc_coint_agg_series,
)
from datetime import datetime

if __name__ == "__main__":

    """
    Putting it all together now:
    1. Extract historical crypto prices
    2. Calculate cointegration for all crypto pairs
    3. Determine if cointegration is significant
    4. Fit spread for significant cointegration
    """
    print("\n")
    print("Downloading crypto wallet for %s" % datetime.now().strftime("%Y-%m-%d"))
    a = crypto_wallet()
    print("\n")
    print("Transforming crypto wallet data to wide format:")
    b = transform_crypto_wallet()
    print(b)
    print("\n")
    print("Plot crypto price data history:")
    print("\n")
    c = plot_crypto_prices(b)
    print("Prices normalized by data start date for each crypto are:")
    print(c)
    print("\n")
    print("Reporting pairwise ADF cointegration values:")
    print("\n")
    calc_coint_agg_series(b)
    print("\n")
    print("Reporting Johansen statistics for all series")
    d = calc_joh_coint_agg_series(b)
    print(d)
    print("\n")
    print("Done!")
