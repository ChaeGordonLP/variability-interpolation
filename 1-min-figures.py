# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 15:41:29 2020

@author: PeterParker
"""

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

delta = 15

t = np.linspace(0, 30, 500, endpoint=False)
#2 * np.pi * 5
plt.plot(t, 50 + 50*signal.square((0.209*t)), label="1-min Power")

# adding arrows
plt.annotate("", xy=(0, 90), xytext=(delta, 90),
             arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
plt.text(delta/2, 90, r'$a_1$',
         {'color': 'black', 'fontsize': 24, 'ha': 'center', 'va': 'center',
          'bbox': dict(boxstyle="round", fc="white", ec="black", pad=0.2)})
plt.annotate("", xy=(delta, 10), xytext=(2*delta, 10),
             arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
plt.text(3*delta/2, 10, r'$a_2$',
         {'color': 'black', 'fontsize': 24, 'ha': 'center', 'va': 'center',
          'bbox': dict(boxstyle="round", fc="white", ec="black", pad=0.2)})
plt.annotate("", xy=(0, 55), xytext=(2*delta, 55),
             arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
plt.text(delta, 55, r'$A$',
         {'color': 'black', 'fontsize': 24, 'ha': 'center', 'va': 'center',
          'bbox': dict(boxstyle="round", fc="white", ec="black", pad=0.2)})

# add p bar

plt.plot(t, len(t)*[50], label="30-min avg. Power")

# add IT size

plt.plot(t, len(t)*[60], label="max IT load")

plt.ylim(-10,110)
plt.xlim(0,30)
plt.title("Worst Case Scenario for Variability")
plt.xlabel("Time / [minutes]")
plt.ylabel("Percentage of Rated Capacity / [%]")
plt.legend()
plt.savefig("square_time.pdf")

# Now depicting the loss for upper 
plt.figure()

plt.plot(t, 50 + 50*signal.square((0.209*t)), label="1-min Power")

# adding arrows

plt.annotate("", xy=(delta, 60), xytext=(delta, 100),
             arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
plt.text(delta, 80, r'$l$',
         {'color': 'black', 'fontsize': 24, 'ha': 'center', 'va': 'center',
          'bbox': dict(boxstyle="round", fc="white", ec="black", pad=0.2)})

# add p bar

plt.plot(t, len(t)*[50], label="30-min avg. Power")

# add IT size

plt.plot(t, len(t)*[60], label="max IT load")

plt.ylim(-10,110)
plt.xlim(0,30)
plt.title("Loss if Maximum IT above or equal to 30-minute Avg.")
plt.xlabel("Time / [minutes]")
plt.ylabel("Percentage of Rated Capacity / [%]")
plt.legend()
plt.savefig("square_loss_above.pdf")

# Now depicting the loss for lower
 
plt.figure()

plt.plot(t, 65 + 35*signal.square((0.209*t)), label="1-min Power")

# adding arrows

plt.annotate("", xy=(delta, 30), xytext=(delta, 50),
             arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
plt.text(delta-1.5, 40, r'$l$',
         {'color': 'black', 'fontsize': 24, 'ha': 'center', 'va': 'center',
          'bbox': dict(boxstyle="round", fc="white", ec="black", pad=0.2)})

# add p bar

plt.plot(t, len(t)*[65], label="30-min avg. Power")

# add IT size

plt.plot(t, len(t)*[50], label="max IT load")

plt.ylim(-10,110)
plt.xlim(0,30)
plt.title("Loss if Maximum IT above or equal to 30-minute Avg.")
plt.xlabel("Time / [minutes]")
plt.ylabel("Percentage of Rated Capacity / [%]")
plt.legend()
plt.savefig("square_loss_below.pdf")