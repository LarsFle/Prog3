#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 20:20:31 2017

@author: pyoneer
"""
import numpy as np
class Body(object):
    def __init__(self, mass, radius, maxrad, initdir=-1, initpos=np.array((0,0,0), dtype=np.float64), r=0.2, g=0.2, b=0.2):
        self.mass = mass*1000
        self.radius = radius
        self.speed = 0
        self.dir = initdir
        self.position = initpos
        self.maxrad = maxrad
        self.r = r
        self.g = g
        self.b = b
    def get_mass(self):
        return self.mass
    def get_radius(self):
        return self.radius/self.maxrad/20
    def get_speed(self):
        return self.speed
    def get_dir(self):
        return self.dir
    def get_pos(self):
        return self.position
    def get_pos_x(self):
        return self.position[0]
    def get_pos_y(self):
        return self.position[1]
    def get_pos_z(self):
        return self.position[2]
    def set_speed(self, speed):
        self.speed = speed
    def set_dir(self, direction):
        self.dir = direction
    def set_pos(self, pos):
        self.position = pos
