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
from numpy import linspace, hstack, pi
from numpy.linalg import norm
import matplotlib.pyplot as plt
from timeFcn import timeConvert, sec2day, day2sec
import pdb
import orbits as o


###############################################################################
#
# 	Problem 1
#
###############################################################################

jupiter = celestialBodies.celestialBody()
jupiter.initJupiter()	
mars = celestialBodies.celestialBody()
mars.initMars()
earth = celestialBodies.celestialBody()
earth.initEarth()
venus = celestialBodies.celestialBody()
venus.initVenus()
sun = celestialBodies.celestialBody()
sun.initSun()
departureJD = 2454085.5
arrivalJD = departureJD + 830

marsDepartureState = mars.meeusStateUpdate(departureJD)
jupiterArrivalState = jupiter.meeusStateUpdate(arrivalJD)


###############################################################################
#
# 	Problem 2
#
###############################################################################

psi12 = []
C312 = []
vInf12 = []
DM12 = []

TOF12 = linspace(100,4265,4166)
#type I/II solutions
for TOFd in TOF12:
	arrivalJD = departureJD + TOFd
	TOFs = day2sec(TOFd)
	# jupiterArrivalState = jupiter.meeusStateUpdate(arrivalJD)
	lam = o.lambert(
		marsDepartureState,jupiterArrivalState,TOFs,mu=sun.mu)
	psi12 = hstack([psi12,lam['psi']])
	C312 = hstack([C312,lam['C3']])
	vInf12 = hstack([vInf12,norm(lam['vInfArrive'])])
	DM12 = hstack([DM12,norm(lam['DM'])])

pdb.set_trace()
psi3 = []
C33 = []
vInf3 = []
TOF3 = linspace(2500,4265,(4265-2500)+1)
DM3 = []

#type III solutions
for TOFd in TOF3:
	arrivalJD = departureJD + TOFd
	TOFs = day2sec(TOFd)
	# jupiterArrivalState = jupiter.meeusStateUpdate(arrivalJD)
	lam = o.lambert(
		marsDepartureState,jupiterArrivalState,TOFs,mu=sun.mu,revs=1,
			type=3)
	psi3 = hstack([psi3,lam['psi']])
	C33 = hstack([C33,lam['C3']])
	vInf3 = hstack([vInf3,lam['vInfArrive']])
	DM3 = hstack([DM3,norm(lam['DM'])])

pdb.set_trace()
psi4 = []
C34 = []
vInf4 = []
TOF4 = linspace(2500,4265,(4265-2500)+1)
DM4 = []
#type IV solutions
for TOFd in TOF4:
	arrivalJD = departureJD + TOFd
	TOFs = day2sec(TOFd)
	# jupiterArrivalState = jupiter.meeusStateUpdate(arrivalJD)
	lam = o.lambert(
		marsDepartureState,jupiterArrivalState,TOFs,mu=sun.mu,revs=1,
			type=4)
	psi4 = hstack([psi4,lam['psi']])
	C34 = hstack([C34,lam['C3']])
	vInf4 = hstack([vInf4,lam['vInfArrive']])
	DM4 = hstack([DM4,norm(lam['DM'])])

pdb.set_trace()#type III/IV solutions


plt.plot(psi12,TOF12,color='green',label='Type I/II Transfers')
plt.xlabel('Psi (rad^2)')
plt.ylabel('TOF (days)')
plt.axvline(4*pi**2, color='black', linestyle='-.')
plt.axvline(0, color='black', linestyle='--')
plt.plot(psi3,TOF3,color='blue',label='Type III/IV Transfers')
plt.xlabel('Psi (rad^2)')
plt.ylabel('TOF (days)')
plt.plot(psi4,TOF4,color='blue')
plt.xlabel('Psi (rad^2)')
plt.ylabel('TOF (days)')
plt.title('Single and Multiple Revolution Transfers')
plt.text(8,550,'0 Revolution Regime')
plt.text(60,1700,'1 Revolution Regime')
plt.legend()
plt.grid(True)
plt.xlim([-3.12,100])
plt.ylim([0,4265])
plt.show()

print("")
print("Problem 1")
print("Mars Position at Departure: " + str(marsDepartureState[0:3]))
print("Jupiter Position at Arrival: " + str(jupiterArrivalState[0:3]))
print("")
print("Problem 4")
print("Minimum TOF (s): " + str(lam['minTOF']))
print("Minimum TOF (d): " + str(sec2day(lam['minTOF'])))
print("Minimizing Psi Value: " + str(lam['minimizingPsi']))

pdb.set_trace()







