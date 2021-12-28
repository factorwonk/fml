import os
import pandas as pd

from datetime import datetime


def pivot_input_dataframe():
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//pairs_crypto//coinbase_outputs"
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # Read in today's dataset
    df = pd.read_csv(
        os.path.join(path, f"coinbase_merged_{date}.csv"), index_col=0
    ).reset_index()
    pivot_df = df.pivot(index="date", columns="symbol", values="close")
    df_output = pd.DataFrame(pivot_df.to_records()).set_index("date")
    print("\nReturning historical close prices\n")
    print(df_output)
    return df_output


def filter_significant_pairs(df_output, significant_pairs):
    cp_list = []
    # Count significant pairs
    n = len(significant_pairs)
    print("There are %d significant pairs." % n)
    print("\n")
    # Return significant pairs
    [print(cp[0], cp[1]) for cp in significant_pairs]
    print("\n")
    print("Here are each of pairs:")
    print("\n")
    cp_list = [[cp[0], cp[1]] for cp in significant_pairs]
    [
        print(cp_list[i][j])
        for i in range(len(significant_pairs))
        for j in range(len(cp_list))
    ]
    print("\n")
    # Take a subset of today's crypto prices which only contain significant pairs
    cp_pairs = [
        cp_list[i][j]
        for i in range(len(significant_pairs))
        for j in range(len(cp_list))
    ]
    df_sig = df_output[cp_pairs]
    return df_sig


if __name__ == "__main__":
    print("Done!")
