'''
Created on 26.11.2017

@author: felicool98
'''
import numpy as np
import random
import body
import system

class default_gen:
    @staticmethod
    def generate(bodyamount, minmass, maxmass, minrad, maxrad, scale, centermass, centerrad):
        sys = system.System()
        
        sys.add_centre(body.Body(centermass, centerrad, scale, maxrad,r=0.5, g=0.5,b=0))
        
        for _ in range(1, bodyamount):
            newmass = random.random()*(maxmass-minmass)+minmass
            newrad = random.random()*(maxrad-minrad)+minrad
            newdir = np.array((random.random()*2-1, random.random()*2-1))
            newpos = np.array(((random.random()*2-1)*scale, (random.random()*2-1)*scale, 0), dtype=np.float64)
            r = random.random()
            g = random.random()
            b = random.random()
            sys.add_planet(body.Body(newmass, newrad, scale, maxrad, newdir, newpos,r=r, g=g,b=b), newpos)
        
        return sys