#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 19:32:02 2017

@author: pyoneer
"""
import math, multiprocessing

import numpy as np

from logic import Logic

GRAVITY_ACC = 6.67384*10**(-11)
class System(object):
    def __init__(self):
        self.bodylist = []
        self.locallistpos = []
        self.system_logic = Logic()
        self.sumHelper = 0
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

    def do_step_threaded_init(self, delta_time):
        self.get_initial_direction()
        self.get_initial_speed()
        cpuCount = multiprocessing.cpu_count()
        NeededCalcs = len(self.bodylist)
        CalcsPerProcess = math.floor(NeededCalcs/cpuCount)
        CalcsInFirst = NeededCalcs%cpuCount
        resultQueue = multiprocessing.Queue()
        if CalcsInFirst != 0:
            start_process = multiprocessing.Process(target=self.do_step_threaded, args=(resultQueue, delta_time, 0, CalcsInFirst))
            processes = [multiprocessing.Process(target=self.do_step_threaded, args=(resultQueue, delta_time, CalcsInFirst + i*CalcsPerProcess, CalcsInFirst + i*CalcsPerProcess+CalcsPerProcess)) for i in range(cpuCount) ]
        else:
            start_process = multiprocessing.Process(target=self.do_step_threaded, args=(resultQueue, delta_time, 0, CalcsPerProcess))
            processes = [multiprocessing.Process(target=self.do_step_threaded, args=(resultQueue, delta_time, (i+1)*CalcsPerProcess, (1+i)*CalcsPerProcess+CalcsPerProcess)) for i in range(cpuCount-1) ]
        for t in processes:
            t.start()
            self.sumHelper += 1
        start_process.start()
        self.sumHelper += 1
        for t in processes:
            t.join()
        start_process.join()
        newlis = []
        for t in range(self.sumHelper):
            results = resultQueue.get()
            for i in results:
                newlis.append(i)

        self.bodylist = newlis
        self.sumHelper = 0
        
    def do_step_threaded(self, resultQueue, delta_time, start, finish):
        

        lis = []
        for i in range(start, finish):
            """do something"""
            newpos = self.system_logic.planet_new_position(self.bodylist[i], delta_time, self) 
            newbody = self.bodylist[i]
            newbody.position = newpos
            lis.append(newbody)
        
        resultQueue.put(lis)
        
        
        
    def do_step(self, delta_time):
        self.get_initial_direction()
        self.get_initial_speed()

        lis = []
        for i in range(0, len(self.bodylist)):
            """do something"""
            lis.append(self.system_logic.planet_new_position(self.bodylist[i], delta_time, self))
        for i in range(0, len(self.bodylist)):
            self.bodylist[i].position = lis[i]
