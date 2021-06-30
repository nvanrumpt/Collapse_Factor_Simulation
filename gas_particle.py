from random import random
import math


class GasParticle():

    def __init__(self, size, mass, energy, x, y, z):
        '''
        Initializes an ideal gas particle with an initial energy

        Params: size, mass, energy, x, y, z
        '''
        self.size = size
        self.energy = energy

        self.pos_x = x
        self.pos_y = y
        self.pos_z = z
    
        self.mass = mass #kg mass of helium

        self.set_dir(2 * math.pi * random(),2 * math.pi * random())

    def set_dir(self,dir_r,dir_z):
        self.dir_r = dir_r % (2 * math.pi)
        self.dir_z = dir_z % (2 * math.pi)

    def step(self, timestep):
        dx = self.velocity() * timestep * math.cos(self.dir_z) * math.cos(self.dir_r)
        dy = self.velocity() * timestep * math.cos(self.dir_z) * math.sin(self.dir_r)
        dz = self.velocity() * timestep * math.sin(self.dir_z)
        self.pos_x += dx
        self.pos_y += dy
        self.pos_z += dz

    def velocity(self):
        return math.sqrt(2 * self.energy / self.mass)
