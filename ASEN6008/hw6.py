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
from analysisTools import computeB, dBdV

from numpy import linspace, hstack, pi, array, arccos, sin, cos, cross
from numpy import rad2deg, arctan2, vstack, sqrt, logspace, ones
from numpy import logical_and, argmax
from numpy.linalg import norm, inv
import matplotlib.pyplot as plt
from timeFcn import timeConvert, sec2day, day2sec
from util import r3
import pdb
import orbits as o
from matplotlib.path import Path
import matplotlib.patches as patches

def closestApproach(psi, mu, vInf):
	return mu/vInf**2*(cos((pi-psi)/2)**-1 -1)

def turningAnlge(rP, mu, vInf):
	return  pi -2*arccos((rP/mu*vInf**2 + 1)**-1 )

###############################################################################
#
# 	Problem 1
#
###############################################################################

sun = celestialBodies.celestialBody()
venus = celestialBodies.celestialBody()
earth = celestialBodies.celestialBody()
jupiter = celestialBodies.celestialBody()
sun.initSun()
venus.initVenus()
earth.initEarth()
jupiter.initJupiter()


launchJD = 2447814
VGA1JD = 2447932
EGA1JD = 2448235
EGA2JD = 2448965.484378
JOIJD = 2450154

launch2VenusSeconds = day2sec(VGA1JD - launchJD)
venus2EarthSeconds = day2sec(EGA1JD - VGA1JD)
earth2EarthSeconds = day2sec(EGA2JD - EGA1JD)
earth2jupiterSeconds = day2sec(JOIJD - EGA2JD)

earthLaunchState = earth.meeusStateUpdate(launchJD)
venusGA1State = venus.meeusStateUpdate(VGA1JD)
earthGA1State = earth.meeusStateUpdate(EGA1JD)
earthGA2State = earth.meeusStateUpdate(EGA2JD)
jupiterArrivalState = jupiter.meeusStateUpdate(JOIJD)

launch2Venus = o.lambert(earthLaunchState,venusGA1State,launch2VenusSeconds,mu=sun.mu)
venus2Earth = o.lambert(venusGA1State,earthGA1State,venus2EarthSeconds,mu=sun.mu)
earth2Earth = o.lambert(earthGA1State,earthGA2State,earth2EarthSeconds,mu=sun.mu)
earth2jupiter = o.lambert(earthGA2State,jupiterArrivalState,earth2jupiterSeconds,mu=sun.mu)

pEarth = 365.242189
pResonant = 2*pEarth
aResonant = ((day2sec(pResonant)/2/pi)**2*sun.mu)**(1/3)

vSCmag = sqrt(2*sun.mu/norm(earthGA1State[0:3])-sun.mu/aResonant)

#vSCmag**2 = vInf**2 + vP**2 - 2*vInf*vP*cosTheta
vInfInEGA1 = venus2Earth['vInfArrive']
vInfInEGA1Norm = norm(vInfInEGA1)
vP = norm(earthGA1State[3:6])
cosTheta = (vInfInEGA1Norm**2 + vP**2 - vSCmag**2)/(2*vInfInEGA1Norm*vP)
theta1 = arccos(cosTheta)


phi = linspace(0,2*pi,1000)
vInfOutEGA1 = vInfInEGA1Norm*vstack([
	cos(pi - theta1)*ones(len(phi)),
	sin(pi - theta1)*cos(phi),
	-sin(pi - theta1)*sin(phi)
	])

vHat = earthGA1State[3:6]/norm(earthGA1State[3:6])
nHat = cross(earthGA1State[0:3],earthGA1State[3:6])
nHat = nHat/norm(nHat)
cHat = cross(vHat,nHat)

VNC2ijk = vstack([vHat,nHat,cHat]).T

vInfOutEGA1 = VNC2ijk.dot(vInfOutEGA1)

vInfInEGA2 = vInfOutEGA1 + earthGA1State[3:6].reshape(-1,1) - earthGA2State[3:6].reshape(-1,1)

vInfInEGA2Norm = norm(vInfInEGA2)
vInfOutEGA2 = earth2jupiter['vInfDepart']
vInfOutEGA2Norm = norm(vInfOutEGA2)

vP = norm(earthGA2State[3:6])
cosTheta = (vInfInEGA2Norm**2 + vP**2 - vSCmag**2)/(2*vInfInEGA2Norm*vP)
theta2 = arccos(cosTheta)

cosPsiEGA1 = \
	vInfOutEGA1.T.dot(vInfInEGA1.reshape(3,1)).T[0]/(vInfInEGA1Norm**2)
psiEGA1 = arccos(cosPsiEGA1)
rPEGA1 = closestApproach(psiEGA1, earth.mu, vInfInEGA1Norm)

cosPsiEGA2 = vInfOutEGA2.dot(vInfInEGA2)/(vInfOutEGA2Norm**2)
psiEGA2 = arccos(cosPsiEGA2)
rPEGA2 = closestApproach(psiEGA2, earth.mu, vInfOutEGA2Norm)

gootPhiInds = logical_and(rPEGA1 > 6378.14+300, rPEGA2 > 6378.14+300)
goodPhis = phi[gootPhiInds]

optimalPhi = phi[argmax(rPEGA2)]




fig = plt.figure()
ax = fig.add_subplot(111)
EGA1, = ax.plot(rad2deg(phi), rPEGA1,label='Earth Gravity Assist 1')
EGA2, = ax.plot(rad2deg(phi), rPEGA2,label='Earth Gravity Assist 2')
verts = [
    (rad2deg(goodPhis)[0], ax.get_ylim()[0]), # left, bottom
    (rad2deg(goodPhis)[0], ax.get_ylim()[1]), # left, top
    (rad2deg(goodPhis)[-1], ax.get_ylim()[1]), # right, top
    (rad2deg(goodPhis)[-1], ax.get_ylim()[0]), # right, bottom
    (0., 0.), # ignored
	]
codes = [Path.MOVETO,
     Path.LINETO,
     Path.LINETO,
     Path.LINETO,
     Path.CLOSEPOLY,
     ]
smallestRp = ax.axhline(6378.14+300, color='black', linestyle='--',
	label=r'Minimum $r_p$ = $r_\oplus + 300$ km')
path = Path(verts, codes)
patch = patches.PathPatch(path, facecolor='orange', lw=0,
	label='Acceptable Gravity Assists')
patch.set_alpha(0.3)
ax.legend(handles=[patch,EGA1,EGA2,smallestRp])
ax.add_patch(patch)
ax.set_title(r'Radius of Periapse for EGA1 and EGA2 versus $\phi$')
ax.set_xlim([0,360])
ax.set_xlabel(r'$\phi$ ($\circ$)')
ax.set_ylabel(r'$r_p$ (km)')



print('vInf at EGA1 Arrival: ' + str(vInfInEGA1))
print('vInf at EGA2 Departure: ' + str(vInfOutEGA2))
print('vInf at EGA1 Arrival (mag): ' + str(norm(vInfInEGA1)))
print('vInf at EGA2 Departure (mag): ' + str(norm(vInfOutEGA2)))
pdb.set_trace()














