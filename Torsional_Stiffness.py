import numpy as np
import matplotlib.pyplot as plt



#Deflection due to Shear
def shearflowsb(S_x, I_yy, B_x1, x_r1, y_r1, B_x2, x_r2, yr_2, R, thetas, t_sk, t_f, y_f):
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
    qb = np.append([qb1],[qb2])

    #Floor Contribution

    qb_f1 = 0
    qb_f2 = 0


    #Moment around origin
    moment = 0
    for i in range(len(thetas)):
        dx = -(R-(R*np.cos(thetas[i+1]-thetas[i])))
        dy = R*np.sin(thetas[i]-thetas[i])
        x_arm = R*np.cos(thetas(thetas[i]))
        y_arm = R*np.sin(thetas[i])
        moment += (x_arm*dy + y_arm*dx)*qb[i] #ADD FLOOR

    moment_floor = y_f*qb_f
    moment += moment_floor
    #deflections

    thetas1 = thetas[:5] #fill in place where cell 2 starts
    thetas2 = thetas[5:9]#fill same as above


    ds_list= []
    totshear = 0
    for i in range(len(thetas1)):
        ds = R*(thetas1[i+1] - thetas1[i])/t_sk
        ds_list.append(ds)
        totshear += qb1[i]*ds


    firstcoeff_1 = 1/(2*A_I)*(totshear + floorcont)
    q01_1 = 1/(2*A_I)*(sum(ds_list)+ ds_floor)
    q02_1 = -1/(2*A_I)*ds_floor
    ds_list2 = []
    for i in range(len(thetas2)):
        ds = R*(thetas2[i+1] - thetas2[i])/t_sk
        ds_list2.append(ds)
        totshear += qb2[i]*ds

    firstcoeff_2 = 1/(2*A_II)*(totshear + floorcont)
    q02_2 = 1/(2*A_II)*(sum(ds_list)+ ds_floor)
    q01_2 = -1/(2*A_II)*ds_floor


    #Solving the Equations

    M = np.array([2*A_I, 2*A_II, 0],
                 [q01_1, q02_1, firstcoeff_1],
                 [q01_2, q02_2, firstcoeff_2])
    M1 = np.array([moment, 0, 0])

    q01, q02, delta_S = np.linalg.solve(M,M1)
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
    q_2_I = -1 / (2 * A_I)*(sum(s_IwII)/t_f)
    q_1_II = -1/ (2*A_II)*sum(s_IwII)/t_f
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

