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
from numpy import array, argmax, argmin, sqrt, pi, arctan2
from numpy.linalg import norm
import matplotlib.pyplot as plt
from timeFcn import timeConvert
import pdb

###########################################################################
#
# Problem 1
#
###########################################################################

muSun = 1.327e11 #km^3/s^2
muEarth = 3.986e5 #km^3/s^2
muMars = 4.305e4 #km^3/s^2
au = 1.4959787e8 #km
aEarth = 1 #AU
aMars = 1.52368 #AU
rEarth = 6378.1363 #km
rMars = 3397.2 #km

e = 0.02454974900598137
aPark = 7191.938817629013
r0 = 7191.938817629013*(1-e)
v0 = 7.6405017927401
rf = 12000
aTrans = (r0+rf)/2
vf = sqrt(2*muEarth/r0-muEarth/aTrans)
deltaVImpulsive = vf-v0

print('Initial Orbital Radius: ' + str(r0))
print('Transfer Periapse: ' + str(r0))
print('Transfer Apoapse: ' + str(rf))
print('Parking Orbit SMA: ' + str(aTrans))
print('Transfer SMA: ' + str(aTrans))
print('Parking Orbit Periapse Velocity: ' + str(v0))
print('Transfer Periapse Velocity: ' + str(vf))
print('Transfer ΔV: ' + str(deltaVImpulsive))

P = 50*3600
#2*pi*sqrt(a50hrs**3/muMars)
a50hrs = ((P/(2*pi))**2*muMars)**(1/3)
Ptest = 2*pi*sqrt(a50hrs**3/muMars)

aAvg = (1000/1606.0000000000 + 1000/1193.7699071470)/2
deltaVFinite = aAvg*1213.19316319/1000

pdb.set_trace()



