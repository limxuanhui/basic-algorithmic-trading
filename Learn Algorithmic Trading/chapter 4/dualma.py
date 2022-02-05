# Examples of momentum strategies
# - Moving average crossover - monitor when current price crosses moving average => change in momentum
# - Dual moving average crossover - to limit number of switches from moving average crossover,
#   when short-term MA crosses long-term MA, momentum will be upward; similarly for the other direction
# - Turtle trading

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from loaddata import load_financial_data
from helper import double_moving_average

##### CONSTANTS
start_date = "2001-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "goog_large_data.pkl"

goog_data = load_financial_data(SRC_DATA_FILENAME, start_date, end_date)
print(goog_data)
ts = double_moving_average(goog_data, 20, 100)
print(ts)

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google price in $")
goog_data["Adj Close"].plot(ax=ax1, color="g", lw=1.)
ts["short_mavg"].plot(ax=ax1, color="r", lw=1.)
ts["long_mavg"].plot(ax=ax1, color="b", lw=1.)

ax1.plot(ts.loc[ts.orders == 1.0].index, goog_data["Adj Close"][ts.orders == 1.0], "^", markersize=3, color="k")
ax1.plot(ts.loc[ts.orders == -1.0].index, goog_data["Adj Close"][ts.orders == -1.0], "v", markersize=3, color="k")

plt.legend(["Price", "Short mavg", "Long mavg", "Buy", "Sell"])
plt.title("Double Moving Average Trading Strategy")
plt.show()


