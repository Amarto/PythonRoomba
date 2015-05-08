# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:28:52 2015

@author: Jaykar_Nayeck
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

class grid():
    def __init__(self,size):
        self.size = size
        self.grid = np.zeros((size,size))  
       
        
    def set_position(self,x,y, value):
        self.grid[x][y] = value
    

    def get_position(self,x,y):
        return self.grid[x][y]
        
    def show_image(self):
        pass
 
class obstacle():
    def __init__(self, grid, coordinates):
        self.grid = grid
        self.coor = coordinates
        
    def place_object(self):
        x0 = self.coor[0][0]
        x1 = self.coor[0][1]
        y0 = self.coor[1][0]
        y1 = self.coor[1][1]
        for i in xrange(x0,x1) :
            for j in xrange(y0,y1):
                self.grid.set_position(i,j,1000)
                
    def delete_object(self):
        x0 = self.coor[0][0]
        x1 = self.coor[0][1]
        y0 = self.coor[1][0]
        y1 = self.coor[1][0]
        for i in xrange(x0,x1) :
            for j in xrange(y0,y1):
                self.grid.set_position(i,j,0)
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
                #if(not((i-x)**2 + (j-y)**2 <= r**2 - epsilon or (i-x)**2 + (j-y)**2 >= r**2 + epsilon)):
                if(((i-x)**2 + (j-y)**2 <= r**2 + epsilon ) and ((i-x)**2 + (j-y)**2 >= r**2 - epsilon )):

                    if(x >= i and (i<=(r*np.cos(np.pi/6) +x + epsilon) or i<=(r*np.cos(np.pi/6) +x-epsilon))):
                        #1st quadrant                        
                        if(y<= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/6) +j-epsilon))):
                            self.grid.set_position(i,j, 100)
                            if(self.grid.get_position(i,j) > 0):
                                self.acoustic_axis[0] = 1
                        #2nd quadrant
                        elif(y >= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/6) +j-epsilon))):
                            self.grid.set_position(i,j, 100)
                            if(self.grid.get_position(i,j) > 0 ):                            
                                self.acoustic_axis[1] = 1
                    elif(x<= i and (i<=(r*np.cos(np.pi/6) +x + epsilon) or i<=(r*np.cos(np.pi/6) +x-epsilon))):
                        #3rd quadrant
                        if(y >= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/6) +j-epsilon))):
                            self.grid.set_position(i,j, 100)  
                            if(self.grid.get_position(i,j) > 0 ):
                                self.acoustic_axis[2] = 1
                        #4th quadrant                        
                        elif(y<= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/6) +j-epsilon))):
                            self.grid.set_position(i,j, 100)
                            if(self.grid.get_position(i,j) > 0):
                                self.acoustic_axis[3] = 1
                        
        return self.acoustic_axis
            
class robot():
    def __init__(self,G):
        self.grid = G
        self.sensor = sensor(self.grid.size, self.grid)
        self.coordinates = [30, 30]
        self.window_size = 50
        
    
    def update_robot_grid(self):
        x = self.coordinates[0]
        y = self.coordinates[1]
        r = 10
        ep = 4
        w = self.draw_window(self.window_size)
        print self.sensor.is_object_in_field_sensor(x, y, r, ep ,w)
    
    def draw_window(self, window_size):
        x0 = self.coordinates[0] - window_size/2
        x1 = self.coordinates[0] + window_size/2
        y0 = self.coordinates[1] - window_size/2
        y1 = self.coordinates[1] + window_size/2
        xVals = [x0, x1]
        yVals = [y0, y1]
        window = [xVals, yVals]
        for i in range (xVals[0], xVals[1]):
                self.grid.set_position(i,yVals[0], 1000)
                self.grid.set_position(i,yVals[1], 1000)
        for i in range (yVals[0], yVals[1]):
                self.grid.set_position(xVals[0], i, 1000)
                self.grid.set_position(xVals[1], i , 1000)
        return window
        
    def delete_inside_window(self, window_size):
        x0 = self.coordinates[0] - window_size/2
        x1 = self.coordinates[0] + window_size/2
        y0 = self.coordinates[1] - window_size/2
        y1 = self.coordinates[1] + window_size/2
        xVals = [x0, x1]
        yVals = [y0, y1]
        window = [xVals, yVals]
        for i in xrange (x0, x1):
            for j in xrange(y0, y1):
                self.grid.set_position(i,j,0)
        return window
    
    def move(self):
        self.delete_inside_window(self.window_size)
        self.coordinates[0] += 1
        self.coordinates[1] += 1
        self.update_robot_grid()
        
class simulation():
    def __init__(self):
        self.size = 200
        self.grid = grid(self.size)
        self.A = robot(self.grid) 
    def draw_boundaries_of_frame(self):
        for i in range (0, self.size):
                self.grid.set_position(i,0, 1000)
                self.grid.set_position(i,self.size-1, 1000)
        for i in range (0,self.size):
                self.grid.set_position(0, i, 1000)
                self.grid.set_position(self.size-1, i , 1000)
    
    
        
    def run(self):    
        self.draw_boundaries_of_frame()
        self.A.update_robot_grid() 
        object_array = []
        box_size = 20        
        n_obstacles = 5
        
        min_val = box_size
        max_val = self.size - box_size
        for i in range(n_obstacles):
            while True:
                x0 = (np.random.randint(0, 400))
                x1 = x0+box_size
                y0 = np.random.randint(0, 400)
                y1 = y0+box_size
                if(x0>min_val and y0 >min_val and x1<max_val and y1 <max_val):
                    break
            ob = obstacle(self.grid, [[x0,x1], [y0,y1]])
            object_array.append(ob)
            ob.place_object()
    def move(self):
        self.A.move()
              

fig = plt.figure()       
A = simulation()
A.run()

plt.imshow(A.grid.grid)
