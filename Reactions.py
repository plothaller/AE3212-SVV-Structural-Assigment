import math
import numpy as np
import matplotlib.pyplot as plt


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

safetyfactor = 1.5
q = W*3*9.81*safetyfactor/L
S_x = S_x*safetyfactor
print(S_x)


def ReactionsFunction(L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q):
    #Fx1, Fx23, Fy1, Fy2, Fy3
    forcex_row1 = np.array([1,1,0,0,0])
    forcey_row2 = np.array([0,0,1,1,1])
    momentx_row3 = np.array([0,0,L_f1,(L_f1+L_f2),(L_f1+L_f2)])
    momenty_row4 = np.array([-L_f1,-(L_f1+L_f2),0,0,0])
    torque_row5 = np.array([R+d_lg,R+d_lg,0,-L_f3/2,L_f3/2])
    matrixA = np.array([forcex_row1,forcey_row2,momentx_row3,momenty_row4,torque_row5])
    matrixB = np.array([[-S_x],
                        [q*L],
                        [q/2*L**2],
                        [S_x*(L+d_ztail)],
                        [S_x*(d_ytail+d_lg-R)]])

    return np.linalg.solve(matrixA,matrixB) #[Fx1, Fx23, Fy1, Fy2, Fy3]


print(ReactionsFunction(L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q))

Forces = ReactionsFunction(L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q) #Order -> [Fx1, Fx23, Fy1, Fy2, Fy3]
Forces = np.array([Forces[0][0],Forces[1][0],Forces[2][0],Forces[3][0],Forces[4][0]])

def step(location,power):
    if location>0 and power==0:
        return 1
    elif location>0 and power>0:
        return location**power
    else:
        return 0

def Momentx(zlocation,Forces,L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q):
    return Forces[2]*step(zlocation-L+L_f1,1)+(Forces[3]+Forces[4])*step(zlocation-L+L_f1+L_f2,1)-q/2*zlocation**2

def Momenty(zlocation,Forces,L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q):
    return -S_x*d_ztail+Forces[0]*step(zlocation-L+L_f1,1)+Forces[1]*step(zlocation-L+L_f1+L_f2,1)

def Torque(zlocation,Forces,L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q):
    return -S_x*d_ytail+Forces[1]*(d_lg+R)*step(zlocation-L+L_f1+L_f2,0)+Forces[0]*(d_lg+R)*step(zlocation-L+L_f1,0)+(Forces[4]-Forces[3])*L_f3/2*step(zlocation-L+L_f1+L_f2,0)

print(Momentx(0,Forces,L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q))
print(Momenty(L,Forces,L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q))
print(Torque(L,Forces,L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q))


for i in np.linspace(0,L,50):
    print(i)
    plt.plot(-i,Momenty(i,Forces,L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q),'ro')
plt.show()