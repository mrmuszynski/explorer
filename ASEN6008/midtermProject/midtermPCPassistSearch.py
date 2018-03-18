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
from numpy import hstack, empty
from numpy.linalg import norm
# import celestialBodies
import orbits as o
from timeFcn import timeConvert, day2sec
# from analysisTools import porkchopPlot, closestApproach

# earth = celestialBodies.celestialBody()
# jupiter = celestialBodies.celestialBody()
# pluto = celestialBodies.celestialBody()
# sun = celestialBodies.celestialBody()
# earth.initEarth()
# jupiter.initJupiter()
# pluto.initPluto()
# sun.initSun()


launch2VGA = load('data/launch2VGA.npz')

VGA2EGA1 = load('data/VGA2EGA1.npz')

EGA22JOI = load('data/EGA22JOI.npz')




#by transposing the departure dates arrays, we ensure that the
#arrivalDates and departure dates have the same number of rows and
#that each row corresponds to a single date for the gravity assist.
#The rows of the two correspond such that the ith row of each
#corresponds to the same date of the assist.
departureDates = launch2VGA['departureJD']
assistInDates = launch2VGA['arrivalJD']
assistOutDates = VGA2EGA1['departureJD'].T
arrivalDates = VGA2EGA1['arrivalJD'].T

c3Depart = launch2VGA['C3']
vInfDepart = sqrt(launch2VGA['C3'])
vInfIn = launch2VGA['vInf']
vInfOut = sqrt(VGA2EGA1['C3']).T
vInfArrive = VGA2EGA1['vInf'].T

# if sum(arrivalDates[:,0] - departureDates[:,0]) != 0:
# 	print('Error! Departure and Arrival Dates Misaligned!!!')
count = 0
helper = zeros(assistOutDates.shape)
goodC3Depart = []
goodVInfDepart = []
goodVInfIn = []
goodVInfOut = []
goodVInfArrive = []
goodDepartureDates = []
goodArrivalDates = []
goodAssistDates = []

for i in range(0,departureDates.shape[1]):
	if departureDates.shape[0] != sum(assistInDates[:,i] == assistInDates[:,i]):
		print('Error! Departure and Arrival Dates Misaligned!!!')

	#define a helper array so for each column we can index with the same
	#ind function as we use to index the second leg
	validAssistInd = abs(vInfOut - (vInfIn[:,i,None] + helper)) < 0.001

	goodC3Depart = \
		hstack([
			goodC3Depart,
			(c3Depart[:,i,None] + helper)[validAssistInd]
		])
	goodVInfDepart = \
		hstack([
			goodVInfDepart,
			(vInfDepart[:,i,None] + helper)[validAssistInd]
		])
	goodVInfIn = \
		hstack([
			goodVInfIn,
			(vInfIn[:,i,None] + helper)[validAssistInd]
		])
	goodVInfOut = \
		hstack([
			goodVInfOut,
			vInfOut[validAssistInd]
		])
	goodVInfArrive = \
		hstack([
			goodVInfArrive,
			vInfArrive[validAssistInd]
		])
	goodDepartureDates = hstack([
		goodDepartureDates,
		(departureDates[:,i,None] + helper)[validAssistInd] 
		])
	goodAssistDates = hstack([
		goodArrivalDates,
		assistOutDates[validAssistInd]
		])
	goodArrivalDates = hstack([
		goodAssistDates,
		arrivalDates[validAssistInd]
		])
	count += sum(sum(validAssistInd))

print("Found " + str(count) + " valid assists out of " + str(
	departureDates.shape[1]*arrivalDates.shape[0]*arrivalDates.shape[1]
	) + " possible combinations.")

pdb.set_trace()



