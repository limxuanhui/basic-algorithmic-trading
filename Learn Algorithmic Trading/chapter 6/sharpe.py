# Sharpe Ratio

import matplotlib.pyplot as plt
import pandas as pd
from statistics import stdev, mean

results = pd.read_csv("volatility_adjusted_mean_reversion.csv")
print(results.head(1))

num_days = len(results.index)
pnl = results["Pnl"]

last_week = 0
weekly_pnls = []
weekly_losses = []

for i in range(0, num_days):
    if i - last_week >= 5:
        pnl_change = pnl[i] - pnl[last_week]
        weekly_pnls.append(pnl_change)
        if pnl_change < 0:
            weekly_losses.append(pnl_change)
        last_week = i

sharpe_ratio = mean(weekly_pnls) / stdev(weekly_pnls)
sortino_ratio = mean(weekly_pnls) / stdev(weekly_losses)
print(f"Sharpe ratio: {sharpe_ratio}")
print(f"Sortino ratio: {sortino_ratio}")
