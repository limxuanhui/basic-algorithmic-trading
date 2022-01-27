import matplotlib.pyplot as plt
import pandas as pd

from loadlargedata import goog_data_large

goog_monthly_return = goog_data_large["Adj Close"] \
                      .pct_change() \
                      .groupby(by=[goog_data_large["Adj Close"].index.year, goog_data_large["Adj Close"].index.month]) \
                      .mean()

goog_monthly_return_list = []
for i in range(len(goog_monthly_return)):
    goog_monthly_return_list.append({"month": goog_monthly_return.index[i][1],
                                     "monthly_return": goog_monthly_return[goog_monthly_return.index[i]]})

goog_monthly_return_list = pd.DataFrame(goog_monthly_return_list, columns=("month", "monthly_return"))
goog_monthly_return_list.boxplot(column="monthly_return", by="month")

ax = plt.gca()
labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ax.set_xticklabels(labels)
ax.set_ylabel("GOOG return")
plt.tick_params(axis="both", which="major", labelsize=7)
plt.title("GOOG monthly return 2001-2018")
plt.suptitle("")
plt.show()


def plot_rolling_statistics_ts(ts, titletext, ytext, window_size=12):
    ts.plot(color="r", label="Original", lw=0.5)
    ts.rolling(window_size).mean().plot(color="b", label="Rolling mean")
    ts.rolling(window_size).std().plot(color="k", label="Rolling std")

    plt.legend(loc="best")
    plt.ylabel(ytext)
    plt.title(titletext)
    plt.show()


# 1)
plot_rolling_statistics_ts(goog_monthly_return[1:], "Goog prices roling mean and standard deviation", "Monthly return")
# - Price growing over time due to trend
# - Wave effect comes from seasonality
# - When we make time series stationary, we remove the trend and seasonality
#   by modeling and removing them from initial data
# - Once we find a model predicting future values for the data without seasonality and trend,
#   we can apply back the seasonality and trend values to get the actual forecasted data


# 2)
plot_rolling_statistics_ts(goog_data_large["Adj Close"], "Goog prices rolling mean and standard deviation",
                           "Daily prices", 365)
