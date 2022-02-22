# Chapter 8 - Connecting to Trading Exchanges

### Network basics - medium for communication
- Wire
- Fiber: more bandwidth than wire
- Microwave: large bandwidth but impacted by storms

### Trading protocols - steps to establish connection and trade
1) Initiate logon describing the trading initiator, recipient and how communication remains alive
2) Inquire about what they expect from the different entities e.g. trading or subscribing to price updates
3) Receive orders and price updates
4) Maintain communication by sending heartbeats
5) Close communication

### FIX libraries
- NYFIX
- Aegisfot - Aethna
- Reuters - Traid
- Financial Fusion - Trade Force
- quickfix

NASDAQ uses direct data feed ITCH and direct-trading OUCH protocol,
which are much faster than FIX protocols due to their limit overhead.

NYSE uses UTP Direct, similar to NASDAQ protocols.


