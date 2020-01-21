# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 13:40:50 2020

@author: PeterParker
"""
import matplotlib.pyplot as plt
import numpy as np

it = [i*20 for i in range(16)]
loss = [0, 4.34, 4.48, 4.37, 4.46, 4.52, 4.59, 4.52, 4.35, 4.06, 3.68, 3.18, 2.54, 1.59, 0.02, 0]

plt.figure()
plt.plot(it,loss)
plt.title("Mean Loss Percentage of Useable Energy(%)")
plt.xlabel("Percentage of Annual Average Power (kW)")
plt.ylabel("Loss Percentage of Useable Energy (%)")
plt.savefig("Orkney_loss_IT.pdf")