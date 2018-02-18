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
sys.path.insert(0, 'classes')
sys.path.insert(0, 'prop')
sys.path.insert(0, 'fsw')
sys.path.insert(0, 'util')

import vehicles, celestialBodies, simScenario
from constants import au
from numpy import array, sqrt, linspace, meshgrid, cos, sin, deg2rad, vstack
from numpy import identity, pi, hstack, empty
from numpy.random import uniform
from util import r1, r2, r3, sphereSample
from adcs import dcm2mrp, mrp2dcm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import rigidBodyKinematics as rbk
from timeFcn import timeConvert, sec2day, day2sec
import pdb

#initialize spacecraft
I = array([
	[1, 0, 0],
	[ 0, 1, 0],
	[ 0, 0, 1],
	])

explorer1 = vehicles.spacecraft()
explorer1.name = 'Explorer 1'
r0 = array([au/1000,0,0])
v0 = array([0,20,0])
PHI = deg2rad(0)
sigma0 = array([0,0,sin(PHI/2)/(1+cos(PHI/2))])
omega0 = array([0,0,0.01])
explorer1.initialState = hstack([r0,v0,sigma0,omega0])
explorer1.I = I
explorer1.addCSS(
	r1(0).dot(r2(0).dot(r3(0))),
	array([0,0,0]))
explorer1.addCSS(
	r1(0).dot(r2(0).dot(r3(deg2rad(90)))),
	array([0,0,0]))
explorer1.addCSS(
	r1(0).dot(r2(0).dot(r3(deg2rad(180)))),
	array([0,0,0]))
explorer1.addCSS(
	r1(0).dot(r2(0).dot(r3(deg2rad(270)))),
	array([0,0,0]))

#initialize stock bodies
sun = celestialBodies.celestialBody()
sun.initSun()

#initialize sim scenario
scen = simScenario.simScenario()
scen.addCentralBody(sun)
scen.addLuminousBody([sun])

scen.addSpacecraft([explorer1])
scen.jdEpoch = .0
scen.jdEndTime = scen.jdEpoch + sec2day(180.)
scen.timeStep = sec2day(1)
scen.propagate()

plt.figure()
plt.plot(explorer1.stateHistory[6:9,:].T)
secSinceEpoch = day2sec(scen.timeHistory - scen.jdEpoch)
for css in explorer1.cssList:
	# f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, sharex=True, sharey=True)
	# ax1.plot(secSinceEpoch, css.northHistory.T[0])
	# ax2.plot(secSinceEpoch, css.southHistory.T[0])
	# ax3.plot(secSinceEpoch, css.eastHistory.T[0])
	# ax4.plot(secSinceEpoch, css.westHistory.T[0])

	f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
	ax1.plot(secSinceEpoch, css.northHistory.T[0] - css.southHistory.T[0])
	ax1.set_title('North minus South')
	ax2.plot(secSinceEpoch, css.eastHistory.T[0] - css.westHistory.T[0])
	ax2.set_title('East minus West')
	ax3.plot(secSinceEpoch, css.northHistory.T[0], label='North')
	ax3.plot(secSinceEpoch, css.southHistory.T[0], label='South')
	ax3.plot(secSinceEpoch, css.eastHistory.T[0], label='East')
	ax3.plot(secSinceEpoch, css.westHistory.T[0], label='West')
	ax3.set_title('CSS Cell History')
	ax3.legend()
	# plt.legend()
	# css.demo()


ellipse = I.dot(sphereSample(10,10))*10

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set the z axis limits so they aren't recalculated each frame.
ax.set_zlim(-1, 1)
ax.set_xlim([-10,10])
ax.set_ylim([-10,10])
ax.set_zlim([-10,10])

# Begin plotting.
wframe = None
for i in range(0,len(explorer1.stateHistory[0])):
    # If a line collection is already remove it before drawing.
    if wframe:
        ax.collections.remove(wframe)
    XYZ = rbk.sigma2C(explorer1.stateHistory[6:9,i]).dot(ellipse)

    # Plot the new wireframe and pause briefly before continuing.
    wframe = ax.scatter(
    	XYZ[0], 
    	XYZ[1], 
    	XYZ[2], 
    	color='blue')
    	# rstride=2, cstride=2)
    plt.pause(.01)
pdb.set_trace()


sc2sun = sun.stateHistory[0:3] - explorer1.stateHistory[0:3]
e2sun = sc2sun/sqrt(sc2sun[0]**2 + sc2sun[1]**2 + sc2sun[2]**2)
scMRP = explorer1.stateHistory[6:9]

eBdy = empty((0,3),float)
angles321 = empty((0,3),float)

for i in range(len(scMRP.T)):
	C = rbk.sigma2C(scMRP[:,i])
	angles321 = vstack([angles321,rbk.C2e321(C)])
	eBdy = vstack([eBdy,C.dot(e2sun[:,i])])


pdb.set_trace()

plt.show()

pdb.set_trace()
