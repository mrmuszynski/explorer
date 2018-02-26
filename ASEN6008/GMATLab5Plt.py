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
from numpy import load, argmin, rad2deg
from timeFcn import timeConvert
import matplotlib.pyplot as plt
import pdb



###############################################################################
#
#	Recreate plot from page 2 of lab.
#
###############################################################################

data2008 = load('GMATLab5Data/opportunity2008.npz')

minC3arg = argmin(data2008['C3'].reshape(1,-1)[0])

print("Launch Date: " + str(
	timeConvert(data2008['departureJD'].reshape(1,-1)[0][minC3arg],
	'jd','calendar')
	))
print("Arrival Date: " + str(
	timeConvert(data2008['arrivalJD'].reshape(1,-1)[0][minC3arg],
	'jd','calendar')
	))
print("Launch C3: " + str(data2008['C3'].reshape(1,-1)[0][minC3arg]))
print("DLA: " + str(rad2deg(data2008['DLA'].reshape(1,-1)[0][minC3arg])))
print("RLA: " + str(rad2deg(data2008['RLA'].reshape(1,-1)[0][minC3arg])))


plt.figure()
C3Levels = [13,14,20,36,50,80,120,200]
DLALevels = [-20,-15,-10,-5,0,5,10,15,20]
RLALevels = [50,60,70,80,90,100,110,120,130,140]
C3 = plt.contour(data2008['C3'],levels=C3Levels,linewidths=0.5,colors='red')
DLA = plt.contour(rad2deg(data2008['DLA']),levels=DLALevels,linewidths=0.5,colors='green')
RLA = plt.contour(rad2deg(data2008['RLA']),levels=RLALevels,linewidths=0.5,colors='blue')
plt.clabel(C3,C3Levels,fmt='%1.1f',fontsize=8)
plt.clabel(DLA,DLALevels,fmt='%1.1f',fontsize=8)
plt.clabel(RLA,RLALevels,fmt='%1.1f',fontsize=8)
# plt.clabel(DLA,DLALevels,fmt='%1.1f',fontsize=8)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label='C3 (km^2/s^2)')
plt.plot([0,0],[0,0],color='green',linewidth=0.5,label='DLA (deg)')
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label='RLA (deg)')
plt.legend(loc='upper left')
plt.xlabel('Days Past 28 Jul 2007')
plt.ylabel('Days Past 28 Feb 2008')
plt.title('2007 Launch Opportunity')

plt.show()





pdb.set_trace()


