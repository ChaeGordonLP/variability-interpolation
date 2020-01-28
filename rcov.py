# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:03:47 2020

@author: chaeg
"""

import numpy as np
import pandas as pd
import math
from scipy.stats import median_absolute_deviation
# import matplotlib.pyplot as plt

"""
Method is:
    1) turn to time series
    2) split into months & years separately
    3) cumulatively sum to aggregate
    4) calculate RCOV = m.a.d/median
"""

month = 48*(365/12)
year = 48*365

df_2 = 2*pd.read_excel("Gigha_data_30_min.xlsx").values

# transform 48 30 min rows into a time series

power = []
for i in range(len(df_2)):
    for j in range(48):
        power.append(df_2[i,j+2])

df = pd.DataFrame(data=power, columns=["Average Power/ kW"])

power_split_m = np.array_split(df.values, len(df)/month) # split into months

power_agg_m = np.array([sum(i) for i in power_split_m]) # aggregate the months

# avoiding the fact that don't have all 5 years use [] in the arguments

# rounds years up

counter = math.ceil(len(df)/year) - 1

listy = [(i+1)*year for i in range(counter)]

power_split_y = np.array_split(df.values, listy) # split into years

power_agg_y = np.array([sum(i) for i in power_split_y]) # aggregate into years

# only inlcuding complete years

# divide by 2 to convert power to energy (kWh)

yearly_figures = 0.5*power_agg_y[:counter]
monthly_figures = 0.5*power_agg_m[:counter*12]

# RCOV -- fractional

rcov_y = median_absolute_deviation(yearly_figures)/np.median(yearly_figures)

print("Yearly RCOV: {0:.2f} %".format(100*float(rcov_y)))

rcov_m = median_absolute_deviation(monthly_figures)/np.median(monthly_figures)

print("Monthly RCOV: {0:.2f} %".format(100*float(rcov_m)))

median_year = np.median(yearly_figures)

# print(median_year)  # closest to last year

sample_year = monthly_figures[-12:]
sample_year_test = monthly_figures[36:48]

# print(sample_year==sample_year_test)  # works

print(sample_year)
