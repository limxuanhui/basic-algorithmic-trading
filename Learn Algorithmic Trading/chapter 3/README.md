# Chapter 3 - Predicting the Markets with Basic Machine Learning

# Problems in Chapter 3

### Page 90 
"For algorithmic trading, the common target is to be able to
predict what the future price will be so that we can take
positions in the market right now that yield a profit
in the future."

#### - Are we really able to predict the future price of a security?


### page 94
#### - In point 3., "target" not in index of goog_data. It was not defined anywhere prior. 
#### - plt.show() required for scatter_matrix to show


### page 96
#### - In "calculate_return" function, why *df['Strategy_Returns'] = df['%s_Returns' % symbol] * df['Predicted_Signal'].shift(1)* ? Shouldn't this be assigned out of this function?
#### - In "calculate_strategy_return" function, symbol argument is not used.


### page 97
#### - In "sharpe_ratio" function, symbol_returns and strategy_returns are arguments in this order. When executing, the cum_strategy_return was passed first in the book. I got sharpe ratio of "-9.071052577168551" when passing arguments in the right order.


### page 101
#### - "create_trading_condition" is not defined. Should be "create_classification_trading_condition"


### page 104
#### - The chart for SVC model prediction seems to be a duplicate chart from page 97, which is the chart for the OLS model prediction.
#### - Logistic Regression prediction code not provided.



