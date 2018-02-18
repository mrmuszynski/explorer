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
from numpy import array, argmax, argmin, sqrt, pi, arctan2
import matplotlib.pyplot as plt
from timeFcn import timeConvert
import pdb

###########################################################################
#
# Problem 1
#
###########################################################################

muSun = 1.327e11 #km^3/s^2
muEarth = 3.986e5 #km^3/s^2
muMars = 4.305e4 #km^3/s^2
au = 1.4959787e8 #km
aEarth = 1 #AU
aMars = 1.52368 #AU
rEarth = 6378.1363 #km
rMars = 3397.2 #km

aTransAU = (aEarth+aMars)/2
aTrans = aTransAU*au #km
vDepart = sqrt(2*muSun/(aEarth*au) - muSun/aTrans)
vArrive = sqrt(2*muSun/(aMars*au) - muSun/aTrans)
vEarth = sqrt(muSun/(aEarth*au))
vMars = sqrt(muSun/(aMars*au))
vInfEarth = vDepart - vEarth
vCircEarth = sqrt(muEarth/(400+rEarth))
vDepart400kmEarth = sqrt((2*muEarth)/(400+rEarth)+vInfEarth**2)
deltaVDepart = vDepart400kmEarth - vCircEarth

vMars = sqrt(muSun/(aMars*au))
vInfMars = vMars - vArrive
vCircMars = sqrt(muMars/(400+rMars))
vArrive400kmMars = sqrt((2*muMars)/(400+rMars)+vInfMars**2)
deltaVArrive = vArrive400kmMars - vCircMars

TOF = 0.5*2*pi*sqrt(aTrans**3/muSun)

print("Part A")
print("Semi-Major Axis of Transfer Orbit (AU): " + str(aTransAU))
print("Semi-Major Axis of Transfer Orbit (km): " + str(aTrans))
print("Departure Velocity: " + str(vDepart))
print("Arrival Velocity: " + str(vArrive))
print("")
print("Part B")
print("Earth Velocity: " + str(vEarth))
print("400km Cicular Orbit Velocity (Earth): " + str(vCircEarth))
print("Earth Departure V Infinity: " + str(vInfEarth))
print("Earth Departure Velocity: " + str(vDepart400kmEarth))
print("Earth Departure Δv: " + str(deltaVDepart))
print("")
print("Mars Velocity: " + str(vMars))
print("400km Cicular Orbit Velocity (Mars): " + str(vCircMars))
print("Mars Arrival V Infinity: " + str(vInfMars))
print("Mars Arrival Velocity: " + str(vArrive400kmMars))
print("Mars Arrival Δv: " + str(deltaVArrive))
print("")
print("Part C")
print("TOF (s): " + str(TOF))
print("TOF (Days): " + str(TOF/3600/24))
print("")

pdb.set_trace()
###########################################################################
#
# Problem 2
#
###########################################################################

from numpy import rad2deg, hstack, ceil,vstack, empty, cos, sin
from numpy.linalg import norm
from scipy.integrate import ode

rEarth0 = [-578441.002878924, -149596751.684464, 0.] #km
vEarth0 = [29.7830732658560, -0.115161262358529, 0.] #km/s
xEarth0 = hstack([rEarth0,vEarth0])
rMarsf = [-578441.618274359, 227938449.869731, 0.] #km
vMarsf = [-24.1281802482527, -0.0612303173808154, 0.] #km/s
xMarsf = hstack([rMarsf,vMarsf])

aEarth = norm(rEarth0)
aMars = norm(rMarsf)

rSC0 = [0,-aEarth,0]
vSC0 = [vDepart,0,0]
xSC0 = hstack([rSC0,vSC0])



nEarth = sqrt(muSun/aEarth**3)
nMars = sqrt(muSun/aMars**3)

thetaEarth0 = arctan2(rEarth0[1],rEarth0[0])
thetaMarsf = arctan2(rMarsf[1],rMarsf[0])
thetaMars0 = thetaMarsf - nMars*TOF

print("")
print("Problem 2")
print("Theta Earth Initial: " + str(rad2deg(thetaEarth0)))
print("Theta Mars Initial: " + str(rad2deg(thetaMars0)))
print("Theta Mars Final: " + str(rad2deg(thetaMarsf)))
print("")

def gSunOnly(t,xSC):
	return hstack([xSC[3:6],-muSun*xSC[0:3]/norm(xSC)**3])

def gAllBodies(t,xSC):
	thetaEarth = thetaEarth0 + nEarth*t
	thetaMars = thetaMars0 + nMars*t

	rEarth = array([aEarth*cos(thetaEarth),aEarth*sin(thetaEarth),0])
	rMars = array([aMars*cos(thetaMars),aMars*sin(thetaMars),0])


	rEarthSC = rEarth - xSC[0:3]
	rMarsSC = rMars - xSC[0:3]

	gSun = -muSun*xSC[0:3]/norm(xSC)**3

	gEarth = muEarth*(
		rEarthSC/norm(rEarthSC)**3 - \
		rEarth/norm(rEarth)**3)
	gMars = muMars*(
		rMarsSC/norm(rMarsSC)**3 - \
		rMars/norm(rMars)**3)

	a = gSun + gEarth + gMars
	return hstack([xSC[3:6],a])

pdb.set_trace()
sunOnlySolver = ode(gSunOnly).set_integrator('dopri5')
allBodySolver = ode(gAllBodies).set_integrator('dopri5')
sunOnlySolver.set_initial_value(xSC0,0)
allBodySolver.set_initial_value(xSC0,0)

xSCfSunOnly = empty((0,6),float)
xSCfAllBody = empty((0,6),float)
xEarth = empty((0,3),float)
xMars = empty((0,3),float)

for i in range(0,int(TOF/86400)):
	t = i*86400
	thetaEarth = thetaEarth0 + nEarth*t
	thetaMars = thetaMars0 + nMars*t
	xSCfSunOnly = vstack([xSCfSunOnly,sunOnlySolver.integrate(t)])
	xSCfAllBody = vstack([xSCfAllBody,allBodySolver.integrate(t)])
	xEarth = vstack([
		xEarth,
		aEarth*array([cos(thetaEarth),sin(thetaEarth),0])
		])
	xMars = vstack([
		xMars,
		aMars*array([cos(thetaMars),sin(thetaMars),0])
		])
thetaEarthf = thetaEarth0 + nEarth*TOF
thetaMarsf = thetaMars0 + nMars*TOF

rEarthf = aEarth*array([cos(thetaEarthf),sin(thetaEarthf),0])
rMarsf = aMars*array([cos(thetaMarsf),sin(thetaMarsf),0])

diff = xSCfSunOnly - xSCfAllBody

plt.plot(xSCfAllBody[:,0],xSCfAllBody[:,1],label="S/C")
plt.plot(xEarth[:,0],xEarth[:,1],label="Earth Orbit")
plt.plot(xMars[:,0],xMars[:,1],label='Mars Orbit')
plt.xlim([-3e8,3e8])
plt.ylim([-2.5e8,2.5e8])
plt.title('Transfer with Gravity From Sun, Earth, and Mars')
plt.axis('equal')
plt.xlabel('x (km)')
plt.ylabel('y (km)')
plt.legend()

plt.figure()
plt.plot(xSCfSunOnly[:,0],xSCfSunOnly[:,1],label="S/C")
plt.plot(xEarth[:,0],xEarth[:,1],label="Earth Orbit")
plt.plot(xMars[:,0],xMars[:,1],label='Mars Orbit')
plt.xlim([-3e8,3e8])
plt.ylim([-2.5e8,2.5e8])
plt.title('Transfer with Solar Gravity Only')
plt.axis('equal')
plt.xlabel('x (km)')
plt.ylabel('y (km)')
plt.legend()

plt.figure()
plt.plot(diff[:,0],label='X-Coordinate Difference')
plt.plot(diff[:,1],label='Y-Coordinate Difference')
plt.title('Difference in X and Y Coordinates')
plt.xlabel('Days since Epoch')
plt.ylabel('Kilometers')
plt.legend()

plt.figure()
plt.plot(xSCfSunOnly[:,0],label='Solar Gravity only')
plt.plot(xSCfAllBody[:,0],label='Sun, Earth, and Mars Gravity')
plt.title('X-Coordinate Comparison')
plt.xlabel('Days since Epoch')
plt.ylabel('Kilometers')
plt.legend()

plt.figure()
plt.plot(xSCfSunOnly[:,1],label='Solar Gravity only')
plt.plot(xSCfAllBody[:,1],label='Sun, Earth, and Mars Gravity')
plt.title('Y-Coordinate Comparison')
plt.xlabel('Days since Epoch')
plt.ylabel('Kilometers')
plt.legend()

plt.figure()
plt.plot(diff[:,3],label='X-Velocity Difference')
plt.plot(diff[:,4],label='Y-Velocity Difference')
plt.title('Difference in X and Y Velocities')
plt.xlabel('Days since Epoch')
plt.ylabel('Kilometers')
plt.legend()

plt.figure()
plt.plot(xSCfSunOnly[:,3],label='Solar Gravity only')
plt.plot(xSCfAllBody[:,3],label='Sun, Earth, and Mars Gravity')
plt.title('X-Velocity Comparison')
plt.xlabel('Days since Epoch')
plt.ylabel('Kilometers')
plt.legend()

plt.figure()
plt.plot(xSCfSunOnly[:,4],label='Solar Gravity only')
plt.plot(xSCfAllBody[:,4],label='Sun, Earth, and Mars Gravity')
plt.title('Y-Velocity Comparison')
plt.xlabel('Days since Epoch')
plt.ylabel('Kilometers')
plt.legend()
plt.show()
pdb.set_trace()



