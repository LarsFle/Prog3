#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 19:32:02 2017

@author: pyoneer
"""
import math

import numpy as np

from logic import Logic
from _operator import pos

GRAVITY_ACC = 6.67384*10**(-11)
class System(object):
    def __init__(self):
        self.bodylist = []
        self.locallistpos = []
        self.system_logic = Logic()
        
        self.scale = 1
        
    def add_centre(self, body):
        self.bodylist.insert(0, body)
        
    def add_planet(self, body, pos):
        self.bodylist.append(body)
        self.locallistpos.append(pos)
        self.update_scale(pos)
        
    def update_scale(self, pos):
        if abs(pos[0]) > self.scale:
            self.scale = abs(pos[0])
        if abs(pos[1]) > self.scale:
            self.scale = abs(pos[1])
        if abs(pos[2]) > self.scale:
            self.scale = abs(pos[2])
        
    def get_sum_mass(self):
        mass = 0
        for bodys in range(0, len(self.bodylist)):
            mass += self.bodylist[bodys].get_mass()
        return mass
    
    def get_sum_pos(self):
        pos = (0, 0, 0)
        for bodys in range(0, len(self.bodylist)):
            pos = (self.bodylist[bodys].get_pos_x()+pos[0], self.bodylist[bodys].get_pos_y()+pos[1], self.bodylist[bodys].get_pos_z()+pos[2])
        return pos
    
    def get_mass_centre(self):
        summ = np.array((0,0,0), dtype=np.float64)
        
        totalmass = self.get_sum_mass()
        for bodys in range(0, len(self.bodylist)):
            summ = summ + self.bodylist[bodys].get_mass()*self.bodylist[bodys].get_pos()
        summ = summ / totalmass
        return summ
        

    def get_mass_centre_planet(self, exbody):
        summ = np.array((0,0,0), dtype=np.float64)
        totalmass = self.get_sum_mass()
        for bodys in range(0, len(self.bodylist)):
            if (self.bodylist[bodys] != exbody):
                summ = summ + self.bodylist[bodys].get_mass()*self.bodylist[bodys].get_pos()
        summ = summ / totalmass
        return summ
    
    def get_initial_speed(self):
        for bodys in range(1, len(self.bodylist)):
            """it does something!! woohoo"""
            formr = self.get_mass_centre()-self.get_mass_centre_planet(self.bodylist[bodys])
            formr = np.linalg.norm(formr)
            summass = self.get_sum_mass()
            leftpart = ((summass-self.bodylist[bodys].get_mass())/summass)
            rightpart = math.sqrt((GRAVITY_ACC*summass)/formr)
            ispd = leftpart*rightpart
            self.bodylist[bodys].set_speed(ispd)

    def get_initial_direction(self):
        for bodys in range(1, len(self.bodylist)):
            """it does somehting woooohoooo!"""
            formr = np.array(self.get_mass_centre()-self.get_mass_centre_planet(self.bodylist[bodys]), dtype=np.float64)
            formz = np.array([0, 0, 1], dtype=np.float64)
            idir = np.cross(formr, formz)/np.linalg.norm((np.cross(formr, formz)))
            self.bodylist[bodys].set_dir(idir)

    def do_step(self, delta_time):
        self.get_initial_direction()
        self.get_initial_speed()

        lis = []
        for i in range(0, len(self.bodylist)):
            """do something"""
            lis.append(self.system_logic.planet_new_position(self.bodylist[i], delta_time, self))
        for i in range(0, len(self.bodylist)):
            self.bodylist[i].position = lis[i]
