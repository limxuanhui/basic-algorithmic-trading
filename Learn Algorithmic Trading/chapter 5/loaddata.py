import pandas as pd
from pandas_datareader import data


def load_financial_data(file_path, start_date: str, end_date: str, ticker: str | list = "GOOG", src: str = "yahoo"):
    try:
        print("Loading data...")
        df = pd.read_pickle(file_path)
    except FileNotFoundError:
        print("Downloading data...")
        df = data.DataReader(ticker, src, start_date, end_date)
        df.to_pickle(file_path)

    return df



