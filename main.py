import Geometry
import numpy as np
import Reactions as reac
import Torsional_Stiffness as tors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

L = 30 #[m]
Lf1 = 4 #[m]
Lf2 = 12.5 #[m]
Lf3 = 5.2 #[m]
R = 2 #[m]
d_lg = 1.8 #[m]
d_ztail = 2.8 #[m]
d_ytail = 5 #[m]
S_x = 1.7*10**(5) #[N]
W = 65000 #[kg]
n_s = 36
h_f = 1.8 #[m]
t_s = 0.003 #[m]
t_f = 0.02 #[m]
t_st = 0.0012 #[m]
h_st = 0.015 #[m]
w_st = 0.02 #[m]

fig = plt.figure()
ax = fig.gca(projection='3d')

y_f = R-h_f #y-loc of floor if origin if circle center
gamma_f = np.arcsin(y_f/R) #angle between x-axis and floor
theta_f = np.pi - 2*gamma_f #angle of sector with floor
A_II = (R**2/2)*(theta_f - np.sin(theta_f)) # Area Cell II
A_I = (np.pi*R**2) - A_II #Area Cell I
w_f = Geometry.floor_width(R, h_f)
stringer_area = t_st*(h_st + w_st)

#Computing q and S_x taking into account the safety factor
safetyfactor = 1.5
q = W*3*9.81*safetyfactor/L
S_x = S_x*safetyfactor

#Calculating Geometrical Properties
#Geometry.idealization(R, n_s, t_st, h_st, w_st, t_f, h_f, t_s)
x_bar, y_bar = Geometry.centroid(R, h_f, t_f, t_s, n_s, t_st, h_st, w_st)
floor_Ixx, fuselage_Ixx, stringer_Ixx = Geometry.MOIxx(x_bar, y_bar, stringer_area, R, h_f, t_f, t_s, n_s, t_st, h_st, w_st, w_f)
floor_Iyy, fuselage_Iyy, stringer_Iyy = Geometry.MOIyy(x_bar, y_bar, stringer_area, R, h_f, t_f, t_s, n_s, t_st, h_st, w_st, w_f)

Ixx_total = floor_Ixx+fuselage_Ixx+stringer_Ixx
Iyy_total = floor_Iyy+fuselage_Iyy+stringer_Iyy
print('h',Iyy_total)

Forces = reac.ReactionsFunction(L,Lf1,Lf2,Lf3,d_lg,d_ztail,d_ytail,S_x,q)

z_distance = 0.5
number_booms = 500

position_x = []
position_y = []
position_z = []
vonMises_list = []

for zlocation in np.arange(z_distance,L,z_distance):
    position_of_booms_total = booms_angle,booms_distance,booms_position = reac.PositionofBooms(number_booms,zlocation,Forces,Ixx_total,Iyy_total)
    booms_area = reac.AreaBoom(booms_angle,zlocation,Ixx_total,Iyy_total,booms_distance)
    delta_T,q1,q2 = tors.deflect_T(1, A_I, A_II, position_of_booms_total, booms_area, t_s, t_f, gamma_f)
    J = tors.J(1,delta_T)
    
    Mx = reac.Momentx(zlocation,Forces)
    Sy = reac.Sheary(zlocation,Forces)
    My = reac.Momenty(zlocation,Forces)
    Sx = reac.Shearx(zlocation,Forces)
    T = reac.Torque(zlocation,Forces)

    #Shear
    delta_S, q1_s, q2_s = tors.shearflowsb(Sx, Sy, Ixx_total, Iyy_total, A_I, A_II, booms_area, position_of_booms_total, t_s, t_f, y_f, gamma_f)
    delta_Tf, q1_T, q2_T = tors.deflect_T(T, A_I, A_II, position_of_booms_total, booms_area, t_s, t_f, gamma_f)
    sigma_b = tors.simga_b(Mx, My, Ixx_total, Iyy_total, position_of_booms_total, booms_area, gamma_f)
    vonMises = tors.vonMises(q1_s,q2_s, q1_T, q2_T , sigma_b, t_s, t_f) #tors.vonMises(q1_s,q2_s, q1_T, q2_T , sigma_b, t_s, t_f)

    for booms in range(len(booms_position)):
        position_x.append(booms_position[booms][0])
        position_y.append(booms_position[booms][1])
        position_z.append(zlocation)
        vonMises_list.append(vonMises[booms])

surf = ax.scatter(position_x, position_y, position_z, c=vonMises_list)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()


