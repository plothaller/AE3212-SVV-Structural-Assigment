import numpy as np

R = 3
n_s = 16
t_st = 1.2/1000
h_st = 1.5/100
w_st = 2/100

stringer_area = t_st*(h_st + w_st)
theta = 2*np.pi/n_s
stringer_Ixx = 0
y_bar = -0.4861712765473184
for i in range(n_s):
    
    
    y = R*np.sin(i*theta)
    stringer_Ixx += stringer_area*(y-y_bar)**2

stringer_Iyy = 0
for j in range(n_s):
    
    
    x = R*np.cos(j*theta)
    stringer_Iyy += stringer_area*(x)**2

print(stringer_Iyy)