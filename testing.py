#Verification testing

import unittest
import Geometry



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


if __name__ == '__main__':
    unittest.main()
