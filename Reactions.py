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


#Inputs: [L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q]
#ReactionFunctions determines the five forces
#Fx1, Fy1 Front landing gear
#Fx23=Fx2+Fx3
#Fx23, Fy2,Fy3 Rear landing gears
#Output: An array with the five forces
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
                        [S_x*(d_ytail-R)]])

    return np.linalg.solve(matrixA,matrixB) #[Fx1, Fx23, Fy1, Fy2, Fy3]

Forces = ReactionsFunction(L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q) #Order -> [Fx1, Fx23, Fy1, Fy2, Fy3]


#Step is a function for the Macaulay step function
#Input: (location = position in z) and (power)
#Output: value and if its negative retuns zero
def step(location,power):
    if location>0 and power==0:
        return 1
    elif location>0 and power>0:
        return location**power
    else:
        return 0

#Function Moment in x
def Momentx(zlocation,Forces):
    return -1*(Forces[2]*step(zlocation-L+L_f1,1)+(Forces[3]+Forces[4])*step(zlocation-L+L_f1+L_f2,1)-q/2*zlocation**2)

#Function Moment in y
def Momenty(zlocation,Forces):
    return -1*(-S_x*(d_ztail+zlocation)-Forces[0]*step(zlocation-L+L_f1,1)-Forces[1]*step(zlocation-L+L_f1+L_f2,1))

#Function Moment in z
def Torque(zlocation,Forces): #,L,L_f1,L_f2,L_f3,d_lg,d_ztail,d_ytail,S_x,q
    return -1*(-S_x*(d_ytail-R)+Forces[1]*(d_lg+R)*step(zlocation-L+L_f1+L_f2,0)+Forces[0]*(d_lg+R)*step(zlocation-L+L_f1,0)+(Forces[4]-Forces[3])*L_f3/2*step(zlocation-L+L_f1+L_f2,0))

#Determines the angle of the neutral axis
def NeutralAxisAngle(zlocation,Forces,Ixx,Iyy): #Degrees
    angle = np.arctan(-(Momenty(zlocation,Forces)*Ixx)/(Momentx(zlocation,Forces)*Iyy))*180/np.pi
    return angle

#Determines the normal stress
def NormalStressZ(zlocation,Forces,Ixx,Iyy,x,y):
    sigma_z = Momentx(zlocation,Forces)/Ixx*y+Momenty(zlocation,Forces)/Iyy*x
    return sigma_z


#PositionOfBooms is a function that sets the position of booms and any of the booms is close to the neutral axis. The tolerance is about 2 degrees
#REMARK the number of booms will be less than n probably. So remember to use LEN for determining the number of booms
#Inputs: (n=number of booms),zlocation, array of Forces and moments of inertia
#Outputs: array angleboomfinal = returns the angle of the position of the booms in RADIANS
        # array b = arc distance between each boom in METERS
def PositionofBooms(n,zlocation,Forces,Ixx,Iyy):
    delta_angle = 360/n * np.pi/180
    b = np.array([])

    angleboom =np.array([])
    alpha = NeutralAxisAngle(zlocation,Forces,Ixx,Iyy)
    tolerance = 2*np.pi/180

    for i in range(n):
        delta = i*delta_angle
        angleboom = np.append(angleboom,delta)

    angleboomfinal = np.array([])
    for i in range(n):
        if alpha - tolerance < angleboom[i] < alpha + tolerance or alpha-tolerance+np.pi<angleboom[i]<alpha+tolerance+np.pi:
            continue
        else:
            angleboomfinal = np.append(angleboomfinal,angleboom[i])
    for i in range(len(angleboomfinal)-1):
        bstep = R*(angleboomfinal[i+1]-angleboomfinal[i])
        b = np.append(b,bstep)
    b = np.append(b,max(b))
    positions = np.zeros((len(angleboomfinal)+3,2))

    for i in range(len(angleboomfinal)):
        positions[i][0] = R*np.cos(angleboomfinal[i])
        positions[i][1] = R*np.sin(angleboomfinal[i])
    positions[len(angleboomfinal)][0] = -np.sqrt(R**2-(R-h_f)**2)
    positions[len(angleboomfinal)][1] = -R + h_f
    positions[len(angleboomfinal)+1][0] = 0
    positions[len(angleboomfinal)+1][1] = -R + h_f
    positions[len(angleboomfinal)+2][0] = np.sqrt(R**2-(R-h_f)**2)
    positions[len(angleboomfinal)+2][1] = -R + h_f
    return angleboomfinal,b,positions

#Same formula from the Geometry file
def total_stringer_area(R, t_s, n_s, t_st, h_st, w_st, t_f, h_f):
    return n_s*t_st*(h_st + w_st)

#Determines the area of the boom
def SkinBoom1(t_s,b,sigma2,sigma1):
    areaskin = t_s*b/6*(2+sigma2/sigma1)
    return areaskin

#AreaBoom computes the area for each boom in the skin in m^2 including the equal contribution of the stringers
#AreaBoom returns an array with the areas
#The angle_bool_final and b_array can be deterimined using the function PositionofBooms

def AreaBoom(angle_boom_final,zlocation,Ixx,Iyy,b_array):
    numberofboom = len(angle_boom_final)
    area_stringer_average = total_stringer_area(R, t_s, n_s, t_st, h_st, w_st, t_f, h_f) / numberofboom
    areabooms = np.ones(numberofboom) * area_stringer_average
    normalstress_circle = np.array([])
    for step in range(numberofboom):
        normalstress_circle = np.append(normalstress_circle,NormalStressZ(zlocation,Forces,Ixx,Iyy,R*np.cos(angle_boom_final[step]),R*np.sin(angle_boom_final[step])))
    for step in range(numberofboom):
        if step == numberofboom-1:
            areabooms[step] += SkinBoom1(t_s, b_array[step - 1], normalstress_circle[step - 1],normalstress_circle[step]) + SkinBoom1(t_s, b_array[step],normalstress_circle[0],normalstress_circle[step])
        else:
            areabooms[step] += SkinBoom1(t_s,b_array[step-1],normalstress_circle[step-1],normalstress_circle[step])+SkinBoom1(t_s,b_array[step],normalstress_circle[step+1],normalstress_circle[step])
    areafloor = t_f*2*np.sqrt(R**2-(R-h_f)**2)
    areabooms = np.append(areabooms, areafloor / 3)
    areabooms = np.append(areabooms, areafloor / 3)
    areabooms = np.append(areabooms, areafloor / 3)
    return areabooms

#for i in np.linspace(0,L,100):
#    plt.plot(-i,Torque(i,Forces),'bo')
#
# plt.figure(2)
# for i in np.linspace(0,L,100):
#     if (i==L or i==0):
#          continue
#      plt.plot(-i,NeutralAxisAngle(i,Forces,1,1),'ro')
#
# plt.figure(3)
# for i in np.linspace(0, L, 100):
#      if (i == L or i == 0):
#          continue
#      plt.plot(-i, NormalStressZ(i,Forces,1,1,R/np.sqrt(2),R/np.sqrt(2)), 'ko')
#
#plt.show()

#print(Momentx(L-1,Forces))
#print(PositionofBooms(8,L-1,Forces,1,1))
#print(AreaBoom(PositionofBooms(8,L-1,Forces,1,1)[0],L-1,1,1,PositionofBooms(8,L-1,Forces,1,1)[1]))
#print(AreaBoom(PositionofBooms(10,L-1,Forces,1,1)[0],L-1,1,1,PositionofBooms(10,L-1,Forces,1,1)[1]))



#print(NormalStressZ(L-1,Forces,1,1,R*np.cos(0.78539816),R*np.sin(0.78539816)))
#print(NormalStressZ(L-1,Forces,1,1,R*np.cos(np.pi/2),R*np.sin(np.pi/2))/NormalStressZ(L-1,Forces,1,1,R*np.cos(0.78539816),R*np.sin(0.78539816)))