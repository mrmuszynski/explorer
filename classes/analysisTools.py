#! /usr/bin/env python3
###############################################################################
#
#	Title   : analysisTools.py
#	Author  : Matt Muszynski
#	Date    : 02/24/18
#	Synopsis: Tools to be used for astrodynamics analysis.
# 
###############################################################################

import sys
sys.path.insert(0, '../../lib')
from numpy import vstack, hstack, array, linspace, pi, arccos, arctan2
from numpy import cross, sqrt, cos
from numpy.linalg import norm
from timeFcn import day2sec
from orbits import lambert, rv2coe

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
		DLA = []
		RLA = []
		i = []
		for arrivalDate in arrivalDates:
			arrivalPos = self.arrivalBody.meeusStateUpdate(arrivalDate)
			print('Computing Arrival Day ' + str(arrivalDate - arrivalDates[0]))
			for departureDate in departureDates:
				departurePos = self.departureBody.meeusStateUpdate(departureDate)
				TOFd = arrivalDate - departureDate
				TOF = hstack([TOF,TOFd])
				TOFs = day2sec(TOFd)

				lam = lambert(
					departurePos,arrivalPos,TOFs,mu=self.centralBody.mu)
				C3 = hstack([C3,lam['C3']])
				normVInf = norm(lam['vInfArrive'])
				vInf = hstack([vInf,normVInf])
				i = hstack([i,lam['i']])
				departureJD = hstack([departureJD,departureDate])
				arrivalJD = hstack([arrivalJD,arrivalDate])

				vHat = lam['vInfDepart']/norm(lam['vInfDepart'])

				DLA = hstack([DLA,pi/2 - arccos(vHat[2])])
				RLA = hstack([RLA,arctan2(vHat[1],vHat[0])])

		self.TOF = TOF.reshape(len(arrivalDates),len(departureDates))
		self.C3 = C3.reshape(len(arrivalDates),len(departureDates))
		self.vInf = vInf.reshape(len(arrivalDates),len(departureDates))		
		self.departureJD = departureJD.reshape(len(arrivalDates),len(departureDates))
		self.arrivalJD = arrivalJD.reshape(len(arrivalDates),len(departureDates))
		self.DLA = DLA.reshape(len(arrivalDates),len(departureDates))
		self.RLA = RLA.reshape(len(arrivalDates),len(departureDates))

def closestApproach(psi, mu, vInf):
	return mu/vInf**2*(cos((pi-psi)/2)**-1 -1)

def turningAngle(rP, mu, vInf):
	return  pi -2*arccos((rP/mu*vInf**2 + 1)**-1 )

def computeBrv(r,v,mu):
	rP = rv2coe(r,v)['r_p']
	s = v/norm(v)
	k = array([0,0,1])
	t = cross(s,k)/norm(cross(s,k))
	h = cross(r,v)/norm(cross(r,v))
	rhat = cross(s,t)
	bHat = cross(s,h)
	b = mu/v.dot(v)*sqrt((1+v.dot(v)*(rP/mu))**2-1)
	ijk2str = vstack([s,t,rhat])
	return (b*bHat,ijk2str)

def computeBvInf(vInfIn,vInfOut,mu):
	h = cross(vInfIn,vInfOut)/norm(cross(vInfIn,vInfOut))
	turnAngle = arccos(
		vInfIn.dot(vInfOut)/norm(vInfIn)/norm(vInfOut)
		)
	rP = closestApproach(turnAngle, mu, norm(vInfIn))
	s = vInfIn/norm(vInfIn)
	k = array([0,0,1])
	t = cross(s,k)/norm(cross(s,k))
	rhat = cross(s,t)
	bHat = cross(s,h)
	b = mu/vInfIn.dot(vInfIn)*sqrt((1+vInfIn.dot(vInfIn)*(rP/mu))**2-1)
	ijk2str = vstack([s,t,rhat])

	return (b*bHat,ijk2str)


def dBdV(vNominal,vPerturbed,r,mu):
	bNominal = computeB(r,vNominal,mu)[0]
	ijk2strNominal = computeB(r,vPerturbed,mu)[1]
	bPerturbed = computeB(r,vPerturbed,mu)[0]
	if sum((vNominal - vPerturbed) == 0) < 2: 
		print('WARNING: Only one element of vInf can be varied!')
	dBdVijk = (bPerturbed - bNominal)/norm(vNominal - vPerturbed)
	return ijk2strNominal.dot(dBdVijk)

