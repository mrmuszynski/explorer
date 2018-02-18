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
from numpy import array, argmax, argmin, sqrt, pi, arctan2, hstack
from numpy import zeros, empty, arccos,rad2deg, logical_and
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


sun = celestialBodies.celestialBody()
sun.initSun()
earth = celestialBodies.celestialBody()
earth.initEarth()
mars = celestialBodies.celestialBody()
mars.initMars()

scen = simScenario.simScenario()
scen.addCentralBody(sun)
scen.addNonGravBody([earth,mars])
scen.jdEpoch = timeConvert('2005/217T00:00:00.0','utc','jd')
scen.jdEndTime = scen.jdEpoch+250

scen.propagate()

plt.figure()
plt.plot(earth.stateHistory[:,0],earth.stateHistory[:,1])
plt.plot(mars.stateHistory[:,0],mars.stateHistory[:,1])
plt.axis('equal')

plt.figure()

ind = (scen.timeHistory-scen.jdEpoch) > 150
earthAtDeparture = earth.stateHistory[0]
marsAtArrival = mars.stateHistory[ind]
TOFd = (scen.timeHistory-scen.jdEpoch)[ind]
TOFs = TOFd*24*3600
C3 = []
vInfArrival = []
psi = []
for i in range(0,len(marsAtArrival)):
	lam = o.lambert(earthAtDeparture,marsAtArrival[i],TOFs[i],mu=sun.mu)
	C3 = hstack([C3, lam['C3']])
	vInfArrival = hstack([vInfArrival,lam['magVInfArrive']])
	psi = hstack([psi,lam['psi']])

plt.plot(TOFd,C3)
plt.plot(TOFd[argmin(C3)],min(C3),'r.',
	label='Minimum C3=' + str(round(min(C3),3)) + 'km^2/s^2')
plt.xlabel('Days since August 5, 2005')
plt.ylabel('C3 (km^2/s^2)')
plt.legend()

plt.figure()
plt.plot(TOFd,vInfArrival)
plt.plot(TOFd[argmin(vInfArrival)],min(vInfArrival),'r.',
	label='Minimum V_inf=' + str(round(min(vInfArrival),3)) + 'km/s')
plt.xlabel('Days since August 5, 2005')
plt.ylabel('V_inf (km/s)')
plt.legend()


###########################################################################
#
# Problem 1a
#
###########################################################################

sun = celestialBodies.celestialBody()
sun.initSun()
earth = celestialBodies.celestialBody()
earth.initEarth()
mars = celestialBodies.celestialBody()
mars.initMars()

scen = simScenario.simScenario()
scen.addCentralBody(sun)
scen.addNonGravBody([earth,mars])
scen.jdEpoch = timeConvert('2018/121T00:00:00.0','utc','jd')
scen.jdEndTime = scen.jdEpoch+350
pdb.set_trace()
scen.propagate()

plt.figure()
plt.plot(earth.stateHistory[:,0],earth.stateHistory[:,1])
plt.plot(mars.stateHistory[:,0],mars.stateHistory[:,1])
plt.axis('equal')

plt.figure()

ind = (scen.timeHistory-scen.jdEpoch) > 50
earthAtDeparture = earth.stateHistory[0]
marsAtArrival = mars.stateHistory[ind]
TOFd = (scen.timeHistory-scen.jdEpoch)[ind]
TOFs = TOFd*24*3600
C3 = []
vInfArrival = []
psi = []
for i in range(0,len(marsAtArrival)):
	lam = o.lambert(earthAtDeparture,marsAtArrival[i],TOFs[i],mu=sun.mu)
	C3 = hstack([C3, lam['C3']])
	vInfArrival = hstack([vInfArrival,lam['magVInfArrive']])
	psi = hstack([psi,lam['psi']])

plt.figure()
plt.plot(TOFd,C3)
plt.xlabel('Days since May 1, 2018')
plt.ylabel('C3 (km^2/s^2)')
plt.title('C3 versis Launch Date')

plt.figure()
plt.plot(TOFd,vInfArrival)
plt.title('V_inf versis Launch Date')
plt.xlabel('Days since May 1, 2018')
plt.ylabel('V_inf (km/s)')

plt.figure()
ind = logical_and(TOFd > 70, TOFd < 242)
plt.plot(TOFd[ind],C3[ind])
plt.plot(TOFd[ind][argmin(C3[ind])],min(C3[ind]),'r.',
	label='Minimum C3=' + str(round(min(C3[ind]),3)) + 'km^2/s^2')
plt.title('C3 versis Launch Date (Type I Transfers Only)')
plt.xlabel('Days since May 1, 2018')
plt.ylabel('C3 (km^2/s^2)')
plt.legend()

plt.figure()
plt.plot(TOFd[ind],vInfArrival[ind])
plt.plot(TOFd[ind][argmin(vInfArrival[ind])],min(vInfArrival[ind]),'r.',
	label='Minimum V_inf=' + str(round(min(vInfArrival[ind]),3)) + 'km/s')
plt.title('V_inf versis Launch Date (Type I Transfers Only)')
plt.xlabel('Days since May 1, 2018')
plt.ylabel('V_inf (km/s)')
plt.legend()

print('Minimum Type I C3: ' + str(min(C3[ind])))
print('Minimum Type I C3 Arrival Date: ' + str(TOFd[ind][argmin(C3[ind])]))

print('Minimum Type I V_inf: ' + str(min(vInfArrival[ind])))
print('Minimum Type I V_inf Arrival Date: ' + str(TOFd[ind][argmin(vInfArrival[ind])]))

plt.figure()
ind = TOFd > 245
plt.plot(TOFd[ind],C3[ind])
plt.plot(TOFd[ind][argmin(C3[ind])],min(C3[ind]),'r.',
	label='Minimum C3=' + str(round(min(C3[ind]),3)) + 'km^2/s^2')
plt.title('C3 versis Launch Date (Type II Transfers Only)')
plt.xlabel('Days since May 1, 2018')
plt.ylabel('C3 (km^2/s^2)')
plt.legend()

plt.figure()
plt.plot(TOFd[ind],vInfArrival[ind])
plt.plot(TOFd[ind][argmin(vInfArrival[ind])],min(vInfArrival[ind]),'r.',
	label='Minimum V_inf=' + str(round(min(vInfArrival[ind]),3)) + 'km/s')
plt.title('V_inf versis Launch Date (Type II Transfers Only)')
plt.xlabel('Days since May 1, 2018')
plt.ylabel('V_inf (km/s)')
plt.legend()

print('Minimum Type II C3: ' + str(min(C3[ind])))
print('Minimum Type II C3 Arrival Date: ' + str(TOFd[ind][argmin(C3[ind])]))

print('Minimum Type II V_inf: ' + str(min(vInfArrival[ind])))
print('Minimum Type II V_inf Arrival Date: ' + str(TOFd[ind][argmin(vInfArrival[ind])]))

###########################################################################
#
# Problem 2
#
###########################################################################

au = 149597870.7
muSun = 1.32712440018e11
dawnPeriapse = 2.17*au #km
dawnApoapse = 2.57*au #km
aTrans = (dawnPeriapse + dawnApoapse)/2.
eTrans = (dawnApoapse - dawnPeriapse)/(dawnApoapse + dawnPeriapse)
ceresPeriod = 1682. #days
ceresPeriod = day2sec(ceresPeriod)
eCeres = 0.0758
aCeres = ((ceresPeriod/(2.*pi))**2*muSun)**(1./3.)
periapseCeres = (1.-eCeres)*aCeres

nu = arccos((aTrans*(1.-eTrans**2)/periapseCeres - 1.)/eTrans)
transferTime = o.anomalies('nu',rad2deg(nu),aTrans,eTrans,mu=muSun)['t']

print('aTrans: ' + str(aTrans))
print('eTrans: ' + str(eTrans))
print('eCeres: ' + str(eCeres))
print('aCeres: ' + str(aCeres))
print('periapseCeres: ' + str(periapseCeres))
print('nu: ' + str(nu))
print('transferTime: ' + str(transferTime))

pdb.set_trace()







