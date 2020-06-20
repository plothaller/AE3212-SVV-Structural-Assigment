import math
import numpy as np


L = 30 #[m]
L_f1 = 4 #[m]
L_f2 = 12.5 #[m]
L_f3 = 5.2 #[m]
R = 2 #[m]
h_f = 1.8 #[m]
d_lg = 1.8 #[m]
d_ztail = 2.8 #[m]
d_ytail = 5 #[m]
S_x = 1.7*10**(5) #[N]
W = 65000 #[kg]

safetyfactor = 1.5
q = W*3*9.81*safetyfactor*0
S_x = S_x*safetyfactor


def ReactionsFunction(L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q):
    #Fx1, Fx23, Fy1, Fy2, Fy3
    forcex_row1 = np.array([1,1,0,0,0])
    forcey_row2 = np.array([0,0,1,1,1])
    momentx_row3 = np.array([0,0,L_f1,(L_f1+L_f2),(L_f1+L_f2)])
    momenty_row4 = np.array([-L_f1,-(L_f1+L_f2),0,0,0])
    torque_row5 = np.array([0,0,0,-L_f3/2,L_f3/2])
    matrixA = np.array([forcex_row1,forcey_row2,momentx_row3,momenty_row4,torque_row5])
    matrixB = np.array([[-S_x],
                        [q*L],
                        [q*L**2/2],
                        [S_x*(L+d_ztail)],
                        [S_x*(d_ytail+d_lg)]])

    return np.dot(np.linalg.inv(matrixA),matrixB) #[Fx1, Fx23, Fy1, Fy2, Fy3]


print(ReactionsFunction(L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q))
ReactionsFunction()