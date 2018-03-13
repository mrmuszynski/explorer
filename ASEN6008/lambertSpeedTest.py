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
from numpy import hstack, vstack, arange, empty, meshgrid
import matplotlib.pyplot as plt
from timeFcn import timeConvert, sec2day, day2sec
import pdb
import orbits as o

###########################################################################
#
# Problem 0: This part remakes plots from KD's homework assignment as 
#	a check that I'm doing this right.
#
###########################################################################
from datetime import datetime

startTime = datetime.now()
sun = celestialBodies.celestialBody()
sun.initSun()
earth = celestialBodies.celestialBody()
earth.initEarth()
mars = celestialBodies.celestialBody()
mars.initMars()

departureDates = arange(2458200.0,2458321.0)
arrivalDates = arange(2458350.0 ,2458601.0)

meshed = meshgrid(departureDates,arrivalDates)
departureDates = meshed[0].reshape(-1)
arrivalDates = meshed[1].reshape(-1)

print(datetime.now() - startTime)
startTime = datetime.now()

earthState = earth.meeusStateUpdate(departureDates)
print(datetime.now() - startTime)
startTime = datetime.now()

marsState = mars.meeusStateUpdate(arrivalDates)
print(datetime.now() - startTime)
startTime = datetime.now()

TOFd = arrivalDates-departureDates
TOFs = day2sec(TOFd)
# pdb.set_trace()
# for i in range(0,len(marsState)):
# 	lam = o.lambert(
# 		earthState[i],
# 		marsState[i],
# 		TOFs[i],
# 		mu=sun.mu)
print(datetime.now() - startTime)
startTime = datetime.now()
lam = o.multiLambert(earthState,marsState,TOFs,mu=sun.mu)
print(datetime.now() - startTime)
from numpy import load
data2018 = load('GMATLab4Data/opportunity2018.npz')


plt.figure()
TOFLevels = [50,100,150,200,250,300,350]
C3Levels = [8,10,12,16,20,25,36,80]
vInfLevels = [3,3.5,4,4.5,5,5.5,8]
TOF = plt.contour(data2018['TOF'], levels=TOFLevels, linewidths=0.5,colors='black')
C3 = plt.contour(data2018['C3'], levels=C3Levels, linewidths=0.5,colors='red')
vInf = plt.contour(data2018['vInf'], levels=vInfLevels, linewidths=0.5,colors='blue')
plt.clabel(TOF,TOFLevels,fmt='%1.0f',fontsize=8)
plt.clabel(C3,C3Levels,fmt='%1.1f',fontsize=8)
plt.clabel(vInf,vInfLevels,fmt='%1.1f',fontsize=8)
#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label='C3 (km^2/s^2)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label='Vinf (km/s)')
plt.legend(loc='lower right')
plt.xlabel('Days Past 22 Mar 2018')
plt.ylabel('Days Past 19 Aug 2018')
plt.title('2018 Launch Opportunity')


plt.figure()
TOFLevels = [50,100,150,200,250,300,350]
C3Levels = [8,10,12,16,20,25,36,80]
vInfLevels = [3,3.5,4,4.5,5,5.5,8]
TOF = plt.contour(
	(arrivalDates - departureDates).reshape(251,121),
	levels=TOFLevels, linewidths=0.5,colors='black')
C3 = plt.contour(lam['C3'].reshape(251,121), levels=C3Levels, linewidths=0.5,colors='red')
vInf = plt.contour(lam['magVInfArrive'].reshape(251,121), levels=vInfLevels, linewidths=0.5,colors='blue')
plt.clabel(TOF,TOFLevels,fmt='%1.0f',fontsize=8)
plt.clabel(C3,C3Levels,fmt='%1.1f',fontsize=8)
plt.clabel(vInf,vInfLevels,fmt='%1.1f',fontsize=8)
#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label='C3 (km^2/s^2)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label='Vinf (km/s)')
plt.legend(loc='lower right')
plt.xlabel('Days Past 22 Mar 2018')
plt.ylabel('Days Past 19 Aug 2018')
plt.title('2018 Launch Opportunity')
plt.show()
pdb.set_trace()





