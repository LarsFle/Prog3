'''
Created on 26.11.2017

@author: felicool98
'''
import numpy as np
import random
import body
from system import System
import math

class default_gen:
    @staticmethod
    def generate(bodyamount, minmass, maxmass, minrad, maxrad, scale, centermass, centerrad):
        sys = System()
        
        sys.add_centre(body.Body(centermass, centerrad, scale, maxrad,r=1.0, g=1.0,b=0))
        
        for _ in range(1, bodyamount):
            density = random.random()*(maxmass-minmass)+minmass
            
            newrad = random.random()*(maxrad-minrad)+minrad
            volume = 4/3*math.pi*newrad**3
            newmass = volume*density
            
            newdir = np.array((random.random()*2-1, random.random()*2-1))
            
            angle = 2*random.random()*math.pi
            radius = random.random()
            
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            
            newpos = np.array((x*scale, y*scale, (random.random()*2-1)*scale/10), dtype=np.float64)
            
            r = random.random()
            g = random.random()
            b = random.random()
            
            sys.add_planet(body.Body(newmass, newrad, maxrad, newdir, newpos, r=r, g=g, b=b), newpos)
        
        return sys