#! /usr/bin/env python3
###############################################################################
#
#	Title   : simScenario.py
#	Author  : Matt Muszynski
#	Date    : 12/23/17
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################
from numpy import empty, hstack, array

from sys import exit
import pdb
class simScenario:
	def __init__(self):
		self.jdEpoch = 2451545.0
		self.jdStartTime = 2451545.0
		self.jdEndTime = 2451545.0 + 365
		self.currentTime = -1
		self.timeStep = 1
		self.timeHistory = -1
		self.gravBodList = []
		self.centralBody = -1
		self.nonGravBodList = []
		self.spacecraftList = []
		self.luminousBodyList = []

	def addCentralBody(self,centralBody):
		self.centralBody = centralBody

	def addGravBody(self,bodList):
		for body in bodList:
			body.simScenario = self
			self.gravBodList.append(body)

	def addLuminousBody(self,bodList):
		for body in bodList:
			body.simScenario = self
			self.luminousBodyList.append(body)

	def addNonGravBody(self,bodList):
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
		self.timeHistory = array([self.jdEpoch])

		if self.centralBody == -1: 
			print('Error: simScenario has no central body.')
			print('Please use simScenario.addCentralBody() and rerun')
			exit()
			return

		for body in self.nonGravBodList:
			body.currentState = body.meeusStateUpdate(self.currentTime)
			body.stateHistory = body.currentState
		for body in self.gravBodList:
			body.currentState = body.meeusStateUpdate(self.currentTime)
			body.stateHistory = body.currentState
		self.centralBody.currentState = self.centralBody.meeusStateUpdate(
			self.currentTime)
		self.centralBody.stateHistory = self.centralBody.currentState

		for sc in self.spacecraftList:
			sc.currentState = sc.initialState.reshape(-1,1)
			sc.stateHistory = sc.initialState.reshape(-1,1)
			sc.sesorUpdate()

		while self.currentTime <= self.jdEndTime:
			self.currentTime += self.timeStep
			self.timeHistory = hstack([self.timeHistory,self.currentTime])

			for sc in self.spacecraftList:
				sc.propagate()

			for body in self.nonGravBodList:
				body.currentState = body.meeusStateUpdate(self.currentTime)
				body.stateHistory = hstack([body.stateHistory,body.currentState])
		
			for body in self.gravBodList:
				body.currentState = body.meeusStateUpdate(self.currentTime)
				body.stateHistory = hstack([body.stateHistory,body.currentState])
			self.centralBody.currentState = self.centralBody.meeusStateUpdate(self.currentTime)
			self.centralBody.stateHistory = hstack([self.centralBody.stateHistory,self.centralBody.currentState])


