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
sys.path.insert(0, '../../classes')
sys.path.insert(0, '../../prop')
sys.path.insert(0, '../../fsw')
sys.path.insert(0, '../../../lib')

import matplotlib.pyplot as plt
import pdb
from numpy import savez, load, sqrt, logical_and, logical_or, zeros, arccos
from numpy import hstack, empty, rad2deg
from numpy.linalg import norm
# import celestialBodies
import orbits as o
from timeFcn import timeConvert, day2sec
# from analysisTools import porkchopPlot, closestApproach

# earth = celestialBodies.celestialBody()
# jupiter = celestialBodies.celestialBody()
# pluto = celestialBodies.celestialBody()
# sun = celestialBodies.celestialBody()
# earth.initEarth()
# jupiter.initJupiter()
# pluto.initPluto()
# sun.initSun()

###############################################################################
#
#	Test Plots
#
###############################################################################


launch2VGA = load('testData/launch2VGA.npz')

actualLaunchJD = timeConvert([1989,291],'ydnhms','jd')
actualVGAJD = timeConvert([1990,41],'ydnhms','jd')

earliestLaunchJD = 2447814 - 50
earliestVGAJD = 2447932 - 50

launch2VGAd = launch2VGA['arrivalJD'] - launch2VGA['departureJD']
pdb.set_trace()
TOFLevels = [50,75,100,125,150,175,200]
TOF = plt.contour(launch2VGAd,levels=TOFLevels,linewidths=0.5,colors='black')
plt.clabel(TOF,TOFLevels,fmt='%1.1f',fontsize=8)

C3Levels = [3,4,5,7,10,15]
C3 = plt.contour(sqrt(launch2VGA['C3']).reshape(141,101),levels=C3Levels,linewidths=0.5,colors='red')
plt.clabel(C3,C3Levels,fmt='%1.1f',fontsize=8)

vInfInLevels = [5,6,8,10,15,25,50]
vInfIn = plt.contour(launch2VGA['vInf'].reshape(141,101),levels=vInfInLevels,linewidths=0.5,colors='blue')
plt.clabel(vInfIn,vInfInLevels,fmt='%1.1f',fontsize=8)

plt.plot(
	actualLaunchJD - earliestLaunchJD, actualVGAJD - earliestVGAJD,
	'.',color='lawngreen',markersize=10)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label='C3 (km^2/s^2)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label=r'$v_{\infty^{in},VGA}$ (km/s)')
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.plot([0,0],[0,0],'.',color='lawngreen',label='True Launch/VGA Dates',markersize=10)
plt.legend(loc='upper left')
plt.xlabel('Days Past August 25, 1989')
plt.ylabel('Days Past December 21, 1989')
plt.title('Galileo--Launch to VGA')

################################################################################
################################################################################
################################################################################

VGA2EGA1 = load('testData/VGA2EGA1.npz')

plt.figure()
actualVGAJD = timeConvert([1990,41],'ydnhms','jd')
actualEGA1JD = timeConvert([1990,281],'ydnhms','jd')

earliestVGAJD = 2447932 - 50
earliestEGA1JD = 2448235 - 210


VGA2EGA1d = VGA2EGA1['arrivalJD'] - VGA2EGA1['departureJD']
TOFLevels = [225,250,275,300,325,350,375]
TOF = plt.contour(VGA2EGA1d,levels=TOFLevels,linewidths=0.5,colors='black')
plt.clabel(TOF,TOFLevels,fmt='%1.1f',fontsize=8)

vInfOutLevels = [4.5,5,6,7,8,9,10,12.5,15,20]
vInfOut = plt.contour(sqrt(VGA2EGA1['C3'].reshape(VGA2EGA1d.shape)),levels=vInfOutLevels,linewidths=0.5,colors='red')
plt.clabel(vInfOut,vInfOutLevels,fmt='%1.1f',fontsize=8)

vInfInLevels = [7,8,9,10,15,25]
vInfIn = plt.contour(VGA2EGA1['vInf'].reshape(VGA2EGA1d.shape),levels=vInfInLevels,linewidths=0.5,colors='blue')
plt.clabel(vInfIn,vInfInLevels,fmt='%1.1f',fontsize=8)

plt.plot(
	actualVGAJD - earliestVGAJD,  actualEGA1JD - earliestEGA1JD,
	'.',color='lawngreen',markersize=10)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label=r'$v_{\infty^{out},VGA}$ (km/s)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label=r'$v_{\infty^{in},EGA1}$ (km/s)')
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.plot([0,0],[0,0],'.',color='lawngreen',label='True VGA/EGA1 Dates',markersize=10)
plt.legend(loc='upper left')
plt.xlabel('Days Past December 21, 1989')
plt.ylabel('Days Past May 13, 1990')
plt.title('Galileo--VGA to EGA1')

################################################################################
################################################################################
################################################################################

EGA22JOI = load('data/EGA22JOI.npz')

plt.figure()
actualEGA2JD = timeConvert([1992,343],'ydnhms','jd')
actualJOIJD = timeConvert([1995,343],'ydnhms','jd')

earliestEGA2JD = 2448965.5 - 100
earliestJOIJD = 2450154 - 150


launch2VGAd = EGA22JOI['arrivalJD'] - EGA22JOI['departureJD']
TOFLevels = [1000,1100,1200,1300]
TOF = plt.contour(launch2VGAd,levels=TOFLevels,linewidths=0.5,colors='black')
plt.clabel(TOF,TOFLevels,fmt='%1.1f',fontsize=8)

vInfOutLevels = [9,10,12.5,15,20]
vInfOut = plt.contour(sqrt(EGA22JOI['C3'].reshape(launch2VGAd.shape)),levels=vInfOutLevels,linewidths=0.5,colors='red')
plt.clabel(vInfOut,vInfOutLevels,fmt='%1.1f',fontsize=8)

vInfInLevels = [6,7,8,9,10,11,12,13,14]
vInfIn = plt.contour(EGA22JOI['vInf'].reshape(launch2VGAd.shape),levels=vInfInLevels,linewidths=0.5,colors='blue')
plt.clabel(vInfIn,vInfInLevels,fmt='%1.1f',fontsize=8)

plt.plot(
	actualEGA2JD - earliestEGA2JD,  actualJOIJD - earliestJOIJD,
	'.',color='lawngreen',markersize=10)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label=r'$v_{\infty^{out},EGA2}$ (km/s)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label=r'$v_{\infty^{in},JOI}$ (km/s)')
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.plot([0,0],[0,0],'.',color='lawngreen',label='True EGA2/JOI Dates',markersize=10)
plt.legend(loc='upper left')
plt.xlabel('Days Past August 31, 1992')
plt.ylabel('Days Past October 13, 1995')
plt.title('Galileo--EGA2 to JOI')
###############################################################################
#
#	Launch to VGA Porkchop
#
###############################################################################

plt.figure()
launch2VGA = load('data/launch2VGA.npz')

actualLaunchJD = timeConvert([1989,291],'ydnhms','jd')
actualVGAJD = timeConvert([1990,41],'ydnhms','jd')

earliestLaunchJD = 2447814 - 50
earliestVGAJD = 2447932 - 50

launch2VGAd = launch2VGA['arrivalJD'] - launch2VGA['departureJD']
TOFLevels = [50,75,100,125,150,175,200]
TOF = plt.contour(launch2VGAd,levels=TOFLevels,linewidths=0.5,colors='black')
plt.clabel(TOF,TOFLevels,fmt='%1.1f',fontsize=8)

C3Levels = [3,4,5,7,10,15]
C3 = plt.contour(sqrt(launch2VGA['C3']),levels=C3Levels,linewidths=0.5,colors='red')
plt.clabel(C3,C3Levels,fmt='%1.1f',fontsize=8)

vInfInLevels = [5,6,8,10,15,25,50]
vInfIn = plt.contour(launch2VGA['vInf'],levels=vInfInLevels,linewidths=0.5,colors='blue')
plt.clabel(vInfIn,vInfInLevels,fmt='%1.1f',fontsize=8)

plt.plot(
	actualLaunchJD - earliestLaunchJD, actualVGAJD - earliestVGAJD,
	'.',color='lawngreen',markersize=10)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label='C3 (km^2/s^2)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label=r'$v_{\infty^{in},VGA}$ (km/s)')
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.plot([0,0],[0,0],'.',color='lawngreen',label='True Launch/VGA Dates',markersize=10)
plt.legend(loc='upper left')
plt.xlabel('Days Past August 25, 1989')
plt.ylabel('Days Past December 21, 1989')
plt.title('Galileo--Launch to VGA')



plt.figure()
actualLaunchJD = timeConvert([1989,291],'ydnhms','jd')
actualVGAJD = timeConvert([1990,41],'ydnhms','jd')

earliestLaunchJD = 2447814 - 50
earliestVGAJD = 2447932 - 50

launch2VGAd = launch2VGA['arrivalJD'] - launch2VGA['departureJD']
TOFLevels = [50,75,100,125,150,175,200]
TOF = plt.contour(launch2VGAd,levels=TOFLevels,linewidths=0.5,colors='black')
plt.clabel(TOF,TOFLevels,fmt='%1.1f',fontsize=8)

C3Levels = [3,4,5,7,10,15]
C3 = plt.contour(sqrt(launch2VGA['C3']),levels=C3Levels,linewidths=0.5,colors='red')
plt.clabel(C3,C3Levels,fmt='%1.1f',fontsize=8)

DLALevels = [-60,-40,-20,0,20,40,60]
DLA = plt.contour(rad2deg(launch2VGA['DLA']),levels=DLALevels,linewidths=0.5,colors='green')
plt.clabel(DLA,DLALevels,fmt='%1.1f',fontsize=8)

RLALevels = [-100,-90,-80,-70,-60,-50,-40,-30,-20]
DLA = plt.contour(rad2deg(launch2VGA['RLA']),levels=RLALevels,linewidths=0.5,colors='blue')
plt.clabel(DLA,RLALevels,fmt='%1.1f',fontsize=8)

plt.plot(
	actualLaunchJD - earliestLaunchJD, actualVGAJD - earliestVGAJD,
	'.',color='lawngreen',markersize=10)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label='C3 (km^2/s^2)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label='RLA (deg)')
plt.plot([0,0],[0,0],color='green',linewidth=0.5,label='DLA (deg)')
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.plot([0,0],[0,0],'.',color='lawngreen',label='True Launch/VGA Dates',markersize=10)
plt.legend(loc='upper left')
plt.xlabel('Days Past August 25, 1989')
plt.ylabel('Days Past December 21, 1989')
plt.title('Galileo--Launch to VGA')
###############################################################################
#
#	Launch to VGA Porkchop
#
###############################################################################

VGA2EGA1 = load('data/VGA2EGA1.npz')

plt.figure()
actualVGAJD = timeConvert([1990,41],'ydnhms','jd')
actualEGA1JD = timeConvert([1990,281],'ydnhms','jd')

earliestVGAJD = 2447932 - 50
earliestEGA1JD = 2448235 - 210


launch2VGAd = VGA2EGA1['arrivalJD'] - VGA2EGA1['departureJD']
TOFLevels = [225,250,275,300,325,350,375]
TOF = plt.contour(launch2VGAd,levels=TOFLevels,linewidths=0.5,colors='black')
plt.clabel(TOF,TOFLevels,fmt='%1.1f',fontsize=8)

vInfOutLevels = [4,4.5,5,6,7,8,9,10,12.5,15,20]
vInfOut = plt.contour(sqrt(VGA2EGA1['C3']),levels=vInfOutLevels,linewidths=0.5,colors='red')
plt.clabel(vInfOut,vInfOutLevels,fmt='%1.1f',fontsize=8)

vInfInLevels = [7,8,9,10,15,25]
vInfIn = plt.contour(VGA2EGA1['vInf'],levels=vInfInLevels,linewidths=0.5,colors='blue')
plt.clabel(vInfIn,vInfInLevels,fmt='%1.1f',fontsize=8)

plt.plot(
	actualVGAJD - earliestVGAJD,  actualEGA1JD - earliestEGA1JD,
	'.',color='lawngreen',markersize=10)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label=r'$v_{\infty^{out},VGA}$ (km/s)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label=r'$v_{\infty^{in},EGA1}$ (km/s)')
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.plot([0,0],[0,0],'.',color='lawngreen',label='True VGA/EGA1 Dates',markersize=10)
plt.legend(loc='upper left')
plt.xlabel('Days Past December 21, 1989')
plt.ylabel('Days Past May 13, 1990')
plt.title('Galileo--VGA to EGA1')

###############################################################################
#
#	Launch to VGA Porkchop
#
###############################################################################

EGA22JOI = load('data/EGA22JOI.npz')

plt.figure()
actualEGA2JD = timeConvert([1992,343],'ydnhms','jd')
actualJOIJD = timeConvert([1995,343],'ydnhms','jd')

earliestEGA2JD = 2448965.5 - 100
earliestJOIJD = 2450154 - 150


launch2VGAd = EGA22JOI['arrivalJD'] - EGA22JOI['departureJD']
TOFLevels = [1000,1100,1200,1300]
TOF = plt.contour(launch2VGAd,levels=TOFLevels,linewidths=0.5,colors='black')
plt.clabel(TOF,TOFLevels,fmt='%1.1f',fontsize=8)

vInfOutLevels = [9,10,12.5,15,20]
vInfOut = plt.contour(sqrt(EGA22JOI['C3']),levels=vInfOutLevels,linewidths=0.5,colors='red')
plt.clabel(vInfOut,vInfOutLevels,fmt='%1.1f',fontsize=8)

vInfInLevels = [6,7,8,9,10,11,12,13,14]
vInfIn = plt.contour(EGA22JOI['vInf'],levels=vInfInLevels,linewidths=0.5,colors='blue')
plt.clabel(vInfIn,vInfInLevels,fmt='%1.1f',fontsize=8)

plt.plot(
	actualEGA2JD - earliestEGA2JD,  actualJOIJD - earliestJOIJD,
	'.',color='lawngreen',markersize=10)

#dummy plots to spoof the legend. There's probably a better way...
plt.plot([0,0],[0,0],color='red',linewidth=0.5,label=r'$v_{\infty^{out},EGA2}$ (km/s)')
plt.plot([0,0],[0,0],color='blue',linewidth=0.5,label=r'$v_{\infty^{in},JOI}$ (km/s)')
plt.plot([0,0],[0,0],color='black',linewidth=0.5,label='TOF (days)')
plt.plot([0,0],[0,0],'.',color='lawngreen',label='True EGA2/JOI Dates',markersize=10)
plt.legend(loc='upper left')
plt.xlabel('Days Past August 31, 1992')
plt.ylabel('Days Past October 13, 1995')
plt.title('Galileo--EGA2 to JOI')




pdb.set_trace()



