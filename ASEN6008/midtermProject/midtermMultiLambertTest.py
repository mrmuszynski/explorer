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
from numpy import savez, arange, meshgrid
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

meshDates =  meshgrid(
	arange(2447764,2447865),
	arange(2447882,2448023)
	)
departureDates = meshDates[0]
arrivalDates = meshDates[1]

earthLaunchStates = earth.meeusStateUpdate(departureDates.reshape(-1))
venusVGAStates = venus.meeusStateUpdate(arrivalDates.reshape(-1))
TOFd = arrivalDates - departureDates
TOFs = day2sec(TOFd).reshape(-1)
lam = o.multiLambert(
	earthLaunchStates,
	venusVGAStates,
	TOFs,mu=sun.mu)
pdb.set_trace()
savez('testData/launch2VGA.npz',
	TOF=TOFd,C3=lam['C3'],vInf=lam['magVInfArrive'],
	arrivalJD=arrivalDates,departureJD=departureDates)


meshDates =  meshgrid(
	arange(2447932 - 50,2447932 - 50 + 200 + 1),
	arange(2448235 - 210,2448235 - 210 + 300 + 1)
	)
departureDates = meshDates[0]
arrivalDates = meshDates[1]

earthLaunchStates = earth.meeusStateUpdate(departureDates.reshape(-1))
venusVGAStates = venus.meeusStateUpdate(arrivalDates.reshape(-1))
TOFd = arrivalDates - departureDates
TOFs = day2sec(TOFd).reshape(-1)
lam = o.multiLambert(
	earthLaunchStates,
	venusVGAStates,
	TOFs,mu=sun.mu)
pdb.set_trace()
savez('testData/VGA2EGA1.npz',
	TOF=TOFd,C3=lam['C3'],vInf=lam['magVInfArrive'],
	arrivalJD=arrivalDates,departureJD=departureDates)

meshDates =  meshgrid(
	arange(2448965.5 - 100,2448965.5 - 100 + 200 + 1),
	arange(2450154 - 150,2450154 - 150 + 300 + 1)
	)
departureDates = meshDates[0]
arrivalDates = meshDates[1]

earthLaunchStates = earth.meeusStateUpdate(departureDates.reshape(-1))
venusVGAStates = venus.meeusStateUpdate(arrivalDates.reshape(-1))
TOFd = arrivalDates - departureDates
TOFs = day2sec(TOFd).reshape(-1)
lam = o.multiLambert(
	earthLaunchStates,
	venusVGAStates,
	TOFs,mu=sun.mu)
pdb.set_trace()
savez('testData/EGA22JOI.npz',
	TOF=TOFd,C3=lam['C3'],vInf=lam['magVInfArrive'],
	arrivalJD=arrivalDates,departureJD=departureDates)



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


