# Chapter 7 - Building a Trading System in Python

### Need to know
- Asset class: used in trading system to determine data structure used
- Trading strategies: design of software architecture will be determined by the type of strategies; high frequency trades require faster programming language
- Number of trading strategies: more strategies require more compliance checks and need a faster trading system

### Trading system will
- collect data (price updates)
- other data like news announcements
- analyse data to decide type and details of order
- decide which specific exchange is best to get the order filled for the requested pride and volume
- send order to that exchange

### Gateways
Collect price updates from venues you will trade with like exchanges, electronic communication network (ECN), dark pools.
This gateway component will connect to exchanges and be receiving/sending streams of data to communicate with it.

#### This *gateway component* serves as the input/output of the trading system.

### Order book management
We receive data from the gateway component so that we can replicate the limit order book from the exchanges into our trading system.
To combine all the different books received from different venues, book builder will be 
in charge of gathering/sorting prices for our strategies.

### Strategy
- Signal: only focuses on generating trading signals (a signal does not mean a successful execution
as order might be rejected)
- Execution: takes care of handling response from the market (for e.g. when an order rejection occurs, the execution component
should reflect that to the signal generator for the next strategy/get an equivalent liquidity)

### Order management system (OMS)
- This component collects the orders sent from the strategies
- Keeps track of order life cycle (creation, execution, amendment, cancellation, rejection)
- OMS may reject orders if an order is malformed/invalid (quantity too large, wrong direction, erroneous prices, 
excessive outstanding position, order type not handled by exchange)
- When order is detected in OMS, the order does not go out from the trading system

### Critical components
- Gateways, book builder, strategies, OMS are critical components for trading
- Performance of trading system is measured by adding the processing time of all critical components
- Timer starts when a price update enters trading system, timer stops when the order triggered by this price update exits
- Goal is to reduce *tick-to-order or tick-to-trade* time to around 300 nanoseconds to 10 microseconds

### Command and control
- A non-critical component
- Command line interface or user interface receiving commands from traders and sending commands to appropriate components
- For e.g. a trader might adjust risk limit using the C&C interface to get strategy component to update risk levels

### Services (non-exhaustive list of additional components)
- Position server: keeps track of all trade positions. OMS might go through this component to see if order size is allowed
- Logging system: gathers all logs and update database. Helps with debugging or generating reports. 
- Viewers (read-only UI): displays positions, orders, trades, task monitoring ...) 
- Control viewers (interactive UI): provides a way to modify parameters/start/stop components 
- News servers: gathers news from news companies and provides news in real-time/on-demand to strategy generator


# Problems with Chapter 7
I copied the code from the book word for word into this directory, with only one or two minor variable name changes on my part. 
### Countless bad code practices
- Variable names inconsistencies
- File names wrong
- Code examples badly aligned in book, difficult to know which nested blocks of code belong to which
- Too many nested if else blocks
- Bad variable names

