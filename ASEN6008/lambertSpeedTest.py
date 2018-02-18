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
from numpy import hstack, argmin
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

sun = celestialBodies.celestialBody()
sun.initSun()
earth = celestialBodies.celestialBody()
earth.initEarth()
mars = celestialBodies.celestialBody()
mars.initMars()

scen = simScenario.simScenario()
scen.addCentralBody(earth)
scen.addNonGravBody([earth,mars])
scen.jdEpoch = timeConvert('2005/217T00:00:00.0','utc','jd')
scen.jdEndTime = scen.jdEpoch+400

scen.propagate()

start = datetime.now()

ind = (scen.timeHistory-scen.jdEpoch) > 150
earthAtDeparture = earth.stateHistory[0]
marsAtArrival = mars.stateHistory[ind]
TOFd = (scen.timeHistory-scen.jdEpoch)[ind]
TOFs = TOFd*24*3600
C3 = []
vInfArrival = []
for i in range(0,len(marsAtArrival)):
	lam = o.slowLambert(earthAtDeparture,marsAtArrival[i],TOFs[i],mu=sun.mu)
	C3 = hstack([C3, lam['C3']])
	vInfArrival = hstack([vInfArrival,lam['magVInfArrive']])

end = datetime.now()
print(end - start)

plt.figure()
plt.plot(earth.stateHistory[:,0],earth.stateHistory[:,1])
plt.plot(mars.stateHistory[:,0],mars.stateHistory[:,1])
plt.axis('equal')

plt.figure()
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


start = datetime.now()

ind = (scen.timeHistory-scen.jdEpoch) > 150
earthAtDeparture = earth.stateHistory[0]
marsAtArrival = mars.stateHistory[ind]
TOFd = (scen.timeHistory-scen.jdEpoch)[ind]
TOFs = TOFd*24*3600
C3 = []
vInfArrival = []
for i in range(0,len(marsAtArrival)):
	lam = o.lambert(earthAtDeparture,marsAtArrival[i],TOFs[i],mu=sun.mu)
	C3 = hstack([C3, lam['C3']])
	vInfArrival = hstack([vInfArrival,lam['magVInfArrive']])
end = datetime.now()
print(end - start)

plt.show()






