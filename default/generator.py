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
        """

        :param bodyamount: Anzahl der Körper
        :param minmass: minimale Masse des jeweiligen Körpers
        :param maxmass: maximale Masse ""
        :param minrad: minimaler Radius
        :param maxrad: maximaler Radius
        :param scale: Skalierung, für GUI relevant
        :param centermass: Masse des Zentrums
        :param centerrad: Radius des Zentrums
        :return:
        """
        sys = system.System()
        
        sys.add_centre(body.Body(centermass, centerrad, scale, maxrad))
        
        for _ in range(1, bodyamount):
            newmass = random.random()*(maxmass-minmass)+minmass
            newrad = random.random()*(maxrad-minrad)+minrad
            newdir = np.array((random.random()*2-1, random.random()*2-1))
            newpos = np.array(((random.random()*2-1)*scale, (random.random()*2-1)*scale, 0), dtype=np.float64)
            sys.add_planet(body.Body(newmass, newrad, scale, maxrad, newdir, newpos), newpos)
        
        return sys

    @staticmethod
    def generate_solar_system():
        sys = system.System()
        centermass = 1.98 * 10 ** 30
        centerrad = 6.96 * 10 ** 8
        scale = 1
        maxrad = 6.96 * 10 ** 8
        sys.add_centre(body.Body(centermass, centerrad, scale, maxrad))
        newdir = np.array((random.random()*2-1, random.random()*2-1), dtype = np.float64)

        newmass = 3.30 * 10 ** 23
        newrad = 4879 * 5 ** 3
        maxrad = 4879 * 5 ** 3
        scale = 1
        newpos =  np.array((58 * 10 ** 9, 0, 0), dtype = np.float64)
        sys.add_planet(body.Body(newmass, newrad, scale, maxrad, newdir, newpos), newpos) # Merkur

        newmass = 4.87 * 10 ** 24
        newrad = 12103 * 5 ** 3
        maxrad = 12103 * 5 ** 3
        scale = 1
        newpos = np.array((0, 108 * 10 ** 9, 0), dtype = np.float64)
        sys.add_planet(body.Body(newmass, newrad, scale, maxrad, newdir, newpos), newpos) # Venus

        newmass = 5.97 * 10 ** 24
        newrad = 12735 * 5 ** 3
        maxrad = 12735 * 5 ** 3
        scale = 1
        newpos = np.array((150 * 10 ** 9, 0, 0), dtype=np.float64)
        sys.add_planet(body.Body(newmass, newrad, scale, maxrad, newdir, newpos), newpos) # Erde

        newmass = 6.42 * 10 ** 23
        newrad = 6772 * 5 ** 3
        maxrad = 6772 * 5 ** 3
        scale = 1
        newpos = np.array((0, 228 * 10 ** 9, 0), dtype=np.float64)
        sys.add_planet(body.Body(newmass, newrad, scale, maxrad, newdir, newpos), newpos) # Mars

        newmass = 1.9 * 10 ** 27
        newrad = 138346 * 5 ** 3
        maxrad = 138346 * 5 ** 3
        scale = 1
        newpos = np.array((778 * 10 ** 9, 0, 0), dtype=np.float64)
        sys.add_planet(body.Body(newmass, newrad, scale, maxrad, newdir, newpos), newpos) # Jupiter

        newmass = 5.69 * 10 ** 26
        newrad = 114632 * 5 ** 3
        maxrad = 114632 * 5 ** 3
        scale = 1
        newpos = np.array((0, 1433 * 10 ** 9, 0), dtype=np.float64)
        sys.add_planet(body.Body(newmass, newrad, scale, maxrad, newdir, newpos), newpos) # Saturn

        newmass = 8.68 * 10 ** 25
        newrad = 50532 * 5 ** 3
        maxrad = 50532 * 5 ** 3
        scale = 1
        newpos = np.array((2872 * 10 ** 9, 0, 0), dtype=np.float64)
        sys.add_planet(body.Body(newmass, newrad, scale, maxrad, newdir, newpos), newpos)  # Uranus

        newmass = 1.02 * 10 ** 26
        newrad = 49105 * 5 ** 3
        maxrad = 49105 * 5 ** 3
        scale = 1
        newpos = np.array((0, 4495 * 10 ** 9, 0), dtype=np.float64)
        sys.add_planet(body.Body(newmass, newrad, scale, maxrad, newdir, newpos), newpos)  # Neptun

        return sys



