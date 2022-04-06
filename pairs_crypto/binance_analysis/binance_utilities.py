import os
import warnings
import pandas as pd

import matplotlib.pyplot as plt

from datetime import datetime, timedelta

# Requires pyarrow and fastparquet libraries to be loaded in


def load_single_binance_pair(symbol) -> pd.DataFrame:
    """Returns a dataframe containing minute-wise trade data for
    crypto pair sourced from binance

    Args:
        symbol (string): Crypto pair symbol to be sourced from binance

    Returns:
        DataFrame: Dataframe containing time, symbol, open, close and
        volume data for crypto pair
    """
    # Hardcode path for binance data - for now
    path = (
        "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_data//"
    )
    engine = "pyarrow"
    try:
        df = pd.read_parquet(
            os.path.join(path, "%s.parquet" % symbol), engine=engine
        ).reset_index()
        select_cols = ["open_time", "close", "volume", "number_of_trades"]
        df = df[select_cols]
        # Convert open_time to pandas timestamp
        df["open_time"] = pd.to_datetime(df["open_time"], errors="coerce")
        # Add close time to DataFrame
        df["close_time"] = df["open_time"] + timedelta(minutes=1)
        # Drop open_time
        df.drop("open_time", axis=1, inplace=True)
        # Add symbol column as identifier
        df["symbol"] = str(symbol.replace("-", "_"))
        return df
    except BaseException as error:
        print("An exception occurred: {}".format(error))


def chart_1min_binance_pair_price_vol(input_df, symbol):
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # init path
    save_path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_outputs//"
    fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8), sharex=True)
    fig.suptitle("Close Price and Volume Charts")
    ax1.plot(input_df["close_time"], input_df["close"], label="Close Price")
    ax2.plot(input_df["close_time"], input_df["volume"], label="Volume")
    plt.legend("Close Price and Volume History")
    plt.savefig(os.path.join(save_path, f"%s_price_vol_{date}.png" % symbol))
    plt.close(fig)


def load_binance_wallet(input_array) -> pd.DataFrame:
    """Takes an input list of crypto-pairs and returns their time series history

    Returns:
        pd.DataFrame: Returns a DataFrame with close price, volume,
        number of trades, close time and symbol
    """
    # Init date = today
    date = datetime.now().strftime("%Y%m%d")
    # Init path
    output_path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_outputs//"
    # Init binance wallet
    crypto_array = input_array
    # init empty df
    wallet_df = pd.DataFrame()
    # Appending dataframes this way is not efficient. Append to a list first, then convert to DF
    wallet_df = pd.concat([load_single_binance_pair(c) for c in crypto_array])
    # for c in crypto_array:
    #     wallet_df = wallet_df.append(load_single_binance_pair(c))
    wallet_df.to_csv(
        os.path.join(output_path, f"binance_merged_{date}.csv"), index=False
    )
    return wallet_df


def pivot_binance_wallet():
    # Must be run after the binance wallet is loaded
    read_path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_outputs//"
    # init date
    date = datetime.now().strftime("%Y%m%d")
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=FutureWarning)
        # Get rid of index_col = 0 later on
        df = pd.read_csv(
            os.path.join(read_path, f"binance_merged_{date}.csv"), index_col=0
        ).reset_index()
        # Pivot
        pivot_df = df.pivot(index="close_time", columns="symbol", values="close")
        output_df = pd.DataFrame(pivot_df.to_records()).set_index("close_time")
        # Forward fill values with linear extrapolation if required
        output_df = output_df.interpolate(method="linear", limit_area="inside")
        # Don't backfill missing values with zero just yet.
        # output_df = output_df.fillna(0)
    return output_df


def normalize_binance_wallet(wallet_df) -> pd.DataFrame:
    """Normalize price history of crypto wallet dataframe dividing by 
    the first available value for each crypto pair

    Args:
        wallet_df (DataFrame): Output of pivot_binance_wallet function

    Returns:
        pd.DataFrame: [description]
    """
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # output path
    save_path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_outputs//"
    norm_prices = [
        wallet_df[col].divide(wallet_df[col].loc[~wallet_df[col].isnull()].iloc[0])
        for col in wallet_df.columns
    ]
    norm_prices = pd.DataFrame(norm_prices).transpose()
    # Write out normalized wallet to folder
    norm_prices.to_csv(
        os.path.join(save_path, f"binance_normalized_{date}.csv"), index=False
    )
    return norm_prices


def plot_normalized_binance_wallet():
    # Today's date
    date = datetime.now().strftime("%Y%m%d")
    # Path to input dataframe
    input_path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_outputs"
    norm_wallet_df = pd.read_csv(
        os.path.join(input_path, f"binance_normalized_{date}.csv")
    )
    # Output path
    output_path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//binance_outputs"
    fig, ax = plt.subplots(1, figsize=(15, 8))
    fig.suptitle("Performance of Cryptocurrencies")
    ax.plot(norm_wallet_df)
    plt.xlabel("History")
    plt.legend("COINS")
    plt.savefig(os.path.join(output_path, f"crypto_performance_{date}.png"))
    plt.close(fig)
    return norm_wallet_df


if __name__ == "__main__":
    # print("\nStart loading 1 minute Binance Data\n")
    # print("Enter Crypto symbol pair: BTC-USDT; ETH-USDT etc")
    # crypto_symbol = input()
    # print("\n %s pair history \n" % str(crypto_symbol))
    # a = load_single_binance_pair(crypto_symbol)
    # print(a)
    # print("\nCharting the price and volume for %s\n" % str(crypto_symbol))
    # chart_1min_binance_pair_price_vol(a, crypto_symbol)
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
    print("\n Pivot loaded crypto wallet \n")
    b = pivot_binance_wallet()
    print(b)
    print("\n Normalize crypto wallet with prices starting at 1.0 \n")
    c = normalize_binance_wallet(b)
    print(c)
    print("\n Plotting normalized crypto price series \n")
    plot_normalized_binance_wallet()
    print("Done!\n")
