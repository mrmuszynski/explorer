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
from numpy import load, argmin
from timeFcn import timeConvert
import matplotlib.pyplot as plt
import pdb



###############################################################################
#
#	Recreate plot from page 2 of lab.
#
###############################################################################

data2005 = load('GMATLab4Data/opportunity2005.npz')
data2016 = load('GMATLab4Data/opportunity2016.npz')
data2018 = load('GMATLab4Data/opportunity2018.npz')

print('')
print('2005 Min C3')
arriveJD = data2005['arrivalJD'].reshape(-1)[argmin(data2005['C3'])]
departJD = data2005['departureJD'].reshape(-1)[argmin(data2005['C3'])]
print(argmin(data2005['C3'])%len(data2005['C3'][0]))
print(int(argmin(data2005['C3'])/len(data2005['C3'][0])))
print(departJD)
print(arriveJD)
print(timeConvert(departJD,'jd','utc'))
print(timeConvert(arriveJD,'jd','utc'))
print(data2005['vInf'].reshape(-1)[argmin(data2005['C3'])])
print(data2005['C3'].reshape(-1)[argmin(data2005['C3'])])
print('2005 Min vInf')
arriveJD = data2005['arrivalJD'].reshape(-1)[argmin(data2005['vInf'])]
departJD = data2005['departureJD'].reshape(-1)[argmin(data2005['vInf'])]
print(argmin(data2005['C3'])%len(data2005['vInf'][0]))
print(int(argmin(data2005['C3'])/len(data2005['vInf'][0])))
print(departJD)
print(arriveJD)
print(timeConvert(departJD,'jd','utc'))
print(timeConvert(arriveJD,'jd','utc'))
print(data2005['vInf'].reshape(-1)[argmin(data2005['vInf'])])
print(data2005['vInf'].reshape(-1)[argmin(data2005['vInf'])])

print('')
print('2018 Min C3')
arriveJD = data2018['arrivalJD'].reshape(-1)[argmin(data2018['C3'])]
departJD = data2018['departureJD'].reshape(-1)[argmin(data2018['C3'])]
print(argmin(data2018['C3'])%len(data2018['C3'][0]))
print(int(argmin(data2018['C3'])/len(data2018['C3'][0])))
print(departJD)
print(arriveJD)
print(timeConvert(departJD,'jd','utc'))
print(timeConvert(arriveJD,'jd','utc'))
print(data2018['vInf'].reshape(-1)[argmin(data2018['C3'])])
print(data2018['C3'].reshape(-1)[argmin(data2018['C3'])])
print('2018 Min vInf')
arriveJD = data2018['arrivalJD'].reshape(-1)[argmin(data2018['vInf'])]
departJD = data2018['departureJD'].reshape(-1)[argmin(data2018['vInf'])]
print(argmin(data2018['vInf'])%len(data2018['vInf'][0]))
print(int(argmin(data2018['vInf'])/len(data2018['vInf'][0])))
print(departJD)
print(arriveJD)
print(timeConvert(departJD,'jd','utc'))
print(timeConvert(arriveJD,'jd','utc'))
print(data2018['vInf'].reshape(-1)[argmin(data2018['vInf'])])
print(data2018['C3'].reshape(-1)[argmin(data2018['vInf'])])

print('')
print('2016 Min C3')
arriveJD = data2016['arrivalJD'].reshape(-1)[argmin(data2016['C3'])]
departJD = data2016['departureJD'].reshape(-1)[argmin(data2016['C3'])]
print(argmin(data2016['C3'])%len(data2016['C3'][0]))
print(int(argmin(data2016['C3'])/len(data2016['C3'][0])))
print(departJD)
print(arriveJD)
print(timeConvert(departJD,'jd','utc'))
print(timeConvert(arriveJD,'jd','utc'))
print(data2018['vInf'].reshape(-1)[argmin(data2018['C3'])])
print(data2018['C3'].reshape(-1)[argmin(data2018['C3'])])
print(data2016['vInf'].reshape(-1)[argmin(data2016['C3'])])
print(data2016['C3'].reshape(-1)[argmin(data2016['C3'])])
print('2016 Min vInf')
arriveJD = data2016['arrivalJD'].reshape(-1)[argmin(data2016['vInf'])]
departJD = data2016['departureJD'].reshape(-1)[argmin(data2016['vInf'])]
print(argmin(data2016['vInf'])%len(data2016['vInf'][0]))
print(int(argmin(data2016['vInf'])/len(data2016['vInf'][0])))
print(departJD)
print(arriveJD)
print(timeConvert(departJD,'jd','utc'))
print(timeConvert(arriveJD,'jd','utc'))
print(data2016['vInf'].reshape(-1)[argmin(data2016['vInf'])])
print(data2016['C3'].reshape(-1)[argmin(data2016['vInf'])])

pdb.set_trace()

plt.figure()
TOFLevels = [50,100,150,200,250,300,350,400,450,500]
C3Levels = [16,17,19,21,25,36,55,100]
vInfLevels = [2.5,3,4,4.5,5,7.5,10]

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
TOFLevels = [100,150,200,250,300,350,400]
C3Levels = [10,12,16,20,25,36,80]
vInfLevels = [4,4.5,5,7.5,10]
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
plt.xlabel('Days Past 01 Jan 2016')
plt.ylabel('Days Past 30 Jun 2016')
plt.title('2016 Launch Opportunity')




plt.show()




pdb.set_trace()


