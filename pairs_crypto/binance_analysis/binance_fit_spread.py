import os
from shutil import SpecialFileError
from turtle import speed
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from datetime import datetime
from scipy.stats import iqr
from numpy.linalg import inv


def regression(xdata, ydata):
    flag = 0
    if isinstance(xdata, pd.DataFrame):
        flag = 1
    xdat = pd.DataFrame(xdata)
    xdat["b0"] = 1
    xdat = xdat.values
    ydat = ydata.values
    n = np.dot(xdat.T, xdat)
    beta = np.dot(np.dot(inv(n), xdat.T), ydat)
    coef = beta[0:-1]
    intercept = beta[-1]

    if flag == 1:
        xdata.drop(labels="b0", axis=1, inplace=True)
        temp = coef * xdata
        residuals = ydat - temp.sum(axis=1) - intercept
    else:
        residuals = ydat - coef * xdat - intercept

    return coef, intercept, residuals.values


def fit_spread_oruh(residuals):
    tau = 1.0 / 252
    spread = pd.DataFrame(residuals)
    spread.columns = ["Spread"]
    spread["Spreadt-1"] = spread["Spread"].shift(1)
    spread.dropna(inplace=True)
    target_y = pd.DataFrame(spread["Spread"])
    target_y.columns = ["y"]
    spread.drop(["Spread"], axis=1, inplace=True)

    # Calculate OU parameters from linear regression
    autoregression_coeff, mean_reverting_term, resids = regression(
        spread["Spreadt-1"], target_y["y"]
    )
    # Create array of OU parameters for each trading session
    # The parameters in this case are constant for each time session
    mean_reverting_term = np.repeat(mean_reverting_term, len(resids))
    autoregression_coeff = np.repeat(autoregression_coeff, len(resids))

    # Compute Half Life of the process
    speed_of_reversion = -1 * np.log(np.absolute(autoregression_coeff)) / tau

    # Computing the mean about which the OU process reverts
    mean = mean_reverting_term / (1 - autoregression_coeff)
    if np.isnan(mean).any():
        mean = np.nan_to_num(mean)

    # Compute the instantaneous and equivalent diffusion for the spread
    diffusion_ou = (
        (2 * speed_of_reversion * np.var(residuals))
        / (1 - np.exp(-2 * speed_of_reversion * tau))
    ) ** 0.5
    speed_of_reversion[speed_of_reversion <= 0] = 1e-15
    diffusion_eq = diffusion_ou / ((2 * speed_of_reversion) ** 0.5)
    half_life = np.log(2) / speed_of_reversion

    return mean, half_life, diffusion_eq


if __name__ == "__main__":
    print("Done!")
