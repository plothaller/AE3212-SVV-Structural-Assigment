import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import operator

with open ('sorted_data.txt') as val_data:
    header = 1
    data_points = 14760
    lines =  val_data.readlines()[header:header+data_points]
    ID = []
    x = []
    y = []
    z = []
    vmavg = []
    for line in lines:
        line = line.split()
        ID.append(float(line[0]))
        x.append(float(line[1]))
        y.append(float(line[2]))
        z.append(float(line[3]))
        vmavg.append(float(line[11]))
    minimum = min(vmavg)
    maximum = max(vmavg)
    idx_min = vmavg.index(minimum)
    idx_max = vmavg.index(maximum)
    x_min   = x[idx_min]
    y_min   = y[idx_min]
    z_min   = z[idx_min]
    x_max   = x[idx_max]
    y_max   = y[idx_max]
    z_max   = z[idx_max]
    print('minimum vm: {}, location {},{},{}'.format(minimum,x_min,y_min,z_min))
    print('maximum vm: {}, location {},{},{}'.format(maximum,x_max,y_max,z_max))
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #ax.plot(x, y, z, zdir = 'z', c= 'r')
    ax.scatter(x, y, z, c = vmavg)
    plt.axis('off')
    plt.show()