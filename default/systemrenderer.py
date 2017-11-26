#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 21:14:36 2017

@author: pyoneer
"""
import sys

import numpy as np

import system
from simulation_constants import END_MESSAGE


def get_body_position_and_size(galaxy):
    nr_of_bodies = len(galaxy.bodylist)
    body_array = np.zeros((nr_of_bodies, 4), dtype=np.float64)
    scale = galaxy.bodylist[0].scale
    for body_index in range(nr_of_bodies):
        body_array[body_index][0] = galaxy.bodylist[body_index].get_pos_x()/scale
        body_array[body_index][1] = galaxy.bodylist[body_index].get_pos_y()/scale
        body_array[body_index][2] = galaxy.bodylist[body_index].get_pos_z()/scale
        if (body_index == 0):
            body_array[body_index][3] = 0.1
        else:
            body_array[body_index][3] = galaxy.bodylist[body_index].get_radius()
    return body_array

def startup(sim_pipe, delta_t):
    """
       Initialise and continuously update a position list.
 
       Results are sent through a pipe after each update step
  
       Args:
           sim_pipe (multiprocessing.Pipe): Pipe to send results
           nr_of_bodies (int): Number of bodies to be created and updated.
           delta_t (float): Simulation step width.
    """
        
    galaxy = system.System(20, 0.33*(10**21), 568*(10**21), 2400000, 70000000, 6*(10**11), 2*(10**27), 7*(10**8), 1)
    while True:
        if sim_pipe.poll():
            message = sim_pipe.recv()
            if isinstance(message, str) and message == END_MESSAGE:
                print('simulation exiting ...')
                sys.exit(0)
        galaxy.do_step(delta_t)
        bodies = get_body_position_and_size(galaxy)
        sim_pipe.send(bodies)
