# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 09:07:42 2020

@author: PeterParker
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# TURKEY
throttle_a = []
loss_a = []
energy_vio_a = []

df = pd.read_csv("T1.csv")
    
sigma = 0.03  # 0.4 needed for 10% loss !!
    
# want to take the 10 minute power data and interpolate into 1-minute data
    
# normalising data into fractional values of total rated power
    
power = df["LV ActivePower (kW)"]/df["LV ActivePower (kW)"].max()
    
max_power = df["LV ActivePower (kW)"].max()  # 3.6 MW
    
power = power.values


for i in range(31):
    throttle = i*(0.1)
        
    interpolated = []
    
    load = throttle*np.average(power)
    
    # if 30 minute data change 10--> 30
    # energy should remain unaffected
                    
    lossy = []
    avg_line = []
    
    for i in range(len(power)-9):
        for j in range(10):
            avg_line.append(power[i])
            # have it so random fluctuation is centred on previous point
            a = power[i+j] + np.random.normal(loc=0,scale=sigma) 
            if a > 0:
                if 1 > a:
                    interpolated.append(a)
                    if power[i]>load:
                        if a < load:
                            lossy.append((load-a)*(1/60))
                        else:
                            lossy.append(0)
                    if load >= power[i]:
                        if a > load:
                            lossy.append((1/60)*(a - load))
                        else:
                            lossy.append(0)
                else:
                    a=1
                    interpolated.append(a)
                    if power[i]>load:
                        if a < load:
                            lossy.append((load-a)*(1/60))
                        else:
                            lossy.append(0)
                    if load >= power[i]:
                        if a > load:
                            lossy.append((1/60)*(a - load))
                        else:
                            lossy.append(0)
                
            else:
                interpolated.append(0)
                lossy.append(0)
    
    lost_E = sum(lossy)*max_power #  kWh
    print("lost Energy: {0:.2f} kWh".format(lost_E))
    # checking energy conservation
        
    energy_interpolated = sum(interpolated)*(1/60)*max_power  # kWh
    energy_data = (1/6)*sum(power)*max_power  # kWh
    
    print("lost Energy: {0:.2f} %".format(100*lost_E/energy_data))
    print("Energy Conservation Violated by {0:.2f} %".format(100*(energy_interpolated-energy_data)/(energy_data)))
    
    throttle_a.append(throttle)
    loss_a.append(100*lost_E/energy_data)
    energy_vio_a.append(100*(energy_interpolated-energy_data)/(energy_data))
    
    if throttle == 1:
        power_g = power[0:3]
        interpolated_g = interpolated[0:21]
        avg_line_g = avg_line[0:21]
        
        plt.figure()
        plt.title("Interpolation of 1-minute Points")
        plt.plot(np.linspace(0, len(interpolated_g),num=len(interpolated_g),endpoint=False), interpolated_g, label="interpolated points")
        plt.plot(np.linspace(0, len(interpolated_g),num=len(interpolated_g),endpoint=False), avg_line_g, label="cumulative average power points")
        plt.scatter(np.linspace(0, 10*len(power_g),num=len(power_g),endpoint=False), power_g, label="inferred average power from data")
        plt.legend()
        plt.xlabel("Time Elapsed (min)")
        plt.ylabel("Power Fraction of Rated Capacity")
        plt.savefig("interpolation_example.pdf")
        plt.show()
        
        energy_t_interpolated = np.log((1/60)*np.cumsum(interpolated)*max_power)
        energy_t_data = np.log((1/6)*np.cumsum(power)*max_power )
        
        plt.figure()
        plt.title("Cumulative Energy for Interpolated and Real Data")
        plt.ylabel(r"ln( Energy/[kWh] )")
        plt.xlabel("Time Elapsed (min)")
        plt.plot(np.linspace(0, len(energy_t_interpolated),num=len(energy_t_interpolated),endpoint=False), energy_t_interpolated)
        plt.plot(np.linspace(0, 10*len(energy_t_data),num=len(energy_t_data),endpoint=False), energy_t_data)
    else:
        pass

# zero loss when IT = 0

loss_a[0]=0

plt.figure()
plt.plot(throttle_a,loss_a)
plt.title("Percentage Energy Loss as a funciton of IT Sizing")
plt.ylabel(r"Percentage Energy Loss (%)")
plt.xlabel("IT sizing as a Fraction of Annual Average Power")

