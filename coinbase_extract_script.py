# First import the libraries that we need to use
import pandas as pd
import requests
import json
import os

from datetime import datetime


def fetch_daily_data(symbol):
    date = datetime.now().strftime("%Y%m%d")
    # symbol must be in format XXX/XXX ie. BTC/EUR
    pair_split = symbol.split("/")
    symbol = pair_split[0] + "-" + pair_split[1]
    path = "//Users//hyperion//Wasteland//Python//Repos//fml//coinbase_data"
    url = f"https://api.pro.coinbase.com/products/{symbol}/candles?granularity=86400"
    response = requests.get(url)
    # check to make sure the response from server is good
    if response.status_code == 200:
        data = pd.DataFrame(
            json.loads(response.text),
            columns=["unix", "low", "high", "open", "close", "volume"],
        )
        # convert to a readable date
        data["date"] = pd.to_datetime(data["unix"], unit="s")
        # multiply the BTC volume by closing price to approximate fiat volume
        data["vol_fiat"] = data["volume"] * data["close"]

        # if we failed to get any data, print an error...otherwise write the file
        if data is None:
            print("Did not return any data from Coinbase for this symbol")
        else:
            data.to_csv(
                os.path.join(
                    path,
                    f"Coinbase_{pair_split[0] + pair_split[1]}_dailydata_{date}.csv",
                ),
                index=False,
            )

    else:
        print("Did not receieve OK response from Coinbase API")


if __name__ == "__main__":
    # we set which pair we want to retrieve data for
    pair = "BTC/USD"
    fetch_daily_data(pair)
