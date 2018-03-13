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
sys.path.insert(0, '../classes')
sys.path.insert(0, '../prop')
sys.path.insert(0, '../fsw')
sys.path.insert(0, '../../lib')

import matplotlib.pyplot as plt
import pdb
from numpy import savez
import celestialBodies
import orbits as o
from timeFcn import timeConvert, day2sec
from analysisTools import porkchopPlot

earth = celestialBodies.celestialBody()
jupiter = celestialBodies.celestialBody()
pluto = celestialBodies.celestialBody()
sun = celestialBodies.celestialBody()
earth.initEarth()
jupiter.initJupiter()
pluto.initPluto()
sun.initSun()

###############################################################################
#
#	Recreate plot from page 1 of lab.
#
###############################################################################

e2j = porkchopPlot()
#June 4, 2005
e2j.earliestDeparture = 2453714.5
#December 1, 2005
e2j.earliestArrival = 2454129.5
e2j.departureBody = earth
e2j.arrivalBody = jupiter
e2j.centralBody = sun
e2j.departureDelta = 2453794.5 - 2453714.5
e2j.arrivalDelta = 2454239.5 - 2454129.5
e2j.runPorkchop()
pdb.set_trace()
savez('GMATLab6Data/e2j.npz',
	TOF=e2j.TOF,C3=e2j.C3,vInf=e2j.vInf,
	arrivalJD=e2j.arrivalJD,departureJD=e2j.departureJD,
	DLA=e2j.DLA, RLA=e2j.RLA)


j2p = porkchopPlot()
#June 4, 2005
j2p.earliestDeparture = 2454129.5
#December 1, 2005
j2p.earliestArrival = 2456917.5
j2p.departureBody = jupiter
j2p.arrivalBody = pluto
j2p.centralBody = sun
j2p.departureDelta = 2454239.5 -2454129.5
j2p.arrivalDelta = 2457517.5 - 2456917.5
j2p.runPorkchop()
pdb.set_trace()
savez('GMATLab6Data/j2p.npz',
	TOF=j2p.TOF,C3=j2p.C3,vInf=j2p.vInf,
	arrivalJD=j2p.arrivalJD,departureJD=j2p.departureJD,
	DLA=j2p.DLA, RLA=j2p.RLA)

pdb.set_trace()


