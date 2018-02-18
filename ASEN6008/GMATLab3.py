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
from numpy import hstack, array
import pdb

import celestialBodies
import orbits as o
from timeFcn import timeConvert, day2sec

muSun = 1.32712440018e11
t0 = timeConvert('2005/222T00:00:00.0','utc','jd')
TOFd = 180
TOFs = day2sec(TOFd)
tf = t0 + TOFd
earth = celestialBodies.celestialBody()
mars = celestialBodies.celestialBody()
earth.initEarth()
mars.initMars()
X0 = earth.meeusStateUpdate(t0)
Xf = mars.meeusStateUpdate(tf)

lam = o.lambert(X0,Xf,TOFs,mu=muSun)

pdb.set_trace()

C3 = []
VInf = [] 
daysSinceLaunch = []
#150 day transfer
deltaV = array([2.8144837829307,3.4938724189366,0.5981784027110])
C3 = hstack([C3,5.2995065728872])
VInf = hstack([VInf,deltaV.dot(deltaV)])
daysSinceLaunch = hstack([daysSinceLaunch,150])

#160 day transfer
deltaV = array([2.7806491908455,3.1972029267680,0.7290833426328])
C3 = hstack([C3,4.6620704265660])
VInf = hstack([VInf,deltaV.dot(deltaV)])
daysSinceLaunch = hstack([daysSinceLaunch,160])

#170 day transfer
deltaV = array([2.7567590653747, 2.9632794233274, 0.8746729150248])
C3 = hstack([C3,4.1251718782489])
VInf = hstack([VInf,deltaV.dot(deltaV)])
daysSinceLaunch = hstack([daysSinceLaunch,170])

#180 day transfer
deltaV = array([2.7371394892965,2.7812999366726,1.0405296598461])
C3 = hstack([C3,3.6800220284301])
VInf = hstack([VInf,deltaV.dot(deltaV)])
daysSinceLaunch = hstack([daysSinceLaunch,180])

#190 day transfer
deltaV = array([2.7175372225417,2.6425802717375,1.2342966056670])
C3 = hstack([C3,3.3222145630765])
VInf = hstack([VInf,deltaV.dot(deltaV)])
daysSinceLaunch = hstack([daysSinceLaunch,190])

#200 day transfer
deltaV = array([2.6947310824872,2.5392081391245,1.4682832394522])
C3 = hstack([C3,3.0514993506126])
VInf = hstack([VInf,deltaV.dot(deltaV)])
daysSinceLaunch = hstack([daysSinceLaunch,200])

#210 day transfer
deltaV = array([2.6657149483647,2.4642340091015,1.7599892845068])
C3 = hstack([C3,2.8730011025046])
VInf = hstack([VInf,deltaV.dot(deltaV)])
daysSinceLaunch = hstack([daysSinceLaunch,210])

#220 day transfer
deltaV = array([2.6269553473924,2.4102844873030,2.1404583835670])
C3 = hstack([C3,2.8000838018205])
VInf = hstack([VInf,deltaV.dot(deltaV)])
daysSinceLaunch = hstack([daysSinceLaunch,220])

#230 day transfer
deltaV = array([2.5727357210025,2.3677652176721,2.6647226295572])
C3 = hstack([C3,2.8608857513649])
VInf = hstack([VInf,deltaV.dot(deltaV)])
daysSinceLaunch = hstack([daysSinceLaunch,230])

#240 day transfer
deltaV = array([2.4904147737504,2.3193444612858,3.4451409231108])
C3 = hstack([C3,3.1183778819754])
VInf = hstack([VInf,deltaV.dot(deltaV)])
daysSinceLaunch = hstack([daysSinceLaunch,240])

#250 day transfer
deltaV = array([2.3426961007685,2.2195545985898,4.7496136031742])
C3 = hstack([C3,3.7344145902533])
VInf = hstack([VInf,deltaV.dot(deltaV)])
daysSinceLaunch = hstack([daysSinceLaunch,250])

#flip C3 and VInf because I screwed up when I wrote the crappy codea above
import matplotlib.pyplot as plt
a = VInf
VInf = C3
C3 = a

plt.figure()
plt.plot(daysSinceLaunch,C3)
plt.title('C3 at Earth versus Arrival Date')
plt.xlabel('Days Since August 10, 2005')
plt.ylabel('C3 (km^2/s^2)')

plt.figure()
plt.plot(daysSinceLaunch,VInf)
plt.title('V_inf at Mars versus Arrival Date')
plt.xlabel('Days Since August 10, 2005')
plt.ylabel('V_inf (km/s)')

pdb.set_trace()


