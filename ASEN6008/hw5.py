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
from numpy import linspace, hstack, pi, array, arccos, cos, cross
from numpy import rad2deg, arctan2, vstack, sqrt, logspace
from numpy.linalg import norm
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

def computeB(r,v):
	rP = o.rv2coe(r,v)['r_p']
	s = v/norm(v)
	k = array([0,0,1])
	t = cross(s,k)/norm(cross(s,k))
	h = cross(r,v)/norm(cross(r,v))
	rhat = cross(s,t)
	bHat = cross(s,h)
	b = earth.mu/v.dot(v)*sqrt((1+v.dot(v)*(rP/earth.mu))**2-1)
	return b*bHat

def dBdV(vNominal,vPerturbed,r):
	bNominal = computeB(r,vNominal)
	bPerturbed = computeB(r,vPerturbed)
	if sum((vNominal - vPerturbed) == 0) != 2: 
		print('WARNING: Only one element of vInf can be varied!')
	return (bPerturbed - bNominal)/norm(vNominal - vPerturbed)

rSOI = array([546507.344255845, -527978.380486028, 531109.066836708])
vSOI = array([-4.9220589268733, 5.36316523097915, -5.22166308425181])

perturbations = logspace(-16,2,6*30+1)

dBTdVx = []
dBTdVy = []
dBRdVx = []
dBRdVy = []
for perturbation in perturbations:
	v = vSOI + array([perturbation,0,0])
	partial = dBdV(vSOI,v,rSOI)
	dBTdVx = hstack([dBTdVx,partial[0]])
	dBRdVx = hstack([dBRdVx,partial[1]])
	v = vSOI + array([0,perturbation,0])
	partial = dBdV(vSOI,v,rSOI)
	dBTdVy = hstack([dBTdVy,partial[0]])
	dBRdVy = hstack([dBRdVy,partial[1]])

f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')

ax1.semilogx(perturbations,dBTdVx)
ax1.set_title('dBTdVx')
ax1.set_xlabel('Peturbation')
ax1.set_ylabel('dBTdVx')

ax2.semilogx(perturbations,dBTdVy)
ax2.set_title('dBTdVy')
ax2.set_xlabel('Peturbation')
ax2.set_ylabel('dBTdVy')

ax3.semilogx(perturbations,dBRdVx)
ax3.set_title('dBRdVx')
ax3.set_xlabel('Peturbation')
ax3.set_ylabel('dBRdVx')

ax4.semilogx(perturbations,dBRdVy)
ax4.set_title('dBRdVy')
ax4.set_xlabel('Peturbation')
ax4.set_ylabel('dBRdVy')

pdb.set_trace()













