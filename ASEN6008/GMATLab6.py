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
from numpy import arctan2, arcsin, arccos, rad2deg, sqrt, cos, arange
from numpy import meshgrid
from numpy.linalg import norm
import celestialBodies
import orbits as o
from timeFcn import timeConvert, day2sec
from analysisTools import closestApproach, turningAngle, computeBrv
from analysisTools import computeBvInf

earth = celestialBodies.celestialBody()
jupiter = celestialBodies.celestialBody()
pluto = celestialBodies.celestialBody()
sun = celestialBodies.celestialBody()
earth.initEarth()
jupiter.initJupiter()
pluto.initPluto()
sun.initSun()

###############################################################################
#
#	Recreate plot from page 1 of lab.
#
###############################################################################
launchJD = 2453755.29167
jgaJD = 2454159.73681
plutoEncounterJD = 2457217.99931

earthStateLaunch = earth.meeusStateUpdate(launchJD)
jupiterStateJGA = jupiter.meeusStateUpdate(jgaJD)
earth2jupiterTOFd = jgaJD - launchJD
earth2jupiterTOFs = day2sec(earth2jupiterTOFd)
lamEarth2JGA = o.lambert(earthStateLaunch,jupiterStateJGA,earth2jupiterTOFs,mu=sun.mu)
RLA = arctan2(lamEarth2JGA['vInfDepart'][1],lamEarth2JGA['vInfDepart'][0])
DLA = arcsin(lamEarth2JGA['vInfDepart'][0]/norm(lamEarth2JGA['vInfDepart']))
print('Part I')
print('Problem 1')
print('C3: ' + str(lamEarth2JGA['C3']) + 'km^2/s^2')
print('RLA: ' + str(rad2deg(RLA)) + ' degrees')
print('DLA: ' + str(rad2deg(DLA)) + ' degrees')
print('Vinf Arriving At Jupiter:' + str(lamEarth2JGA['vInfArrive']))
print('Vinf Arriving At Jupiter (mag):' + str(norm(lamEarth2JGA['vInfArrive'])))

plutoStateEncoutner = pluto.meeusStateUpdate(plutoEncounterJD)
jupiter2PlutoTOFd = plutoEncounterJD - jgaJD
jupiter2PlutoTOFs = day2sec(jupiter2PlutoTOFd)
lamJGA2Pluto = o.lambert(jupiterStateJGA,plutoStateEncoutner,jupiter2PlutoTOFs,mu=sun.mu)
print('Problem 2')
print('Vinf Departing Jupiter:' + str(lamJGA2Pluto['vInfDepart']))
print('Vinf Departing Jupiter (mag):' + str(norm(lamJGA2Pluto['vInfDepart'])))
print('Vinf Arriving at Pluto (mag):' + str(norm(lamJGA2Pluto['vInfArrive'])))
print('Vinf Arriving at Pluto:' + str(lamJGA2Pluto['vInfArrive']))

print('Problem 3')
print('')
print('Problem 4')
rJupiter = 71492 #km
# bPlaneParams = computeB(r,v,jupiter.mu)
turnAngle = arccos(
	lamEarth2JGA['vInfArrive'].dot(lamJGA2Pluto['vInfDepart'])/
	norm(lamEarth2JGA['vInfArrive'])/norm(lamJGA2Pluto['vInfDepart'])
	)
rClosestApproach = closestApproach(
	turnAngle, jupiter.mu, norm(lamJGA2Pluto['vInfDepart']))
print('turnAngle (rad): ' + str(turnAngle))
print('turnAngle (deg): ' + str(rad2deg(turnAngle)))
print('rClosestApproach: ' + str(rClosestApproach))
print('altClosestApproach: ' + str(rClosestApproach-rJupiter))
print('Problem 5')
bPlaneParams = computeBvInf(
	lamEarth2JGA['vInfArrive'],lamJGA2Pluto['vInfDepart'],jupiter.mu)
print('bPlane: ' + str(bPlaneParams[1].dot(bPlaneParams[0])))
vInHelio = jupiterStateJGA[3:6] + lamEarth2JGA['vInfArrive']
vOutHelio = jupiterStateJGA[3:6] + lamJGA2Pluto['vInfDepart']
print('Helocentric DeltaV: ' + str(vOutHelio-vInHelio))
print('Helocentric DeltaV (mag): ' + str(norm(vOutHelio-vInHelio)))

print('Part 2')
launchDates = arange(2453714.5,2453794.5)
jupiterDates = arange(2454129.5,2454239.5)
plutoDates = arange(2456917.5,2457517.5)

meshed1 = meshgrid(launchDates,jupiterDates)
meshed2 = meshgrid(jupiterDates,plutoDates)

earthDepartureDates = meshed1[0].reshape(-1)
jupiterArrivalDates = meshed1[1].reshape(-1)
earthStates = earth.meeusStateUpdate(earthDepartureDates)
jupiterStates1 = jupiter.meeusStateUpdate(jupiterArrivalDates)
jupiterDepartureDates = meshed2[0].reshape(-1)
plutoArrivalDates = meshed2[1].reshape(-1)
jupiterStates2 = jupiter.meeusStateUpdate(jupiterDepartureDates)
plutoStates = pluto.meeusStateUpdate(plutoArrivalDates)

e2jTOFd = jupiterArrivalDates - earthDepartureDates
e2jTOFs = day2sec(e2jTOFd)
j2pTOFd = plutoArrivalDates - jupiterDepartureDates
j2pTOFs = day2sec(j2pTOFd)

from datetime import datetime
start = datetime.now()
e2jLam = o.multiLambert(earthStates,jupiterStates1,e2jTOFs,mu=sun.mu,iterations=100)

TOFLevels = [350,375,400,425,450,475,500]
C3Levels = [150,175,200,225,250,275,300]
vInfLevels = [14,15,16,17,18]

TOF = plt.contour(e2jTOFd.reshape(110,80),levels=TOFLevels,linewidths=0.5,colors='black')
C3 = plt.contour(e2jLam['C3'].reshape(110,80),levels=C3Levels,linewidths=0.5,colors='red')
vInf = plt.contour(e2jLam['magVInfArrive'].reshape(110,80),levels=vInfLevels,linewidths=0.5,colors='blue')

plt.clabel(TOF,TOFLevels,fmt='%1.1f',fontsize=8)
plt.clabel(C3,C3Levels,fmt='%1.1f',fontsize=8)
plt.clabel(vInf,vInfLevels,fmt='%1.1f',fontsize=8)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label='C3 (km^2/s^2)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label=r'$v_\infty$ (deg)')
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.legend(loc='upper left')
plt.xlabel('Days Past December 10, 2005')
plt.ylabel('Days Past January 29, 2007')
plt.title('New Horizons--Launch to Jupiter')


print(datetime.now() - start)
start = datetime.now()
j2pLam = o.multiLambert(jupiterStates2,plutoStates,j2pTOFs,mu=sun.mu)

plt.figure()
TOFLevels = [2700,2800,2900,3000,3100,3200,3300]
vInfLevels1 = [16,16.5,17,17.5,18]
vInfLevels2 = [7.3,7.4,7.5,7.6]

TOF = plt.contour(j2pTOFd.reshape(600,110),levels=TOFLevels,linewidths=0.5,colors='black')
vInf1 = plt.contour(sqrt(j2pLam['C3']).reshape(600,110),levels=vInfLevels1,linewidths=0.5,colors='red')
vInf2 = plt.contour(j2pLam['magVInfArrive'].reshape(600,110),levels=vInfLevels2,linewidths=0.5,colors='blue')

plt.clabel(TOF,TOFLevels,fmt='%1.1f',fontsize=8)
plt.clabel(vInf1,vInfLevels1,fmt='%1.1f',fontsize=8)
plt.clabel(vInf2,vInfLevels2,fmt='%1.1f',fontsize=8)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label='C3 (km^2/s^2)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label=r'$v_\infty$ (deg)')
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.legend(loc='upper left')
plt.xlabel('Days Past December 10, 2005')
plt.ylabel('Days Past January 29, 2007')
plt.title('New Horizons--Launch to Jupiter')
print(datetime.now() - start)

pdb.set_trace()


