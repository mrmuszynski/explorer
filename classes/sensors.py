#! /usr/bin/env python3
###############################################################################
#
#	Title   : vehicles.py
#	Author  : Matt Muszynski
#	Date    : 12/23/17
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################
from numpy import array, sqrt, linspace, meshgrid, cos, sin, deg2rad, vstack
from numpy import empty
from numpy.linalg import norm
import rigidBodyKinematics as rbk
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class css:
	def __init__(self):
		self.vehicle = -1
		self.north = array([1,0,1])/sqrt(2)
		self.south = array([1,0,-1])/sqrt(2)
		self.east =  array([1,1,0])/sqrt(2)
		self.west =  array([1,-1,0])/sqrt(2)
		self.northHistory = empty((0,1),float)
		self.southHistory = empty((0,1),float)
		self.eastHistory = empty((0,1),float)
		self.westHistory = empty((0,1),float)
		self.northState = 0
		self.southState = 0
		self.eastState = 0
		self.westState = 0

	def updateState(self):
		scState = self.vehicle.currentState.T[0,0:3]
		self.northState = 0
		self.southState = 0
		self.eastState = 0
		self.westState = 0
		for bod in self.vehicle.simScenario.luminousBodyList:

			#in inertial frame
			sc2Bod = bod.currentState[0:3].T[0] - scState
			eBod = sc2Bod/norm(sc2Bod)

			#rotate to body frame
			sigmaSC = self.vehicle.currentState.T[0,6:9]
			dcmSC = rbk.sigma2C(sigmaSC)
			eBod = dcmSC.dot(eBod)

			northUpdate = self.north.dot(eBod)
			southUpdate = self.south.dot(eBod)
			eastUpdate = self.east.dot(eBod)
			westUpdate = self.west.dot(eBod)

			if northUpdate > 0: self.northState += northUpdate
			if southUpdate > 0: self.southState += southUpdate
			if eastUpdate > 0: self.eastState += eastUpdate
			if westUpdate > 0: self.westState += westUpdate

		self.northHistory = \
			vstack([self.northHistory,self.northState])
		self.southHistory = \
			vstack([self.southHistory,self.southState])
		self.eastHistory = \
			vstack([self.eastHistory,self.eastState])
		self.westHistory = \
			vstack([self.westHistory,self.westState])


	def demo(self):
		phi = deg2rad(linspace(0,180,37))
		theta = deg2rad(linspace(-180,180,73))
		phi, theta = meshgrid(phi,theta)

		x = sin(phi)*cos(theta)
		y = sin(phi)*sin(theta)
		z = cos(phi)

		phi = phi.reshape(1,-1)[0]
		theta = theta.reshape(1,-1)[0]
		x = x.reshape(1,-1)[0]
		y = y.reshape(1,-1)[0]
		z = z.reshape(1,-1)[0]

		eSun = vstack([x,y,z])

		northPercent = self.north.dot(eSun)
		southPercent = self.south.dot(eSun)
		eastPercent = self.east.dot(eSun)
		westPercent = self.west.dot(eSun)
		northPercent[northPercent < 0] = 0
		southPercent[southPercent < 0] = 0
		eastPercent[eastPercent < 0] = 0
		westPercent[westPercent < 0] = 0

		fig = plt.figure()
		gridspec.GridSpec(4,2)

		plt.subplot2grid((4,2),(0,0))
		plt.imshow(northPercent.reshape(73,37).T)
		plt.title('North CSS Response')
		plt.subplot2grid((4,2),(0,1))
		plt.imshow(southPercent.reshape(73,37).T)
		plt.title('South CSS Response')
		plt.subplot2grid((4,2),(1,0))
		plt.imshow(eastPercent.reshape(73,37).T)
		plt.title('East CSS Response')
		plt.subplot2grid((4,2),(1,1))
		plt.imshow(westPercent.reshape(73,37).T)
		plt.title('West CSS Response')
		plt.subplot2grid((4,2),(2,0),colspan=4,rowspan=2)
		plt.imshow((
			northPercent + \
			southPercent + \
			eastPercent + \
			westPercent
			).reshape(73,37).T)
		plt.title('Combined CSS Response')
		fig.tight_layout()
		# fig.set_size_inches(w=11,h=7)

