import pandas as pd
from pandas_datareader import data


def load_financial_data(file_path, start_date: str, end_date: str, ticker: str = "GOOG", src: str = "yahoo"):
    try:
        df = pd.read_pickle(file_path)
    except FileNotFoundError:
        df = data.DataReader(ticker, src, start_date, end_date)
        df.to_pickle(file_path)

    return df

