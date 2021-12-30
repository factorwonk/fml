import numpy as np
import pandas as pd

from numpy.linalg import inv


def calc_corr_matrix(wallet_df):
    """Calculates the Pearson correlation coefficient between cryptocurrency pairs

    Args:
        wallet_df (DataFrame): Transformed DF containing historical price data for cryptocurrencies
    """
    corrmat_df = wallet_df.corr()
    return corrmat_df


def fillna_pivoted_df(input_df):
    output_df = input_df.fillna(0)
    return output_df


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


if __name__ == "__main__":
    print("Done")
