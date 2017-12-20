#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 19:32:02 2017

@author: pyoneer
"""
import math
import multiprocessing
import numpy as np
from FrozenSystem import FrozenSystem as FrozenSystem
from Client import Client as Client

import logic

GRAVITY_ACC = 6.67384*10**(-11)
class System(object):
    def __init__(self):
        self.bodylist = []
        self.locallistpos = []
        self.inputQueue = multiprocessing.Queue()
        self.outputQueue = multiprocessing.JoinableQueue()
        self.Clients = []
        for i in range(multiprocessing.cpu_count()):
            c = Client(i, self.outputQueue,self.inputQueue)
            self.Clients.append(c)
            c.createJob()
            print('Client created ID: '+str(c.myID))
        
    def add_centre(self, body):
        self.bodylist.insert(0, body)
        
    def add_planet(self, body, pos):
        self.bodylist.append(body)
        self.locallistpos.append(pos)
        
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

        fSys = FrozenSystem()
        fSys.deepcopySystem(self)



        #for body in self.bodylist:
            #body.move(delta_time,fSys)

        l = []
        x = 0
        for i in range(multiprocessing.cpu_count()):
            ls = []
            while len(ls) <= len(self.bodylist)/multiprocessing.cpu_count():
                if(x <len(self.bodylist)):
                    ls.append(self.bodylist[x])
                    x = x + 1
                else:
                    break
            l.append(ls)

        for lists in l:
            stuff = (lists,delta_time,fSys)
            self.outputQueue.put(stuff)


        self.outputQueue.join()



        blist = []
        for i in range(len(l)):
            lis = self.inputQueue.get()
            for elem in lis:
                blist.append(elem)



        for bA in self.bodylist:
            for bB in blist:
                if bA.bodyID == bB.bodyID:
                    bA.set_pos(bB.get_pos())






