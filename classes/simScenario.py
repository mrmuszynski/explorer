#! /usr/bin/env python3
###############################################################################
#
#	Title   : simScenario.py
#	Author  : Matt Muszynski
#	Date    : 12/23/17
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################
from numpy import empty, hstack, vstack, array

from sys import exit
import pdb
class simScenario:
	def __init__(self):
		self.jdEpoch = 2451545.0
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

	def clearNonGravBodyList(self):
		self.gravBodList = []

	def clearGravBodyList(self):
		self.nonGravBodList = []

	def clearSpacecraftList(self):
		self.spacecraftList = []

	def clearLuminiousBodyList(self):
		self.luminousBodyList = []

	def clearCentralBody(self):
		self.nonGravBodList = -1

	def clearAll(self):
		self.clearNonGravBodyList()
		self.clearGravBodyList()
		self.clearSpacecraftList()
		self.clearLuminiousBodyList()
		self.clearCentralBody()

	def propagate(self):
		#record initial states as state at t0
		self.currentTime = 0
		self.timeHistory = empty(0,float)
		self.jdEndTime -= self.jdEpoch

		if self.centralBody == -1: 
			print('Error: simScenario has no central body.')
			print('Please use simScenario.addCentralBody() and rerun')
			exit()
			return

		# for body in self.nonGravBodList:
		# 	body.currentState = body.meeusStateUpdate(
		# 		self.currentTime + self.jdEpoch)
		# 	body.stateHistory = body.currentState
		# for body in self.gravBodList:
		# 	body.currentState = body.meeusStateUpdate(
		# 		self.currentTime + self.jdEpoch)
		# 	body.stateHistory = body.currentState

		# self.centralBody.currentState = self.centralBody.meeusStateUpdate(
		# 	self.currentTime + self.jdEpoch)
		# self.centralBody.stateHistory = self.centralBody.currentState

		for sc in self.spacecraftList:
			sc.currentState = sc.initialState
			sc.stateHistory = sc.initialState
			sc.sesorUpdate()

		while self.currentTime <= self.jdEndTime:
			for sc in self.spacecraftList:
				sc.propagate()

			for body in self.nonGravBodList:
				body.currentState = body.meeusStateUpdate(self.currentTime + \
					self.jdEpoch)
				body.stateHistory = vstack([body.stateHistory,body.currentState])
		
			for body in self.gravBodList:
				body.currentState = body.meeusStateUpdate(self.currentTime + \
					self.jdEpoch)
				body.stateHistory = vstack([body.stateHistory,body.currentState])
			self.centralBody.currentState = self.centralBody.meeusStateUpdate(self.currentTime + \
					self.jdEpoch)
			self.centralBody.stateHistory = vstack([self.centralBody.stateHistory,self.centralBody.currentState])
			self.timeHistory = hstack([self.timeHistory,self.currentTime])
			self.currentTime += self.timeStep

		self.currentTime += self.jdEpoch
		self.timeHistory += self.jdEpoch
		self.jdEndTime += self.jdEpoch
