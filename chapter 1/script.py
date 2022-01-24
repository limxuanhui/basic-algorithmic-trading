import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas_datareader import data

start_date = "2014-01-01"
end_date = "2018-01-01"

goog_data = data.DataReader("GOOG", "yahoo", start_date, end_date)

goog_data_signal = pd.DataFrame(index=goog_data.index)

goog_data_signal["price"] = goog_data["Adj Close"]
goog_data_signal["daily_difference"] = goog_data_signal["price"].diff()
goog_data_signal["signal"] = np.where(goog_data_signal["daily_difference"] > 0, 1, 0)
goog_data_signal["positions"] = goog_data_signal["signal"].diff()
buy_at = goog_data_signal.iloc[np.where(goog_data_signal["positions"] > 0)[0][0]]["price"]
buy_on = goog_data_signal.iloc[np.where(goog_data_signal["positions"] > 0)[0][0]].name
sell_at = goog_data_signal.iloc[np.where(goog_data_signal["positions"] < 0)[0][0]]["price"]
sell_on = goog_data_signal.iloc[np.where(goog_data_signal["positions"] < 0)[0][0]].name

print(f"Buy GOOG @ {round(buy_at, 4)} on {buy_on}\
        Sell GOOG @ {round(sell_at, 4)} on {sell_on}\
        for a PnL of {round(sell_at - buy_at, 4)}")

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google price in $")
goog_data_signal["price"].plot(ax=ax1, color="r", lw=2.)
ax1.plot(goog_data_signal.loc[goog_data_signal.positions == 1.0].index,\
         goog_data_signal.price[goog_data_signal.positions == 1.0],\
         "^", markersize=5, color="m")
ax1.plot(goog_data_signal.loc[goog_data_signal.positions == -1.0].index,\
         goog_data_signal.price[goog_data_signal.positions == -1.0],\
         "v", markersize=5, color="k")
plt.show()

initial_capital = float(1000.0)
positions = pd.DataFrame(index=goog_data_signal.index).fillna(0.0)
portfolio = pd.DataFrame(index=goog_data_signal.index).fillna(0.0)
positions["GOOG"] = goog_data_signal["signal"]
portfolio["positions"] = positions.multiply(goog_data_signal["price"], axis=0)
portfolio["cash"] = initial_capital - (positions.diff().multiply(goog_data_signal["price"], axis=0)).cumsum()
portfolio["total"] = portfolio["positions"] + portfolio["cash"]
plt.plot(portfolio["total"], color="r")
plt.plot(portfolio["positions"], color="b")
plt.plot(portfolio["cash"], color="k")
plt.show()