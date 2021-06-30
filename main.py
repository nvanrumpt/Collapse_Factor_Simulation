from gas_particle import GasParticle
from tank import Tank
from environment import Environment
import matplotlib.pyplot as plt
from random import random
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np
import tqdm
import math
import csv

A = 6.02*10**23
N = 1 * A #blob particle size
k = 1.38065*10**-23
temp = 464 #kelvin
energy = N * 3/2 * k * temp
mass = N * 6.6464731*10**-27
atomic_size = 0.0001

w = 0.2032 #m
l = 0.69 #m


fill_density = 1141 #kg/m**3
fill_mass = math.pi*(w/2)**2 * l *fill_density * 0.9 #kg
fill_temp = 90 #K
tank_CdA = 1.7 * 10**-2


sim_time_tot = 18 #sec
dt = 3*10**-5 #sec

target_pressure = 2.6 * 10**6 #Pa

t = Tank(w,l)
env = Environment(t, dt, N)


def initialize_simulation():
    t.fill_tank(mass=fill_mass,density=fill_density,temp=fill_temp)
    t.CdA = tank_CdA
    while env.pressure() < target_pressure:
        env.add_particle(GasParticle(atomic_size,mass,energy,-w/2 + w*random(), -w/2 + w*random(), t.fill_height() + (l-t.fill_height())*random() ))

def run_simulation():
    history = []
    sim_time = 0
    times = np.arange(0,sim_time_tot,dt)

    for i in tqdm.tqdm(range(len(times))):
        while env.pressure() < target_pressure:
            p = GasParticle(atomic_size,mass,energy,0,0,l)
            p.set_dir(2*math.pi*random(),2*math.pi*random())
            env.add_particle(p)
        env.step()
        if i % 1000 == 0:
            pos_rs = [p.pos_x for p in env.particles]
            pos_zs = [p.pos_z for p in env.particles]
            tank_height = t.fill_height()
            press = env.pressure()
            temp = env.gas_temp()
            num_part = len(env.particles)
            history.append([sim_time,pos_rs,pos_zs,tank_height,press,temp,num_part])
        sim_time += dt
    return history

def init():
    sim_time_artist = ax2.text(0.5, 0.5, "0", size=20)
    return particle_pos_artist, fill_patch_artist, sim_time_artist

def show_sim(i):
    sim_time_artist.set_text("Sim Time: " + "{:.4f}".format(history[i][0]) + " sec")
    pressure_artist.set_text("Pressure: " + "{:.2f}".format(history[i][4]/1000) + " kPa")
    temp_artist.set_text("Temp: " + "{:.1f}".format(history[i][5]) + " K")
    num_part_artist.set_text("Num: " + "{:.2e}".format(history[i][6]*N/A) + " mol")
    particle_pos_artist.set_data(history[i][1], history[i][2])
    fill_patch_artist.set_height(history[i][3])
    return particle_pos_artist, fill_patch_artist, sim_time_artist, pressure_artist, temp_artist, num_part_artist

initialize_simulation()
history = run_simulation()

with open("results.csv","w",newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Time","Fill","Pressure","Temp","Num"])
    for step in history:
        writer.writerow([step[0],step[3],step[4],step[5],step[6]*N/A])

fig = plt.figure(figsize=(8,6))

ax1 = plt.subplot2grid((3,3),(0,0), colspan=2, rowspan=3)
tank_patch = patches.Rectangle((-t.rad,0),t.rad*2,t.length,fill=False)
ax1.add_patch(tank_patch)
particle_pos_artist, = ax1.plot([],[],'bo')
fill_patch = patches.Rectangle((-t.rad,0),t.rad*2,t.length,fill=True)
fill_patch_artist = ax1.add_patch(fill_patch)

ax2 = plt.subplot2grid((3,3),(0,2))
sim_time_artist = ax2.text(0, 0, "", size=10)
pressure_artist = ax2.text(0, 0.25, "", size=10)
temp_artist = ax2.text(0,0.50,"",size = 10)
num_part_artist = ax2.text(0,0.75,"",size=10)

ani = animation.FuncAnimation(fig,show_sim,frames=len(history),interval=10,blit=True, init_func=init)
plt.show()

f = r"c://Users/natha/Desktop/animation_scuba.gif" 
writergif = animation.PillowWriter(fps=30) 
ani.save(f, writer=writergif)