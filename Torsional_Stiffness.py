import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style



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
