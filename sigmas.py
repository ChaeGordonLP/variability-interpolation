import numpy as np
import math
import matplotlib.pyplot as plt

T = np.array(
    [[  0.9905, 0.0094, 0.0001, 0,      0,      0,      0,      0,      0,      0       ],
    [   0.0183, 0.9592, 0.0220, 0.0002, 0.0001, 0.0001, 0,      0,      0,      0       ],
    [   0.0007, 0.0247, 0.9448, 0.0295, 0.0001, 0.0000, 0,      0,      0,      0       ],
    [   0.0004, 0.0003, 0.0339, 0.9302, 0.0350, 0.0001, 0,      0,      0,      0       ],
    [   0.0004, 0.0002, 0.0002, 0.0408, 0.9151, 0.0428, 0.0004, 0.0001, 0,      0       ],
    [   0.0004, 0.0001, 0.0005, 0.0003, 0.0455, 0.9066, 0.0465, 0.0001, 0,      0       ],
    [   0.0001, 0.0004, 0.0001, 0.0003, 0.0005, 0.0465, 0.9118, 0.0399, 0.0002, 0       ],
    [   0.0004, 0,      0.0001, 0.0002, 0.0001, 0.0002, 0.0399, 0.9192, 0.0400, 0       ],
    [   0.0004, 0,      0.0003, 0.0001, 0,      0,      0.0001, 0.0431, 0.9328, 0.0231  ],
    [   0.0001, 0.0003, 0.0001, 0.0001, 0.0001, 0.0001, 0.0003, 0.0003, 0.0364, 0.9620  ]]
)

def list_of_sigmas(T, step_precision=0.1):
    """ returns a list of sigmas for each series
        if step_precision is 0.1, that means the states are 10%, 20%, 30%,..., 100% """
    sigmas_list = []
    for index, array in enumerate(T):
        x = np.linspace(0-step_precision*index, (len(T)-1)*step_precision-step_precision*index,num=len(T))
        sigmas_list.append(sigma_from_np_array(array, x))
    return sigmas_list

def sigma_from_np_array(array, x):
    """ takes an array of frequencies and another of values and returns the standard deviation assuming the mean is 0 """
    return math.sqrt(sum(array*x**2))

def plot_graphs(T):
    plt.figure()
    x = np.linspace(0, (10-1)*0.1,num=10)
    T14 = np.linalg.matrix_power(T,14)
    T29 = np.linalg.matrix_power(T,29)
    plt.plot(x, list_of_sigmas(T))
    plt.plot(x, list_of_sigmas(T14))
    plt.plot(x, list_of_sigmas(T29))
    plt.annotate(f"max sigma T = {round(max(list_of_sigmas(T)),3)}", xy=(0.1*list_of_sigmas(T).index(max(list_of_sigmas(T))),max(list_of_sigmas(T))))
    plt.annotate(f"max sigma T^14= {round(max(list_of_sigmas(T14)),3)}", xy=(0.1*list_of_sigmas(T14).index(max(list_of_sigmas(T14))),max(list_of_sigmas(T14))))
    plt.annotate(f"max sigma T^29= {round(max(list_of_sigmas(T29)),3)}", xy=(0.1*list_of_sigmas(T29).index(max(list_of_sigmas(T29))),max(list_of_sigmas(T29))))
    plt.title("sigmas")
    plt.show()