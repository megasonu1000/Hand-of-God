###############################################################################
#     Project C (Hand of God) Dated July 3rd 2018 Tuesday 2100 Hours          #
#     Developer- Kuldeep Paul                                                 #
#     Developed for Quinch Systems Pvt. Ltd.                                  #
#     Copyright 2018                                                          #
###############################################################################

from pymouse import PyMouse

m = PyMouse()
x_length, y_length = m.screen_size()

def position(x, y):
    m.move(x*3, y*3)
