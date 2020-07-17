import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import operator
import math
from main import position_x, position_y, position_z, vonMises_list

R = 2000

x_num = []
y_num = []
z_num = []
vm_num = []
for val in position_x:
    new_val = val*10**3
    x_num.append(new_val)
for val in position_y:
    new_val = val*10**3
    y_num.append(new_val)
for val in position_z:
    new_val = val*10**3
    z_num.append(new_val)
for val in vonMises_list:
    new_val = val*10**(-6)
    vm_num.append(new_val)
    

boom_locs = [(R,0),(0, R),(-R,0),(0,-R),(0,0)]

def closest(i,xlst,ylst):
    min = 500

    for idx,j in enumerate(xlst):
        diff = math.sqrt((i[0]-j)**2+(i[1]-ylst[idx])**2)
        if diff < min:
            min = diff
            k = idx
    return k

def boomline(j, m, x_lst, y_lst, z_lst, vm_lst):
    x = []
    y = []
    z = []
    vm = []
    for i, k in enumerate(x_lst):
        if math.isclose(k,j,abs_tol=0.001) and math.isclose(y_lst[i],m,abs_tol=0.001):
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
    indices_x_nm = []
    for i in boom_locs:
        idx = closest(i,x,y)
        indices_x.append(idx)
        idx_nm = closest(i,x_num, y_num)
        indices_x_nm.append(idx_nm)
    
    x_final = []
    y_final = []
    z_final = []
    vm_final = []

    x_final_nm = []
    y_final_nm = []
    z_final_nm = []
    vm_final_nm = []
    

    for l in indices_x_nm:
        x_val_nm = x_num[l]
        y_val_nm = y_num[l]

        x_nm, y_nm, z_nm, vm_nm = boomline(x_val_nm, y_val_nm, x_num, y_num, z_num, vm_num)
        x_final_nm.append(x_nm)
        y_final_nm.append(y_nm)
        z_final_nm.append(z_nm)
        vm_final_nm.append(vm_nm)

    for j in indices_x:
        x_val = x[j]
        y_val = y[j]

        x_new, y_new, z_new, vm_new = boomline(x_val, y_val, x, y, z, vmavg)
        x_final.append(x_new)
        y_final.append(y_new)
        z_final.append(z_new)
        vm_final.append(vm_new)
    
    x_final1 = np.array(x_final[0])
    x_final2 = np.array(x_final[1])
    x_final3 = np.array(x_final[2])
    x_final4 = np.array(x_final[3])
    x_final5 = np.array(x_final[4])
    x_final = np.append(x_final1,x_final2)
    x_final = np.append(x_final,x_final3)
    x_final = np.append(x_final,x_final4)
    x_final = np.append(x_final,x_final5)

    y_final1 = np.array(y_final[0])
    y_final2 = np.array(y_final[1])
    y_final3 = np.array(y_final[2])
    y_final4 = np.array(y_final[3])
    y_final5 = np.array(y_final[4])
    y_final = np.append(y_final1,y_final2)
    y_final = np.append(y_final,y_final3)
    y_final = np.append(y_final,y_final4)
    y_final = np.append(y_final,y_final5)

    z_final1 = np.array(z_final[0])
    z_final2 = np.array(z_final[1])
    z_final3 = np.array(z_final[2])
    z_final4 = np.array(z_final[3])
    z_final5 = np.array(z_final[4])
    z_final = np.append(z_final1,z_final2)
    z_final = np.append(z_final,z_final3)
    z_final = np.append(z_final,z_final4)
    z_final = np.append(z_final,z_final5)
    
    vm_final1 = np.array(vm_final[0])
    vm_final2 = np.array(vm_final[1])
    vm_final3 = np.array(vm_final[2])
    vm_final4 = np.array(vm_final[3])
    vm_final5 = np.array(vm_final[4])
    vm_final = np.append(vm_final1,vm_final2)
    vm_final = np.append(vm_final,vm_final3)
    vm_final = np.append(vm_final,vm_final4)
    vm_final = np.append(vm_final,vm_final5)

    x_final1_nm = np.array(x_final_nm[0])
    x_final2_nm = np.array(x_final_nm[1])
    x_final3_nm = np.array(x_final_nm[2])
    x_final4_nm = np.array(x_final_nm[3])
    x_final5_nm = np.array(x_final_nm[4])
    x_final_nm = np.append(x_final1_nm,x_final2_nm)
    x_final_nm = np.append(x_final_nm,x_final3_nm)
    x_final_nm = np.append(x_final_nm,x_final4_nm)
    x_final_nm = np.append(x_final_nm,x_final5_nm)

    y_final1_nm = np.array(y_final_nm[0])
    y_final2_nm = np.array(y_final_nm[1])
    y_final3_nm = np.array(y_final_nm[2])
    y_final4_nm = np.array(y_final_nm[3])
    y_final5_nm = np.array(y_final_nm[4])
    y_final_nm = np.append(y_final1_nm,y_final2_nm)
    y_final_nm = np.append(y_final_nm,y_final3_nm)
    y_final_nm = np.append(y_final_nm,y_final4_nm)
    y_final_nm = np.append(y_final_nm,y_final5_nm)

    z_final1_nm = np.array(z_final_nm[0])
    z_final2_nm = np.array(z_final_nm[1])
    z_final3_nm = np.array(z_final_nm[2])
    z_final4_nm = np.array(z_final_nm[3])
    z_final5_nm = np.array(z_final_nm[4])
    z_final_nm = np.append(z_final1_nm,z_final2_nm)
    z_final_nm = np.append(z_final_nm,z_final3_nm)
    z_final_nm = np.append(z_final_nm,z_final4_nm)
    z_final_nm = np.append(z_final_nm,z_final5_nm)
    

    vm_final1_nm = np.array(vm_final_nm[0])
    vm_final2_nm = np.array(vm_final_nm[1])
    vm_final2_nm = vm_final2_nm
    vm_final3_nm = np.array(vm_final_nm[2])
    vm_final3_nm = vm_final3_nm
    vm_final4_nm = np.array(vm_final_nm[3])
    vm_final4_nm = vm_final4_nm
    vm_final5_nm = np.array(vm_final_nm[4])
    vm_final_nm = np.append(vm_final1_nm,vm_final2_nm)
    vm_final_nm = np.append(vm_final_nm,vm_final3_nm)
    vm_final_nm = np.append(vm_final_nm,vm_final4_nm)
    vm_final_nm = np.append(vm_final_nm,vm_final5_nm)
    
    
    

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.scatter(x_final*10**(-3), y_final*10**(-3), z_final*10**(-3), c=vm_final)
    fig.colorbar(surf, shrink=0.5, aspect=5, label='von Mises stress [Mpa]')
    plt.show()
 

    fig, axs = plt.subplots(3,2)
    axs[0, 0].scatter((z_final1*10**(-3)), vm_final1, s=5)
    axs[0, 0].scatter((-z_final1_nm*10**(-3)), vm_final1_nm, s=5, c='orange')
    axs[0, 0].set_title('Closest boom to [R,0]')
    axs[0, 0].set_xlabel('z-location [m]')
    axs[0, 0].set_ylabel('von Mises stress [Mpa]')
    axs[0, 1].scatter((z_final2*10**(-3)), vm_final2, s=5)
    axs[0, 1].scatter((-z_final2_nm*10**(-3)), vm_final2_nm, s=5, c='orange')
    axs[0, 1].set_title('Closest boom to [0,R]')
    axs[0, 1].set_xlabel('z-location [m]')
    axs[0, 1].set_ylabel('von Mises stress [Mpa]')
    axs[1, 0].scatter((z_final3*10**(-3)), vm_final3, s=5)
    axs[1, 0].scatter((-z_final3_nm*10**(-3)), vm_final3_nm, s=5, c='orange')
    axs[1, 0].set_title('Closest boom to [-R,0]')
    axs[1, 0].set_xlabel('z-location [m]')
    axs[1, 0].set_ylabel('von Mises stress [Mpa]')
    axs[1, 1].scatter(z_final4*10**(-3), vm_final4, s=5)
    axs[1, 1].scatter(-z_final4_nm*10**(-3), vm_final4_nm, s=5, c='orange')
    axs[1, 1].set_title('Closest boom to [0,-R]')
    axs[1, 1].set_xlabel('z-location [m]')
    axs[1, 1].set_ylabel('von Mises stress [Mpa]')
    axs[2, 0].scatter((z_final5*10**(-3)), vm_final5, s=5)
    axs[2, 0].scatter((-z_final5_nm*10**(-3)), vm_final5_nm, s=5, c='orange')
    axs[2, 0].set_title('Closest boom to [0,0]')
    axs[2, 0].set_xlabel('z-location [m]')
    axs[2, 0].set_ylabel('von Mises stress [Mpa]')
    # for ax in axs.flat:
    #     ax.set(xlabel='z-location', ylabel='von Mises stress')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    # for ax in axs.flat:
    #     ax.label_outer()
    fig.delaxes(axs[2,1])
    plt.tight_layout() 
    plt.show()
    
    