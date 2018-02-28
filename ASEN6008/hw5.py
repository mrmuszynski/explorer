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
	ijk2str = vstack([s,t,rhat])
	return (b*bHat,ijk2str)

def dBdV(vNominal,vPerturbed,r):
	bNominal = computeB(r,vNominal)[0]
	ijk2strNominal = computeB(r,vPerturbed)[1]
	bPerturbed = computeB(r,vPerturbed)[0]
	if sum((vNominal - vPerturbed) == 0) < 2: 
		print('WARNING: Only one element of vInf can be varied!')
	dBdVijk = (bPerturbed - bNominal)/norm(vNominal - vPerturbed)
	return ijk2strNominal.dot(dBdVijk)

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
	dBTdVx = hstack([dBTdVx,partial[1]])
	dBRdVx = hstack([dBRdVx,partial[2]])
	v = vSOI + array([0,perturbation,0])
	partial = dBdV(vSOI,v,rSOI)
	dBTdVy = hstack([dBTdVy,partial[1]])
	dBRdVy = hstack([dBRdVy,partial[2]])

plt.figure()
plt.semilogx(perturbations,dBTdVx,label=r'$\frac{\partial B_T}{\partial V_x}$')
plt.semilogx(perturbations,dBTdVy,label=r'$\frac{\partial B_T}{\partial V_y}$')
plt.semilogx(perturbations,dBRdVx,label=r'$\frac{\partial B_R}{\partial V_x}$')
plt.semilogx(perturbations,dBRdVy,label=r'$\frac{\partial B_R}{\partial V_y}$')
plt.legend()

pdb.set_trace()













