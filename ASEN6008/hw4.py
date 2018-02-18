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

import vehicles, celestialBodies, simScenario
from numpy import linspace, hstack, pi, array, arccos, cos, cross
from numpy import rad2deg, arctan2
from numpy.linalg import norm
import matplotlib.pyplot as plt
from timeFcn import timeConvert, sec2day, day2sec
from util import r3
import pdb
import orbits as o


###############################################################################
#
# 	Problem 1
#
###############################################################################

vSpacecraftSun = array([-10.8559, -35.9372,0]) #km/s
vVenusSun = array([-15.1945, -31.7927, 0]) #km/s
rVenusSun = array([-96948447.3751, 46106976.1901, 0]) #km
muSun = 1.32712440018e11 #km^3/s^2
muVenus = 3.257e5 #km^3/s^2
rVenus = 6052 #km

epsilon = vSpacecraftSun.dot(vSpacecraftSun)/2 - muSun/norm(rVenusSun)

print('')
print('Problem 1')
print('Specific Energy: ' + str(epsilon))

def closestApproach(psi, mu, vInf):
	return mu/vInf**2*(cos((pi-psi)/2)**-1 -1)
def turningAnlge(rP, mu, vInf):
	return  pi -2*arccos((rP/mu*vInf**2 + 1)**-1 )
	 

vInfVec = vSpacecraftSun - vVenusSun
vInf = norm(vInfVec)
rP = linspace(0,200000,2001)
psi = turningAnlge(rP,muVenus,vInf)
plt.plot(rP/1000,psi,vInf)
#plt.title('Raduys if Oeruaose abd Tyrbubg Raduys')
plt.title('Radius of Periapse and Turning Radius')
plt.ylabel('Turning Angle (rad)')
plt.xlabel('Periapse Radius (thousands of km)')
plt.xlim([-10,200])
plt.ylim([0,pi])
plt.figure()

epsilonAfterLeading = []
epsilonAfterTrailing = []
for angle in psi:
	leadingTurn = r3(-angle)
	trailingTurn = r3(angle)
	vInfAfterLead = leadingTurn.dot(vInfVec)
	vInfAfterTrail = trailingTurn.dot(vInfVec)
	vSpacecraftSunAfterLead = vInfAfterLead + vVenusSun
	vSpacecraftSunAfterTrail = vInfAfterTrail + vVenusSun
	epsilonAfterLeading = hstack([
		epsilonAfterLeading,
		vSpacecraftSunAfterLead.dot(vSpacecraftSunAfterLead)/2 - \
		muSun/norm(rVenusSun)
		])
	epsilonAfterTrailing = hstack([
		epsilonAfterTrailing,
		vSpacecraftSunAfterTrail.dot(vSpacecraftSunAfterTrail)/2 - \
		muSun/norm(rVenusSun)
		])
plt.plot(rP/1000,epsilonAfterLeading,label='Leading Passes')
plt.plot(rP/1000,epsilonAfterTrailing,label='Trailing Passes')
plt.axhline(epsilon, color='black', linestyle='--',label='Prepass Energy')
plt.axvline(rVenus/1000, color='black', linestyle='-.',label='Venus Radius')
plt.title('Post-Pass Energy for Leading and Trailing Encounters')
plt.xlabel('Closest Approach (thousands of km)')
plt.ylabel('Specific Energy after Pass (m^2/s^2)')
plt.grid(True)
plt.legend()

###############################################################################
#
# 	Problem 2
#
###############################################################################

vInfIn = array([-5.19425, 5.19424, -5.19425]) #km/s
vInfOut = array([-8.58481, 1.17067, -2.42304]) #km/s
muEarth = 3.986004415e5 #km^3/s^2
k = array([0,0,1])
psiEarthFlyby = arccos(vInfIn.dot(vInfOut)/(norm(vInfIn)*norm(vInfOut)))
rP = closestApproach(psiEarthFlyby, muEarth, norm(vInfIn))

S = vInfIn/norm(vInfIn)
bHat = cross(S,k)
bMag = \
	muEarth/vInfIn.dot(vInfIn)*(
		(1 + vInfIn.dot(vInfIn)*rP/muEarth)**2 - 1
		)**0.5
B = bMag*bHat
bT = B[1]
bR = B[0]
thetaRad = arctan2(bT,bR)
thetaDeg = rad2deg(thetaRad)

print('')
print('Problem 2')
print('Periapse Radius: ' + str(rP))
print('psiEarthFlyby (rad): ' + str(psiEarthFlyby))
print('psiEarthFlyby (deg): ' + str(rad2deg(psiEarthFlyby)))
print('bT: ' + str(bT))
print('bR: ' + str(bR))
print('bMag: ' + str(bMag))
print('thetaRad: ' + str(thetaRad))
print('thetaDeg: ' + str(thetaDeg))

###############################################################################
#
# 	Problem 3
#
###############################################################################

launchJD = timeConvert('1989/281T00:00:00.000','utc','jd')
venusEncounterDate = timeConvert('1990/041T00:00:00.000','utc','jd')
earthEncounter1JD = timeConvert('1990/344T00:00:00.000','utc','jd')
earthEncounter2JD = timeConvert('1992/344T12:00:00.000','utc','jd')
juiterArrivalJD = timeConvert('1996/081T12:00:00.000','utc','jd')



earth = celestialBodies.celestialBody()
earth.initEarth()
venus = celestialBodies.celestialBody()
venus.initVenus()
jupiter = celestialBodies.celestialBody()
jupiter.initJupiter()

earthLaunchState = earth.meeusStateUpdate(launchJD)
venusEncounterState = venus.meeusStateUpdate(venusEncounterDate)
earthEncounter1State = earth.meeusStateUpdate(earthEncounter1JD)
earthEncounter2State = earth.meeusStateUpdate(earthEncounter2JD)
jupiterArrivalState = jupiter.meeusStateUpdate(juiterArrivalJD)

launch2VenusDays = venusEncounterDate - launchJD
venus2EarthDays = earthEncounter1JD - venusEncounterDate
Earth2EarthDays = earthEncounter2JD - earthEncounter1JD
Earth2JupiterDays = juiterArrivalJD - earthEncounter2JD

launch2VenusSeconds = day2sec(launch2VenusDays)
venus2EarthSeconds = day2sec(venus2EarthDays)
Earth2EarthSeconds = day2sec(Earth2EarthDays)
Earth2JupiterSeconds = day2sec(Earth2JupiterDays)

launch2Venus = o.lambert(
	earthLaunchState,venusEncounterState,launch2VenusSeconds,mu=muSun)
venus2Earth = o.lambert(
	venusEncounterState,earthEncounter1State,venus2EarthSeconds,mu=muSun)
#note, earth2earth is not type I/II, so this lambert solver fails.
#I could figure it out, but I don't think I need it for this assignment
#so I'm not going to right now.
earth2Earth = o.lambert(
	earthEncounter1State,earthEncounter2State,Earth2EarthSeconds,mu=muSun)
earth2Jupiter = o.lambert(
	earthEncounter2State,jupiterArrivalState,Earth2JupiterSeconds,mu=muSun)


vInfIncoming = launch2Venus['vInfArrive']
vInfDeparting = venus2Earth['vInfDepart']
psiVenusFlyby = arccos(vInfIncoming.dot(vInfDeparting)/(norm(vInfIncoming)*norm(vInfDeparting)))
rP = closestApproach(psiVenusFlyby, muEarth, norm(vInfIncoming))

vSpacecraftSunArrival = vInfIncoming + venusEncounterState[3:6]
vSpacecraftSunDeparture = vInfDeparting + venusEncounterState[3:6]

epsilonArrive = \
	vSpacecraftSun.dot(vSpacecraftSunArrival)/2 - muSun/norm(venusEncounterState[0:3])
epsilonDepart = \
	vSpacecraftSun.dot(vSpacecraftSunDeparture)/2 - muSun/norm(venusEncounterState[0:3])

print('')
print('Problem 3')
print('Launch JD: ' + str(launchJD))
print('Venus Encoutner JD: ' + str(venusEncounterDate))
print('Earth Encounter 1 JD: ' + str(earthEncounter1JD))
print('vInf In (vec): '+ str(vInfIncoming))
print('vInf Out (vec): '+ str(vInfDeparting))
print('vInf In (mag): '+ str(norm(vInfIncoming)))
print('vInf Out (mag): '+ str(norm(vInfDeparting)))
print('Velocity before Venus Encounter (vec): ' + str(vSpacecraftSunArrival))
print('Velocity after Venus Encounter (vec): ' + str(vSpacecraftSunDeparture))
print('Velocity before Venus Encounter (mag): ' + str(norm(vSpacecraftSunArrival)))
print('Velocity after Venus Encounter (mag): ' + str(norm(vSpacecraftSunDeparture)))
print('Energy before Venus Encounter: ' + str(epsilonArrive))
print('Energy after Venus Encounter: ' + str(epsilonDepart))
plt.show()

pdb.set_trace()
















