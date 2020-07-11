import numpy as np
import matplotlib.pyplot as plt
from Reactions import *


def celldivision(positionsofbooms, areaofbooms, gamma_f):
    '''
    Division of all the booms accoring to cells
    :param positionsofbooms: outputs of definition
    :param areaofbooms: output of definiotn
    :param gamma_f: angle between a-axis and floor
    :return: angle, distancebetween, area, position
    floor is in both cells
    '''
    thetas1 =[]
    thetas2 =[]
    thetas3 = []
    s1 = []
    s2 = []
    s3 = []
    B1 = []
    B2 = []
    B3 = []
    pos1 = np.array([[0,0]])
    pos2 = np.array([[0,0]])
    pos3 = np.array([[0,0]])

    ag_1 = np.pi + gamma_f
    ag_2 = np.pi*2 - gamma_f

    for i in range(len(positionsofbooms[0])):
        if  ag_1 < positionsofbooms[0][i] < ag_2:
            thetas2 = np.append(thetas2, positionsofbooms[0][i])
            s2 = np.append(s2,positionsofbooms[1][i])
            B2 = np.append(B2, areaofbooms[i])
            pos2 = np.append(pos2, [positionsofbooms[2][i]], axis = 0)

        elif positionsofbooms[0][i] < ag_1:
            thetas1 = np.append(thetas1, positionsofbooms[0][i])
            s1 = np.append(s1,positionsofbooms[1][i])
            B1 = np.append(B1, areaofbooms[i])
            pos1 = np.append(pos1, [positionsofbooms[2][i]], axis = 0)
        elif positionsofbooms[0][i] > ag_2:
            thetas3 = np.append(thetas3, positionsofbooms[0][i])
            s3 = np.append(s3, positionsofbooms[1][i])
            B3 = np.append(B3, areaofbooms[i])
            pos3 = np.append(pos3, [positionsofbooms[2][i]], axis=0)
    #start the count from were the floor meets the skin
    pos1 = np.delete(pos1,0,0)
    pos2 = np.delete(pos2,0,0)
    pos3 = np.delete(pos3, 0,0)
    thetas1 = np.concatenate((thetas3,thetas1))
    s1 = np.concatenate((s3,s1))
    B1 = np.concatenate((B3,B1))
    pos1 = np.concatenate((pos3,pos1) , axis = 0 )


    #adding the floor

    B1 = np.append(B1,areaofbooms[-3:])
    B2 = np.append(B2, areaofbooms[-3:])
    pos1 = np.append(pos1, positionsofbooms[2][-3:], axis = 0)
    pos2 = np.append(pos2, np.flip(positionsofbooms[2][-3:], axis = 0), axis=0)



    return thetas1,thetas2,s1,s2,B1,B2,pos1,pos2


#Deflection due to Shear
def shearflowsb(S_x,S_y, I_xx, I_yy, A_I, A_II, areaofbooms, positionsofbooms, t_sk, t_f, y_f,gamma_f):
    '''
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
    '''

    #transformations
    thetas1, thetas2, s1, s2, B1, B2, pos1, pos2 = celldivision(positionsofbooms, areaofbooms, gamma_f)
    thetas = np.append(thetas1,thetas2)

    #base shear
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

    qb = np.append(qb, np.subtract(qb1[-3:], qb2[-3:])) #last 3 are floor

    #Moment around origin
    moment = 0
    thetas = np.insert(thetas, 0, 0)
    for i in range(len(thetas)):
        dx = -(R-(R*np.cos(thetas[i]-thetas[i-1])))
        dy = R*np.sin(thetas[i]-thetas[i-1])
        x_arm = R*np.cos(thetas[i])
        y_arm = R*np.sin(thetas[i])
        moment += (x_arm*dy + y_arm*dx)*qb[i]

    moment_floor = y_f*sum(qb[-3:])
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

    q1 = qb1 + q01
    q2 = qb2 + q02

    return delta_S, q1, q2





#Deflection due to torsion

def deflect_T(T, A_I, A_II, positionsofbooms, areaofbooms, t_sk, t_f,gamma_f):
    '''
    Sheart due to torsion
    :param T: Torsion
    :param A_I: Area cell I
    :param A_II: Area  Cell II
    :param positionsofbooms: output of positions of booms
    :param areaofbooms: output of area of booms
    :param t_sk: thickness skin
    :param t_f: thickness floor
    :return:
    GdO/dz, shear flow cell I and cell II
    '''
    thetas1,thetas2,s1,s2,B1,B2,pos1,pos2 = celldivision(positionsofbooms, areaofbooms,gamma_f)

    s_I = s1[:-3]
    s_IwII = s1[3:]
    s_II = s2[:-3]


    q_1_I = 1/(2*A_I) * (sum(s_I)/t_sk + sum(s_IwII)/t_f )
    q_2_I = -1 / (2 * A_I)*(sum(s_IwII)/t_f)
    q_1_II = -1/ (2*A_II)*(sum(s_IwII)/t_f)
    q_2_II = 1/ (2 * A_II)*(sum(s_II)/t_sk + sum(s_IwII)/t_f)

    M = np.array([[2*A_I, 2*A_II, 0],
                 [q_1_I, q_2_I, -1],
                 [q_1_II, q_2_II, -1]], dtype='float')
    M1 = np.array([T,0,0], dtype='float')
    q1, q2, delta_T = np.linalg.solve(M,M1)


    return delta_T,q1,q2

def J(T, delta_T):
    return T/( delta_T)

def simga_b(Mx,My, Ixx,Iyy,positionsofbooms, areaofbooms, gamma_f):
    thetas1, thetas2, s1, s2, B1, B2, pos1, pos2 = celldivision(positionsofbooms, areaofbooms, gamma_f)
    pos = np.append(pos1[:-3], pos2[:-3], axis=0)
    pos = np.append(pos, np.subtract(pos1[-3:], pos2[-3:]), axis=0)
    sigma_z = np.array([])
    for i in range(len(pos)):
        sigma = Mx/Ixx*pos[i][1]+My/Iyy*pos[i][0]
        sigma_z = np.append(sigma_z, sigma)

    return sigma_z

def vonMises(q1_s,q2_s, q1_t, q2_t , sigma_b, t_sk, t_f):
    '''
    Calculates von Mises stresses
    :param q1_s: shear flow due to shear cell 1
    :param q2_s: shear flow due to shear cell 2
    :param q1_t: shear flow due to torsion cell 1
    :param q2_t: shear flow due to torsion cell 2
    :param sigma_b: nomrmal stress
    :param t_sk: skin thcikness
    :param t_f: floor thickness
    :return: von Mises stresses
    '''
    q1 = q1_s +q1_t
    q2 = q2_s + q2_t
    q = np.append(q1[:-3], q2[:-3])
    q = np.append(q, np.subtract(q1[-3:], q2[-3:]))

    tao1 = q[:-3] / t_sk
    tao2 = q[-3:] / t_f
    tao = np.append(tao1,tao2)
    vonmis = np.array([])
    for i in range(len(tao)):
        s = np.sqrt(sigma_b[i]**2 + 3*tao[i]**2)
        vonmis = np.append(vonmis,s)
    return tao


