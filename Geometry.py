#Structural Idealization
#All input and output values are to be given in kg, m or s



import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style

#Stylizing plots
style.use('seaborn-talk') #sets the size of the charts
style.use('ggplot')


def floor_width(R, h_f):
    return 2*np.sqrt(R**2 - (R-h_f)**2)

def floor_location_y(R, h_f):
    return -(R-h_f)

def total_area(R, t_s, n_s, t_st, h_st, w_st, t_f, h_f):

    w_f = floor_width(R, h_f)

    fuselage_area = 2*np.pi*R*t_s
    total_stringer_area = n_s*t_st*(h_st + w_st)
    floor_area = w_f*t_f

    return fuselage_area + total_stringer_area + floor_area


def centroid(R, h_f, t_f, t_s, n_s, t_st, h_st, w_st):

    #due to symmetry around the y_axis, x_bar equals 0
    x_bar = 0

    #due to symmetry around the x_axis the fuselage and stringers will not influence the location of y_bar
    y_bar = (floor_width(R, h_f)*floor_location_y(R, h_f)*t_f)/(total_area(R, t_s, n_s, t_st, h_st, w_st, t_f, h_f))

    return x_bar, y_bar

def MOIxx(x_bar, y_bar, stringer_area, R, h_f, t_f, t_s, n_s, t_st, h_st, w_st, w_f):
    #Floor MOIxx
    floor_y = floor_location_y(R, h_f)
    x_bar, y_bar = centroid(R, h_f, t_f, t_s, n_s, t_st, h_st, w_st)
    floor_y_dist2 = (floor_y - y_bar)**2
    floor_area = w_f*t_f
    floor_Ixx =  (w_f*t_f**3)/12 + floor_area*floor_y_dist2

    #Fuselage MOIxx
    fuselage_area = np.pi*R**2 - np.pi*(R-t_s)**2
    fuselage_Ixx = np.pi/64*(R**4-(R-t_s)**4) + fuselage_area*y_bar**2

    #Stringer MOIxx
    theta = (2*np.pi)/n_s
    stringer_Ixx = 0
    for i in range(n_s):
        height = R*np.sin(i*theta) - y_bar
        stringer_Ixx += stringer_area*height**2

    return floor_Ixx, fuselage_Ixx, stringer_Ixx

def MOIyy(x_bar, y_bar, stringer_area, R, h_f, t_f, t_s, n_s, t_st, h_st, w_st, w_f):

    #Floor MOIyy
    floor_Iyy =  (w_f**3*t_f)/12 #+ floor_area*floor_y_dist2

    #Fuselage MOIyy
    fuselage_Iyy = np.pi/64*(R**4-(R-t_s)**4)# + fuselage_area*y_bar**2

    #Stringer MOIyy
    theta = (2*np.pi)/n_s
    stringer_Iyy = 0
    for i in range(n_s):
        width = R*np.cos(i*theta) #- y_bar
        stringer_Iyy += stringer_area*width**2

    return floor_Iyy, fuselage_Iyy, stringer_Iyy

def stringer_distance(R, n_s):
    return (2*np.pi*R)/(n_s)



def idealization(R, n_s, t_st, h_st, w_st, t_f, h_f, t_s):

    #visulization of idealization

    #plotting
    plt.close('all')
    ax = plt.gca()
    ax.cla() # clear things for fresh plot

    # change default range
    ax.set_xlim((-R-1, R+1))
    ax.set_ylim((-R-1, R+1))

    #adding origin
    origin = plt.Circle((0, 0), 0.1, color='k', fill=False)
    plt.gcf().gca().add_artist(origin)
    plt.text(0 + 0.1, 0, "Origin")


    #adding centroid
    centroid_location = plt.Circle((centroid(R, h_f, t_f, t_s, n_s, t_st, h_st, w_st)[0], centroid(R, h_f, t_f, t_s, n_s, t_st, h_st, w_st)[1]), 0.05, color='r', fill=True)
    plt.gcf().gca().add_artist(centroid_location)
    plt.text(centroid(R, h_f, t_f, t_s, n_s, t_st, h_st, w_st)[0] + 0.1, centroid(R, h_f, t_f, t_s, n_s, t_st, h_st, w_st)[1] + 0.1, "Centroid")


    #Fuselage
    fuselage = plt.Circle((0, 0), R, color='k', fill=False)
    plt.gcf().gca().add_artist(fuselage)

    #Stringers
    theta = (2*np.pi)/n_s


    for i in range(n_s):

        stringer = plt.Circle((R*np.sin(i*theta), R*np.cos(i*theta)), 0.05, color='k', fill=True)
        plt.gcf().gca().add_artist(stringer)
        plt.text(R*np.sin(i*theta) + 0.1, R*np.cos(i*theta), "A" + str(i+1))

    #Floor
    plt.plot([-floor_width(R, h_f)/2, floor_width(R, h_f)/2], [floor_location_y(R, h_f), floor_location_y(R, h_f)], color='k', linestyle='-', linewidth=1)

    #Adding boom of the floor
    floor_boom = plt.Circle((0, floor_location_y(R, h_f)), 0.05, color='k', fill=True)
    plt.gcf().gca().add_artist(floor_boom)
    plt.text(0 + 0.1, floor_location_y(R, h_f) + 0.1, "A" + str(n_s+1))



    plt.show()
    #plt.close("all")



