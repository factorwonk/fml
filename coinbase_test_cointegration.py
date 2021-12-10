import os
import numpy as np
import pandas as pd
import statsmodels.api as sm


from datetime import datetime
from numpy.linalg import inv
from scipy.stats import t


def transform_data():
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//coinbase_outputs"
    # init date
    date = datetime.now().strftime("%Y%m%d")
    # Get rid of index_col = 0 later on
    df = pd.read_csv(os.path.join(path, f"coinbase_merged_{date}.csv"), index_col=0)
    # Select either Ethereum or Bitcoin for now
    df = df[(df.symbol == "ETH/USD") | (df.symbol == "BTC/USD")].reset_index()
    # Pivot
    pivot_df = df.pivot(index="date", columns="symbol", values="close")
    df = pd.DataFrame(pivot_df.to_records()).set_index("date")
    return df


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


def calc_residuals(df):
    x = df.iloc[:, 0]  # BTC/USD
    y = df.iloc[:, 1]  # ETH/USD
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


def test_significance(xdata, ydata, residuals):
    """Testing the significance of the coefficient of lagged residual using it's t-statistic.
    The cointegration is relevant only if the significance test is passed at the specified confidence interval.

    Args:
        xdata ([type]): [description]
        ydata ([type]): [description]
        residuals ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Augmenting 1-period lagged residual into the dataset
    residuals = pd.DataFrame(residuals)
    ecm_data = pd.DataFrame(residuals.shift(1))
    ecm_data.columns = ["et-1"]
    ecm_data["y1"] = ydata.values
    ecm_data["y2"] = xdata.values
    ecm_data["deltay"] = ecm_data["y1"] - ecm_data["y1"].shift(1)
    ecm_data["deltax"] = ecm_data["y2"] - ecm_data["y2"].shift(1)
    ecm_data.dropna(inplace=True)

    target_y = pd.DataFrame(ecm_data["deltay"])
    ecm_data.drop(["y1", "y2", "deltay"], axis=1, inplace=True)

    # Regressing the delta y against the delta x and the 1 period lagged residuals
    ecm_regressor1_model = sm.OLS(target_y, ecm_data)
    ecm_regressor1 = ecm_regressor1_model.fit()

    # Returning the results of the regression
    print(ecm_regressor1)
    print(ecm_regressor1.summary())
    return ecm_regressor1


def test_cointegration(xdata, ydata, stat_value_ci, sig_value_ci, s1, s2):
    adf_critical_values1 = {"0.99": -3.46, "0.95": -2.88, "0.9": -2.57}
    adf_critical_values2 = {"0.99": -3.44, "0.95": -2.87, "0.9": -2.57}
    adf_critical_values3 = {"0.99": -3.43, "0.95": -2.86, "0.9": -2.57}

    # Lets pass the residual values directly into here
    coef1, intercept1, residuals1 = regression(xdata, ydata)
    coef2, intercept2, residuals2 = regression(ydata, xdata)
    flag1 = 0

    stat_test = test_stationarity(residuals1)
    print("The following is the result of the Augmented Dickey Fuller test")
    print(stat_test.summary())
    if len(residuals1) > 500:
        if abs(stat_test.tvalues["y-1"]) > abs(
            adf_critical_values3[str(stat_value_ci)]
        ):
            print("\n")
            print(
                "The t-statistic value of the unit root coefficient is {} and the null hypothesis of a unit root is rejected. Hence, no unit root exists and residuals are stationary".format(
                    stat_test.tvalues["y-1"]
                )
            )
            # pass
        else:
            print("\n")
            print(
                "The t-statistic value of the unit root coefficient is {} and the null hypothesis of a unit root is accepted. Hence, a unit root exists and residuals are not stationary and Error Correction Model is not checked for".format(
                    stat_test.tvalues["y-1"]
                )
            )
            # return -1

    elif len(residuals1) > 250:
        if abs(stat_test.tvalues["y-1"]) > abs(
            adf_critical_values2[str(stat_value_ci)]
        ):
            print("\n")
            print(
                "The t-statistic value of the unit root coefficient is {} and the null hypothesis of a unit root is rejected. Hence, no unit root exists and residuals are stationary".format(
                    stat_test.tvalues["y-1"]
                )
            )
            # pass
        else:
            print(
                "The t-statistic value of the unit root coefficient is {} and the null hypothesis of a unit root is accepted. Hence, a unit root exists and residuals are not stationary and Error Correction Model is not checked for".format(
                    stat_test.tvalues["y-1"]
                )
            )
            # return -1

    elif len(residuals1) > 100:
        if abs(stat_test.tvalues["y-1"]) > abs(
            adf_critical_values1[str(stat_value_ci)]
        ):
            print("\n")
            print(
                "The t-statistic value of the unit root coefficient is {} and the null hypothesis of a unit root is rejected. Hence, no unit root exists and residuals are stationary".format(
                    stat_test.tvalues["y-1"]
                )
            )
            # pass
        else:
            print("\n")
            print(
                "The t-statistic value of the unit root coefficient is {} and the null hypothesis of a unit root is accepted. Hence, a unit root exists and residuals are not stationary and Error Correction Model is not checked for".format(
                    stat_test.tvalues["y-1"]
                )
            )
            return -1

    sig_1 = test_significance(xdata, ydata, residuals1)
    sig_2 = test_significance(ydata, xdata, residuals2)

    print("\n")
    print(
        "The following is the regression result of the Error Correction model when {} is the independent and {} is the dependent variable".format(
            s1, s2
        )
    )
    print(sig_1.summary())

    critical_value = abs(
        t.ppf(sig_value_ci + 0.5 * (1 - sig_value_ci), len(residuals1))
    )
    if abs(sig_1.tvalues["et-1"]) > critical_value:
        print("\n")
        print(
            "The t-statistic value of the lagged residual coefficient in the error correction model is {} against a critical value of {} and the null hypothesis of the coefficient not being significant is rejected. Hence, cointegration is significant".format(
                sig_1.tvalues["et-1"], critical_value
            )
        )

    else:
        print("\n")
        print(
            "The t-statistic value of the lagged residual coefficient in the error correction model is {} against a critical value of {} and the null hypothesis of the coefficient not being significant is accepted. Hence, cointegration is not significant".format(
                sig_1.tvalues["et-1"], critical_value
            )
        )
        flag1 += 1

    print("\n")
    print(
        "The following is the regression result of the Error Correction model when {} is the independent and {} is the dependent variable".format(
            s2, s1
        )
    )
    print(sig_2.summary())
    critical_value = abs(
        t.ppf(sig_value_ci + 0.5 * (1 - sig_value_ci), len(residuals2))
    )
    if abs(sig_2.tvalues["et-1"]) > critical_value:
        print("\n")
        print(
            "The t-statistic value of the lagged residual coefficient in the error correction model is {} against a critical value of {} and the null hypothesis of the coefficient not being significant is rejected. Hence, cointegration is significant".format(
                sig_2.tvalues["et-1"], critical_value
            )
        )
    else:
        print("\n")
        print(
            "The t-statistic value of the lagged residual coefficient in the error correction model is {} against a critical value of {} and the null hypothesis of the coefficient not being significant is accepted. Hence, cointegration is not significant".format(
                sig_2.tvalues["et-1"], critical_value
            )
        )
        flag1 += 1

    if flag1 == 2:
        return -2

    if abs(sig_1.tvalues["et-1"]) < abs(sig_2.tvalues["et-1"]):
        print("\n")
        print(
            "For the cointegration problem, the independent variable in regression between the asset classes is {} and the dependent variable is {}".format(
                s1, s2
            )
        )
        return 2
    else:
        print("\n")
        print(
            "For the cointegration problem, the independent variable in regression between the asset classes is {} and the dependent variable is {}".format(
                s2, s1
            )
        )
        return 1


if __name__ == "__main__":
    print("Going to extract and transform the data from csv...")
    print("\n")
    a = transform_data()
    print(a)
    print("\n")
    # print("Here's basic regression")
    # x = regression(a.iloc[:, 0], a.iloc[:, 1])
    # print("Here's just the residuals")
    # print(x[2])
    # print("\n")
    # print("Going to calculate the residuals with OLS function...")
    # b = calc_residuals(a)
    # print("residuals1")
    # print(b)
    # print("\n")
    # print("Significance of the residuals")
    # print("\n")
    c = test_significance(a.iloc[:, 0], a.iloc[:, 1], b)
    print(c)
    print("\n")
    print("Test against critical t-value of ADF and ECM")
    d = test_cointegration(
        a.iloc[:, 0],
        a.iloc[:, 1],
        stat_value_ci=0.95,
        sig_value_ci=0.95,
        s1=str(list(a.columns.values)[0]),
        s2=str(list(a.columns.values)[1]),
    )
    print(d)
    print("Done!")
