# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 09:07:42 2020

@author: PeterParker
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("T1.csv")

# want to take the 10 minute power data and interpolate into 1-minute data

# normalising data into fractional values of total rated power

power = df["LV ActivePower (kW)"]/df["LV ActivePower (kW)"].max()

power = power.values

interpolated = []

# if 30 minute data change 10--> 30
# energy should remain unaffected

for i in range(len(power)-1):
    for j in range(10):
        if 10 > j > 0:
            a = power[i] + j*(power[i+1]-power[i])/10 + np.random.normal(loc=0,scale=0.05)
        else:
            a = power[i] + j*(power[i+1]-power[i])/10
        if a > 0:
            if 1 > a:
                interpolated.append(a)
            else:
                interpolated.append(1)
        else:
            interpolated.append(0)
    

power = power[0:3]
interpolated = interpolated[0:21]

plt.figure()
plt.plot(np.linspace(0, len(interpolated),num=len(interpolated),endpoint=False), interpolated)
#plt.figure()
plt.scatter(np.linspace(0, 10*len(power),num=len(power),endpoint=False), power)
plt.show()
