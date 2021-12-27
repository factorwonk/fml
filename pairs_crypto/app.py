from coinbase_analysis.coinbase_agg_crypto import (
    crypto_wallet,
    transform_crypto_wallet,
)
from coinbase_analysis.coinbase_agg_coint_test import (
    calc_joh_coint_agg_series,
    plot_crypto_prices,
    calc_coint_agg_series,
    identify_significant_pairs,
)
from datetime import datetime


def run():
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
    print(a)
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
    d = calc_coint_agg_series(b)
    print(d)
    print("\n")
    print("Reporting Johansen statistics for all series")
    e = calc_joh_coint_agg_series(b)
    print(e)
    print("\n")
    print("These are the significant pairs:")
    print("\n")
    f = identify_significant_pairs(d)
    print(f)
    print("\n")
    print("Done!")


if __name__ == "__main__":
    run()
