import pandas as pd
from pandas_datareader import data

start_date = "2001-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "goog_data_large.pkl"

try:
    goog_data_large = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    goog_data_large = data.DataReader("GOOG", "yahoo", start_date, end_date)
    goog_data_large.to_pickle(SRC_DATA_FILENAME)