import Geometry
import numpy as np

n_s  = 16
R    = 3
t_st = 1.2/1000
h_st = 1.5/100
w_st = 2/100
t_f  = 2.5/100
L    = 30
Lf1  = 2
Lf2  = 16
h_f  = 1.85 #hieght of floor
y_f = R-h_f #y-loc of floor if origin if circle center
gamma_f = np.arcsin(y_f/R) #angle between x-axis and floor
theta_f = np.pi - 2*gamma_f #angle of sector with floor
A_II = (R**2/2)*(theta_f - np.sin(theta_f)) # Area Cell II
A_I = (np.pi*R**2) - A_II #Area Cell I
t_s = 1/100
w_f = Geometry.floor_width(R, h_f)
stringer_area = t_st*(h_st + w_st)

#Calculating Geometrical Properties
Geometry.idealization(R, n_s, t_st, h_st, w_st, t_f, h_f, t_s)
x_bar, y_bar = Geometry.centroid(R, h_f, t_f, t_s, n_s, t_st, h_st, w_st)
floor_Ixx, fuselage_Ixx, stringer_Ixx = Geometry.MOIxx(x_bar, y_bar, stringer_area, R, h_f, t_f, t_s, n_s, t_st, h_st, w_st, w_f)
floor_Iyy, fuselage_Iyy, stringer_Iyy = Geometry.MOIyy(x_bar, y_bar, stringer_area, R, h_f, t_f, t_s, n_s, t_st, h_st, w_st, w_f)

