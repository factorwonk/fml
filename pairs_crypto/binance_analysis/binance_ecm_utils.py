import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

from datetime import datetime
from numpy.linalg import inv
from scipy.stats import t


def calc_residuals(df):
    x = df.iloc[:, 0]  # e.g. BTC/USD
    y = df.iloc[:, 1]  # e.g. ETH/USD
    X1 = sm.add_constant(x)
    # Y1 = sm.add_constant(y)

    ols1 = sm.OLS(y, X1).fit()
    # ols2 = sm.OLS(x, Y1).fit()
    # calculate residuals here
    residuals = ols1.resid
    # residuals2 = ols2.resid
    return residuals


def test_stationarity(residuals):
    adf_data = pd.DataFrame(residuals)
    adf_data.columns = ["y"]
    adf_data["drift_constant"] = 1
    # Lag residual
    adf_data["y-1"] = adf_data["y"].shift(1)
    adf_data.dropna(inplace=True)
    # Diff between residual and lag residual
    adf_data["deltay1"] = adf_data["y"] - adf_data["y-1"]
    # Lag difference
    adf_data["deltay-1"] = adf_data["deltay1"].shift(1)
    adf_data.dropna(inplace=True)
    target_y = pd.DataFrame(adf_data["deltay1"], columns=["deltay1"])
    adf_data.drop(["y", "deltay1"], axis=1, inplace=True)

    # Auto regressing the residuals with lag1, drift constant and lagged 1 delta (delta_et-1)
    adf_regressor_model = sm.OLS(target_y, adf_data)
    adf_regressor = adf_regressor_model.fit()

    # Returning the results
    print(adf_data)
    print(adf_regressor.summary())
    return adf_regressor

