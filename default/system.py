#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 19:32:02 2017

@author: pyoneer
"""
import math
import random

import numpy as np

from logic import Logic

GRAVITY_ACC = 6.67384*10**(-11)
class System(object):
    def __init__(self):
        self.bodylist = []
        self.locallistpos = []
        self.locallistmass = []
        self.system_logic = Logic()
        
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
        sumx = 0
        sumy = 0
        sumz = 0
        totalmass = self.get_sum_mass()
        for bodys in range(0, len(self.bodylist)):
            sumx += self.bodylist[bodys].get_mass()*self.bodylist[bodys].get_pos_x()
            sumy += self.bodylist[bodys].get_mass()*self.bodylist[bodys].get_pos_y()
            sumz += self.bodylist[bodys].get_mass()*self.bodylist[bodys].get_pos_z()
        return np.array((sumx/totalmass, sumy/totalmass, sumz/totalmass))

    def get_mass_centre_planet(self, exbody):
        sumx = 0
        sumy = 0
        sumz = 0
        totalmass = self.get_sum_mass()
        for bodys in range(0, len(self.bodylist)):
            if (self.bodylist[bodys] != exbody):
                sumx += self.bodylist[bodys].get_mass()*self.bodylist[bodys].get_pos_x()
                sumy += self.bodylist[bodys].get_mass()*self.bodylist[bodys].get_pos_y()
                sumz += self.bodylist[bodys].get_mass()*self.bodylist[bodys].get_pos_z()
        return np.array((sumx/totalmass, sumy/totalmass, sumz/totalmass))
    
    def get_initial_speed(self):
        for bodys in range(1, len(self.bodylist)):
            """it does something!! woohoo"""
            formr = self.get_mass_centre()-self.get_mass_centre_planet(self.bodylist[bodys])
            formr = np.linalg.norm(formr)
            summass = self.get_sum_mass()
            leftpart = ((summass-self.bodylist[bodys].get_mass())/summass)
            rightpart = math.sqrt((GRAVITY_ACC*summass)/formr)
            ispd = leftpart*rightpart*10
            self.bodylist[bodys].set_speed(ispd)

    def get_initial_direction(self):
        for bodys in range(1, len(self.bodylist)):
            """it does somehting woooohoooo!"""
            formr = self.get_mass_centre()-self.get_mass_centre_planet(self.bodylist[bodys])
            formz = np.array([0, 0, 1])
            idir = np.cross(formr, formz)/np.linalg.norm((np.cross(formr, formz)))
            self.bodylist[bodys].set_dir(idir)

    def do_step(self, delta_time):
        self.get_initial_direction()
        self.get_initial_speed()
        list = []
        for i in range(0, len(self.bodylist)):
            """do something"""
            list.append(self.system_logic.planet_new_position(self.bodylist[i], delta_time, self))
        for i in range(0, len(self.bodylist)):
            self.bodylist[i].position = list[i]
