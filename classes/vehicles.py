#! /usr/bin/env python3
###############################################################################
#
#	Title   : vehicles.py
#	Author  : Matt Muszynski
#	Date    : 12/23/17
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################
from numpy import array, hstack, empty, zeros
from scipy.linalg import norm, inv
from scipy.integrate import ode
import sys
sys.path.insert(0, 'util')
from util import tilde
import sensors
import rigidBodyKinematics as rbk

class spacecraft:
	def __init__(self):
		self.simScenario = -1
		self.initialState = empty((0,12),float)
		self.stateHistory = empty((0,12),float)
		self.currentState = empty((0,12),float)
		self.cssList = []
		self.name = -1
		self.I = -1

	def initOrbitDynamics(self):
		for bod in self.simScenario.gravBodList:
			print(bod.name)

	def gCB(self, t, r):
		a = -self.simScenario.centralBody.mu*r/norm(r)**3
		return a

	def rigidBodyEOM(self, omega, I, L):
		IomegaDot = -tilde(omega).dot(I.dot(omega)) + L
		omegaDot = inv(I).dot(IomegaDot)
		return omegaDot

	def gThirdBody(self, t, state, thirdBody):
		rSC = state[0:3]
		v = state[3:6]
		rBod = (thirdBody.currentState - \
			self.simScenario.centralBody.currentState)[0:3]
		rSC2Bod = rBod - self.currentState[0:3]
		a = -thirdBody.mu*(
			rSC2Bod/norm(rSC2Bod)**3 - rBod/norm(rBod)**3
			)
		return a

	def sesorUpdate(self):
		for css in self.cssList:
			css.updateState()


	def propagate(self):
		def accel(t, state):
			r = state[0:3]
			v = state[3:6]
			# if norm(self.currentState[6:9]) > 1: 
			# 	self.currentState[6:9]/=-sum(self.currentState[6:9]**2)
			sigma = state[6:9]
			# if norm(sigma) < 1: sigma *=-1
			omega = state[9:12]
			rDot = v
			vDot = self.gCB(t,r)
			sigmaDot = rbk.omega2sigmaDot(omega,sigma)
			L = 0
			omegaDot = self.rigidBodyEOM(omega, self.I, L)
			# for body in self.simScenario.gravBodList:
			# 	a += self.gThirdBody(t, state, body)

			return hstack([rDot,vDot,sigmaDot,omegaDot])
		if norm(self.currentState[6:9]) > 1: 
			self.currentState[6:9]/=-sum(self.currentState[6:9]**2)
		solver = ode(accel).set_integrator('dopri5')
		solver.set_initial_value(self.currentState, 0)

		self.currentState = solver.integrate(
			self.simScenario.timeStep*24*3600).reshape(-1,1)
		self.stateHistory = hstack([self.stateHistory,self.currentState])

		self.sesorUpdate()



	def addCSS(self,bod2sensorDCM,bod2sensorVector):
		newCSS = sensors.css()
		newCSS.name  = 'CSS' + str(len(self.cssList))
		newCSS.north = bod2sensorDCM.dot(newCSS.north)
		newCSS.south = bod2sensorDCM.dot(newCSS.south)
		newCSS.east  = bod2sensorDCM.dot(newCSS.east)
		newCSS.west  = bod2sensorDCM.dot(newCSS.west)
		newCSS.vehicle = self
		self.cssList.append(newCSS)