# Trading Signal Generation and Strategies
# Deciphering the Markets with Technical Analysis
# - For our algorithm to exit a position, we will need to add more parameters to change the behavior in order to
#   enter a position. These include:
#   1) Shorter rolling window
#   2) Number of times the price reaches a support or resistance line
#   3) Tolerance margin can be added to consider that a support or resistance value can attain around a certain
#      percentage of this value

import matplotlib.pyplot as plt
from loaddata import goog_data

goog_data = goog_data.tail(620)
lows = goog_data["Low"]
highs = goog_data["High"]

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google price in $")
highs.plot(ax=ax1, color="c", lw=2.)
lows.plot(ax=ax1, color="y", lw=2.)
plt.hlines(highs.head(200).max(), lows.index.values[0], lows.index.values[-1], linewidth=2, color="g")
plt.hlines(lows.head(200).min(), lows.index.values[0], lows.index.values[-1], linewidth=2, color="r")
plt.axvline(linewidth=2, color="b", x=lows.index.values[200], linestyle=":")
plt.show()
