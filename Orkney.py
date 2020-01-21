# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 10:22:24 2020

@author: PeterParker
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("10min 2019 export.xls")

load = 800  # kW

power = df["Power (Ø) [kW]"].values
power_max = df["Power (max) [kW]"].values
power_min = df["Power (min) [kW]"].values

time_period = 10

expected_power = []

for i in range(len(power)):
    if load >= power[i]:
        expected_power.append(power[i])
    else:
        expected_power.append(load)

lossy = []

# this is eating up memory SO am doing on excel --> diagnose why later

"""
for i in range(len(power)):
    if load >= power[i]:
        loss_mag = power_max - load
        
        # need to avoid dividing by 0
        if power_min[i]+power_max[i] < 0.01:
            loss = 0
        else:
            time_loss = time_period*((power[i]-power_min[i])/(power_min[i]+power_max[i]))
            loss = loss_mag*time_loss
    else:
        if power_min[i] < load:
            loss_mag = load - power_min
            time_loss = time_period - time_period*((power[i]-power_min[i])/(power_min[i]+power_max[i]))
            loss = loss_mag*time_loss
        else:
            loss = 0
    lossy.append(loss)

"""