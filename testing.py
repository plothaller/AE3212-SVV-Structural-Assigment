#Verification testing

import unittest
import Geometry

#Geometry functions tested with below variables
n_s  = 16
R    = 3
t_st = 1.2/1000
h_st = 1.5/100
w_st = 2/100
t_f  = 2.5/100
L    = 30
Lf1  = 2
Lf2  = 16
h_f  = 1.85
t_s  = 1/100
w_f = Geometry.floor_width(R, h_f)
stringer_area = t_st*(h_st + w_st)



class TestGeometry(unittest.TestCase):

    def test_floor_width(self):
        #Testing the correct implementation of the floor width calculation
        #Assertion value retrieved from the SVV pointers setup document

        floor_width = Geometry.floor_width(3, 1.85)
        assert round(floor_width, 3) == round(5541.7/1000,3)

    def test_floor_location(self):
        #Testing the correct implementation of the floor location from the origin in the y-direction calculation
        #Assertion value retrieved from the SVV pointers setup document

        floor_location = Geometry.floor_location_y(3, 1.85)
        assert round(floor_location, 3) == round(-1150/1000,3)

    def test_centorid(self):
        #Testing the correct implementation of the centriod calculation
        #This test will also verify the implementation of the total area calculation
        #Assertion value retrieved from the SVV pointers setup document

        x_bar, y_bar = Geometry.centroid(3, 1.85, 2.5/100, 1/100, 16, 1.2/1000, 1.5/100, 2/100)
        assert x_bar == 0
        assert round(y_bar, 3) == round(-486.1/1000,3)

    def test_stringer_distance(self):
        #Testing the correct implementation of the floor width calculation
        #Assertion value retrieved from the SVV pointers setup document

        d_s = Geometry.stringer_distance(3, 16)
        assert round(d_s, 3) == round(1178.1/1000,3)

    def test_moixx(self):
        #Testing the moment of inertia calculations for floor contribution
        #Values are compared to hand calculated values

        x_bar, y_bar = Geometry.centroid(R, h_f, t_f, t_s, n_s, t_st, h_st, w_st)
        floor_Ixx, fuselage_Ixx, stringer_Ixx = Geometry.MOIxx(x_bar, y_bar, stringer_area, R, h_f, t_f, t_s, n_s, t_st, h_st, w_st, w_f)
        assert round(floor_Ixx, 4) == round(0.0610583336, 4)
        assert round(fuselage_Ixx, 4) == round(0.097228, 4)
        assert round(stringer_Ixx, 4) == round(0.003182835606813844, 4)

    def test_moiyy(self):
        #Testing the moment of inertia calculations for floor contribution
        #Values are compared to hand calculated values

        x_bar, y_bar = Geometry.centroid(R, h_f, t_f, t_s, n_s, t_st, h_st, w_st)
        floor_Iyy, fuselage_Iyy, stringer_Iyy = Geometry.MOIyy(x_bar, y_bar, stringer_area, R, h_f, t_f, t_s, n_s, t_st, h_st, w_st, w_f)
        assert round(floor_Iyy, 4) == round(0.354558415, 4)
        assert round(fuselage_Iyy, 4) == round(0.052749892705925, 4)
        assert round(stringer_Iyy, 4) == round(0.0030239999999999998, 4)




if __name__ == '__main__':
    unittest.main()
