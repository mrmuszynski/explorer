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
from numpy import load
import matplotlib.pyplot as plt
import pdb



###############################################################################
#
#	Recreate plot from page 2 of lab.
#
###############################################################################
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

data2005 = load('GMATLab4Data/opportunity2005.npz')
data2016 = load('GMATLab4Data/opportunity2016.npz')
data2018 = load('GMATLab4Data/opportunity2018.npz')

plt.figure()
TOFLevels = [50,100,150,200,250,300,350,400,450,500]
C3Levels = [16,17,19,21,25,36,55,100]
vInfLevels = [2.5,3,4,5,7.5,10]

TOF = plt.contour(data2005['TOF'],levels=TOFLevels,linewidths=0.5,colors='black')
C3 = plt.contour(data2005['C3'], levels=C3Levels,linewidths=0.5,colors='red')
vInf = plt.contour(data2005['vInf'], levels=vInfLevels,linewidths=0.5,colors='blue')
plt.clabel(TOF,TOFLevels,fmt='%1.0f',fontsize=8)
plt.clabel(C3,C3Levels,fmt='%1.1f',fontsize=8)
plt.clabel(vInf,vInfLevels,fmt='%1.1f',fontsize=8)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label='C3 (km^2/s^2)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label='Vinf (km/s)')
plt.legend(loc='upper left')
plt.xlabel('Days Past 4 Jun 2005')
plt.ylabel('Days Past 1 Dec 2005')
plt.title('2005 Launch Opportunity')

plt.figure()
TOFLevels = [100,150,200,250,300,350,400]
C3Levels = [10,12,16,20,25,36,80]
vInfLevels = [4,5,7.5,10]
TOF = plt.contour(data2016['TOF'], levels=TOFLevels, linewidths=0.5,colors='black')
C3 = plt.contour(data2016['C3'], levels=C3Levels, linewidths=0.5,colors='red')
vInf = plt.contour(data2016['vInf'], levels=vInfLevels, linewidths=0.5,colors='blue')
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
plt.xlabel('Days Past 01 Jan 2016')
plt.ylabel('Days Past 30 Apr 2016')
plt.title('2016 Launch Opportunity')


plt.show()




pdb.set_trace()


