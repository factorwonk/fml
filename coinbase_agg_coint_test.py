import os
import pandas as pd
import matplotlib.pyplot as plt

from coinbase_agg_crypto import crypto_wallet
from datetime import datetime


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
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//coinbase_outputs"
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
    return norm_prices


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
    print("Done")

