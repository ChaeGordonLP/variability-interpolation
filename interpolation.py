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

sigma = 0.03

# want to take the 10 minute power data and interpolate into 1-minute data

# normalising data into fractional values of total rated power

power = df["LV ActivePower (kW)"]/df["LV ActivePower (kW)"].max()

power = power.values

interpolated = []

# if 30 minute data change 10--> 30
# energy should remain unaffected

# not linearly interpolating j*(power[i+1]-power[i])/10 +
# beacause its a sumulative average
# + j*(power[i+1]-power[i])/10

for i in range(len(power)-9):
    for j in range(10):
        if 10 > j > 0:
            # have it so random fluctuation is centred on previous point
            a = power[i+j] + np.random.normal(loc=0,scale=sigma)
        else:
            a = power[i] 
        if a > 0:
            if 1 > a:
                interpolated.append(a)
            else:
                interpolated.append(1)
        else:
            interpolated.append(0)
    

power_g = power[0:3]
interpolated_g = interpolated[0:21]

plt.figure()
plt.plot(np.linspace(0, len(interpolated_g),num=len(interpolated_g),endpoint=False), interpolated_g)
#plt.figure()
plt.scatter(np.linspace(0, 10*len(power_g),num=len(power_g),endpoint=False), power_g)
plt.show()

# checking energy conservation (want a plot!)
# energy

energy_interpolated = sum(interpolated)*(1/60)*df["LV ActivePower (kW)"].max()  # kWh
energy_data = (1/6)*sum(power)*df["LV ActivePower (kW)"].max()  # kWh

print((energy_interpolated-energy_data)/(np.average(power)*df["LV ActivePower (kW)"].max()))

# 44 hours in 365 days

# print(100*(2/365))  # 0.54%

# Want E cons. as a function of time

energy_t_interpolated = []
energy_t_data = []

# want to count loss