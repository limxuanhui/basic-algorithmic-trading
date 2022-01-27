# Absolute Price Oscillator (APO)
# The APO is a class of indicators that builds on top of moving averages of prices to capture
# specific short-term deviations in prices
# APO = EMA_fast - EMA_slow

import matplotlib.pyplot as plt
import pandas as pd
from loaddata import goog_data

close = pd.Series(goog_data["Adj Close"])

num_periods_fast = 10
K_fast = 2 / (num_periods_fast + 1)
ema_fast = 0

num_periods_slow = 40
K_slow = 2 / (num_periods_slow + 1)
ema_slow = 0

ema_fast_values = []
ema_slow_values = []
apo_values = []

for close_price in close:
    if ema_fast == 0:
        ema_fast, ema_slow = close_price, close_price
    else:
        ema_fast = K_fast * close_price + (1 - K_fast) * ema_fast  # (close_price - ema_fast) * K_fast + ema_fast
        ema_slow = K_slow * close_price + (1 - K_slow) * ema_slow   # (close_price - ema_slow) * K_slow + ema_slow

    ema_fast_values.append(ema_fast)
    ema_slow_values.append(ema_slow)
    apo_values.append(ema_fast - ema_slow)


goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(FastExponential10DayMovingAverage=pd.Series(ema_fast_values, index=goog_data.index))
goog_data = goog_data.assign(SlowExponential40DayMovingAverage=pd.Series(ema_slow_values, index=goog_data.index))
goog_data = goog_data.assign(AbsolutePriceOscillator=pd.Series(apo_values, index=goog_data.index))
close_price = goog_data["ClosePrice"]
ema_f = goog_data["FastExponential10DayMovingAverage"]
ema_s = goog_data["SlowExponential40DayMovingAverage"]
apo = goog_data["AbsolutePriceOscillator"]

fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel="Google price in $")
close_price.plot(ax=ax1, color="g", lw=2., legend=True)
ema_f.plot(ax=ax1, color="b", lw=2., legend=True)
ema_s.plot(ax=ax1, color="r", lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel="APO")
apo.plot(ax=ax2, color="k", lw=2., legend=True)
plt.show()

