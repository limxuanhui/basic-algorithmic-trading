# Exponential Moving Average (EMA)
# Instead of weighing all prices in the history equally, it places more weight on the most recent price observation
# and less weight on older price observations
# - captures idea that new price observations have more up-to-date information
# - also possible to place more weight on older price observations to capture the idea that longer-term trends
#   have more information than short-term volatile price movements
# - weighting depends on selected time period; shorter time period => more reactive EMA is to new price
#   => EMA converges to new price observations faster and forgets older observations faster (Fast EMA)
# - longer time period => less reactive EMA is to new price observations (Slow EMA)

import matplotlib.pyplot as plt
import pandas as pd
from loaddata import goog_data

close = pd.Series(goog_data["Adj Close"])
num_periods = 20
K = 2 / (num_periods + 1)
ema_p = 0
ema_values = []

for close_price in close:
    if ema_p == 0:
        ema_p = close_price
    else:
        ema_p = K * close_price + (1 - K) * ema_p  # (close_price - ema_p) * K + ema_p
    ema_values.append(ema_p)

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(Exponential120DayMovingAverage=pd.Series(ema_values, index=goog_data.index))

close_price = goog_data["ClosePrice"]
ema = goog_data["Exponential120DayMovingAverage"]

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google price in $")
close_price.plot(ax=ax1, color="g", lw=2., legend=True)
ema.plot(ax=ax1, color="b", lw=2., legend=True)

plt.savefig("ema.png")
plt.show()


