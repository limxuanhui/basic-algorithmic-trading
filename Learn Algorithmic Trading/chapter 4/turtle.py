# Turtle Strategy
# - Long signal when the price reaches the highest for the last window_size days
# - Short signal when the price reaches its lowest point
# - Exit a position by having the price cross the moving average of the last window_size days
# Entry rule: stock price > the highest value for window_size day
#               stock price < the lowest value for window_size day
# Exit rule: stock price crosses the mean of past window_size days

import matplotlib.pyplot as plt
from loaddata import load_financial_data
from helper import  turtle_trading

##### CONSTANTS
start_date = "2001-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "goog_large_data.pkl"

goog_data = load_financial_data(SRC_DATA_FILENAME, start_date, end_date)
ts = turtle_trading(goog_data, 50)

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google price in $")
goog_data["Adj Close"].plot(ax=ax1, color="k", lw=2.)
ax1.plot(ts.loc[ts.orders == 1.0].index, goog_data["Adj Close"][ts.orders == 1], "^", markersize=3, color="g")
ax1.plot(ts.loc[ts.orders == -1.0].index, goog_data["Adj Close"][ts.orders == -1], "v", markersize=3, color="r")

plt.legend(["Price", "Buy", "Sell"])
plt.title("Turtle Trading Strategy")
plt.show()
