# Chapter 10 - Adapting to Market Participants and Conditions

### Strategy performance in backtester vs live markets
- The shorter the position holding period and the large the trading sizes,
the greater the chance that simulation results are different from results 
actually achieved in live trading markets.
- Basic problem boils down to trade prices and sizes not identical in backtester and live environment
- Need to align pessimism/optimism of backtester with live trading

#### Impact of backtester dislocations
Not having a good backtester causes a variety of problems with historical research and live deployment of strategies

1) Signal validation:

Backtester must be able to accurately synchronize different market data sources
and playing market data back with accurate timestamps and event synchronization.
Otherwise, the signal predictions and performance observed in historical research
may not be realized in live trading and hurt profitability of strategy.

2) Strategy validation:

Backtester must be able to simulate the behavior and performance of a trading strategy 
over historical data as if it were trading in live markets by performing order matching
like an exchange environment. 

3) Risk estimates:

Risk measures have to be quantified in a backtester before deploying a strategy live. Failure
to do so will cause inaccuracies in measuring expected risk limits when strategies get deployed.

4) Risk management system

It is difficult to build an optimal risk management system because we not only want an RMS, but also
a system of slowly increasing trading exposure and risk limits after good performance as well as lower
exposure and risk following a poor performance. 

5) Choice of strategies for deployment

A good backtester must be able to build a portfolio of strategies to deploy live in a way that
minimises risk for the entire portfolio. A backtester that cannot do this may cause live trading
to take on more risk than historical simulations would have.

6) Expected performance

A backtester that deviates a lot from live trading will cause performance expectations derived from
simulations to not hold up during live trading.


#### Causes of simulation dislocations
What are some factors that cause a backtester to be inaccurate of live trading?

1) Slippage

Expected execution prices in simulation and actual trading prices realized in live trading are likely to be different

2) Fees

Transaction costs that are not taken into account in simulation often inflate profitability,
especially for strategies that trade with high volume.

3) Operational issues

During the operation of live trading, manual intervention is often a bad idea if 
the trading algorithms have been extensively backtested.

4) Market data issues

Issues with playing back historical market data to trading strategies can be a problem
if the market data that trading strategies observed in live trading is different from simulation data.
This can be because of difference in servers, the way market data gets decoded, issues in how the data gets
timestamped and stored, or the way data gets read and inputted to trading strategy, or data source/vendors. 

5) Latency variance

Each component in the trading system as well as the transmission of order from trading engine
to the matching engine at the exchange contributes to latency, or time lag, and has to be accounted for
in simulation. However, these latencies vary depending on a lot of factors such as trading signal/strategy 
implementation, market conditions, peak network traffic etc. Live trading performance can differ greatly 
from expected simulation performance if latencies are not considered during backtesting.

6) Place-in-line estimates

Since electronic trading exchanges have different possible matching algorithms such as FIFO or pro-rata, 
if a trading strategy performance depends on having a good place in line. If a trading algorithm is too optimistic in 
estimating a trading strategy's order priority in the limit order book compared to other market participants, then
trading performance may be inflated and false.

7) Market impact

Market impact refers to what happens when our trading strategy is deployed to live markets as compared to when it is not.
This is trying to quantify and understand the reactions of other market participants in response to our order.
Market impact is difficult to model, and gets progressively worse the more trading strategy is scaled up.

Profitability does not increase linearly with risk. Instead, the rate of increase of profitability slows down as size
is increased, but risk continues to increase due to market impact reasons. Eventually, strategies reach a size where
large increases in risk only marginally increase profitability, the upper limit of the strategy scale.  

#### Tweaking Backtesting and strategies in response to live trading
Possible approaches/solutions to deviation of simulation performance from live trading performance:

1) Historical market data accuracy

Quality and quantity of historical market data is crucial to a profitable algorithmic trading business.

2) Measuring and modeling latencies

Ideally in live trading, timestamps at each trading system component should be recorded precisely in nanoseconds,
and total latencies be calculated and used in backtester. During periods of higher market activity due to busy market
conditions and large price moves, or when a lot of participants are sending a higher-than-normal amount of order to the
exchange thereby generating unusually large amount of market data, many latency measures are likely to be higher than 
normal and in fact, be a function of increased market activity. This makes sense because the trading exchange has to process
more orders, perform more matching per order, and generate/disseminate more market data for every order, resulting in
increased processing times.

On our side, more market data implies more data to read, decode and normalize, more time to update our limit order books
and update trading signals, more orders generated to deal with increased market activity, and more work done by our order
gateway to deal with the increased order activity.

3) Improving backtesting sophistication

Modern electronic exchanges provide a lot of information about every aspect of the matching process beyond just accurate 
timestamps. Non-conforming transactions such as self-match-prevention cancellations, stop-order releases during matching
events, iceberg orders with hidden liquidity that over-execute or replenished after being fully executed, matches during
auction events, implied/pro-rata matching considerations, all can cause simulation to deviate from live trading if not 
accounted for in backtesting.

Different asset classes have their own set of matching rules and complications. Dark pools, hidden liquidity, price improvements,
hidden counter-parties etc. can cause simulation dislocations.

4) Adjusting expected performance for backtester bias

Backtester bias can be optimistic or pessimistic in nature and can be a constant/varying bias depending on strategy type,
strategy parameters, market conditions etc. We can try to model the magnitude of backtester optimism/pessimism as a function
of traded volume and market conditions such as how busy the market is or how much prices have changed. Then we adjust simulation
results by this modeled bias to get an estimate of live trading performance.

5) Analytics on live trading strategies

Instead of relying completely on backtesting performance and behaviour, you can invest in adding enough intelligence and
sophistication directly to live trading strategies to reduce the likelihood of simulation dislocation. For e.g. we can
add Post Trade Analytics (PTA) to analyse strategy action records and classify winning/losing positions and their statistics.


### Continued profitability in algorithmic trading
#### Profit decay in algorithmic trading strategies
1) Signal decay due to lack of optimization

Trading signals need to be constantly re-evaluated and re-adjusted to stay relevant/profitable. This is partially because
trading signals with constant parameters cannot perform equally well through different market conditions.
It is important to set up a systematic optimization pipeline to adapt trading signals to changing markets.

2) Signal decay due to absence of leading participants

Many trading signals capture specific market participant behaviour to predict future price movements.
For e.g. trading signals trying to detect order flow from HFT participants to get a sense of the proportion of liquidity
from fast participants, who can add/remove liquidity very quickly. If a large amount of market participants become more 
informed or are able to disguise their intentions, then the trading signals will lose their predictive abilities.

3) Signal discovery by other participants

Most market participants are also searching for new trading signal like we do. Often they may discover the same trading 
signals that our strategies are using to be profitable. These market participants may try to change their trading strategy's
order flow to disguise their intent and make the signal not profitable for us. They may also start using the same trading 
signals for their strategies and overcrowd the market with the same strategy, thus reducing our ability to scale up. They 
may also use better infrastructure or more capital to squeeze us out of the market. The simpler the strategy the easier 
it is to be discovered, and while the more complex strategies are less likely to be discovered by others, they are more 
difficult to develop and requires a lot of research. 

4) Profit decay due to exit of losing participants

Trading is a zero-sum game, where for one participant to profit, one or more other participants must lose money. The 
problem with this is that participants that are losing money either get smarter or faster and stop losing money, or they 
continue losing money and eventually exit the market. This exit of losing participants will hurt the continued profitability
of our trading strategies.

5) Profit decay due to discovery by other participants

It is possible for other market participants to discover our order flow and strategy behaviour, and then find ways to 
anticipate and leverage our trading strategy's order flow to trade against us in a way that causes our strategies to lose 
money. Sophisticated market participants often use one or more of the following ways to disguise their strategy behaviour:
- Use of GTC orders to build queue priority in FIFO markets
- Use icebergs to disguise the true liquidity behind orders
- Use of stop orders to be triggered at specific prices ahead of time
- 'Fill and Kill' or 'Immediate or Cancel' orders to mask the true liquidity sent to exchange
- Spoofing, which is an illegal method, is the faking of orders 

6) Profit decay due to changes in underlying assumptions/relationships

All trading strategies are built upon assumptions, which may be true when the strategy was first built,
but become false as time passes and market conditions change. It is important to detect, analyse and understand
what strategies will not perform as expected, and have a diverse set of trading strategies with non-overlapping assumption
ready for disposal.

7) Seasonal profit decay

Seasonality is an assumption that dictates a trading strategy's profitability. Trading strategies need to account for 
seasonal behaviour of asset classes and adapt.


#### Adapting to market conditions and changing participants
1) Building a trading signals dictionary/database

It is a large database containing statistics of different trading signals and different trading signal parameter sets 
over years of data. These statistics are primarily the ones to capture predictive abilities of these signals over their
prediction horizon, for e.g.
- Correlation of trading signal value with price movements of trading instrument
- Variance in predictive power over days 
The point of having such a database is that when market conditions change, we can query this database to understand/analyse
which trading signal, signal input and signal parameter sets do better than others.

2) Optimizing trading signals

We also need a data-mining/optimization system capable of taking existing trading signals, building a large number of 
instrument and parameter combinations, then optimize over that large population of similar but slightly different trading 
signals of different prediction horizons, then summarise results of the optimal one. 

3) Optimizing prediction models

We also need to consider the optimization method used to optimize the prediction model, which is a combination of 
individual trading signals. 

4) Optimizing trading strategy parameters

A trading signal has input parameters that control its output. Similarly, prediction models, which are combinations of 
trading signals, have weights/coefficients/parameters that control how trading signals interact with each other. Trading 
strategies also have parameters that control how trading signals, prediction models and execution models work together to 
send the order flow. Optimization objectives are PnL and risk instead of predictive ability, which is used to evaluate 
trading signals and predictive models. 

5) Researching new trading signals

Trading signal ideas are brainstormed from live trading analytics, by inspecting periods of losses or inspecting market
data and interactions between market data, market participants, trading signals and strategies. Based on observation,
new trading signals are conceptualised based on what *appears* like it would have helped avoid losing positions, help 
produce more winning positions or increase the magnitude of winning positions. At this point, the trading signal is just 
an idea without quantitative research to back it up. Then we implement the trading signal and tweak/validate signal outputs
to understand its predictive abilities.

If the newly-developed trading signal appears to show potential predictive abilities, it passes the prototyping stage
(many trading signals do not pass this stage), and forwarded to the trading signal optimization pipeline. At the optimization
step, we find the best variants of the new trading signal and add it to prediction models, where it interacts with other 
signals. After many iterations of trying to combine this signal with others to produce a better prediction model than before,
the new trading signal is used in a final trading strategy with strategy parameters that get evaluated and optimized. Then, 
we determine if the addition of the new trading signal improves the strategy's profitability.

6) Expanding to new trading strategies

Similar to researching new trading signals that interact with existing trading signals to add non-overlapping predictive 
abilities, we need to build new trading strategies that interact with existing strategies to add non-overlapping profits.
It is important for new trading strategies to be making money when other strategies might be losing money. By having a 
diverse pool of trading strategies, we can deal with changing market conditions.

7) Portfolio optimization

With a portfolio of multiple trading strategies, how do we decide how much risk to allocate to each strategy to maximise 
the profit of our entire portfolio?
   - Uniform risk allocation - Equally distribute risk among all trading strategies
   - PnL-based risk allocation - Distribute more risk to better performing strategies
   - PnL-sharpe-based risk allocation

Penalise strategies with high volatility returns; does not take into account 
correlation of returns between strategies (individual strategy may have good risk-adjusted PnL but the entire portfolio 
is highly volatile due to the correlation)
   - Markowitz allocation

Minimise variance of portfolio return, while taking into account covariances of returns of 
all trading strategies. Allocation seeks to maximise diversity of different trading strategies in the portfolio, by ensuring 
that stategies with uncorrelated returns have risk allocated to them.

   - Regime predictive allocation 

A technique that studies the performance of different trading strategies as a function of different economic indicators.
Builds machine learning models that can predict what kinds of trading strategies and what product groups are most likely 
to do well given current market conditions. This method uses economic indicators as input features to a model that predicts
trading strategies' expected performance in the current market regime, then uses those predictions to balance allocations 
to strategies. 


9) Incorporating technological advances
