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
Mx = 11955.9375
T = 1.62981451e-09
I_xx = 0.008778750299678163
I_yy = 0.11279647006253683
y_f = R-h_f #y-loc of floor if origin if circle center
gamma_f = np.arcsin(y_f/R) #angle between x-axis and floor
theta_f = np.pi - 2*gamma_f #angle of sector with floor
A_II = (R**2/2)*(theta_f - np.sin(theta_f)) # Area Cell II(q1_s,q2_s, q1_t, q2_t , sigma_b, t_sk, t_f)
A_I = (np.pi*R**2) - A_II #Area Cell I


b = AreaBoom(PositionofBooms(100,L-1,Forces,1,1)[0],L-1,1,1,PositionofBooms(100,L-1,Forces,1,1)[1])
a = PositionofBooms(100,L-1,Forces,1,1)

c = thetas1,thetas2,s1,s2,B1,B2,pos1,pos2 = tors.celldivision(a,b,gamma_f)
'''
#Deflection due to Shear
def shearflowsb(S_x,S_y, I_xx, I_yy, A_I, A_II, areaofbooms, positionsofbooms, t_sk, t_f, y_f,gamma_f):
    
    Calclulates the shear flows due to shear force
    :param S_x: shear flow
    :param I_yy: moment of inertia
    :param A_I: area cell I
    :param A_II: area cell II
    :param areaofbooms: output of definition
    :param positionsofbooms: output of definition
    :param t_sk: thickness skin
    :param t_f: thickness floor
    :param y_f: distance from orgigin to floor
    :return: delfetion, shear flow in cell 1 and 2
    

    #transformations
    thetas1, thetas2, s1, s2, B1, B2, pos1, pos2 = tors.celldivision(positionsofbooms, areaofbooms, gamma_f)
    thetas = np.append(thetas1,thetas2)

    #base shear
    pos1 = np.flip(pos1, axis = 0)
    pos2 = np.flip(pos2, axis=0)
    qb1 = np.array([0])
    qb2 = np.array([0])
    Kx = S_x/I_yy
    Ky = S_y/I_xx
    for i in range(len(pos1[:, 1])):
        qx = Kx * B1[i] * pos1[i][0]
        qy = Ky * B1[i] * pos1[i][1]
        q = -qx -qy + qb1[i]
        qb1 = np.append(qb1, q)
    qb1 = np.delete(qb1, 1)
    for i in range(len(pos2[:, 1])):
        qx = Kx * B2[i] * pos2[i][0]
        qy = Ky * B2[i] * pos2[i][1]
        q = qx + qy + qb2[i]
        qb2 = np.append(qb2, q)
    qb2 = np.delete(qb2, 1)
    qb = np.append(qb1[:-3], qb2[:-3])

    qb = np.append(qb, qb2[-3:]) #last 3 are floor

    #Moment around origin
    moment = 0
    thetas = np.insert(thetas, 0, 0)
    for i in range(len(thetas)):
        dx = -(R-(R*np.cos(thetas[i]-thetas[i-1])))
        dy = R*np.sin(thetas[i]-thetas[i-1])
        x_arm = R*np.cos(thetas[i])
        y_arm = R*np.sin(thetas[i])
        moment += (x_arm*dy + y_arm*dx)*qb[i]

    moment_floor = y_f*sum(qb[:3])
    moment += moment_floor
    #deflections



    ds_list= []
    totshear = 0
    thetas1 = np.insert(thetas1, 0, 0)
    for i in range(len(thetas1)):
        ds = R*(thetas1[i] - thetas1[i-1])/t_sk
        ds_list.append(ds)
        totshear += qb1[i]*ds
    ds_floor = 3.96/t_f
    floorcont = 1.98/t_f*(sum(qb1[-2:]))

    firstcoeff_1 = 1/(2*A_I)*(totshear + floorcont)
    q01_1 = 1/(2*A_I)*(sum(ds_list)+ ds_floor)
    q02_1 = -1/(2*A_I)*ds_floor
    ds_list2 = []
    thetas2 = np.insert(thetas2, 0, 0)
    for i in range(len(thetas2)):
        ds = R*(thetas2[i] - thetas2[i-1])/t_sk
        ds_list2.append(ds)
        totshear += qb2[i]*ds
    floorcont = 1.98/t_f * (sum(qb2[-2:]))
    firstcoeff_2 = 1/(2*A_II)*(totshear + floorcont)
    q02_2 = 1/(2*A_II)*(sum(ds_list)+ ds_floor)
    q01_2 = -1/(2*A_II)*ds_floor


    #Solving the Equations

    M = np.array([[2*A_I, 2*A_II, 0],
                 [q01_1, q02_1, firstcoeff_1],
                 [q01_2, q02_2, firstcoeff_2]])

    M1 = np.array([moment, 0, 0])

    q01, q02, delta_S = np.linalg.solve(M,M1)

    q1 = qb1 - q01
    q2 = qb2 - q02

    return delta_S, q1, q2






d = shearflowsb(Sx,Sy, I_xx, I_yy, A_I, A_II, b, a, t_s, t_f, y_f,gamma_f)
'''
std_lst = []
x = np.arange(10,2000,10)
for i in x:
    b = AreaBoom(PositionofBooms(i,L-1,Forces,1,1)[0],L-1,1,1,PositionofBooms(i,L-1,Forces,1,1)[1])
    a = PositionofBooms(i,L-1,Forces,1,1)

    c = thetas1,thetas2,s1,s2,B1,B2,pos1,pos2 = tors.celldivision(a,b,gamma_f)
    e = delta_S, q1_s, q2_s = tors. shearflowsb(Sx,Sy, I_xx, I_yy, A_I, A_II, b, a, t_s, t_f, y_f,gamma_f)

    f = delta_T,q1_t,q2_t = tors.deflect_T(T,A_I, A_II, a, b, t_s, t_f, gamma_f)
    j = tors.J(1,f[0])
    sigma_b = tors.simga_b(Mx,0, I_xx,I_yy,a, b, gamma_f)
    vonMises = tors.vonMises(q1_s,q2_s, q1_t, q2_t , sigma_b, t_s, t_f)

    std = np.mean(vonMises)/10
    std_lst.append(std)

plt.plot(x, std_lst)
plt.xlabel('Number of Booms')
plt.ylabel('Mean of Von Mises[Pa]')
plt.title('Convergence test of Von Mises')
plt.grid()

