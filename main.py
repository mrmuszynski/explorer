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
from numpy import array, argmax, argmin
import matplotlib.pyplot as plt
from timeFcn import timeConvert
import pdb

#initialize spacecraft
explorer1 = vehicles.spacecraft()
explorer1.name = 'Explorer 1'
explorer1.initialState = array([au,0,0,0,29784,0])

#initialize stock bodies
sun = celestialBodies.celestialBody()
sun.initSun()
venus = celestialBodies.celestialBody()
venus.initVenus()
earth = celestialBodies.celestialBody()
earth.initEarth()
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

#initialize sim scenario
scen = simScenario.simScenario()
# scen.addSpacecraft([explorer1])
scen.addNonGravBod([
	# venus, earth, mars, jupiter, saturn, uranus, neptune, pluto
	earth
	])
scen.addGravBod([sun])
# scen.addGravBod([sun,earth])
scen.jdEndTime = 2451545.0 + 365
scen.timeStep = 0.1
scen.propagate()

for bod in scen.nonGravBodList:
	plt.plot(bod.stateHistory[:,0],bod.stateHistory[:,1],label=bod.name)

# argmax(earth.stateHistory[:,0])
# argmax(earth.stateHistory[:,1])
# argmin(earth.stateHistory[:,0])
# argmin(earth.stateHistory[:,2])

plt.legend()
pdb.set_trace()