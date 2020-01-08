# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 10:40:54 2020

@author: PeterParker
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("T1.csv")

# extract max values

# max wind speed

w_m = 14.169 # df["Wind Speed (m/s)"].max()

# max power 

p_m = df["LV ActivePower (kW)"].max()

# get fractional change in wind speed

w_s = df["Wind Speed (m/s)"]/w_m

w_1 = w_s.shift(periods=1, fill_value=0)

del_w = w_s - w_1

# get fractional change in power

p = df["LV ActivePower (kW)"]/p_m

p_1 = p.shift(periods=1, fill_value=0)

del_p = p - p_1

plt.figure()

g = sns.distplot(del_p, kde=True)
g.set(xlabel="x : Fractional Power Change", ylabel="P(x) : Probability Density", title="Turkish Scada Data")

plt.figure()

g = sns.distplot(del_w, kde=True)
g.set(xlabel="x : Fractional Wind Speed Change", ylabel="P(x) : Probability Density", title="Turkish Scada Data")

plt.figure()

plt.plot(del_w[0:144], label="Fractional Wind Speed Change")
plt.plot(del_p[0:144], label="Fractional Power Change")
plt.legend()