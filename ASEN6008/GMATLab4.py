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

earth = celestialBodies.celestialBody()
mars = celestialBodies.celestialBody()
sun = celestialBodies.celestialBody()
earth.initEarth()
mars.initMars()
sun.initSun()

class porkchopPlot:
	def __init__(self):
		self.earliestDeparture = -1
		self.earliestArrival = -1
		self.departureDelta = -1
		self.arrivalDelta = -1
		self.departurDates = -1
		self.arrivalDates = -1
		self.TOF = -1
		self.C3 = -1
		self.vInf = -1
		self.departureBody = -1
		self.arrivalBody = -1
		self.centralBody = -1

	def runPorkchop(self):
		from numpy import vstack, hstack, array, linspace
		from numpy.linalg import norm
		latestDeparture = self.earliestDeparture + self.departureDelta
		latestArrival = self.earliestArrival + self.arrivalDelta
		departureDates = linspace(
			self.earliestDeparture,
			latestDeparture,
			latestDeparture-self.earliestDeparture+1)
		arrivalDates = linspace(
			self.earliestArrival,
			latestArrival,
			latestArrival-self.earliestArrival+1)

		TOF = []
		C3 = []
		vInf = []
		departureJD = []
		arrivalJD = []
		i = []
		for arrivalDate in arrivalDates:
			arrivalPos = self.arrivalBody.meeusStateUpdate(arrivalDate)
			print('Computing Arrival Day ' + str(arrivalDate - arrivalDates[0]))
			for departureDate in departureDates:
				departurePos = self.departureBody.meeusStateUpdate(departureDate)
				TOFd = arrivalDate - departureDate
				TOF = hstack([TOF,TOFd])
				TOFs = day2sec(TOFd)
				lam = o.lambert(
					departurePos,arrivalPos,TOFs,mu=self.centralBody.mu)
				C3 = hstack([C3,lam['C3']])
				vInf = hstack([vInf,norm(lam['vInfArrive'])])
				i = hstack([i,lam['i']])
				departureJD = hstack([departureJD,departureDate])
				arrivalJD = hstack([arrivalJD,arrivalDate])
		self.TOF = TOF.reshape(len(arrivalDates),len(departureDates))
		self.C3 = C3.reshape(len(arrivalDates),len(departureDates))
		self.vInf = vInf.reshape(len(arrivalDates),len(departureDates))		
		self.departureJD = departureJD.reshape(len(arrivalDates),len(departureDates))
		self.arrivalJD = arrivalJD.reshape(len(arrivalDates),len(departureDates))
###############################################################################
#
#	Recreate plot from page 2 of lab.
#
###############################################################################

opportunity2005 = porkchopPlot()
#June 4, 2005
opportunity2005.earliestDeparture = timeConvert(
	'2005/155T00:00:00.00','utc','jd')
#December 1, 2005
opportunity2005.earliestArrival = timeConvert(
	'2005/335T00:00:00.00','utc','jd')
opportunity2005.departureBody = earth
opportunity2005.arrivalBody = mars
opportunity2005.centralBody = sun
opportunity2005.departureDelta = 140
opportunity2005.arrivalDelta = 450
opportunity2005.runPorkchop()
savez('GMATLab4Data/opportunity2005.npz',
	TOF=opportunity2005.TOF,C3=opportunity2005.C3,vInf=opportunity2005.vInf,
	arrivalJD=opportunity2005.arrivalJD,departureJD=opportunity2005.departureJD)

###############################################################################
#
#	Lab 4 question 2	
#
###############################################################################

opportunity2018 = porkchopPlot()
opportunity2018.earliestDeparture = 2458200.0
opportunity2018.earliestArrival = 2458350.0 
opportunity2018.departureBody = earth
opportunity2018.arrivalBody = mars
opportunity2018.centralBody = sun
opportunity2018.departureDelta = 2458320.0 - opportunity2018.earliestDeparture
opportunity2018.arrivalDelta = 2458600.0 - opportunity2018.earliestArrival
opportunity2018.runPorkchop()
savez('GMATLab4Data/opportunity2018.npz',
	TOF=opportunity2018.TOF,C3=opportunity2018.C3,vInf=opportunity2018.vInf,
	arrivalJD=opportunity2018.arrivalJD,departureJD=opportunity2018.departureJD)


###############################################################################
#
#	Lab 4 question 3
#
###############################################################################

opportunity2016 = porkchopPlot()
opportunity2016.earliestDeparture = 2457389.0 
opportunity2016.earliestArrival = 2457570.0 
opportunity2016.departureBody = earth
opportunity2016.arrivalBody = mars
opportunity2016.centralBody = sun
opportunity2016.departureDelta = 2457509.0  - opportunity2016.earliestDeparture
opportunity2016.arrivalDelta = 2457790.0  - opportunity2016.earliestArrival
opportunity2016.runPorkchop()
savez('GMATLab4Data/opportunity2016.npz',
	TOF=opportunity2016.TOF,C3=opportunity2016.C3,vInf=opportunity2016.vInf,
	arrivalJD=opportunity2016.arrivalJD,departureJD=opportunity2016.departureJD)


pdb.set_trace()


