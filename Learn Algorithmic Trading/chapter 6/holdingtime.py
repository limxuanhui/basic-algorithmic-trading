import matplotlib.pyplot as plt
import pandas as pd

results = pd.read_csv("volatility_adjusted_mean_reversion.csv")
print(results.head(20))

num_days = len(results.index)
position_holding_times = []
current_pos = 0
current_pos_start = 0

for i in range(0, num_days):
    pos = results["Position"].iloc[i]

    if current_pos == 0:
        if pos != 0:
            current_pos = pos
            current_pos_start = i
        continue

    if current_pos * pos <= 0:
        current_pos = pos
        position_holding_times.append(i - current_pos_start)
        current_pos_start = i

print(position_holding_times)
plt.hist(position_holding_times, 100)
plt.gca().set(title="Position Holding Time Distribution", xlabel="Holding time days", ylabel="Frequency")
plt.show()
