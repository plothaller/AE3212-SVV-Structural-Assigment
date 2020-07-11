import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import operator

with open ('Validation_load_case.txt') as val_data:
    header = 15
    data_points = 14760
    lines =  val_data.readlines()[header:header+data_points]
    ID = []
    x = []
    y = []
    z = []
    vm = []
    for line in lines:
        line = line.split()
        ID.append(float(line[0]))
        x.append(float(line[2]))
        y.append(float(line[3]))
        z.append(float(line[4]))
        vm.append(float(line[5]))
    ID = np.array(ID)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    vm = np.array(vm)
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(x, y, z, color=vm)
    i = 0
    x_dict = dict()
    while i <= (len(z)-1):
        x_dict[ID[i]]=x[i]
        i+=1
    
    sorted_d = dict(sorted(x_dict.items(), key=operator.itemgetter(1)))

with open ('Validation_load_case.txt') as val_data:
    header2 = header+data_points+10
    data_points2 = 14760
    lines =  val_data.readlines()[header2:header2+data_points2]
    
    ID2 = []
    x2 = []
    y2 = []
    z2 = []
    vm2 = []
    for line in lines:
        line = line.split()
        ID2.append(float(line[0]))
        x2.append(float(line[2]))
        y2.append(float(line[3]))
        z2.append(float(line[4]))
        vm2.append(float(line[5]))
    x2 = np.array(x2)
    y2 = np.array(y2)
    z2 = np.array(z2)
    vm2 = np.array(vm2)

    
    sorted_d = dict(sorted(x_dict.items(), key=operator.itemgetter(1)))
    with open("sorted_data.txt", "w") as file:
        file.write('ID      x-pos       y-pos      z-pos      vm    |    x-pos       y-pos      z-pos      vm    |   vm_average')
        file.write("\n")
        for i, k in sorted_d.items():
            file.write(str(int(i))+'  '+str(k)+'  '+str(y[int(i)-1])+'  '+str(z[int(i)-1])+'  '+str(vm[int(i)-1])+' | ' +str(x2[int(i)-1])+'  '+str(y2[int(i)-1])+'  '+str(z2[int(i)-1])+'  '+str(vm2[int(i)-1]) + ' | ' + str((vm2[int(i)-1]+vm[int(i)-1])/2))
            file.write("\n")

     
    file.close()

    







    
