# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:17:46 2020

@author: Chae Gordon
"""
"""
The aim of this code is to calculate the probable value for loss occuring from
aggregation onto a month scale.

I think the thing to do to save on computing time is initially calculate the
loss due to aggregation compared with 30 min data --> then apply the 14% from
previous analysis.

Then can look to interpolate entire months (longer compute time)
"""

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

throttle_a = []
loss_a = []
energy_vio_a = []

sigma = 0.03  

# 30 min period

month = 48*(365/12)
year = 48*365
p_to_E_conv = 1/2

df_2 = (1/p_to_E_conv)*pd.read_excel("Gigha_data_30_min.xlsx").values

# transform 48 30 min rows into a time series

power = []
for i in range(len(df_2)):
    for j in range(48):
        power.append(df_2[i,j+2])
        

df = pd.DataFrame(data=power, columns=["Average Power/ kW"])

power_split_m = np.array_split(df.values, math.ceil(len(df)/month)) # split into months

power_agg_m = np.array([sum(i) for i in power_split_m]) # aggregate the months

"""Want to calculate utilisation from this & from the agg. value and compare"""

# need list comps like this --> for it to work
test_logic = [i if i <= np.average(power_agg_m) else np.average(power_agg_m) for i in power_agg_m]


agg_useable_energy = sum([i if i <= np.average(power_agg_m) else np.average(power_agg_m) for i in power_agg_m])
max_useable_energy = (len(power_agg_m)*np.average(power_agg_m))
agg_utilisation = agg_useable_energy/max_useable_energy

# the loss is high but this is partly a sizing issue, can get to ca. 21% error with 1.5 times sizing
# going to need to run sizing algorithm


acc_useable_energy = sum([i if i <= 1.5*np.average(power_agg_m)/month else 1.5*np.average(power_agg_m)/month for i in df.values])
acc_utilisation = acc_useable_energy/max_useable_energy

util_error = acc_utilisation - agg_utilisation
total_agg_spill = abs(util_error)+(1-abs(util_error))*0.14
print("util error", util_error)

print("total spill then",total_agg_spill)

# avoiding the fact that don't have all 5 years use [] in the arguments

"""
# rounds years up

counter = [math.ceil(len(df)/year) -1  if math.ceil(len(df)/year) > 1 else 0][0]

listy = [(i+1)*year for i in range(counter)]

power_split_y = np.array_split(df.values, listy) # split into years

power_agg_y = np.array([sum(i) for i in power_split_y]) # aggregate into years

# only inlcuding complete years

# p_to_E_conv to convert power to energy (kWh)
if counter == 0:
    yearly_figures = (p_to_E_conv)*power_agg_y[:]
    monthly_figures = (p_to_E_conv)*power_agg_m[:]
else:
    yearly_figures = (p_to_E_conv)*power_agg_y[:counter]
    monthly_figures = (p_to_E_conv)*power_agg_m[:counter*12]
    
    
# want to take the 30 minute power data and interpolate into 1-minute data
    
# normalising data into fractional values of total rated power
    
power = df["Average Power/ kW"]
    
max_power = df["Average Power/ kW"].max() 

power_split = np.array_split(power.values, int(len(power)/24)) # split into 12 hrs

power_agg = np.array([sum(i) for i in power_split]) # aggregate the 12 hours

sigma_12 = np.std(power_agg/max(power_agg))

power = df["Average Power/ kW"]/max_power

power = power.values

print(sigma_12)

loss_at_load_factor = 0

for i in range(1):
    throttle = 1  # i*(0.1) # just want to analyse the case of box @ l.f
        
    interpolated = []
    
    load = throttle*np.average(power)
    
    # if 30 minute data change 10--> 30
    # energy should remain unaffected
                    
    lossy = []
    avg_line = []
    
    for i in range(len(power)-29):
        for j in range(30):
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
    energy_data = (1/2)*sum(power)*max_power  # kWh
    
    print("lost Energy: {0:.2f} %".format(100*lost_E/energy_data))
    print("Energy Conservation Violated by {0:.2f} %".format(100*(energy_interpolated-energy_data)/(energy_data)))
    
    throttle_a.append(throttle)
    loss_a.append(100*lost_E/energy_data)
    energy_vio_a.append(100*(energy_interpolated-energy_data)/(energy_data))
    
    if throttle == 1:
        power_g = power[0:3]
        interpolated_g = interpolated[0:61]  # check this
        avg_line_g = avg_line[0:61]
        
        loss_at_load_factor = 100*lost_E/energy_data  # loss when IT sized at average power
        
        plt.figure()
        plt.title("Interpolation of 1-minute Points")
        plt.plot(np.linspace(0, len(interpolated_g),num=len(interpolated_g),endpoint=False), interpolated_g, label="interpolated points")
        plt.plot(np.linspace(0, len(interpolated_g),num=len(interpolated_g),endpoint=False), avg_line_g, label="cumulative average power points")
        plt.scatter(np.linspace(0, 30*len(power_g),num=len(power_g),endpoint=False), power_g, label="inferred average power from data")
        plt.legend()
        plt.xlabel("Time Elapsed (min)")
        plt.ylabel("Power Fraction of Rated Capacity")
        plt.savefig("interpolation_example.pdf")
        plt.show()
        
        energy_t_interpolated = np.log((1/60)*np.cumsum(interpolated)*max_power)
        energy_t_data = np.log((1/2)*np.cumsum(power)*max_power )
        
        plt.figure()
        plt.title("Log of Cumulative Energy for Interpolated and Real Data")
        plt.ylabel(r"ln( Energy/[kWh] )")
        plt.xlabel("Time Elapsed (min)")
        plt.plot(np.linspace(0, len(energy_t_interpolated),num=len(energy_t_interpolated),endpoint=False), energy_t_interpolated)
        plt.plot(np.linspace(0, 30*len(energy_t_data),num=len(energy_t_data),endpoint=False), energy_t_data)
        plt.savefig("energy_cons.pdf")
    else:
        pass

# zero loss when IT = 0

loss_a[0]=0

plt.figure()
plt.plot(throttle_a,loss_a)
plt.title("Percentage Energy Loss as a funciton of IT Sizing")
plt.ylabel(r"Percentage Energy Loss (%)")
plt.xlabel("IT sizing as a Fraction of Annual Average Power")
plt.savefig("loss_load.pdf")
"""

