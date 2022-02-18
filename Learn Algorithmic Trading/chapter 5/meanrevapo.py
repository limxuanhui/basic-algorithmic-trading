# Mean reversion strategy using Absolute Price Oscillator trading signal

import pandas as pd
from loaddata import load_financial_data

SYMBOL = "GOOG"
start_date = "2014-01-01"
end_date = "2018-01-01"
SRC_DATA_FILENAME = SYMBOL + "_data.pkl"

data = load_financial_data(SRC_DATA_FILENAME, start_date, end_date, ticker=SYMBOL)

NUM_PERIODS_FAST = 10
K_FAST = 2 / (NUM_PERIODS_FAST + 1)
ema_fast = 0
ema_fast_values = []

NUM_PERIODS_SLOW = 40
K_SLOW = 2 / (NUM_PERIODS_SLOW + 1)
ema_slow = 0
ema_slow_values = []

apo_values = []

orders = []
positions = []
pnls = []

last_buy_price = 0  # used to prevent over-trading at/around same price
last_sell_price = 0
position = 0
buy_sum_price_qty = 0
buy_sum_qty = 0
sell_sum_price_qty = 0
sell_sum_qty = 0
open_pnl = 0  # Open/unrealised PnL marked to market
closed_pnl = 0  # Closed/realised PnL so far

APO_VALUE_FOR_BUY_ENTRY = -10
APO_VALUE_FOR_SELL_ENTRY = 10
# Minimum price change since last trade before considering trading again,
# to prevent over-trading at/around same price
MIN_PRICE_MOVE_FROM_LAST_TRADE = 10
MIN_PROFIT_TO_CLOSE = 10  # Minimum Open/unrealised profit at which to close positions and lock profits
NUM_SHARES_PER_TRADE = 10  # Number of shares to buy/sell on every trade


close = data["Close"]
for close_price in close:
    if ema_fast == 0:  # first observation
        ema_fast = close_price
        ema_slow = close_price
    else:
        ema_fast = K_FAST * close_price + (1 - K_FAST) * ema_fast
        ema_slow = K_SLOW * close_price + (1 - K_SLOW) * ema_slow

    apo = ema_fast - ema_slow
    ema_fast_values.append(ema_fast)
    ema_slow_values.append(ema_slow)
    apo_values.append(apo)

    if (apo > APO_VALUE_FOR_SELL_ENTRY and abs(close_price - last_sell_price) > MIN_PRICE_MOVE_FROM_LAST_TRADE)\
            or (position > 0 and (apo >= 0 or open_pnl > MIN_PROFIT_TO_CLOSE)):
        orders.append(-1)
        last_sell_price = close_price
        position -= NUM_SHARES_PER_TRADE
        sell_sum_price_qty += close_price * NUM_SHARES_PER_TRADE
        sell_sum_qty += NUM_SHARES_PER_TRADE
        print(f"Sell {NUM_SHARES_PER_TRADE} @ {close_price} | Position: {position}")

    elif (apo < APO_VALUE_FOR_BUY_ENTRY and abs(close_price - last_buy_price) > MIN_PRICE_MOVE_FROM_LAST_TRADE)\
            or (position < 0 and (apo <= 0 or open_pnl > MIN_PROFIT_TO_CLOSE)):
        orders.append(1)
        last_buy_price = close_price
        position += NUM_SHARES_PER_TRADE
        buy_sum_price_qty += close_price * NUM_SHARES_PER_TRADE
        buy_sum_qty += NUM_SHARES_PER_TRADE
        print(f"Buy {NUM_SHARES_PER_TRADE} @ {close_price} | Position: {position}")

    else:
        orders.append(0)
    positions.append(position)

    open_pnl = 0
    if position > 0:
        if sell_sum_qty > 0:
            open_pnl = abs(sell_sum_qty) * (sell_sum_price_qty/sell_sum_qty - buy_sum_price_qty/buy_sum_qty)
            pass  # stop following code




