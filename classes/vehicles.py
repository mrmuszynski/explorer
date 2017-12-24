#! /usr/bin/env python3
###############################################################################
#
#	Title   : vehicles.py
#	Author  : Matt Muszynski
#	Date    : 12/23/17
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################
from numpy import array, hstack, vstack, empty
from scipy.linalg import norm
from scipy.integrate import ode

class spacecraft:
	def __init__(self):
		self.simScenario = -1
		self.initialState = array([0,0,0,0,0,0])
		self.stateHistory = empty((0,6),float)
		self.currentState = empty((0,6),float)
		self.name = -1

	def propagate(self):
		#need to actually propagate something here :-P
		def g(t, state):
			r = state[0:3]
			v = state[3:6]
			mu = 1.32712440018e20
			return hstack([
				v,
				-mu*r/norm(r)**3
				])
		# import pdb
		# pdb.set_trace()
		solver = ode(g).set_integrator('dopri5')
		solver.set_initial_value(self.currentState, 0)
		self.currentState = solver.integrate(1*24*3600)
		print(self.currentState)
		self.stateHistory = vstack([self.stateHistory,self.currentState])