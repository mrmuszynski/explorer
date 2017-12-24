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
sys.path.insert(0, '../util')

import vehicles, celestialBodies, simScenario
from constants import au
from numpy import array, argmax, argmin
import matplotlib.pyplot as plt
from timeFcn import timeConvert
import pdb

def test_meeusStateUpdate():
	"""!
	Test taken from Vallado Algorithm 33. P 296-298
	"""

	jupiter = celestialBodies.celestialBody()
	jupiter.initJupiter()
	scen = simScenario.simScenario()
	scen.addNonGravBod([jupiter])
	t = scen.currentTime = timeConvert([1994,140,20],'ydnhms','jd')

	#note that Vallado uses omega tilde where Davis uses PI.
	#also, Vallado uses lambda_M where Davis uses L
	a,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['a'], t)
	e,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['e'], t)
	i,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['i'], t)
	OMEGA,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['OMEGA'], t)
	PI,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['PI'], t)
	L,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['L'], t)
	#2449493.333 is given by Vallado. This asserts that they
	#match within sigfigs 
	assert( abs(scen.currentTime - 2449493.333) < 0.0005 )
	#-0.05617158 is given by Vallado. I believe that there is an
	#error in his book, and the last sigfig should be a 7 instead
	#of an 8, so i check to one fewer sigfig than I normally would
	assert( abs(T - (-0.05617158)) < 0.00000005 )
	import pdb
	pdb.set_trace()

	assert( abs(a - 5.202603) < 0.0000005 )
	assert( abs(e - 0.048486) < 0.0000005 )
	assert( abs(i - 1.303382) < 0.0000005 )
	assert( abs(OMEGA - 100.454519) < 0.0000005 )
	assert( abs(PI - 14.319203) < 0.0000005 )
	assert( abs(L - (-136.12394)) < 0.000005)
	assert( abs((L - PI) - (-150.443142)) < 0.0000005 )
	assert( abs((PI - OMEGA) - (-86.135316)) < 0.0000005 )



# #initialize spacecraft
# explorer1 = vehicles.spacecraft()
# explorer1.name = 'Explorer 1'
# explorer1.initialState = array([au,0,0,0,29784,0])

# #initialize stock bodies
# sun = celestialBodies.celestialBody()
# sun.initSun()
# venus = celestialBodies.celestialBody()
# venus.initVenus()
# earth = celestialBodies.celestialBody()
# earth.initEarth()
# mars = celestialBodies.celestialBody()
# mars.initMars()
# jupiter = celestialBodies.celestialBody()
# jupiter.initJupiter()
# saturn = celestialBodies.celestialBody()
# saturn.initSaturn()
# uranus = celestialBodies.celestialBody()
# uranus.initUranus()
# neptune = celestialBodies.celestialBody()
# neptune.initNeptune()
# pluto = celestialBodies.celestialBody()
# pluto.initPluto()

# #initialize sim scenario
# scen = simScenario.simScenario()
# scen.addSpacecraft([explorer1])
# scen.addNonGravBod([
# 	# venus, earth, mars, jupiter, saturn, uranus, neptune, pluto
# 	earth
# 	])
# scen.addGravBod([sun])
# # scen.addGravBod([sun,earth])
# scen.jdEndTime = 2451545.0 + 365
# scen.timeStep = 0.1
# scen.propagate()

# for bod in scen.nonGravBodList:
# 	plt.plot(bod.stateHistory[:,0],bod.stateHistory[:,1],label=bod.name)

# # argmax(earth.stateHistory[:,0])
# # argmax(earth.stateHistory[:,1])
# # argmin(earth.stateHistory[:,0])
# # argmin(earth.stateHistory[:,2])

# plt.legend()
# pdb.set_trace()