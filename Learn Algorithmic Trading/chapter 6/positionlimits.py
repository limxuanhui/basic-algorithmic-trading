# Position limits
# The maximum position, long or short, that the strategy should have at any point in its trading lifetime

import matplotlib.pyplot as plt
import pandas as pd

results = pd.read_csv("volatility_adjusted_mean_reversion.csv")
print(results.head(1))

position = results["Position"]
plt.hist(position, 20)
plt.gca().set(title="Position Distribution", xlabel="Shares", ylabel="Frequency")
plt.show()
