# Trading Signal Generation and Strategies
# Deciphering the Markets with Technical Analysis
# - For our algorithm to exit a position, we will need to add more parameters to change the behavior in order to
#   enter a position. These include:
#   1) Shorter rolling window
#   2) Number of times the price reaches a support or resistance line
#   3) Tolerance margin can be added to consider that a support or resistance value can attain around a certain
#      percentage of this value

import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data

start_date = "2014-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "goog_data.pkl"

try:
    goog_data2 = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    goog_data2 = data.DataReader("GOOG", "yahoo", start_date, end_date)
    goog_data2.to_pickle(SRC_DATA_FILENAME)

goog_data2 = goog_data2.tail(620)
lows = goog_data2["Low"]
highs = goog_data2["High"]

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google price in $")
highs.plot(ax=ax1, color="c", lw=2.)
lows.plot(ax=ax1, color="y", lw=2.)
plt.hlines(highs.head(200).max(), lows.index.values[0], lows.index.values[-1], linewidth=2, color="g")
plt.hlines(lows.head(200).min(), lows.index.values[0], lows.index.values[-1], linewidth=2, color="r")
plt.axvline(linewidth=2, color="b", x=lows.index.values[200], linestyle=":")
plt.show()
