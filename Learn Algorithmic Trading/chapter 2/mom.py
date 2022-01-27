# Momentum (MOM)
# An important measure of speed and magnitude of price movements
# Often a key indicator of trend/breakout-based trading algorithms
# Momentum is the difference between the current price and price of some fixed time periods in the past
# - Consecutive periods of positive momentum values indicate an uptrend; likewise for downtrend
# - Often use simple/exponential moving averages of the MOM indicator to detect sustained trends
# MOM = Price_t - Price_t-n

import matplotlib.pyplot as plt
import pandas as pd
from loaddata import goog_data

close = pd.Series(goog_data["Adj Close"])
time_period = 20
history = []
mom_values = []

for close_price in close:
    history.append(close_price)
    if len(history) > time_period:
        del history[0]

    mom = close_price - history[0]
    mom_values.append(mom)

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(MomentumFromPrice20DaysAgo=pd.Series(mom_values, index=goog_data.index))
close_price = goog_data["ClosePrice"]
mom = goog_data["MomentumFromPrice20DaysAgo"]

fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel="Google price in $")
close_price.plot(ax=ax1, color="g", lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel="Momentum in $")
mom.plot(ax=ax2, color="b", lw=2., legend=True)
plt.show()

# - Momentum values peak when the stock price changes by a large amount as compared to the price 20 days ago
# - Most momentum values are positive mainly because Google stock has been increasing in value over the course
#   of its lifetime and has large upward momentum values from time to time
# - During brief periods where the stock prices decline, we observe negative momentum values
