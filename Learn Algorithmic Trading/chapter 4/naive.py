import matplotlib.pyplot as plt
from loaddata import load_financial_data
from helper import naive_momentum_trading

##### CONSTANTS
start_date = "2001-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "goog_large_data.pkl"

goog_data = load_financial_data(SRC_DATA_FILENAME, start_date, end_date)
ts = naive_momentum_trading(goog_data, 5)

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google price in $")
goog_data["Adj Close"].plot(ax=ax1, color="g", lw=1.)
ax1.plot(ts.loc[ts.orders == 1.0].index, goog_data["Adj Close"][ts.orders == 1], "^", markersize=4, color="k")
ax1.plot(ts.loc[ts.orders == -1.0].index, goog_data["Adj Close"][ts.orders == -1], "v", markersize=4, color="k")

plt.legend(["Price", "Buy", "Sell"])
plt.title("Turtle Trading Strategy")
plt.show()
