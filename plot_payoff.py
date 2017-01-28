import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("output/MAX_BOOKED_280_PER_SLOT_50_NUMBER_OF_SLOTS_3_prob_0.5.csv")
print df.keys()

payoff = "PAYOFF"
plt.plot(list(df[payoff][0:-1]))
plt.show()
print "test"
