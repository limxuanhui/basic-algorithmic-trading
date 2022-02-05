import numpy as np
import pandas as pd
import seaborn as sb
from statsmodels.tsa.stattools import coint


def double_moving_average(financial_data, short_window, long_window):
    signals = pd.DataFrame(index=financial_data.index)
    signals["signal"] = 0.0
    signals["short_mavg"] = financial_data["Close"].rolling(window=short_window, min_periods=1, center=False).mean()
    signals["long_mavg"] = financial_data["Close"].rolling(window=long_window, min_periods=1, center=False).mean()
    signals["signal"][short_window:] = np.where(signals["short_mavg"][short_window:] >
                                                signals["long_mavg"][short_window:], 1.0, 0.0)
    signals["orders"] = signals["signal"].diff()
    return signals


def naive_momentum_trading(financial_data, nb_conseq_days):
    signals = pd.DataFrame(index=financial_data.index)
    signals["orders"] = 0
    cons_day = 0
    prior_price = 0
    init = True

    for k in range(len(financial_data["Adj Close"])):
        price = financial_data["Adj Close"][k]
        if init:
            prior_price = price
            init = False
        elif price > prior_price:
            if cons_day < 0:
                cons_day = 0
            cons_day += 1
        elif price < prior_price:
            if cons_day > 0:
                cons_day = 0
            cons_day -= 1

        if cons_day == nb_conseq_days:
            signals["orders"][k] = 1
        elif cons_day == -nb_conseq_days:
            signals["orders"][k] = -1

    return signals


def turtle_trading(financial_data, window_size):
    signals = pd.DataFrame(index=financial_data.index)
    signals["orders"] = 0

    signals["high"] = financial_data["Adj Close"].shift(1).rolling(window=window_size).max()
    signals["low"] = financial_data["Adj Close"].shift(1).rolling(window=window_size).min()
    signals["avg"] = financial_data["Adj Close"].shift(1).rolling(window=window_size).mean()

    signals["long_entry"] = financial_data["Adj Close"] > signals.high
    signals["short_entry"] = financial_data["Adj Close"] < signals.low

    signals["long_exit"] = financial_data["Adj Close"] < signals.avg
    signals["short_exit"] = financial_data["Adj Close"] > signals.avg

    init = True
    position = 0
    for k in range(len(signals)):
        if signals["long_entry"][k] and position == 0:
            signals.orders.values[k] = 1
            position = 1
        elif signals["short_entry"][k] and position == 0:
            signals.orders.values[k] = -1
            position = -1
        elif signals["short_exit"][k] and position > 0:
            signals.orders.values[k] = -1
            position = 0
        elif signals["long_exit"][k] and position < 0:
            signals.orders.values[k] = 1
            position = 0
        else:
            signals.orders.values[k] = 0

    return signals


def find_cointegrated_pairs(data):
    n = data.shape[1]
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            result = coint(data[keys[i]], data[keys[j]])
            pvalue_matrix[i, j] = result[1]

            if result[1] < 0.02:
                pairs.append((keys[i], keys[j]))
    return pvalue_matrix, pairs


def zscore(series):
    return (series - series.mean()) / np.std(series)
