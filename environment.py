from gas_particle import GasParticle
from tank import Tank
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import math
from random import random

class Environment():

    def __init__(self, tank, timestep,N):
        '''
        A class to manage the particles within the tank
        '''
        self.tank = tank
        self.particles = []
        self.dt = timestep
        self.time_elapsed = 0
        self.N = N
        self.k = 1.38065*10**-23

    def add_particle(self, particle):
        self.particles.append(particle)

    def step(self):
        #advance particles timestep
        for p in self.particles:
            p.step(self.dt)

        #check particle bounds
        for p in self.particles:
            p_rad = math.sqrt(p.pos_x**2 + p.pos_y**2)
            if p_rad > self.tank.rad:
                self.reflect_r(p)
                self.interact_wall(p)
            if p.pos_z < self.tank.fill_height():
                self.reflect_z(p,z_line=self.tank.fill_height())
                self.interact_fluid(p)
            if p.pos_z > self.tank.length:
                self.reflect_z(p,z_line=self.tank.length)
                self.interact_wall(p)

        #check for particle collisions
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i+1:]: #only need to check the particles after the one we are on
                if self.collision(p1,p2):
                    self.interact(p1,p2)

        if self.tank.fill_mass > 0:
            tank_press = self.pressure()
            mass_flow = self.tank.CdA * math.sqrt(2*tank_press/self.tank.fill_density)
            self.tank.fill_mass -= mass_flow * self.dt

    def interact_fluid(self,p):
        p.energy = self.N * 3/2 * self.k * self.tank.fill_temp


    def interact_wall(self,p):
        p.energy = self.N * 3/2 * self.k * self.tank.wall_temp
        
    def collision(self,p1,p2):
        dx = p1.pos_x - p2.pos_x
        dy = p1.pos_y - p2.pos_y
        dz = p1.pos_z - p2.pos_z
        dr = math.sqrt(dx**2 + dy**2 + dz**2)
        return dr < p1.size + p2.size

    def interact(self,p1,p2):
        #share energy
        e_tot = p1.energy + p2.energy
        rand = random()
        p1.energy = rand * e_tot
        p2.energy = (1-rand) * e_tot

        #swap their directions, crude 
        dr = p1.dir_r
        dz = p1.dir_z
        p1.set_dir(p2.dir_r, p2.dir_z)
        p2.set_dir(dr,dz)

    def reflect_r(self, particle):
        '''
        Reflects the position and the velocity of particle across x=x_line
        '''
        diff = 2*(self.tank.rad - math.sqrt(particle.pos_x**2 + particle.pos_y**2))
        particle.pos_x += diff * math.cos(particle.dir_z) * math.cos(particle.dir_r)
        particle.pos_y += diff * math.cos(particle.dir_z) * math.sin(particle.dir_r)
        
        particle.set_dir(particle.dir_r + math.pi, particle.dir_z)

    def reflect_z(self, particle, z_line):
        '''
        Reflects the position and the velocity of particle across y_line
        '''
        particle.pos_z -= 2*(particle.pos_z - z_line)
        particle.set_dir(particle.dir_r, particle.dir_z + math.pi)

    def total_energy(self):
        U = 0
        for p in self.particles:
            U += p.energy
        return U

    def pressure(self):
        return 2/3 * self.total_energy()/self.tank.ullage_vol()

    def gas_temp(self):
        return self.pressure() * self.tank.ullage_vol() / (self.N * len(self.particles) * self.k)
