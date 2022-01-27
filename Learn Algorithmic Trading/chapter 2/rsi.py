# Relative Strength Indicator (RSI)
# Based on price changes over periods to capture the strength/magnitude of price moves

import matplotlib.pyplot as plt
import pandas as pd
import statistics as stats
from loaddata import goog_data

close = pd.Series(goog_data["Adj Close"])
time_period = 20
gain_history = []
loss_history = []
avg_gain_values = []
avg_loss_values = []
rsi_values = []
last_price = 0

for close_price in close:
    if last_price == 0:
        last_price = close_price

    gain_history.append(max(0, close_price - last_price))
    loss_history.append(max(0, last_price - close_price))
    last_price = close_price

    if len(gain_history) > time_period:
        del gain_history[0]
        del loss_history[0]

    avg_gain = stats.mean(gain_history)
    avg_loss = stats.mean(loss_history)
    avg_gain_values.append(avg_gain)
    avg_loss_values.append(avg_loss)

    rs = 0
    if avg_loss > 0:
        rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    rsi_values.append(rsi)

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(RelativeStrengthAvgGainOver20Days=pd.Series(avg_gain_values, index=goog_data.index))
goog_data = goog_data.assign(RelativeStrengthAvgLossOver20Days=pd.Series(avg_loss_values, index=goog_data.index))
goog_data = goog_data.assign(RelativeStrengthIndicatorOver20Days=pd.Series(rsi_values, index=goog_data.index))
close_price = goog_data["ClosePrice"]
rs_gain = goog_data["RelativeStrengthAvgGainOver20Days"]
rs_loss = goog_data["RelativeStrengthAvgLossOver20Days"]
rsi = goog_data["RelativeStrengthIndicatorOver20Days"]

fig = plt.figure()
ax1 = fig.add_subplot(311, ylabel="Google price in $")
close_price.plot(ax=ax1, color="k", lw=1., legend=True)
ax2 = fig.add_subplot(312, ylabel = "RS")
rs_gain.plot(ax=ax2, color="r", lw=1., legend=True)
rs_loss.plot(ax=ax2, color="g", lw=1., legend=True)
ax3 = fig.add_subplot(313, ylabel="RSI")
rsi.plot(ax=ax3, color="b", lw=1., legend=True)
plt.hlines(50, goog_data.index.values[0], goog_data.index.values[-1], linewidth=1, color="r", linestyles="--")
plt.show()

