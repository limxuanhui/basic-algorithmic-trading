# Mean Reversion

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas_datareader import data
from statsmodels.tsa.stattools import coint
from loaddata import load_financial_data
from helper import find_cointegrated_pairs, zscore
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)
np.random.seed(17)

symbols = ["SPY", "AAPL", "ADBE", "LUV", "MSFT", "SKYW", "QCOM", "HPQ", "JNPR", "AMD", "IBM"]
start_date = "2001-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "multi_data_large.pkl"

data = load_financial_data(SRC_DATA_FILENAME, start_date, end_date, ticker=symbols)
print("Finding cointegrated pairs...")
pvalues, pairs = find_cointegrated_pairs(data["Adj Close"])
print(f"Pvalues: {pvalues} | pairs: {pairs}")

print("Plotting heatmap...")

ax = sns.heatmap(pvalues, xticklabels=symbols, yticklabels=symbols, annot=True, cmap="RdYlGn_r", mask=(pvalues >= 0.98))
plt.show()


Symbol1_returns = np.random.normal(0, 1, 100)
Symbol1_prices = pd.Series(np.cumsum(Symbol1_returns), name="Symbol1") + 10
Symbol1_prices.plot(figsize=(15, 7))
plt.show()


noise = np.random.normal(0, 1, 100)
Symbol2_prices = Symbol1_prices + 10 + noise
Symbol2_prices.name = "Symbol2"
plt.title("Symbol1 and Symbol2 prices")
Symbol1_prices.plot()
Symbol2_prices.plot()
plt.show()


score, pvalue, _ = coint(Symbol1_prices, Symbol2_prices)  # Score: -9.255417954730088 | Pvalue: 1.9363686387899392e-14
print(f"Score: {score} | Pvalue: {pvalue}")


ratios = Symbol1_prices / Symbol2_prices
ratios.plot()
plt.show()


train = ratios[:75]
test = ratios[75:]
zscores = zscore(ratios)
zscores.plot()
plt.axhline(zscores.mean(), color="k")
plt.axhline(1.0, color="g")
plt.axhline(-1.0, color="r")
plt.legend(["Ratio", "Mean", "Mean + 1.0", "Mean - 1.0"])
plt.show()


ratios.plot()
buy = ratios.copy()
sell = ratios.copy()
buy[zscores > -1] = 0
sell[zscores < 1] = 0
buy.plot(color="g", linestyle="None", marker="^")
sell.plot(color="r", linestyle="None", marker="v")
plt.axhline(ratios.mean(), color="k")
x1, x2, y1, y2 = plt.axis()
plt.axis((x1, x2, ratios.min(), ratios.max()))
plt.legend(["Ratio", "Buy signal", "Sell signal", "Mean"])
plt.show()


print("--- Pair Correlation Trading Strategy ---")
pair_correlation_trading_strategy = pd.DataFrame(index=Symbol1_prices.index)
pair_correlation_trading_strategy["symbol1_price"] = Symbol1_prices
pair_correlation_trading_strategy["symbol1_buy"] = np.zeros(len(Symbol1_prices))
pair_correlation_trading_strategy["symbol1_sell"] = np.zeros(len(Symbol1_prices))
pair_correlation_trading_strategy["symbol2_buy"] = np.zeros(len(Symbol1_prices))
pair_correlation_trading_strategy["symbol2_sell"] = np.zeros(len(Symbol1_prices))

# ...
