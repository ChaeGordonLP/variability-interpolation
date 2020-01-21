# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:29:49 2020

@author: PeterParker
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sigma = 0.03

df_2 = 2*pd.read_excel("Gigha_data_30_min_2y.xlsx").values

power = []
for i in range(len(df_2)):
    for j in range(48):
        power.append(df_2[i,j+2])
        

data = pd.DataFrame(data=power, columns=["Average Power/ kW"])

data.to_csv("gigha_1y_power_data.csv")

power = np.array(power)

print(np.mean(power))

print(np.std(power))

print(np.std(power) + np.mean(power))

plt.figure()

g = sns.distplot(power, kde=True)
g.set(xlabel="x : Power", ylabel="P(x) : Probability Density", title="Dec 2015--> Dec 2019")

"""Want to write a code that applies the methodology to the data then 
aggregates it into monthly values"""

"""method simpler than the calculation done in 1-min methodology as we can 
literally just add the variability and then count the loss

could also calculate the loss function for comparison & see how it compares, 
validate self consistency"""

"""
# v1.1

def weibull(x,k,a):
    if x >= 0:
        b = (k/a)*(x/a)**(k-1)
        c = np.exp(-1*(x/a)**k)
        return b*c
    else:
        return 0
    
# now want to fit this to the transition matrix for each row of matrix
# then save the params for use later
"""

# want to take the 30 minute power data and interpolate into 1-minute data

# normalising data into fractional values of total rated power

power_n = power/max(power)

interpolated = []

for i in range(len(power_n)-1):
    for j in range(30):
        if 30 > j > 0:
            if power_n[i] < sigma:
                a = power_n[i]
            else:
                a = power_n[i] + np.random.normal(loc=0,scale=sigma)
        else:
            a = power_n[i] 
        if a > 0:
            if 1 > a:
                interpolated.append(a)
            else:
                interpolated.append(1)
        else:
            interpolated.append(0)
    

# sense check

plt.figure()
plt.plot(np.linspace(0, len(interpolated[0:21]), num=len(interpolated[0:21]), endpoint=False), interpolated[0:21])
#plt.figure()
plt.scatter(np.linspace(0, 10*len(power_n[0:3]), num=len(power_n[0:3]), endpoint=False), power_n[0:3])
plt.title("Sense Check")
plt.show()

loss = []

"""need to define the IT sizing, might be best to do this by optimising it as
a functional parameter? For moment select the sizing we actually have 200kW"""

it_load_n = 172.2/max(power)

for i in range(len(interpolated)):
    if interpolated[i] > it_load_n:
        lossy = interpolated[i] - it_load_n
        loss.append(lossy)
    else:
        loss.append(0)
        
use_energy = (1/60)*max(power)*(np.array(interpolated) - np.array(loss)) # kWh (1 minute=1/60th of an hour)
loss_load_factor = 60*np.average(use_energy)/max(power)

it_utilisation = 100*loss_load_factor/it_load_n

# now want to aggregate the data

# now want to account for "leap" day effect -- interpolated data is in minutes!
# this gets you eleven months

# int(len(use_energy)/(30*48*(365/12))) --> gives 11 :/ so change to just range(12)

useable_energy_agg = [sum(use_energy[i*int(30*48*(365/12)):i*int(30*48*(365/12))+int(30*48*(365/12))]) for i in range(24)]
data_agg = pd.DataFrame(data=useable_energy_agg, columns=["Aggregated Monthly Power/ kWh"])

data_agg.to_csv("agg_gigha_2y_power_data.csv")
