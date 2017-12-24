#! /usr/bin/env python3
###############################################################################
#
#	Title   : simScenario.py
#	Author  : Matt Muszynski
#	Date    : 12/23/17
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################
from numpy import empty, vstack

class simScenario:
	def __init__(self):
		self.jdEpoch = 2451545.0
		self.jdStartTime = 2451545.0
		self.jdEndTime = 2451545.0 + 36500
		self.currentTime = -1
		self.timeStep = 10
		self.timeHistory = empty((0,1),float)
		self.gravBodList = []
		self.nonGravBodList = []
		self.spacecraftList = []

	def addGravBod(self,bodList):
		for body in bodList:
			body.simScenario = self
			self.gravBodList.append(body)

	def addNonGravBod(self,bodList):
		for body in bodList:
			body.simScenario = self
			self.nonGravBodList.append(body)

	def addSpacecraft(self,scList):
		for sc in scList:
			sc.simScenario = self
			self.spacecraftList.append(sc)

	def propagate(self):
		#record initial states as state at t0
		self.currentTime = self.jdEpoch
		for sc in self.spacecraftList:
			sc.currentState = sc.initialState
			sc.stateHistory = vstack([sc.stateHistory,sc.initialState])
		for body in self.nonGravBodList:
			body.meeusStateUpdate()
			body.stateHistory = vstack([body.stateHistory,body.currentState])
		for body in self.gravBodList:
			body.meeusStateUpdate()
			body.stateHistory = vstack([body.stateHistory,body.currentState])



		self.timeHistory = vstack([self.timeHistory,self.currentTime])

		while self.currentTime <= self.jdEndTime:

			self.timeHistory = vstack([self.timeHistory,self.currentTime])

			for sc in self.spacecraftList:
				sc.propagate()
			self.currentTime += self.timeStep

			for body in self.nonGravBodList:
				body.meeusStateUpdate()
				body.stateHistory = vstack([body.stateHistory,body.currentState])
		
			for body in self.gravBodList:
				body.meeusStateUpdate()
				body.stateHistory = vstack([body.stateHistory,body.currentState])


