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
from coinbase_analysis.coinbase_fit_spread_oruh import (
    filter_significant_pairs,
    regression,
    fit_spread_oruh,
)
from datetime import datetime


def fillna_pivoted_df(input_df):
    output_df = input_df.fillna(0)
    return output_df


def run():
    """
    Putting it all together now:
    1. Extract historical crypto prices
    2. Calculate cointegration for all crypto pairs
    3. Determine if cointegration is significant
    4. Fit spread for significant cointegration
    """
    today = datetime.now().strftime("%Y-%m-%d")
    print("\n")
    print("Downloading crypto wallet for %s" % str(today))
    a = crypto_wallet()
    print("\n")
    print(a)
    print("Transforming crypto wallet data to wide format:\n")
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
    print("Filtering for significant pairs:")
    print("\n")
    g = fillna_pivoted_df(b)
    print(g)
    print("\n")
    h = filter_significant_pairs(g, f)
    print("Subsetted DataFrame with significant pairs:\n")
    print(h)
    print("\n")
    print(h.iloc[:, 2])
    print("\n")
    print(h.iloc[:, 3])
    print("\n")
    print("Get Regression Value for each pair:\n")
    x, y, z = regression(h.iloc[:, 2], h.iloc[:, 3])
    print("\nCoefficients:\n")
    print(x)
    print("\nIntercept\n")
    print(y)
    print("\nResiduals\n")
    print(z)
    print("\n")
    print("Fit the spread to the OH process")
    print("\n")
    fit_spread_oruh(z)
    print("Done!")


if __name__ == "__main__":
    run()
