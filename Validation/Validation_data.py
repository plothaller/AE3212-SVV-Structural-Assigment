import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import operator

with open ('Validation\sorted_data.txt') as val_data:
    header = 1
    data_points = 120
    lines =  val_data.readlines()[header:header+data_points]
    ID = []
    x = []
    y = []
    z = []
    vm = []
    for line in lines:
        line = line.split()
        ID.append(float(line[0]))
        x.append(float(line[1]))
        y.append(float(line[2]))
        z.append(float(line[3]))
        vm.append(float(line[4]))
    plt.scatter(z, vm)
    plt.show()