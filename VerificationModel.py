import math
import numpy as np
import matplotlib.pyplot as plt

#Inputs from Description Assignments
L = 30 #[m]
L_f1 = 4 #[m]
L_f2 = 12.5 #[m]
L_f3 = 5.2 #[m]
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

#Computing q and S_x taking into account the safety factor
safetyfactor = 1.5
q = W*3*9.81*safetyfactor/L
S_x = S_x*safetyfactor

def step(location,power):
    if location>0 and power==0:
        return 1
    elif location>0 and power>0:
        return location**power
    else:
        return 0

def Case1():
    F_yR = q * L / L_f2 * (L / 2 - L_f1)
    F_y1 = q * L * (1 - 1 / L_f2 * (L / 2 - L_f1))
    return F_yR,F_y1

def ShearYCase1(zlocation,F_yR,F_y1):
    Sheary = -q*zlocation*step(zlocation,0) + F_yR*step(zlocation-L+L_f1+L_f2,0) + F_y1*step(zlocation-L+L_f1,0)
    return Sheary

def MomentXCase1(zlocation,F_yR,F_y1):
    Momentx =  -q*zlocation/2*step(zlocation,1) + F_yR*step(zlocation-L+L_f1+L_f2,1) + F_y1*step(zlocation-L+L_f1,1)
    return -Momentx

def Case2():
    F_xr = S_x*(L-L_f1)/L_f2
    F_x1 = S_x*(1-(L-L_f1)/L_f2)
    return F_xr,F_x1

def ShearXCase2(zlocation,F_xr,F_x1):
    Shearx = S_x*step(zlocation,0)-F_xr*step(zlocation-L+L_f1+L_f2,0)-F_x1*step(zlocation-L+L_f1,0)
    return Shearx

def MomentYCase2(zlocation,F_xr,F_x1):
    Momenty = S_x*step(zlocation,1)-F_xr*step(zlocation-L+L_f1+L_f2,1)-F_x1*step(zlocation-L+L_f1,1)
    return Momenty

def TorqueCase2(zlocation):
    Torque = -S_x*(1-(L-L_f1)/L_f2)*(d_lg+R)*(step(zlocation-L+L_f1+L_f2,0)-step(zlocation-L+L_f1,0))
    return Torque

def TorqueCase3(zlocation):
    Torque = S_x*(d_ytail-R)*(step(zlocation,0)-step(zlocation-L+L_f1+L_f2,0))
    return Torque

def ShearXCase4(zlocation):
    ShearX = S_x*d_ztail/L_f2*(step(zlocation-L+L_f1+L_f2,0)-step(zlocation-L+L_f1,0))
    return ShearX

def MomentYCase4(zlocation):
    MomentY = S_x*d_ztail*(step(zlocation,0)-step(zlocation-L+L_f1,0))-S_x*d_ztail/L_f2*(zlocation-L+L_f1+L_f2)*(step(zlocation-L+L_f1+L_f2,0)-step(zlocation-L+L_f1,0))
    return MomentY

def TorqueCase4(zlocation):
    Torque = S_x*d_ztail/L_f2*(d_lg+R)*(step(zlocation-L+L_f1+L_f2,0)-step(zlocation-L+L_f1,0))
    return Torque



############################################################
##########FUNCTIONS FOR VERIFICATION########################
def MomentX_Verification(zlocation,Case1,Case2):
    return MomentXCase1(zlocation,Case1[0],Case1[1])

def MomentY_Verfication(zlocation,Case1,Case2):
    return MomentYCase2(zlocation,Case2[0],Case2[1])+MomentYCase4(zlocation)

def Torque_Verfication(zlocation,Case1,Case2):
    return TorqueCase2(zlocation)+TorqueCase3(zlocation)+TorqueCase4(zlocation)

def J_Verification():
     J=np.pi*2*t_s*R**3+2*np.sqrt(R**2-(R-h_f)**2)*t_f**3*1/3
     return J

for i in np.linspace(0,L,100):
      plt.plot(-i,Torque_Verfication(i,Case1(),Case2()),'bo')
plt.show()
