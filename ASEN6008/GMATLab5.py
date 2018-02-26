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
mars = celestialBodies.celestialBody()
sun = celestialBodies.celestialBody()
earth.initEarth()
mars.initMars()
sun.initSun()

###############################################################################
#
#	Recreate plot from page 1 of lab.
#
###############################################################################

opportunity2008 = porkchopPlot()
#June 4, 2005
opportunity2008.earliestDeparture = 2454310
#December 1, 2005
opportunity2008.earliestArrival = 2454525
opportunity2008.departureBody = earth
opportunity2008.arrivalBody = mars
opportunity2008.centralBody = sun
opportunity2008.departureDelta = 140
opportunity2008.arrivalDelta = 350
opportunity2008.runPorkchop()
savez('GMATLab5Data/opportunity2008.npz',
	TOF=opportunity2008.TOF,C3=opportunity2008.C3,vInf=opportunity2008.vInf,
	arrivalJD=opportunity2008.arrivalJD,departureJD=opportunity2008.departureJD,
	DLA=opportunity2008.DLA, RLA=opportunity2008.RLA)


pdb.set_trace()


