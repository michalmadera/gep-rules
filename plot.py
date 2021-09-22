import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_excel("result/summary_report_f1.xlsx")

atr_4 = data.loc[data['attributes'] == 4]
atr_5 = data.loc[data['attributes'] == 5]
atr_7 = data.loc[data['attributes'] == 7]
atr_10 = data.loc[data['attributes'] == 10]
atr_15 = data.loc[data['attributes'] == 15]
atr_20 = data.loc[data['attributes'] == 20]

plt.style.use('seaborn-darkgrid')
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, sharex=True, sharey=True)
fig.suptitle("Mean duration time for tensorflow")

ax1.plot(atr_5.samples, atr_5['numpy duration'], label="numpy - mean duration")
ax1.plot(atr_5.samples, atr_5['tensorflow duration'], label="tensorflow - mean duration")
ax1.plot(atr_5.samples, atr_5['numpy generations'], '--', label="numpy - mean number of generations")
ax1.plot(atr_5.samples, atr_5['tensorflow generations'], '--', label="tensorflow - mean number of generations")
ax1.set(xlabel="samples for 5 attributes", ylabel="mean duration time [s]")

ax2.plot(atr_10.samples, atr_10['numpy duration'])
ax2.plot(atr_10.samples, atr_10['tensorflow duration'])
ax2.plot(atr_10.samples, atr_10['numpy generations'], '--')
ax2.plot(atr_10.samples, atr_10['tensorflow generations'], '--')
ax2.set(xlabel="samples for 10 attributes")

ax3.plot(atr_15.samples, atr_15['numpy duration'])
ax3.plot(atr_15.samples, atr_15['tensorflow duration'])
ax3.plot(atr_15.samples, atr_15['numpy generations'], '--')
ax3.plot(atr_15.samples, atr_15['tensorflow generations'], '--')
ax3.set(xlabel="samples for 15 attributes")

ax4.plot(atr_20.samples, atr_20['numpy duration'])
ax4.plot(atr_20.samples, atr_20['tensorflow duration'])
ax4.plot(atr_20.samples, atr_20['numpy generations'], '--')
ax4.plot(atr_20.samples, atr_20['tensorflow generations'], '--')
ax4.set(xlabel="samples for 20 attributes")
ax1.legend()

plt.show()
