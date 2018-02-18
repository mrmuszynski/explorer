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
from numpy import identity, pi, zeros, outer, empty, arctan2, arcsin, pi
from numpy import hstack
from numpy.linalg import norm
from numpy.random import uniform
import rigidBodyKinematics as rbk
from util import r1, r2, r3, tilde, sphereSample
from adcs import dcm2mrp, mrp2dcm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from timeFcn import timeConvert, sec2day, day2sec
import pdb
from scipy.integrate import ode

I = array([
	[10, 0, 0],
	[ 0, 5, 0],
	[ 0, 0, 2],
	])

#initialize spacecraft
explorer1 = vehicles.spacecraft()
explorer1.name = 'Explorer 1'
explorer2 = vehicles.spacecraft()
explorer2.name = 'Explorer 2'
explorer3 = vehicles.spacecraft()
explorer3.name = 'Explorer 3'

r0 = array([au/1000,0,0])
v0 = array([0,20,0])
sigma0 = array([0,0,0])
omega0 = array([0.1,0.0001,0])
explorer1.initialState = hstack([r0,v0,sigma0,omega0])
omega0 = array([0,0.1,0.0001])
explorer2.initialState = hstack([r0,v0,sigma0,omega0])
omega0 = array([0.,0,0.1])
explorer3.initialState = hstack([r0,v0,sigma0,omega0])
explorer1.I = I
explorer2.I = explorer1.I
explorer3.I = explorer1.I

#initialize stock bodies
sun = celestialBodies.celestialBody()
sun.initSun()

#initialize sim scenario
scen = simScenario.simScenario()
scen.addCentralBody(sun)

scen.addSpacecraft([explorer1,explorer2,explorer3])
scen.jdEpoch = 2451545.0
scen.jdEndTime = scen.jdEpoch + sec2day(600.)
scen.timeStep = sec2day(1)
scen.propagate()

secondsSinceEpoch = day2sec(scen.timeHistory-scen.jdEpoch)

for sc in scen.spacecraftList:
	plt.figure()
	plt.plot(sc.stateHistory[6:9,:].T)
	plt.title(sc.name + ' MRP History')
	plt.figure()
	plt.plot(sc.stateHistory[9:12,:].T)
	plt.title(sc.name + ' Omega History')


pdb.set_trace()
ellipse = I.dot(sphereSample(10,10))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set the z axis limits so they aren't recalculated each frame.
ax.set_zlim(-1, 1)
ax.set_xlim([-10,10])
ax.set_ylim([-10,10])
ax.set_zlim([-10,10])

# Begin plotting.
wframe = None
for i in range(0,len(explorer3.stateHistory[0])):
    # If a line collection is already remove it before drawing.
    if wframe:
        ax.collections.remove(wframe)
    XYZ = rbk.sigma2C(explorer3.stateHistory[6:9,i]).dot(ellipse)

    # Plot the new wireframe and pause briefly before continuing.
    wframe = ax.scatter(
    	XYZ[0], 
    	XYZ[1], 
    	XYZ[2], 
    	color='blue')
    	# rstride=2, cstride=2)
    plt.pause(.01)
pdb.set_trace()



fig = plt.figure()
ax = p3.Axes3D(fig)
line_ani = animation.FuncAnimation(
	fig, update_lines, 25, fargs=(data, lines),
                                   interval=50, blit=False)



pdb.set_trace()


I = identity(3)
L = 0
sigma = array([0,0,0])
omega = array([1,0.5,-1])/sqrt(2.25)*pi/125


sigmaHist = empty((0,3),float)
omegaHist = empty((0,3),float)
euler321Hist = empty((0,3),float)
euler321HistFromMrp = empty((0,3),float)

omegaTilde = tilde(omega)
t = 0
dt = 0.005

# def mrpState():
# 	return mrpStateDot

# solver = ode(accel).set_integrator('dopri5')
# solver.set_initial_value(self.currentState, 0)
# self.currentState = solver.integrate(self.simScenario.timeStep*24*3600)
# self.stateHistory = vstack([self.stateHistory,self.currentState])
dcm = rbk.sigma2C(sigma)
e321angles = rbk.C2e321(dcm)
euler321HistFromMrp = vstack([euler321HistFromMrp,e321angles])
sigmaHist = vstack([sigmaHist,sigma])

for i in range(0,1001):

	sigmaDot = rbk.omega2sigmaDot(omega, sigma)
	e321Dot = rbk.omega2e321dot(omega, e321angles)
	e321angles = e321angles + e321Dot*dt
	euler321Hist = vstack([euler321Hist,e321angles])

	omegaDot = -omegaTilde.dot(I.dot(omega)) + L
	sigma = sigma + sigmaDot*dt
	if norm(sigma) > 1: sigma = -sigma
	omega = omega + omegaDot*dt

	sigmaHist = vstack([sigmaHist,sigma])
	omegaHist = vstack([omegaHist,omega])

	dcm = rbk.sigma2C(sigma)
	e321anglesFromMrp = rbk.C2e321(dcm)
	euler321HistFromMrp = vstack([euler321HistFromMrp,e321anglesFromMrp])
	t+=dt

euler321Hist[euler321Hist >180] -=360

plt.figure()
plt.plot(sigmaHist)
plt.title('MRP History')
plt.figure()
plt.plot(euler321Hist)
plt.title('Euler Angle (3-2-1) History (computed directly)')
plt.figure()
plt.plot(euler321HistFromMrp)
plt.title('Euler Angle (3-2-1) History (converted from MRP)')
plt.figure()
plt.plot(omegaHist)
plt.title('Omega History')


pdb.set_trace()
