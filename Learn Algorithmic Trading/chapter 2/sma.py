# Creating trading signals based on fundamental technical analysis
# Simple Moving Average (SMA)
# SMA = [SUM(i=1:N) P_i]/N

import matplotlib.pyplot as plt
import pandas as pd
import statistics as stats
from loaddata import goog_data

time_period = 20
history = []
sma_values = []

close = pd.Series(goog_data["Adj Close"])
for close_price in close:
    history.append(close_price)
    if len(history) > time_period:
        del (history[0])
    sma_values.append(stats.mean(history))

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(Simple20DayMovingAverage=pd.Series(sma_values, index=goog_data.index))
close_price = goog_data["ClosePrice"]
sma = goog_data["Simple20DayMovingAverage"]
print(goog_data)

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google price in $")
close_price.plot(ax=ax1, color="g", lw=2., legend=True)
sma.plot(ax=ax1, color="r", lw=2., legend=True)
plt.show()
