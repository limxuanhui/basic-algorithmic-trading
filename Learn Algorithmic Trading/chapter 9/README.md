# Chapter 9 - Creating a Backtester in Python

## Learning how to build a backtester
###


### Assumptions
#### Fundamental assumption 
Since we use historical data stored in databases to reproduce the behaviour of trading:
1) We assume that any methodology that worked in the past is probably going to work in the future.
2) Any strategies that performed badly in the past are probably going to perform badly in the future.

A backtester can be a **for-loop** or **event-driven** backtester.
A backtester is just trying to model reality, and it is not possible to exactly model the future.

#### Basic rules to follow:
1) Training/testing data:
Should not test model with the data that is used to create the model.
You need to validate your model on unseen/test dataset to prevent overfitting. 

2) Survivorship-bias free data:
If your strategy is long-term position strategy, it is important to use survivorship-bias free data.
This prevents you from only focusing on winners and forgo the losers. This means your
survivorship-bias free data includes the losers so that your model will include the losers.

3) Look-ahead data:
When you build a strategy, you should not look ahead to make a trading decision.
This might happen when you calculate quantities like averages using the whole dataset,
when you should only be using data up to the "current" point.

4) Market change regime:
Modeling stock distribution parameters are not constant in time because the market changes regime

5) Transaction costs:
It is important to consider transaction costs of trading because a profitable strategy might
become unprofitable once transaction costs are taken into account.

6) Data quality/source:
Since there are many financial data sources, data composition differs greatly.
For e.g., Open-High-Low_Close (OHLC) data from Google Finance is an aggregation of many exchange feeds.

7) Money constraint: 
Always consider the amount of money you trade is not infinite. 
Additionally, a credit/margin account is limits the position you take.

8) Average daily volume (ADV):
The average number of shares traded over a day for a given ticker.
You should decide the quantity of shares to trade based the ADV to avoid having any impact on the market.

9) Benchmark testing:
In order to test the performance of your trading strategy, you will compare against another type of strategy,
or just the return of some indices. If you trade futures, do not test against the S&P500.
If you trade in airlines, check whether the airline industry as a whole performs better than your model.

10) Initial condition assumption:
In order to have a robust way of making money, you should not depend on the day you start your backtesting or the month.
More generally, you should not assume that the initial condition is always the same.

11) Psychology:
Even when we build a trading bot, when we trade with real money there is always a way to override the algorithm manually
and most of the time it is not advisable to do so if a proper backtest result was obtained.

Other assumptions:
1) Fill ratio:
When we place an order, the chance of the order being filled varies with the type of strategies we use.
An HFT strategy may have 95% of orders rejected and when trading is done during important news announcements,
most orders may be rejected. This fill ratio needs to be properly assumed for the backtester.

2) Market making strategies:
Market making strategies add liquidity to the market, so it is important to assume when order will be executed or not at all.
This assumption will add a condition to the backtester.

4) Latency assumption:
Trading systems rely on many components, each of which has its latency and contributes to the
overall communication latency, network latency, latency to have order processed.

## For-loop backtest systems
### Advantages
- Simple, easily implemented in any programming language
- Need for computational power is low
- Execution does not take too long and quick to obtain results regarding performance of strategies

### Disadvantages
- Accuracy in relation to market as it neglects transaction costs, transaction time, bid offer price, volume.
- Easy to introduce look-ahead bias


## Event-driven backtest systems
### Advantages
- Closer to reality due to more trading components being used.
- Look-ahead bias elimination - we receive events and therefore do not look at the data ahead
- Code encapsulation - because we use objects for the different parts of the trading system,
we can change the behaviour of the system easily by changing each component 
- We can insert a position/risk management system and check that we do not go against the limit

### Disadvantages
- Difficult to code
- Requires a lot of handling like log management, unit testing, version control
- Execution can be slow

## Evaluating what the value of time is
