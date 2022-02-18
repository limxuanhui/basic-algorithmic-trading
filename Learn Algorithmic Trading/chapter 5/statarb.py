# StatArb trading strategy in Python

import pandas as pd
from loaddata import load_financial_data

TRADING_INSTRUMENT = "CADUSD=X"
SYMBOLS = ["AUDUSD=X", "GBPUSD=X", "CADUSD=X", "CHFUSD=X", "EURUSD=X", "JPYUSD=X", "NZDUSD=X"]
START_DATE = "2014-01-01"
END_DATE = "2018-01-01"

symbols_data = {}
for symbol in SYMBOLS:
    SRC_DATA_FILENAME = symbol + "_data.pkl"
    symbols_data[symbol] = load_financial_data(SRC_DATA_FILENAME, START_DATE, END_DATE, symbol)

    # stop following code
