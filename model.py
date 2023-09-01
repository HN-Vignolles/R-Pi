import pandas as pd
from IPython.display import display,Math,Latex,Markdown
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

df = pd.read_csv("model.csv", sep="\t")
display(df.head(6))

t, v1 = df['time'], df['V(Reset,N003)']

fig = plt.figure(figsize=(12,4))
ax1 = fig.add_subplot(1,2,1)

ax1.plot(t, v1, label="...")

ax1.set_title("...")
ax1.legend()
#ax.set_xlim(1, 1.3)
#ax1.set_ylim(4, 5)
#ax1.set_xlabel("Time")
ax1.set_ylabel("V(Reset,N003)")
#ax1.xaxis.set_major_locator(MultipleLocator(0.5))
#ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
#ax1.yaxis.set_major_locator(MultipleLocator(0.25))
#ax1.yaxis.set_minor_locator(AutoMinorLocator(10))
#ax1.grid(which='major', color='#CCCCCC', linestyle='--')
#ax1.grid(which='minor', color='#CCCCCC', linestyle=':')
plt.show()
