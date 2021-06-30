from gas_particle import GasParticle
import math

class Tank():

    def __init__(self, dia, length, fill_mass = 0, fill_density = 0, CdA = 0,fill_temp=0,wall_temp=200):
        self.rad = dia/2
        self.length = length
        self.tank_vol = math.pi * self.rad**2 * self.length

        self.fill_mass = fill_mass
        self.fill_density = fill_density
        self.fill_temp=fill_temp
        self.wall_temp=wall_temp
        self.CdA = CdA

    def ullage_vol(self):
        return math.pi * self.rad**2 * (self.length - self.fill_height())

    def fill_height(self):
        if self.fill_mass <= 0:
            return 0
        else:
            percent_full = self.fill_mass/self.fill_density/self.tank_vol
            return self.length * percent_full

    def fill_tank(self, mass, density,temp):
        fill_vol = mass / density
        if fill_vol > self.tank_vol:
            return False
        else:
            self.fill_mass = mass
            self.fill_density = density
            self.fill_temp=temp
            return True


    

