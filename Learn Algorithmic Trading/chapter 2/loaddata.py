import pandas as pd
from pandas_datareader import data

start_date = "2014-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "goog_data.pkl"

try:
    goog_data = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    goog_data = data.DataReader("GOOG", "yahoo", start_date, end_date)
    goog_data.to_pickle(SRC_DATA_FILENAME)