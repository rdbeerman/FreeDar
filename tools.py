"""
@Title:         Tools
@Description:   Tools for the FreeDar project such as emulating input.
@Author:        R.D. Beerman
@Date:          10/04/2018
@License:
"""
import numpy as np
import matplotlib.pyplot as plt

def e_data_s(samplerate, speed, x, y):
    """ Description: generates datastream emulating 2D lidar in square.
        Parameters:
            samplerate:     time of flight sensor samplerate.
            speed:          rad per second of emulated lidar along horizontal axis.
            x:         length of rectangle in m.
        Output:
            array with distance values for a single rotation.
    """
    x = x
    y = y
    speed = speed
    timestep = 1/samplerate
    d_array = []
    angle = 0
    time = 0
    oct1 = np.arctan((0.5*y)/(0.5*x))
    oct2 = oct1 + np.arctan((0.5*x)/(0.5*y))
    oct3 = oct2 + np.arctan((0.5*x)/(0.5*y))
    oct4 = oct3 + np.arctan((0.5*y)/(0.5*x))
    oct5 = oct4 + np.arctan((0.5*y)/(0.5*x))
    oct6 = oct5 + np.arctan((0.5*x)/(0.5*y))
    oct7 = oct6 + np.arctan((0.5*x)/(0.5*y))
    oct8 = oct7 + np.arctan((0.5*y)/(0.5*x))
    while 0.0 <= angle <= 2*np.pi:
        angle = speed * time
        if 0.0 <= angle <= oct1:                 #octant 1
            d = (0.5*x)/np.cos(angle)
        elif angle <= oct2:                      #octant 2
            d = (0.5*y)/np.cos((0.5*np.pi)-angle)
        elif angle <= oct3:                      #octant 3
            d = (0.5*y)/np.cos(angle-(0.5*np.pi))
        elif angle <= oct4:                      #octant 4
            d = (0.5*x)/np.cos(angle-np.pi)
        elif angle <= oct5:                      #octant 5
            d = (0.5*x)/np.cos(angle-np.pi)
        elif angle <= oct6:                      #octant 6
            d = (0.5*y)/np.cos(angle-(6/4*np.pi))
        elif angle <= oct7:                      #octant 7
            d = (0.5*y)/np.cos(angle-(6/4*np.pi))
        elif angle <= oct8:                      #octant 8
            d = (0.5*x)/np.cos(angle-(8/4*np.pi))
        d_array.append(d)
        time = time + timestep
    return d_array

def e_data_c(samplerate, speed, x, y):
    """ Description: generates datastream emulating 2D lidar in square.
        Parameters:
            samplerate:     time of flight sensor samplerate.
            speed:          rad per second of emulated lidar along horizontal axis.
            x:              length of rectangle in m.
            y:              width of rectangle in m.
        Output:
            continuous datasteam as distance values.
    """
    y = y
    x = x
    speed = speed
    timestep = 1/samplerate
    angle = 0.0
    time = 0
    while True:
        try:
            angle = speed*(time)
            time = time + timestep
            d = np.sqrt((np.sin(angle)**2)+(x/2)**2)
            print(d)
        except KeyboardInterrupt:                    #only works when running in separate window, click kill in pycharm
            exit()
    return d

def e_angle_s(samplerate, speed):
    """ Description: generates datastream emulating angle from 2D LIDAR with samplerate and speed.
            Parameters:
                samplerate:     time of flight sensor samplerate.
                speed:          rad per second of emulated lidar along horizontal axis.
            Output:
                array of angle values for a single rotation.
        """
    speed = speed
    timestep = 1 / samplerate
    angle = 0.0
    time = 0.0
    angle_array = []
    while angle < 2 * np.pi:
        angle = speed * time
        time = time + timestep
        angle_array.append(angle)
    return angle_array