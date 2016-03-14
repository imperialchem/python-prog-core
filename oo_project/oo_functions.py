import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import display, clear_output
import time 
import numpy as np
import pyximport; pyximport.install()
from oo_fast_functions import Vector

class Particle():
    def __init__(self, position, momentum, radius, mass):
        self.position = position
        self.momentum = momentum
        self.radius = radius
        self.mass = mass
        
    def velocity(self):
        return self.momentum/self.mass
    
    def overlap(self, other):
        displacement = self.position - other.position
        return displacement.norm() < (self.radius + other.radius)

def animate_trajectory(s,loop=False):

        def update_frame(i, frame):
            x = [p.x for p in s.trajectory[i]]
            y = [p.y for p in s.trajectory[i]]
            frame.set_data([x,y])
            return frame,

        no_steps = len(s.trajectory)
        particle_size = s.particles[0].radius * 12
        try: 
            length = s.box_length /10
        except AttributeError:
            length = 10

        fig = plt.figure(figsize=(length,length))

        frame, = plt.plot([],[],  c='b',linestyle='', marker='o',markersize=particle_size ) # initialise plot

        try:
            plt.xlim(-2, s.box_length+2) # set x and y limits with a bit of extra padding
            plt.ylim(-2, s.box_length+2)
        except AttributeError:
            plt.xlim(-2, 102) # set x and y limits with a bit of extra padding
            plt.ylim(-2, 102)

        frame_ani = animation.FuncAnimation(fig, update_frame, no_steps, fargs=(frame,),
                                           interval=5, blit=True, repeat=loop)

        plt.show()

def clunky_display_frame(s):
    clear_output(wait=True)
    try:
        fig = s.fig
        ax = s.ax
        frame = s.frame
    except AttributeError:
        plt.ion()
        s.fig = plt.figure(figsize=(10,10))
        s.ax = s.fig.add_subplot(111)
        s.ax.set_xlim(-2, s.box_length+2) # set x and y limits with a bit of extra padding
        s.ax.set_ylim(-2, s.box_length+2)
        s.frame, = s.ax.plot([],[],c='b',linestyle='', marker='o',markersize=16.5)
        fig=s.fig
        ax=s.ax
        frame=s.frame
        plt.show(False)

    particle_x = [p.position.x for p in s.particles]
    particle_y = [p.position.y for p in s.particles]

    frame.set_data([particle_x,particle_y])
    #fig.canvas.draw()
    plt.show()
    display(fig)

def display_final_speeds(s, bins=10):
    plt.figure(figsize=(10,10))
    speeds = [p.speed() for p in self.particles]
    plt.hist(speeds, bins=bins)
    plt.show()

def display_particle(p):
    plt.figure(figsize=(10,10))
    plt.plot([p.position.x],[p.position.y],marker='o',linestyle='', markersize=12)
    plt.show()

def display_trajectory(positions):
    def update_frame(i, frame):
        x=[positions[i].x]
        y=[positions[i].y]
        frame.set_data([x,y])
        return frame,

    fig = plt.figure(figsize=(10,10))
    no_steps = len(positions) 
    frame, = plt.plot([],[],marker='o',linestyle='', markersize=12)
   
    min_x,max_x = min([p.x for p in positions]), max([p.x for p in positions])
    min_y,max_y = min([p.y for p in positions]), max([p.y for p in positions])

    if min_x != max_x:
        plt.xlim(min_x,max_x)
    if min_y != max_y:
        plt.ylim(min_y,max_y)

    frame_ani = animation.FuncAnimation(fig, update_frame, no_steps, fargs=(frame,), interval=5, blit=True, repeat=False)
    plt.show()


def get_particles(no_particles, box_length, init_momentum=None):
    particles = []
    gen_momentum = init_momentum is None
    for i in range(no_particles):
        init_xy = (np.random.random(2)) * box_length
        init_position = Vector(init_xy[0], init_xy[1])
        
        if gen_momentum:
            init_mxmy = (np.random.random(2)-0.5) * box_length/100
            init_momentum = Vector(init_mxmy[0], init_mxmy[1])
       
        particles.append(Particle(init_position, init_momentum, 1, 1))
    
    return particles

from ipywidgets import interactive
def display_vecs():
    plt.figure()
    def interactive_display(directionx=1.0, directiony=0.0):
        plt.clf()
        vec = Vector(np.float64(3),np.float64(2))

        direction = Vector(directionx,directiony)
        normal = direction/direction.norm()

        normal_component = vec.dot(normal)
    
        remainder = vec - (normal*normal_component)
        tangent = remainder/remainder.norm()
    
        np_vec =np.array( [ [0,0,vec.x,vec.y]]) 
        np_components = np.array( [ [0,0,normal_component*normal.x, normal_component*normal.y], 
                                  [0,0,remainder.x,remainder.y]])

        X1,Y1,U1,V1 = zip(*np_vec)
        X2,Y2,U2,V2 = zip(*np_components)

        ax = plt.gca()
        ax.quiver(X1,Y1,U1,V1,angles='xy',scale_units='xy',scale=1, color='r')
        ax.quiver(X2,Y2,U2,V2,angles='xy',scale_units='xy',scale=1, linestyle='--', color='b')

        ax.set_xlim([-5,5])
        ax.set_ylim([-5,5])
        plt.draw()
        plt.show() 

    return interactive(interactive_display, directionx=(-1,1,0.1), directiony=(-1,1,0.1))
