import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from loaddata import load_financial_data
from helper import create_regression_trading_condition, create_train_split_group, calculate_returns,\
                   calculate_strategy_returns, plot_chart, sharpe_ratio

##### CONSTANTS
start_date = "2001-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "goog_data.pkl"

goog_data = load_financial_data(SRC_DATA_FILENAME, start_date, end_date)
X, Y = create_regression_trading_condition(goog_data)
pd.plotting.scatter_matrix(goog_data[["Open-Close", "High-Low", "Target"]], grid=True, diagonal="kde")
plt.show()

##### OLS model
X_train, X_test, Y_train, Y_test = create_train_split_group(X, Y, split_ratio=0.8)
ols_model = LinearRegression()
ols_model.fit(X_train, Y_train)
print(f"Coefficients: {ols_model.coef_}")  # Coefficients: [ 0.02410178 -0.05781463]
print(f"Mean squared error (train set): {round(mean_squared_error(Y_train, ols_model.predict(X_train)), 5)}")
print(f"R squared (train set): {round(r2_score(Y_train, ols_model.predict(X_train)), 5)}")
print(f"Mean squared error (test set): {round(mean_squared_error(Y_test, ols_model.predict(X_test)), 5)}")
print(f"R squared (test set): {round(r2_score(Y_test, ols_model.predict(X_test)), 5)}")

goog_data = goog_data[0:-1]
goog_data["Predicted_Signal"] = ols_model.predict(X)
goog_data["GOOG_Returns"] = np.log(goog_data["Close"] / goog_data["Close"].shift(1))
# Is it correct to use actual GOOG_Returns to multiply with Predicted_Signals?
goog_data["Strategy_Returns"] = goog_data["GOOG_Returns"] * goog_data["Predicted_Signal"].shift(1)


cum_goog_returns = calculate_returns(goog_data, split_value=len(X_train), symbol="GOOG")
cum_strategy_returns = calculate_strategy_returns(goog_data, split_value=len(X_train))
plot_chart(cum_goog_returns, cum_strategy_returns, symbol="GOOG")
print(f"cum_strategy_return: {cum_strategy_returns} | cum_goog_return: {cum_goog_returns}")
print(f"Sharpe ratio: {sharpe_ratio(cum_goog_returns, cum_strategy_returns)}")


##### Regularization and Shrinkage - LASSO and Ridge Regression
print(f"OLS coefficients: {ols_model.coef_}")
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, Y_train)
print(f"LASSO coefficients: {lasso.coef_}")

ridge = Ridge(alpha=10000)
ridge.fit(X_train, Y_train)
print(f"Ridge coefficients: {ridge.coef_}")
