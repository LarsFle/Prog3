import math

import numpy as np  # Enthält numpy bzw. Vektor-Arrays und viele nützliche Funktionen zur Vektor-Berechnung

import system

GRAV_ACC = 6.672 * 10**(-11)
"""
GRAV ACC = Gravitationsbeschleunigung G (2)
"""
class Logic:
    def planet_new_position(self, planet, delta_time, galaxy):
        """
        Finale Formel, die neue Position der Planeten berechnet
        :param planet:
        :param delta_time: Zeit zwischen 2 Schritten
        :param speed_pos:
        :return: neue Position
        """
        galaxy.get_initial_direction()
        galaxy.get_initial_speed()
        speed = self.get_speed(planet, delta_time, galaxy)
        part1 = planet.position + np.multiply(delta_time, speed)
        part2 = (delta_time*delta_time)/2 * self.get_acceleration(planet, galaxy)

        new_position = np.add(part1, part2)
        planet.position = new_position
        return planet.position

    def single_grav_force(self, current_planet, other_planet):
        """
        to Do: Test, ob return wirklich Numpy-Array ist
        :param current_planet:
        :param other_planet:
        :return:
        """
        r2_r1 = np.subtract(other_planet.get_pos(), current_planet.get_pos())
        result = GRAV_ACC * current_planet.get_mass() * other_planet.get_mass() / ((np.linalg.norm(r2_r1)**3) * r2_r1)
        return result

    def grav_force(self, current_planet, galaxy):
        total_grav_force = np.array((0, 0, 0), dtype=np.float16)
        for body in galaxy.bodylist:
            if(body != current_planet):
                single_force = self.single_grav_force(current_planet, body)
                total_grav_force += single_force
        return total_grav_force

    def get_acceleration(self, planet, galaxy):
        """

        :param planet:
        :return:
        """
        acc = np.divide(self.grav_force(planet, galaxy), planet.mass)
        print('acceleration: '+str(acc))
        return acc

    def get_speed(self, planet, delta_time, galaxy):
        """mass_centre = galaxy.get_mass_centre_planet(planet)"""


        abs_speed = planet.get_speed()
        dir_speed = planet.get_dir()
        initial_speed = dir_speed * abs_speed
        delta_speed = np.multiply(self.get_acceleration(planet, galaxy), delta_time)
        speed = np.add(initial_speed, delta_speed)
        print('Speed: '+str(speed))
        return speed



    # def total_mass_centre(self):
    #     """
    #     Methode zur Berechnung des Massenschwerpunkts
    #     (4)
    #     muss noch mitNumpy optimiert werden
    #     :param total_mass: Gesamtmasse des Systems
    #     :return: Massenschwerpunkt
    #     """
    #     total_mass_centre = np.array((0,0,0), dtype = np.float16)
    #
    #     for planet in Data.planet_list:
    #         total_mass_centre += np.multiply(planet.position, planet.mass)
    #         total_mass_centre /= Simulation.total_mass
    #     return total_mass_centre
    #
    #
    #
    # def planet_mass_centre(self, planet):
    #
    #     individual_mass_centre = np.array((0, 0, 0), dtype = np.float16)
    #
    #     for body in Data.planet_list:
    #         if(body != planet):
    #             individual_mass_centre += np.multiply(body.position, body.mass)
    #             individual_mass_centre /= Simulation.total_mass
    #     return individual_mass_centre
    #
    #
    # def planet_speed_pos(self, planet, planet_mass_centre):
    #     """
    #     Berechnet (Ri - Rs,i) wird in den beiden unteren Funktionen verwendet
    #     mit Numpy optimiert
    #     :param planet: übergebenes Planet Objekt
    #     :param planet_mass_centre: individueller Masseschwerpunkt für übergebenen Planeten
    #     :return: Ergebnis von (Ri - Rs,i)
    #     """
    #     speed_pos = planet.position - planet.mass_centre
    #     return speed_pos
    #
    # def planet_abs_speed(self, planet,  planet_mass_centre, total_mass, speed_pos):
    #     """
    #     Berechnet die Geschwindigkeit eines Planeten als Betrag
    #     (8)
    #     mit Numpy optimiert
    #     :param planet: übergebenes Planeten-Objekt
    #     :param planet_mass_centre: individueller Masseschwerpunkt ohne Planet
    #     :param total_mass: Gesamtmasse
    #     :param speed_pos: Code-Bestandteil, zur Vermeidung von Code-Duplikation ausgelagert, siehe oben
    #     :return: Geschwindigkeit als Betrag
    #     """
    #     speed_factor1 = (total_mass - planet.mass) / Simulation.total_mass
    #
    #
    #     speed_pos_abs = math.hypot(speed_pos[0], (math.exp(speed_pos[1], 2) + math.exp(speed_pos[2], 2)))
    #     speed_factor2 = math.sqrt((GRAV_ACC * Simulation.total_mass) / speed_pos_abs)
    #
    #     abs_speed = math.fabs(speed_factor1 * speed_factor2)
    #     return abs_speed
    #
    # def planet_direction_vector(self, speed_pos):
    #     """
    #
    #     :param speed_pos:
    #     :return:
    #     """
    #     z = np.array((0, 0, 1), dtype=np.float16)
    #     direction_formula = np.cross(speed_pos, z) / np.linalg.norm(np.cross(speed_pos, z))
    #     return direction_formula








