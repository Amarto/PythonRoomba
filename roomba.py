# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:28:52 2015

@author: Jaykar_Nayeck
"""

import numpy as np
from matplotlib import pyplot as plt

MAX_WEIGHT = 1000 #for setting boundaries
SMALL_WEIGHT = 100 #for obstacle detection
X_COORD = 30 #coords of robot
Y_COORD = 30
WINDOW_SIZE = 50 #for defining robot in frame
BOX_SIZE = 20 #size of obstacles       
N_OBSTACLES = 5 #number of obstacles
MAX_RAND_VAL = 400 #maximum random value for generating obstacle coords
RADIUS = 10
EP = 4   

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
                self.grid.set_position(i,j,MAX_WEIGHT)
                
    def delete_object(self):
        x0 = self.coor[0][0]
        x1 = self.coor[0][1]
        y0 = self.coor[1][0]
        y1 = self.coor[1][1]
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

        self.acoustic_axis = [0.0 for z in range(4)]
        
        for i in xrange(x0,x1):
            for j in xrange(y0, y1):
                #if(not((i-x)**2 + (j-y)**2 <= r**2 - epsilon or (i-x)**2 + (j-y)**2 >= r**2 + epsilon)):
                if(((i-x)**2 + (j-y)**2 <= r**2 + epsilon ) and ((i-x)**2 + (j-y)**2 >= r**2 - epsilon )):

                    if(x >= i and (i<=(r*np.cos(np.pi/6) +x + epsilon) or i<=(r*np.cos(np.pi/4) +x-epsilon))):
                        #1st quadrant                        
                        if(y<= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/4) +j-epsilon))):
                           # used for debbugging:
                            #self.grid.set_position(i,j, SMALL_WEIGHT)
                            if(self.grid.get_position(i,j) > 0):
                                self.acoustic_axis[0] = 1
                        #2nd quadrant
                        elif(y >= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/6) +j-epsilon))):
                            #self.grid.set_position(i,j, SMALL_WEIGHT)
                            if(self.grid.get_position(i,j) > 0 ):                            
                                self.acoustic_axis[1] = 1
                    elif(x<= i and (i<=(r*np.cos(np.pi/6) +x + epsilon) or i<=(r*np.cos(np.pi/6) +x-epsilon))):
                        #3rd quadrant
                        if(y >= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/6) +j-epsilon))):
                            #self.grid.set_position(i,j, SMALL_WEIGHT)  
                            if(self.grid.get_position(i,j) > 0 ):
                                self.acoustic_axis[2] = 1
                        #4th quadrant                        
                        elif(y<= j and (j<=(r*np.sin(np.pi/6) + y + epsilon) or j<=(r*np.sin(np.pi/6) +j-epsilon))):
                            #self.grid.set_position(i,j, SMALL_WEIGHT)
                            if(self.grid.get_position(i,j) > 0):
                                self.acoustic_axis[3] = 1
                    #self.grid.set_position(i,j, 100+j*10)
    
        return self.acoustic_axis
            
class robot():

    def __init__(self,G):    

        self.grid = G
        
        self.sensor = sensor(self.grid.size, self.grid)
        self.coordinates = [X_COORD, Y_COORD]
        self.window_size = WINDOW_SIZE
    
    def update_robot_grid(self):
        x = self.coordinates[0]
        y = self.coordinates[1]
        
        r = RADIUS
        ep = EP      
        w = self.update_window(self.window_size,1)

        #because the of the size of box
        #This sees if anything is in the radius of the robot, but an accuracy 
        #based on how we increment r, in this case we're incrementing by 3 so it 
        #see's if anything is in the radius 3 away
        for i in xrange(5):
            print self.sensor.is_object_in_field_sensor(x, y, r, ep ,w)
            ep += 5
            r += 3
    
    #specify 0 args to delete window, and non-zero args to draw window
    def update_window(self, window_size, delete):
        x0 = self.coordinates[0] - window_size/2
        x1 = self.coordinates[0] + window_size/2
        y0 = self.coordinates[1] - window_size/2
        y1 = self.coordinates[1] + window_size/2
        xVals = [x0, x1]
        yVals = [y0, y1]
        window = [xVals, yVals]
        if(delete != 0):
            for i in range (xVals[0], xVals[1]):
                    self.grid.set_position(i,yVals[0], 1000)
                    self.grid.set_position(i,yVals[1], 1000)
            for i in range (yVals[0], yVals[1]):
                    self.grid.set_position(xVals[0], i, 1000)
                    self.grid.set_position(xVals[1], i , 1000)
            return window
        if(delete == 0):
            for i in range (xVals[0], xVals[1]):
                    self.grid.set_position(i,yVals[0], 0)
                    self.grid.set_position(i,yVals[1], 0)
            for i in range (yVals[0], yVals[1]):
                    self.grid.set_position(xVals[0], i, 0)
                    self.grid.set_position(xVals[1], i , 0)
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
        #deletes the window frame of the robot, so it doesn't see values
        self.update_window(self.window_size, 0)
        #moves it somehow, right now just goingin along -1, -1
        self.coordinates[0] -= 1
        self.coordinates[1] -= 1
        #updates the robot grid
        self.update_robot_grid()
        
    def check_radii(self):
        x = self.coordinates[0]
        y = self.coordinates[1]
        r = RADIUS
        ep = EP
        w = self.update_window(self.window_size,1)
        directions = {}
        for i in xrange(5):
            directions[i] = [(str(j+1),self.sensor.is_object_in_field_sensor(x, y, r, ep ,w)[j])for j in range(4)]
            ep += 5
            r += 3
        return self.choose_next_step(directions)

    def choose_next_step(self,directions):
        weight = 100
        for r in directions:
            for d in directions[r]:
                d = (d[0], d[1] * weight)
            weight = weight / 2
         
        ranked_dirs = {}
        ranked_dirs['1'] = 0
        ranked_dirs['2'] = 0
        ranked_dirs['3'] = 0
        ranked_dirs['4'] = 0
        for r in directions:
            for d in directions[r]:
                ranked_dirs[d[0]] = ranked_dirs[d[0]] + d[1]
                 
        sorted_ranked_dirs = sorted(ranked_dirs)
        return sorted_ranked_dirs[0]
                 
        
                 

        
            

        

        
class simulation():
    def __init__(self):
        self.size = 200
        self.grid = grid(self.size)
        self.A = robot(self.grid) 
    def draw_boundaries_of_frame(self):
        for i in range (0, self.size):
                self.grid.set_position(i,0, MAX_WEIGHT)
                self.grid.set_position(i,self.size-1, MAX_WEIGHT)
        for i in range (0,self.size):
                self.grid.set_position(0, i, MAX_WEIGHT)
                self.grid.set_position(self.size-1, i , MAX_WEIGHT)
    
    
        
    def run(self):    
        self.draw_boundaries_of_frame()
        '''
        object_array = []
        box_size = BOX_SIZE       
        n_obstacles = N_OBSTACLES
        
        min_val = box_size
        max_val = self.size - box_size
        
        for i in range(n_obstacles):
            while True:
                x0 = (np.random.randint(0, MAX_RAND_VAL))
                x1 = x0+box_size
                y0 = np.random.randint(0, MAX_RAND_VAL)
                y1 = y0+box_size
                if(x0>min_val and y0 >min_val and x1<max_val and y1 <max_val):
                    break
            ob = obstacle(self.grid, [[x0,x1], [y0,y1]])
            object_array.append(ob)
            ob.place_object()

            #place object in the frame of the object, used for debugging            
        '''        
        ob = obstacle(self.grid, [[40,60],[40,60]])
        ob.place_object()
        pos = self.A.check_radii()
        print "Robot's next positon: " + str(pos)
        print "Should be 1,2, or 3"
        ob.delete_object()
        ob = obstacle(self.grid, [[0,20],[0,20]])
        ob.place_object()
        
        
            

fig = plt.figure()       
A = simulation()
A.run()

plt.imshow(A.grid.grid)
