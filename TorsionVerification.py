import Torsional_Stiffness as tors
from Reactions import *
import numpy as np
import matplotlib.pyplot as plt
R = 2 #[m]
L = 30 #[m]
Lf1 = 4 #[m]
Lf2 = 12.5 #[m]
Lf3 = 5.2 #[m]
R = 2 #[m]
d_lg = 1.8 #[m]
d_ztail = 2.8 #[m]
d_ytail = 5 #[m]
W = 65000 #[kg]
n_s = 36
h_f = 1.8 #[m]
t_s = 0.003 #[m]
t_f = 0.02 #[m]
t_st = 0.0012 #[m]
h_st = 0.015 #[m]
w_st = 0.02 #[m]
Sx = 191295.0
Sy = 191295.0
I_xx = 0.008778750299678163
I_yy = 0.11279647006253683
y_f = R-h_f #y-loc of floor if origin if circle center
gamma_f = np.arcsin(y_f/R) #angle between x-axis and floor
theta_f = np.pi - 2*gamma_f #angle of sector with floor
A_II = (R**2/2)*(theta_f - np.sin(theta_f)) # Area Cell II
A_I = (np.pi*R**2) - A_II #Area Cell I


b = AreaBoom(PositionofBooms(100,L-1,Forces,1,1)[0],L-1,1,1,PositionofBooms(100,L-1,Forces,1,1)[1])
a = PositionofBooms(100,L-1,Forces,1,1)

c = thetas1,thetas2,s1,s2,B1,B2,pos1,pos2 = tors.celldivision(a,b,gamma_f)



d = tors.shearflowsb(Sx,Sy, I_xx, I_yy, A_I, A_II, b, a, t_s, t_f, y_f,gamma_f)

plt.scatter(pos1[:,0],pos1[:,1], c=d[1] , label = 'Cell I')
plt.scatter(pos2[:,0],pos2[:,1],  c=d[2], label = 'Cell II')
plt.title('Geometry with $h_f = 2$')
plt.xlabel('x coordinate [m]')
plt.ylabel('y coordinate [m]')
plt.legend()


