#! /usr/bin/env python3
###############################################################################
#
#	Title   : main.py
#	Author  : Matt Muszynski
#	Date    : 12/23/17
#	Synopsis: Wrapper script for explorer
#
###############################################################################

import sys
sys.path.insert(0, 'classes')
sys.path.insert(0, 'prop')
sys.path.insert(0, 'fsw')
sys.path.insert(0, 'util')

import vehicles, celestialBodies, simScenario
from constants import au
from numpy import array, argmax, argmin, sqrt
import matplotlib.pyplot as plt
from timeFcn import timeConvert
import pdb

#initialize stock bodies
sun = celestialBodies.celestialBody()
sun.initSun()
earth = celestialBodies.celestialBody()
earth.initEarth()
venus = celestialBodies.celestialBody()
venus.initVenus()
mars = celestialBodies.celestialBody()
mars.initMars()
jupiter = celestialBodies.celestialBody()
jupiter.initJupiter()
saturn = celestialBodies.celestialBody()
saturn.initSaturn()
uranus = celestialBodies.celestialBody()
uranus.initUranus()
neptune = celestialBodies.celestialBody()
neptune.initNeptune()
pluto = celestialBodies.celestialBody()
pluto.initPluto()

#initialize spacecraft
explorer1 = vehicles.spacecraft()
explorer1.name = 'Explorer 1'
explorer1.initialState = array([7000,0,0,0,7.5460532901075412,0])


#initialize sim scenario
scen = simScenario.simScenario()
# scen.addSpacecraft([explorer1])

scen.addCentralBody(earth)
scen.addNonGravBod([
	sun, venus, mars, jupiter, saturn, uranus, neptune, pluto
	])

# scen.addGravBod([sun,earth])
scen.jdEpoch = 2451545.0 + 100
scen.jdEndTime = scen.jdEpoch + 365*250
scen.timeStep = 100
pdb.set_trace()
scen.propagate()

	
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.show()
# plt.plot(explorer1.stateHistory[:,0],explorer1.stateHistory[:,1])
plt.plot([0,0],[0,0],'x')
plt.axis('equal')
plt.figure()
# plt.plot(explorer1.stateHistory[:,0] + earth.stateHistory[:,0],explorer1.stateHistory[:,1] + earth.stateHistory[:,1],'g')
plt.plot(scen.centralBody.stateHistory[:,0],
	scen.centralBody.stateHistory[:,1],'b')
for bod in scen.nonGravBodList:
	plt.plot(bod.stateHistory[:,0],bod.stateHistory[:,1],label=bod.name)

plt.plot([0,0],[0,0],'x')

plt.axis('equal')

plt.show()
plt.legend()
pdb.set_trace()






# fig, ax = plt.subplots()
# xdata, ydata = [], []
# earthLn, = plt.plot([], [], 'bo', animated=True)
# explorer1Ln, = plt.plot([], [], 'go', animated=True)


# def init():
#     ax.set_xlim(-2e8, 2e8)
#     ax.set_ylim(-2e8, 2e8)
#     return earthLn, explorer1Ln

# def earthUpdate(frame):
#     xdata.append(earth.stateHistory[:,0][frame])
#     ydata.append(earth.stateHistory[:,1][frame])
#     earthLn.set_data(xdata, ydata)
#     return earthLn,

# def explorer1Update(frame):
#     xdata.append(explorer1.stateHistory[:,0][frame])
#     ydata.append(explorer1.stateHistory[:,1][frame])
#     explorer1Ln.set_data(xdata, ydata)
#     return explorer1Ln,

# ani1 = FuncAnimation(fig, earthUpdate, frames=range(0,len(scen.timeHistory)),
#                     init_func=init, blit=True)

# ani2 = FuncAnimation(fig, explorer1Update, frames=range(0,len(scen.timeHistory)),
#                     init_func=init, blit=True)
