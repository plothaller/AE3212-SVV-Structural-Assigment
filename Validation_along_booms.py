import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import operator
import math

R = 1994


boom_locs = [(R,0),(0,R),(-R,0),(0,-R)]

def closest(i,xlst,ylst):
    min = 500

    for idx,j in enumerate(xlst):
        diff = math.sqrt((i[0]-j)**2+(i[1]-ylst[idx])**2)
        if diff < min:
            min = diff
            k = idx
    return k

def boomline(j, x_lst, y_lst, z_lst, vm_lst):
    x = []
    y = []
    z = []
    vm = []
    for i, k in enumerate(x_lst):
        if k == j:
            x.append(k)
            y.append(y_lst[i])
            z.append(z_lst[i])
            vm.append(vm_lst[i])
    return x, y, z, vm



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

    indices_x = []
    for i in boom_locs:
        idx = closest(i,x,y)
        indices_x.append(idx)
    
    x_final = []
    y_final = []
    z_final = []
    vm_final = []
    

    for j in indices_x:
        x_val = x[j]
        x_new, y_new, z_new, vm_new = boomline(x_val, x, y, z, vmavg)
        x_final.append(x_new)
        y_final.append(y_new)
        z_final.append(z_new)
        vm_final.append(vm_new)
    
    x_final1 = np.array(x_final[0])
    x_final2 = np.array(x_final[1])
    x_final3 = np.array(x_final[2])
    x_final4 = np.array(x_final[3])
    x_final = np.append(x_final1,x_final2)
    x_final = np.append(x_final,x_final3)
    x_final = np.append(x_final,x_final4)
    
    y_final1 = np.array(y_final[0])
    y_final2 = np.array(y_final[1])
    y_final3 = np.array(y_final[2])
    y_final4 = np.array(y_final[3])
    y_final = np.append(y_final1,y_final2)
    y_final = np.append(y_final,y_final3)
    y_final = np.append(y_final,y_final4)

    z_final1 = np.array(z_final[0])
    z_final2 = np.array(z_final[1])
    z_final3 = np.array(z_final[2])
    z_final4 = np.array(z_final[3])
    z_final = np.append(z_final1,z_final2)
    z_final = np.append(z_final,z_final3)
    z_final = np.append(z_final,z_final4)
    
    vm_final1 = np.array(vm_final[0])
    vm_final2 = np.array(vm_final[1])
    vm_final3 = np.array(vm_final[2])
    vm_final4 = np.array(vm_final[3])
    vm_final = np.append(vm_final1,vm_final2)
    vm_final = np.append(vm_final,vm_final3)
    vm_final = np.append(vm_final,vm_final4)
    
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #ax.plot(x, y, z, zdir = 'z', c= 'r')
    ax.scatter(x_final, y_final, z_final, c=vm_final)
    plt.axis('off')
    plt.show()


