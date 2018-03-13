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
from analysisTools import computeB, dBdV

from numpy import linspace, hstack, pi, array, arccos, cos, cross
from numpy import rad2deg, arctan2, vstack, sqrt, logspace
from numpy.linalg import norm, inv
import matplotlib.pyplot as plt
from timeFcn import timeConvert, sec2day, day2sec
from util import r3
import pdb
import orbits as o


###############################################################################
#
# 	Problem 1
#
###############################################################################

earth = celestialBodies.celestialBody()
earth.initEarth()

rSOI = array([546507.344255845, -527978.380486028, 531109.066836708])
vSOI = array([-4.9220589268733, 5.36316523097915, -5.22166308425181])

perturbations = logspace(-16,2,6*30+1)

dBTdVx = []
dBTdVy = []
dBRdVx = []
dBRdVy = []
for perturbation in perturbations:
	v = vSOI + array([perturbation,0,0])
	partial = dBdV(vSOI,v,rSOI,earth.mu)
	dBTdVx = hstack([dBTdVx,partial[1]])
	dBRdVx = hstack([dBRdVx,partial[2]])
	v = vSOI + array([0,perturbation,0])
	partial = dBdV(vSOI,v,rSOI,earth.mu)
	dBTdVy = hstack([dBTdVy,partial[1]])
	dBRdVy = hstack([dBRdVy,partial[2]])

plt.figure()
plt.semilogx(perturbations,dBTdVx,label=r'$\partial B_T/ \partial V_{\infty,x}$')
plt.semilogx(perturbations,dBTdVy,label=r'$\partial B_T/ \partial V_{\infty,y}$')
plt.semilogx(perturbations,dBRdVx,label=r'$\partial B_R/ \partial V_{\infty,x}$')
plt.semilogx(perturbations,dBRdVy,label=r'$\partial B_R/ \partial V_{\infty,y}$')
plt.title(r'Partials of $\vec{B}$ with respect to $\vec{v}_\infty$')
plt.ylabel(r'Partial Derivative ($\frac{km}{km/s}$)')
plt.xlabel(r'Deviation in $V_{\infty,i}$ ($\frac{km}{s}$)')
plt.legend(bbox_to_anchor=(0.1,0.2))

###############################################################################
#
# 	Problem 2
#
###############################################################################

r = rSOI
v = array(vSOI)
pert = 1e-10
bDesired = array([0,13135.7982982557,5022.26511510685])

normDeltaB = 1
while normDeltaB > 1e-6:
	b = computeB(r,v,earth.mu)
	bNomstr = b[1].dot(b[0])
	dBdVx = dBdV(v,v + array([pert,0,0]),r,earth.mu)
	dBdVy = dBdV(v,v + array([0,pert,0]),r,earth.mu)
	bMatrix = vstack([dBdVx[1:3],dBdVy[1:3]]).T
	bInv = inv(bMatrix)
	deltaB = (bDesired - bNomstr)[1:3]
	deltaV = hstack([bInv.dot(deltaB),0]) #in STR frame?
	v += deltaV
	normDeltaB = norm(deltaB)

deltaVFinal = v - vSOI
print('Final Delta V: ' + str(deltaVFinal))
print('Final V: ' + str(v))


pdb.set_trace()













