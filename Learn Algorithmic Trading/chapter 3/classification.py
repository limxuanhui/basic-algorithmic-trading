import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from loaddata import load_financial_data
from helper import create_classification_trading_condition, create_train_split_group, calculate_returns,\
                   calculate_strategy_returns, plot_chart

##### CONSTANTS
start_date = "2001-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = "goog_data.pkl"
goog_data = load_financial_data(SRC_DATA_FILENAME, start_date, end_date)
X, Y = create_classification_trading_condition(goog_data)
X_train, X_test, Y_train, Y_test = create_train_split_group(X, Y, split_ratio=0.8)

##### Decision Tree Regression

##### K-Nearest Neighbors
knn = KNeighborsClassifier(n_neighbors=15)
knn.fit(X_train, Y_train)
accuracy_train = accuracy_score(Y_train, knn.predict(X_train))
accuracy_test = accuracy_score(Y_test, knn.predict(X_test))

goog_data["KNN_Predicted_Signal"] = knn.predict(X)
goog_data["GOOG_Returns"] = np.log(goog_data["Close"] / goog_data["Close"].shift(1))
# Is it correct to use actual GOOG_Returns to multiply with Predicted_Signals?
goog_data["KNN_Strategy_Returns"] = goog_data["GOOG_Returns"] * goog_data["KNN_Predicted_Signal"].shift(1)

cum_goog_returns = calculate_returns(goog_data, split_value=len(X_train), symbol="GOOG")
cum_knn_strategy_returns = calculate_strategy_returns(goog_data, split_value=len(X_train), strat_type="KNN")
plot_chart(cum_goog_returns, cum_knn_strategy_returns, symbol="GOOG")


##### Support Vector Machines
svc = SVC()
svc.fit(X_train, Y_train)

goog_data["SVC_Predicted_Signal"] = svc.predict(X)
goog_data["SVC_Strategy_Returns"] = goog_data["GOOG_Returns"] * goog_data["SVC_Predicted_Signal"].shift(1)
cum_svc_strategy_returns = calculate_strategy_returns(goog_data, split_value=len(X_train), strat_type="SVC")
plot_chart(cum_goog_returns, cum_svc_strategy_returns, symbol="GOOG")
print(goog_data)


##### Logistic Regression