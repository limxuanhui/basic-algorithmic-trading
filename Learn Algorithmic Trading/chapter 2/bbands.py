# Bollinger Bands (BBANDS)
# BBANDS also builds on top of moving averages, but incorporates recent price volatility that makes the indicator
# more adaptive to different market conditions
# - it computes a moving average of the prices
# - it also computes the standard deviation of the prices in the lookback period
#   by treating the moving average as the mean price
# - it creates an upper band (moving average + some k * standard deviation of price), likewise for lower band
# - this band represents the expected volatility of the prices by treating the moving average of the price
#   as the reference price
# - when prices move out of these bands, it can be interpreted as a breakout/trend signal or an overbought/sold
#   mean-reversion signal
# BBAND_middle = SMA_n_periods
# BBAND_upper = BBAND_middle + (beta * sigma)
# BBAND_lower = BBAND_middle - (beta * sigma)

import matplotlib.pyplot as plt
import math
import pandas as pd
import statistics as stats

from loaddata import goog_data

close = pd.Series(goog_data["Adj Close"])

time_period = 20
std_factor = 2
history = []
sma_values = []
upper_band = []
lower_band = []

for close_price in close:
    history.append(close_price)
    if len(history) > time_period:
        del history[0]

    sma = stats.mean(history)
    sma_values.append(sma)
    variance = 0

    for hist_price in history:
        variance = variance + (hist_price - sma)**2
    variance /= len(history)
    std = math.sqrt(variance)

    upper_band.append(sma + std * std_factor)
    lower_band.append(sma - std * std_factor)

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(MiddleBollingerBand20DaySMA=pd.Series(sma_values, index=goog_data.index))
goog_data = goog_data.assign(UpperBollingerBand20DaySMA2StdFactor=pd.Series(upper_band, index=goog_data.index))
goog_data = goog_data.assign(LowerBollingerBand20DaySMA2StdFactor=pd.Series(lower_band, index=goog_data.index))

close_price = goog_data["ClosePrice"]
mband = goog_data["MiddleBollingerBand20DaySMA"]
uband = goog_data["UpperBollingerBand20DaySMA2StdFactor"]
lband = goog_data["LowerBollingerBand20DaySMA2StdFactor"]

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google price in $")
close_price.plot(ax=ax1, color="k", lw=2., legend=True, )
mband.plot(ax=ax1, color="b", lw=1., legend=True, linestyle="--")
uband.plot(ax=ax1, color="g", lw=1., legend=True, linestyle="--")
lband.plot(ax=ax1, color="r", lw=1., legend=True, linestyle="--")
plt.show()