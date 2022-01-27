# Standard Deviation (STD)

import matplotlib.pyplot as plt
import math
import pandas as pd
import statistics as stats
from loaddata import goog_data

close = pd.Series(goog_data["Adj Close"])
time_period = 20
history = []
sma_values = []
std_values = []

for close_price in close:
    history.append(close_price)
    if len(history) > time_period:
        del history[0]

    sma = stats.mean(history)
    sma_values.append(sma)

    variance = 0
    for hist_price in history:
        variance += (hist_price - sma)**2
    variance /= len(history)
    std = math.sqrt(variance)
    std_values.append(std)

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(StandardDeviationOver20Days=pd.Series(std_values, index=goog_data.index))
close_price = goog_data["ClosePrice"]
std = goog_data["StandardDeviationOver20Days"]

fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel="Google price in $")
close_price.plot(ax=ax1, color="g", lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel="Std in $")
std.plot(ax=ax2, color="b", lw=2., legend=True)
plt.show()



