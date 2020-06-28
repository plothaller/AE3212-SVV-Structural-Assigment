import numpy as np
import matplotlib.pyplot as plt



#Deflection due to Shear
def shearflowsb(S_x, I_yy, B_x1, x_r1, B_x2, x_r2):
    '''
    :param S_x: Shear immaginary so = 1
    :param I_yy: Moment of Inertia
    :param B_x1: Boom areas cell 1
    :param x_r1: Boom loacation cell 1
    :param B_x2: Boom area cell 2
    :param x_r2: Boom location cell 2
    :return: Base Shear flows in each section
    '''
    qb1 = []
    qb2 = []
    K = S_x/I_yy
    for i in range(len(B_x1)):
        q = K*B_x1[i]*x_r1[i]
        qb1.append(q)
    qb1.append(0)
    for i in range(len(B_x2)):
        q = K * B_x2[i] * x_r2[i]
        qb2.append(q)
    qb2[3] = 0

    return qb1, qb2

def deflect_S():


    return delta_S



#Deflection due to torsion

def deflect_T(T, A_I, A_II, s, t_sk, t_f):
   '''
   Delfections due to torsion
   :param T: torsion
   :param A_1: Area Cell I
   :param A_2: Area Cell II
   :param s: lenght between booms
   :param t: thickness
   :return: deflection
   '''
    s_I = s[0:5] #need to know where the Cell starts for slicing
    s_IwII = s[8:10]
    s_II = s[5:7]
    q_1_I = 1/(2*A_I) * (sum(s_I)/t_sk + sum(s_IwII)/t_f )
    q_2_I = -1 / (2 * A_I)*(sum(s_IwII))
    q_1_II = -1/ (2*A_II)*sum(s_IwII)
    q_2_II = 1/ (2 * A_II)*(sum(s_II)/t_sk + sum(s_IwII)/t_f)

    M = np.array([2*A_I, 2*A_II, 0],
                 [q_1_I, q_2_I, -1],
                 [q_1_II, q_2_II, -1])
    M1 = np.array([T,0,0])
    q1, q2, delta_T = np.linalg.solve(M,M1)

    return delta_T

def J(T, A_I, A_II, s, t_sk, t_f):


    delta_T =deflect_T(T, A_I, A_II, s, t_sk, t_f)
    delta_S = 1

    return J/(delta_S + delta_T)

