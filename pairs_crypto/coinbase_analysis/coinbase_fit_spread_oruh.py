import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from datetime import datetime
from numpy.linalg import inv
from scipy.stats import iqr


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


def regression(xdata, ydata):
    flag = 0
    if isinstance(xdata, pd.DataFrame):
        flag = 1
    xdat = pd.DataFrame(xdata)
    xdat["b0"] = 1
    xdat = xdat.values
    ydata = ydata.values
    n = np.dot(xdat.T, xdat)
    beta = np.dot(np.dot(inv(n), xdat.T), ydata)
    coef = beta[0:-1]
    intercept = beta[-1]

    if flag == 1:
        xdata.drop(labels="b0", axis=1, inplace=True)
        temp = coef * xdata
        residuals = ydata - temp.sum(axis=1) - intercept
    else:
        coef = coef[0]
        residuals = ydata - coef * xdata - intercept

    return coef, intercept, residuals.values


def fit_spread_oruh(residuals):
    tau = 1.0 / 252
    # start with residuals
    spread = pd.DataFrame(residuals)
    # rename
    spread.columns = ["Spread"]
    # lag by one period
    spread["Spreadt-1"] = spread["Spread"].shift(1)
    spread.dropna(inplace=True)
    target_y = pd.DataFrame(spread["Spread"])
    target_y.columns = ["y"]
    spread.drop(["Spread"], axis=1, inplace=True)

    # Calculating Ornstein-Uhlenbeck parameters from linear regression
    autoregression_coefficient, mean_reverting_term, resids = regression(
        spread["Spreadt-1"], target_y["y"]
    )
    # Creating an array of CONSTANT Ornstein-Uhlenbeck parameters for each trading session
    mean_reverting_term = np.repeat(mean_reverting_term, len(residuals))
    autoregression_coefficient = np.repeat(autoregression_coefficient, len(residuals))

    # Computing half-life of Ornstein-Uhlenbeck
    mean_reversion_speed = -1 * np.log(np.absolute(autoregression_coefficient)) / tau

    # Computing mean around which OU process reverts
    mean_r = mean_reverting_term / (1 - autoregression_coefficient)
    # Use mean value for any NaNs
    if np.isnan(mean_r).any():
        mean_r = np.nan_to_num(mean_r)

    # Compute the instantaneous and equivalent diffusion for the spread
    diffusion_or_uh = np.sqrt(
        (2 * mean_reversion_speed * np.var(residuals))
        / (1 - np.exp(-2 * mean_reversion_speed * tau))
    )
    mean_reversion_speed[mean_reversion_speed <= 0] = 1e-15
    diffusion_eq = diffusion_or_uh / (np.sqrt(2 * mean_reversion_speed))
    half_life = np.log(2) / mean_reversion_speed

    print("\n")
    print(
        "The spread fitted to the Ornstein-Uhlenbeck process has the following paraemeters:"
    )
    print(
        "The mean reversion for this spread is {} \nSigma of reversion for this spread is {} \nMean reversion speed, short term diffusion and half-life of OU is {}, {} and {}".format(
            mean_r[0],
            diffusion_eq[0],
            mean_reversion_speed[0],
            diffusion_or_uh[0],
            half_life[0],
        )
    )

    iqr_mr = iqr(mean_r) * 4
    iqr_sr = iqr(diffusion_eq) * 4
    iqr_spr = iqr(mean_reversion_speed) * 4
    iqr_ds = iqr(diffusion_or_uh) * 4
    lim = [iqr_mr, iqr_sr, iqr_spr, iqr_ds]

    path = "//Users//hyperion//Wasteland//Python//Repos//fml//coinbase_outputs"
    date = datetime.now().strftime("%Y%m%d")
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, figsize=(24, 24), sharex=True)
    # fig.suptitle("Trading Sessions")
    xlabel = "Trading Sessions"
    ylabel = [
        "OU Mean",
        "OU Diffusion",
        "Rate of Revesion",
        "Diffusion over short time",
    ]
    title = [
        "Mean of Reversion",
        "Sigma of Reversion",
        "Speed of Reversion",
        "Diffusion over short timescale",
    ]
    subplots = [411, 412, 413, 414]
    labels = [
        "Mean of Reversion",
        "Sigma of Reversion",
        "Speed of Reversion",
        "Diffusion over short timescale",
    ]
    plots = [mean_r, diffusion_eq, mean_reversion_speed, diffusion_or_uh]

    for i in range(0, 4):
        plt.subplot(subplots[i])
        plt.title(title[i])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel[i])
        plt.ylim(
            np.percentile(plots[i], 25) - lim[i], np.percentile(plots[i], 75) + lim[i]
        )
        plt.plot(plots[i], label=labels[i])
        plt.legend()
    plt.savefig(os.path.join(path, f"mean_reversion_plots_{date}.png"))
    plt.close(fig)

    return mean_r, diffusion_eq


if __name__ == "__main__":
    print("Done!")
