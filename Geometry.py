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


idealization(3, 16, 1.2/1000, 1.5/100, 2/100, 2.5/100, 1.85, 1/100)

