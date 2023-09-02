import pandas as pd
from IPython.display import display,Math,Latex,Markdown
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

df = pd.read_csv("model.csv", sep="\t")
display(df.head(6))

fig = plt.figure(figsize=(32,4))
ax1 = fig.add_subplot(1,1,1)

t = df['time']*1000
VB1, VRE, VRG, VP = df['V(vl)'], df['V(reset)'], df['V(Reset,R-PI_GND)'], df['V(pulse)']
ax1.plot(t, VRE, 'g-', label="V(reset)")
ax1.legend()
ax1.set_ylim(-350, 350)
ax1.set_xlabel("t (ms)")
ax1.set_ylabel("V(reset)")

ax2 = ax1.twinx()
ax2.plot(t, VRG, 'r-', label="V(Reset,R-PI_GND)")
ax2.legend()
ax2.set_ylim(-1, 5)
ax2.set_ylabel("V(Reset,R-PI_GND)")
ax2.xaxis.set_major_locator(MultipleLocator(100))
ax2.xaxis.set_minor_locator(AutoMinorLocator(10))
ax2.yaxis.set_major_locator(MultipleLocator(1))
ax2.yaxis.set_minor_locator(AutoMinorLocator(10))
ax2.grid(which='major', color='#CCCCCC', linestyle='--')
ax2.grid(which='minor', color='#CCCCCC', linestyle=':')

ax3 = ax1.twinx()
ax3.plot(t, VP, 'b-', label="V(pulse)")
ax3.legend()
ax3.set_ylim(-2, 4)
ax3.tick_params(right=False, labelright=False)

plt.show()
