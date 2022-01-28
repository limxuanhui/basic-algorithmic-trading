import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split


def create_regression_trading_condition(df):
    df["Open-Close"] = df.Open - df.Close
    df["High-Low"] = df.High - df.Low
    df["Target"] = df["Close"].shift(-1) - df["Close"]
    df.dropna(inplace=True)
    x = (df[["Open-Close", "High-Low"]])[0:-1]
    y = (df["Close"].shift(-1) - df["Close"])[0:-1]
    return x, y


def create_classification_trading_condition(df):
    df["Open-Close"] = df.Open - df.Close
    df["High-Low"] = df.High - df.Low
    df["Target"] = np.where(df["Close"].shift(-1) > df["Close"], 1, -1)
    df.dropna(inplace=True)
    x = (df[["Open-Close", "High-Low"]])
    y = (np.where(df["Close"].shift(-1) > df["Close"], 1, -1))
    return x, y


def create_train_split_group(x, y, split_ratio=0.8):
    return train_test_split(x, y, shuffle=False, train_size=split_ratio)


def calculate_returns(df, split_value, symbol):
    cum_return = df[split_value:][f"{symbol}_Returns"].cumsum() * 100
    # df["Strategy_Returns"] = df[f"{symbol}_Returns"] * df["Predicted_Signal"].shift(1)
    return cum_return


def calculate_strategy_returns(df, split_value, strat_type=None):
    if strat_type is None:
        strat_col_name = "Strategy_Returns"
    else:
        strat_col_name = f"{strat_type}_Strategy_Returns"

    cum_strat_returns = df[split_value:][strat_col_name].cumsum() * 100
    return cum_strat_returns


def plot_chart(cum_symbol_returns, cum_strat_returns, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(cum_symbol_returns, label=f"{symbol} Returns")
    plt.plot(cum_strat_returns, label="Strategy Returns")
    plt.legend()
    plt.show()


def sharpe_ratio(symbol_returns, strategy_returns):
    strategy_std = strategy_returns.std()  # standard deviation here and numpy implementation should be different. Why?
    sharpe = (strategy_returns - symbol_returns) / strategy_std
    sharpe = sharpe.mean()
    return sharpe
