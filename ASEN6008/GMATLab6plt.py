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
from numpy import savez, load, sqrt, logical_and, logical_or, zeros, arccos
from numpy import hstack
from numpy.linalg import norm
import celestialBodies
import orbits as o
from timeFcn import timeConvert, day2sec
from analysisTools import porkchopPlot, closestApproach

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

e2jLam = load('GMATLab6Data/opportunity2008.npz')

TOFLevels = [350,375,400,425,450,475,500]
C3Levels = [125,150,175,200,225,250,275,300,325,350]
vInfLevels = [14,15,16,17,18,19,20,21]

e2jTOFd = e2jLam['arrivalJD'] - e2jLam['departureJD']

TOF = plt.contour(e2jTOFd.reshape(111,81),levels=TOFLevels,linewidths=0.5,colors='black')
C3 = plt.contour(e2jLam['C3'].reshape(111,81),levels=C3Levels,linewidths=0.5,colors='red')
vInf = plt.contour(e2jLam['vInf'].reshape(111,81),levels=vInfLevels,linewidths=0.5,colors='blue')

plt.clabel(TOF,TOFLevels,fmt='%1.1f',fontsize=8)
plt.clabel(C3,C3Levels,fmt='%1.1f',fontsize=8)
plt.clabel(vInf,vInfLevels,fmt='%1.1f',fontsize=8)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label='C3 (km^2/s^2)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label=r'$v_\infty$ (km/s)')
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.legend(loc='upper left')
plt.xlabel('Days Past December 10, 2005')
plt.ylabel('Days Past January 29, 2007')
plt.title('New Horizons--Launch to Jupiter')


plt.figure()

j2pLam = load('GMATLab6Data/j2p.npz')

TOFLevels = [2700,2800,2900,3000,3100,3200,3300]
vInfLevels1 = [17.5,18,18.5,19,19.5,20,20.5,21]
vInfLevels2 = [12.5,13,13.5,14,14.5,15,15.5]

j2pTOFd = j2pLam['arrivalJD'] - j2pLam['departureJD']
pdb.set_trace()

TOF = plt.contour(j2pTOFd.reshape(601,111),levels=TOFLevels,linewidths=0.5,colors='black')
vInf1 = plt.contour(sqrt(j2pLam['C3']).reshape(601,111),levels=vInfLevels1,linewidths=0.5,colors='red')
vInf2 = plt.contour(j2pLam['vInf'].reshape(601,111),levels=vInfLevels2,linewidths=0.5,colors='blue')

plt.clabel(TOF,TOFLevels,fmt='%1.1f',fontsize=8)
plt.clabel(vInf1,vInfLevels1,fmt='%1.1f',fontsize=8)
plt.clabel(vInf2,vInfLevels2,fmt='%1.1f',fontsize=8)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label=r'$v_\infty$ out of Jupiter (km/s))')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label=r'$v_\infty$ into Pluto (km/s)')
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.legend(loc='upper left')
plt.xlabel('Days Past January 29, 2007')
plt.ylabel('Days Past September 17, 2014')
plt.title('New Horizons--Jupiter to Pluto/Charon')


departureDate = [2006,9]
departureJD = timeConvert(departureDate,'ydnhms','jd')


jupiterArrivalInd = e2jLam['departureJD'] == departureJD
possibleJupiterArrivalJD = e2jLam['arrivalJD'][jupiterArrivalInd]
possibleC3s = e2jLam['C3'][jupiterArrivalInd]
possibleVInf = e2jLam['vInf'][jupiterArrivalInd]

possibleC3ind = possibleC3s < 180
possibleJupiterArrivalJD = possibleJupiterArrivalJD[possibleC3ind]
possibleC3s = possibleC3s[possibleC3ind]
possibleVInf = possibleVInf[possibleC3ind]

finalInd = zeros(j2pLam['departureJD'].shape)
launchC3 = zeros(j2pLam['departureJD'].shape)
vInfArrive = zeros(j2pLam['departureJD'].shape)
count=0
for i in range(0,len(possibleJupiterArrivalJD)):
	ind = logical_and(
		j2pLam['departureJD'] == possibleJupiterArrivalJD[i],
		abs(sqrt(j2pLam['C3']) - possibleVInf[i]) < 0.4
		)
	ind = logical_and(
		ind,
		j2pLam['vInf'] < 14.5
		)	
	launchC3[ind] = possibleC3s[i]
	vInfArrive[ind] = possibleVInf[i]
	finalInd = logical_or(finalInd,ind)


jupiterDepatureJD = j2pLam['departureJD'][finalInd]
plutoArrivalJD = j2pLam['arrivalJD'][finalInd]

launchIndex = [x in jupiterDepatureJD for x in possibleJupiterArrivalJD]
print('Smallest C3: ' + str(min(possibleC3s[launchIndex])))
print('Earliest Arrival: ' + str(min(plutoArrivalJD)))
print('Smallest vInf: ' + str(min(j2pLam['vInf'][finalInd])))

#FUCKMEIHAVETOCALCULATEPSINOW
earthState = earth.meeusStateUpdate(departureJD)
jupiterStates = jupiter.meeusStateUpdate(jupiterDepatureJD)
plutoStates = pluto.meeusStateUpdate(plutoArrivalJD)

psi = []
rP = []
vInfDiff = []
C333 = []
asdf = []
zcxv = []
for i in range(0,len(jupiterDepatureJD)):
	lamIn = o.lambert(
		earthState,
		jupiterStates[i],
		day2sec(jupiterDepatureJD[i] - departureJD),
		mu=sun.mu
		)
	lamOut = o.lambert(
		jupiterStates[i],
		plutoStates[i],
		day2sec(plutoArrivalJD[i] - jupiterDepatureJD[i]),
		mu=sun.mu
		)
	vInfDiff = hstack([
		vInfDiff,
		abs(norm(lamIn['vInfArrive']) - norm(lamOut['vInfDepart']))
		])
	asdf = hstack([asdf,norm(lamIn['vInfArrive'])])
	zcxv = hstack([zcxv,norm(lamOut['vInfDepart'])])
	C333 = hstack([C333,lamIn['C3']])
	thisPsi = \
	arccos(
		lamIn['vInfArrive'].dot(lamOut['vInfDepart'])/norm(lamIn['vInfArrive'])/norm(lamOut['vInfDepart']))
	
	psi = hstack([psi,thisPsi])
	
	rP = hstack([rP,
		norm(
			closestApproach(thisPsi,jupiter.mu,lamIn['magVInfArrive']))])

from numpy import argmin
minArg = argmin(vInfDiff)
min(vInfDiff)
print('C3: ' + str(C333[minArg]))
print('Jupiter: ' + str(jupiterDepatureJD[argmin(possibleC3s[launchIndex])]))
print('Arrival: ' + str(plutoArrivalJD[argmin(possibleC3s[launchIndex])]))
print('Smallest vInf: ' + str(j2pLam['vInf'][finalInd][argmin(possibleC3s[launchIndex])]))
print(asdf[minArg])
print(zcxv[minArg])

highEnough = rP > 2144760*31/30
jupiterDepatureJD2 = jupiterDepatureJD[highEnough]
plutoArrivalJD2 = plutoArrivalJD[highEnough]
rPHighEnough = rP[highEnough] 
vInfDiffHighEnough = vInfDiff[highEnough]
minArg = argmin(vInfDiffHighEnough)

launchIndex2 = [x in jupiterDepatureJD2 for x in possibleJupiterArrivalJD]
print('Problem 7')
print('Smallest C3: ' + str(min(possibleC3s[launchIndex2])))
print('Earliest Arrival: ' + str(plutoArrivalJD2))
print('Smallest vInf: ' + str(min(j2pLam['vInf'][finalInd][highEnough])))
print('Problem 7b')
print('C3: ' + str(C333[minArg]))
print('Jupiter: ' + str(jupiterDepatureJD2[argmin(possibleC3s[launchIndex2])]))
print('Arrival: ' + str(plutoArrivalJD2[argmin(possibleC3s[launchIndex2])]))
print('Smallest vInf: ' + str(j2pLam['vInf'][finalInd][argmin(possibleC3s[launchIndex2])]))
pdb.set_trace()



