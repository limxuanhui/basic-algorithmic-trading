# Variance of Pnl

import matplotlib.pyplot as plt
import pandas as pd
from statistics import stdev

results = pd.read_csv("volatility_adjusted_mean_reversion.csv")
print(results.head(1))

num_days = len(results.index)
pnl = results["Pnl"]

last_week = 0
weekly_pnls = []

for i in range(0, num_days):
    if i - last_week >= 5:
        weekly_pnls.append(pnl[i] - pnl[last_week])
        last_week = i

print(f"Weekly PnL Standard Deviation: {stdev(weekly_pnls)}")

plt.hist(weekly_pnls, 50)
plt.gca().set(title="Weekly PnL Distribution", xlabel="$", ylabel="Frequency")
plt.show()
