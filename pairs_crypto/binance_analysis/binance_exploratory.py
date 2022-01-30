import os
import pandas as pd

import matplotlib.pyplot as plt

from datetime import datetime

# Reequires pyarrow and fastparquet libraries to be loaded in


def load_single_binance_pair(symbol) -> pd.DataFrame:
    """Returns a dataframe containing minute-wise trade data for crypto pair sourced from binance

    Args:
        symbol (string): Crypto pair symbol to be sourced from binance

    Returns:
        DataFrame: Dataframe containing time, symbol, open, close and volume data for crypto pair
    """
    # Hardcode path for binance data - for now
    path = (
        "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_data//"
    )
    try:
        df = pd.read_parquet(os.path.join(path, "%s.parquet" % symbol))
        select_cols = ["open", "volume", "number_of_trades"]
        df = df[select_cols].reset_index()
        # Add symbol column as identifier
        df["symbol"] = str(symbol.replace("-", "_"))
        return df
    except BaseException as error:
        print("An exception occurred: {}".format(error))


def load_binance_wallet() -> pd.DataFrame:
    """[summary]

    Returns:
        pd.DataFrame: [description]
    """
    # Init date = today
    date = datetime.now().strftime("%Y%m%d")
    # Init path
    output_path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_outputs//"
    # Init binance wallet
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
    # init empty df
    wallet_df = pd.DataFrame()
    # Appending dataframes this way is not efficient. Append to a list first, then convert to DF
    for c in crypto_array:
        wallet_df = wallet_df.append(load_single_binance_pair(c))
    wallet_df.to_csv(
        os.path.join(output_path, f"binance_merged_{date}.csv"), index=False
    )
    return wallet_df


def chart_1min_binance_price_vols(input_df, symbol):
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # init path
    save_path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_outputs//"
    fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8), sharex=True)
    fig.suptitle("Close Price and Volume Charts")
    ax1.plot(input_df["open_time"], input_df["open"], label="Open Price")
    ax2.plot(input_df["open_time"], input_df["volume"], label="Volume")
    plt.legend("Price and Volume History")
    plt.savefig(os.path.join(save_path, f"%s_price_vol_{date}.png" % symbol))
    plt.close(fig)


if __name__ == "__main__":
    # print("\nStart loading 1 minute Binance Data\n")
    # print(
    #     "Enter the Crypto symbol you want price and volume history for: BTC-USDT; ETH-USDT etc"
    # )
    # crypto_symbol = input()
    # print("\n %s pair history \n" % str(crypto_symbol))
    # a = load_single_binance_pair(crypto_symbol)
    # print(a)
    # print("\nCharting the price and volume for %s\n" % str(crypto_symbol))
    # chart_1min_binance_price_vols(a, crypto_symbol)
    print("\n Loading in the entire Binance Crypto Wallet\n")
    b = load_binance_wallet()
    print(b)
    print("Done!\n")
