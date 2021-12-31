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
from coinbase_analysis.coinbase_test_cointegration import (
    test_stationarity,
    test_significance,
    test_cointegration,
)
from coinbase_analysis.coinbase_fit_spread_oruh import (
    filter_significant_pairs,
    fit_spread_oruh,
)
from coinbase_analysis.coinbase_utilities import (
    fillna_pivoted_df,
    calc_corr_matrix,
    regression,
)
from datetime import datetime


def run():
    """
    Putting it all together now:
    1. Extract historical crypto prices
    2. Calculate cointegration for all crypto pairs
    3. Determine if cointegration is significant
    4. Fit spread for significant cointegration to OH process
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
    g = fillna_pivoted_df(b)
    print(g)
    print("\n")
    print("Here are the correlations between all the pairs:\n")
    g_corr = calc_corr_matrix(g)
    print(g_corr)
    print("\n")
    print("These are the significant pairs:")
    print("\n")
    f = identify_significant_pairs(d)
    print(f)
    print("\n")
    print("Filtering for significant pairs:\n")
    h = filter_significant_pairs(g, f)
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
    print("Test the stationarity of the pair:\n")
    zz = test_stationarity(z)
    print(z)
    print("\n")
    print("Test the significance of these residuals:\n")
    yy = test_significance(h.iloc[:, 2], h.iloc[:, 3], z)
    print(yy)
    print("\n")
    print("Test against critical t-value of ADF and ECM\n")
    dd = test_cointegration(
        h.iloc[:, 2],
        h.iloc[:, 3],
        stat_value_ci=0.95,
        sig_value_ci=0.95,
        s1=str(list(h.columns.values)[0]),
        s2=str(list(h.columns.values)[1]),
    )
    print(dd)
    print("\n")
    print("Fit the spread to the OH process")
    print("\n")
    fit_spread_oruh(z)
    print("Done!")


if __name__ == "__main__":
    run()
