'''
Created on 26.11.2017

@author: felicool98
'''
import numpy as np
import random
from default import body
from default import system

class default_gen:
    @staticmethod
    def generate(bodyamount, minmass, maxmass, minrad, maxrad, scale, centermass, centerrad):
        sys = system.System()
        
        sys.bodylist.append(body.Body(centermass, centerrad, scale, maxrad))
        
        for _ in range(1, bodyamount):
            newmass = random.random()*(maxmass-minmass)+minmass
            newrad = random.random()*(maxrad-minrad)+minrad
            newdir = np.array((random.random()*2-1, random.random()*2-1))
            newpos = np.array(((random.random()*2-1)*scale, (random.random()*2-1)*scale, 0), dtype=np.float64)
            sys.bodylist.append(body.Body(newmass, newrad, scale, maxrad, newdir, newpos))
            sys.locallistpos.append(newpos)
            sys.locallistmass.append(newmass)
        sys.get_initial_speed()
        sys.get_initial_direction()
        
        return sys