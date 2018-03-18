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
sys.path.insert(0, '../../classes')
sys.path.insert(0, '../../prop')
sys.path.insert(0, '../../fsw')
sys.path.insert(0, '../../../lib')

import matplotlib.pyplot as plt
import pdb
from numpy import savez
import celestialBodies
import orbits as o
from timeFcn import timeConvert, day2sec
from analysisTools import porkchopPlot

earth = celestialBodies.celestialBody()
venus = celestialBodies.celestialBody()
jupiter = celestialBodies.celestialBody()
sun = celestialBodies.celestialBody()
earth.initEarth()
venus.initVenus()
jupiter.initJupiter()
sun.initSun()

###############################################################################
#
#	Recreate plot from page 1 of lab.
#
###############################################################################

# launch2VGA = porkchopPlot()
# launch2VGA.earliestDeparture = 2447814 - 50
# launch2VGA.earliestArrival = 2447932 - 50
# launch2VGA.departureBody = earth
# launch2VGA.arrivalBody = venus
# launch2VGA.centralBody = sun
# launch2VGA.departureDelta = 100
# launch2VGA.arrivalDelta = 140
# launch2VGA.runPorkchop()
# savez('data/launch2VGA.npz',
# 	TOF=launch2VGA.TOF,C3=launch2VGA.C3,vInf=launch2VGA.vInf,
# 	arrivalJD=launch2VGA.arrivalJD,departureJD=launch2VGA.departureJD,
# 	DLA=launch2VGA.DLA, RLA=launch2VGA.RLA)

# VGA2EGA1 = porkchopPlot()
# #June 4, 2005
# VGA2EGA1.earliestDeparture = 2447932 - 50
# #December 1, 2005
# VGA2EGA1.earliestArrival = 2448235 - 210
# VGA2EGA1.departureBody = venus
# VGA2EGA1.arrivalBody = earth
# VGA2EGA1.centralBody = sun
# VGA2EGA1.departureDelta = 140
# VGA2EGA1.arrivalDelta = 240
# VGA2EGA1.runPorkchop()
# savez('data/VGA2EGA1.npz',
# 	TOF=VGA2EGA1.TOF,C3=VGA2EGA1.C3,vInf=VGA2EGA1.vInf,
# 	arrivalJD=VGA2EGA1.arrivalJD,departureJD=VGA2EGA1.departureJD,
# 	DLA=VGA2EGA1.DLA, RLA=VGA2EGA1.RLA)
# pdb.set_trace()
EGA22JOI = porkchopPlot()
#June 4, 2005
EGA22JOI.earliestDeparture = 2448965.5 - 100
#December 1, 2005
EGA22JOI.earliestArrival = 2450154 - 150
EGA22JOI.departureBody = earth
EGA22JOI.arrivalBody = jupiter
EGA22JOI.centralBody = sun
EGA22JOI.departureDelta = 200
EGA22JOI.arrivalDelta = 300
EGA22JOI.runPorkchop()
savez('data/EGA22JOI.npz',
	TOF=EGA22JOI.TOF,C3=EGA22JOI.C3,vInf=EGA22JOI.vInf,
	arrivalJD=EGA22JOI.arrivalJD,departureJD=EGA22JOI.departureJD,
	DLA=EGA22JOI.DLA, RLA=EGA22JOI.RLA)

pdb.set_trace()


