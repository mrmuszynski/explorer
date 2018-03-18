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
from numpy import savez, load, sqrt, logical_and, logical_or, zeros, arccos
from numpy import hstack, empty, pi, linspace, vstack, sin, cos, ones
from numpy import argmax, arctan2, arcsin, rad2deg
from numpy import cross
from numpy.linalg import norm
import celestialBodies
import orbits as o
from timeFcn import timeConvert, day2sec
from analysisTools import porkchopPlot, closestApproach, computeBvInf

earth = celestialBodies.celestialBody()
jupiter = celestialBodies.celestialBody()
venus = celestialBodies.celestialBody()
sun = celestialBodies.celestialBody()
earth.initEarth()
jupiter.initJupiter()
venus.initVenus()
sun.initSun()

earthLaunchState = earth.meeusStateUpdate(2447814)
venusVGAState = venus.meeusStateUpdate(2447932)
earthEGA1State = earth.meeusStateUpdate(2448235)
earthEGA2State = earth.meeusStateUpdate(2448965.484378)
jupiterJOIState = jupiter.meeusStateUpdate(2450154)

###############################################################################
#
#	VGA Caluclations
#
###############################################################################

launchVInf = o.lambert(
	earthLaunchState,venusVGAState,day2sec(2447932-2447814),mu=sun.mu
	)['vInfDepart']

launchC3 = o.lambert(
	earthLaunchState,venusVGAState,day2sec(2447932-2447814),mu=sun.mu
	)['C3']

DLAEarthDepartureRad = pi/2 - arccos(launchVInf[2]/norm(launchVInf))
RLAEarthDepartureRad = arctan2(launchVInf[1],launchVInf[0])

# RLAEarthDepartureRad = arctan(launchVInf[1]/launchVInf[0])
# DLAEarthDepartureRad = arcsin(launchVInf[0]/norm(launchVInf))
RLAEarthDepartureDeg = rad2deg(RLAEarthDepartureRad)
DLAEarthDepartureDeg = rad2deg(DLAEarthDepartureRad)


VGAVInfIn = o.lambert(
	earthLaunchState,venusVGAState,day2sec(2447932-2447814),mu=sun.mu
	)['vInfArrive']
VGAVInfOut = o.lambert(
	venusVGAState,earthEGA1State,day2sec(2448235-2447932),mu=sun.mu
	)['vInfDepart']

bPlane = computeBvInf(VGAVInfIn,VGAVInfOut,venus.mu)
bIJK = bPlane[0]
ijk2str = bPlane[1]
bSTR = ijk2str.dot(bIJK)




pdb.set_trace()



