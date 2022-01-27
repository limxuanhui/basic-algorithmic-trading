import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from loaddata import goog_data

goog_data_signal = pd.DataFrame(index=goog_data.index)
goog_data_signal["price"] = goog_data["Adj Close"]
print(goog_data_signal)


def trading_support_resistance(df, bin_width=20):
    df["sup_tolerance"] = pd.Series(np.zeros(len(df)))
    df["res_tolerance"] = pd.Series(np.zeros(len(df)))
    df["sup_count"] = pd.Series(np.zeros(len(df)))
    df["res_count"] = pd.Series(np.zeros(len(df)))
    df["sup"] = pd.Series(np.zeros(len(df)))
    df["res"] = pd.Series(np.zeros(len(df)))
    df["positions"] = pd.Series(np.zeros(len(df)))
    df["signal"] = pd.Series(np.zeros(len(df)))
    in_support = 0
    in_resistance = 0

    for x in range((bin_width - 1) + bin_width, len(df)):
        df_section = df[x - bin_width: x + 1]
        support_level = min(df_section["price"])
        resistance_level = max(df_section["price"])
        range_level = resistance_level - support_level
        df["res"][x] = resistance_level
        df["sup"][x] = support_level
        df["sup_tolerance"][x] = support_level + 0.2 * range_level
        df["res_tolerance"][x] = resistance_level - 0.2 * range_level

        if df["res_tolerance"][x] <= df["price"][x] <= df["res"][x]:
            in_resistance += 1
            df["res_count"][x] = in_resistance
        elif df["sup"][x] <= df["price"][x] <= df["sup_tolerance"][x]:
            in_support += 1
            df["sup_count"] = in_support
        else:
            in_support, in_resistance = 0, 0

        if in_resistance > 2:
            df["signal"][x] = 1
        elif in_support > 2:
            df["signal"][x] = 0
        else:
            df["signal"][x] = df["signal"][x - 1]

    df["positions"] = df["signal"].diff()


trading_support_resistance(goog_data_signal)

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Google price in $")
goog_data_signal["sup"].plot(ax=ax1, color="g", lw=2.)
goog_data_signal["res"].plot(ax=ax1, color="b", lw=2.)
goog_data_signal["price"].plot(ax=ax1, color="r", lw=1.)
ax1.plot(goog_data_signal.loc[goog_data_signal.positions == 1.0].index,\
         goog_data_signal.price[goog_data_signal.positions == 1.0],\
         "^", markersize=7, color="k", label="buy")
ax1.plot(goog_data_signal.loc[goog_data_signal.positions == -1.0].index,\
         goog_data_signal.price[goog_data_signal.positions == -1.0],\
         "v", markersize=7, color="k", label="sell")
plt.legend()
plt.show()


