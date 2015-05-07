# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:28:52 2015

@author: Jaykar_Nayeck
"""

import numpy as np
from matplotlib import pyplot as plt
import Image

class grid():
    def __init__(self,size):
        self.size = size
        self.grid = np.zeros((size,size))  
        
    def set_position(self,x,y, value):
        self.grid[x][y] = value
    
    def get_position(self,x,y):
        return self.grid[x][y]
        
    def show_image(self):
        img = Image.fromarray(self.grid)
        img.show()
        
class sensor(): 
    def __init__(self, size, grid):
        self.acoustic_axis = [0.0 for x in range(4)]
        self.size = size
        self.grid = grid
        
        
    def set_acoustic_axis(self, a):
        self.acoustic_axis = a
    
    def is_object_in_field_sensor(self, x,y,r, epsilon, window):
        
        x0 = window[0][0]
        x1 = window[0][1]
        y0 = window[1][0]
        y1 = window[1][1]   
        r = 10
        self.acoustic_axis = [0.0 for z in range(4)]
        
        for i in xrange(x0,x1):
            for j in xrange(y0, y1):
                if(not((i-x)**2 + (j-y)**2 <= r**2 - epsilon or (i-x)**2 + (j-y)**2 >= r**2 + epsilon)):
                    
                    if(x >= i and (i<=(r*np.cos(np.pi/6) +x + epsilon) or i<=(r*np.cos(np.pi/6) +x-epsilon))):
                        #1st quadrant                        
                        if(y<= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/6) +j-epsilon))):
                            self.grid.set_position(i,j, 100)
                            if(self.grid.get_position(i,j) ==1):
                                self.acoustic_axis[0] = 1
                        #2nd quadrant
                        elif(y >= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/6) +j-epsilon))):
                            self.grid.set_position(i,j, 100)
                            if(self.grid.get_position(i,j) ==1):                            
                                self.acoustic_axis[1] = 1
                    elif(x<= i and (i<=(r*np.cos(np.pi/6) +x + epsilon) or i<=(r*np.cos(np.pi/6) +x-epsilon))):
                        #3rd quadrant
                        if(y >= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/6) +j-epsilon))):
                            self.grid.set_position(i,j, 100)  
                            if(self.grid.get_position(i,j) ==1):
                                self.acoustic_axis[2] = 1
                        #4th quadrant                        
                        elif(y<= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/6) +j-epsilon))):
                            self.grid.set_position(i,j, 100)
                            if(self.grid.get_position(i,j) ==1):
                                self.acoustic_axis[3] = 1
                        
        return self.acoustic_axis
            
class robot():
    def __init__(self,G):
        self.grid = G
        self.sensor = sensor(self.grid.size, self.grid)
    
    def update_robot_grid(self):
        print self.sensor.is_object_in_field_sensor(30, 30, 10, 7, [[15,50],[15,50]])
        
        
class simulation():
    def __init__(self):
        self.Grid = grid(100)
    def run(self):    
        A = robot(self.Grid)
        A.update_robot_grid()   
        self.Grid.show_image()

A = simulation()
A.run()