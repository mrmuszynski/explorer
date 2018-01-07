#! /usr/bin/env python3
###############################################################################
#
#	Title   : celestialBodies.py
#	Author  : Matt Muszynski
#	Date    : 12/23/17
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################
from numpy import sin, array, empty
import sys
sys.path.insert(0, 'util')
from orbits import coe2rv
from constants import au

class celestialBody:
	def __init__(self):
		self.name = 'None'
		self.mu = -1
		self.state = -1
		self.simScenario = -1
		self.stateHistory = empty((6,0),float)
		self.currentState = empty((6,0),float)

	def initSun(self):
		self.name = 'Sun'
		self.mu = 1.32712440018e11
		self.meeusCoeffs = {
		 'L': array([0, 0, 0, 0, 0, 0]),
		 'a': array([0, 0, 0, 0, 0, 0]),
		 'e': array([0, 0, 0, 0, 0, 0]),
		 'i': array([0, 0, 0, 0, 0, 0]),
		 'OMEGA': array([0, 0, 0, 0, 0, 0]),
		 'PI': array([0, 0, 0, 0, 0, 0])
		}

	def initVenus(self):
		self.name = 'Venus'
		self.mu = 3.24859e5
		self.meeusCoeffs = {
		 'L': array([181.979801, 58517.8156760, 0.00000165, -0.000000002]),
		 'a': array([0.72332982, 0, 0, 0]),
		 'e': array([0.00677188, -0.000047766, 0.0000000975, 0.00000000044]),
		 'i': array([3.394662, -0.0008568, -0.00003244, 0.000000010]),
		 'OMEGA': array([76.679920, -0.2780080, -0.00014256, -0.000000198]),
		 'PI': array([131.563707, 0.0048646, -0.00138232, -0.000005332])
		}

	def initEarth(self):
		self.name = 'Earth'
		self.mu = 3.986004418e5
		self.meeusCoeffs = {
		 'L': array([100.466449, 35999.3728519, -0.00000568, 0.0]),
		 'a': array([1.000001018, 0, 0, 0]),
		 'e': array([0.01670862, -0.000042037, -0.0000001236, 0.00000000004]),
		 'i': array([0.0, 0.0130546, -0.00000931, -0.000000034]),
		 'OMEGA': array([174.873174, -0.2410908, 0.00004067, -0.000001327]),
		 'PI': array([102.937348, 0.3225557, 0.00015026, 0.000000478])
		}

	def initMars(self):
		self.name = 'Mars'
		self.mu = 4.282837e4
		self.meeusCoeffs = {
		 'L': array([355.433275, 19140.2993313, 0.00000261, -0.000000003]),
		 'a': array([1.523679342, 0, 0, 0]),
		 'e': array([0.09340062, 0.000090483, -0.0000000806, -0.00000000035]),
		 'i': array([1.849726, -0.0081479, -0.00002255, -0.000000027]),
		 'OMEGA': array([49.558093, -0.2949846, -0.00063993, -0.000002143]),
		 'PI': array([336.060234, 0.4438898, -0.00017321, 0.000000300])
		}

	def initJupiter(self):
		self.name = 'Jupiter'
		self.mu = 1.26686534e8
		self.meeusCoeffs = {
		 'L': array([34.351484, 3034.9056746, -0.00008501, 0.000000004]),
		 'a': array([5.202603191, 0.0000001913, 0, 0]),
		 'e': array([0.04849485, 0.000163244, -0.0000004719, -0.00000000197]),
		 'i': array([1.303270, -0.0019872, 0.00003318, 0.000000092]),
		 'OMEGA': array([100.464441, 0.1766828, 0.00090387, -0.000007032]),
		 'PI': array([14.331309, 0.2155525, 0.00072252, -0.000004590])
		}

	def initSaturn(self):
		self.name = 'Saturn'
		self.mu = 3.7931187e14
		self.meeusCoeffs = {
		 'L': array([50.077471, 1222.1137943, 0.00021004, -0.000000019]),
		 'a': array([9.554909596, -0.0000021389, 0, 0]),
		 'e': array([0.05550862, -0.000346818, -0.0000006456, 0.00000000338]),
		 'i': array([2.488878, 0.0025515, -0.00004903, 0.000000018]),
		 'OMEGA': array([113.665524, -0.2566649, -0.00018345, 0.000000357]),
		 'PI': array([93.056787, 0.5665496, 0.00052809, 0.000004882])
		}

	def initUranus(self):
		self.name = 'Uranus'
		self.mu = 5.793939e6
		self.meeusCoeffs = {
		 'L': array([314.055005, 429.8640561, 0.00030434, 0.000000026]),
		 'a': array([19.218446062, -0.0000000372, 0.00000000098, 0]),
		 'e': array([0.04629590, -0.000027337, 0.0000000790, 0.00000000025]),
		 'i': array([0.773196, 0.0007744, 0.00003749, -0.000000092]),
		 'OMEGA': array([74.005947, 0.5211258, 0.00133982, 0.000018516]),
		 'PI': array([173.005159, 1.4863784, 0.0021450, 0.000000433])
		}

	def initNeptune(self):
		self.name = 'Neptune'
		self.mu = 6.836529e6
		self.meeusCoeffs = {
		 'L': array([304.348665, 219.8833092, 0.00030926, 0.000000018]),
		 'a': array([30.110386869, -0.0000001663, 0.00000000069, 0]),
		 'e': array([0.00898809, 0.000006408, -0.0000000008, -0.00000000005]),
		 'i': array([1.769952, -0.0093082, -0.00000708, 0.000000028]),
		 'OMEGA': array([131.784057, 1.1022057, 0.00026006, -0.000000636]),
		 'PI': array([48.123691, 1.4262677, 0.00037918, -0.000000003])
		}

	def initPluto(self):
		self.name = 'Pluto'
		self.mu = 8.71e2
		self.meeusCoeffs = {
		 'L': array([238.92903833, 145.20780515, 0.0, 0.0]),
		 'a': array([39.48211675, -0.00031596, 0.0, 0.0]),
		 'e': array([0.24882730, 0.00005170, 0.0, 0.0]),
		 'i': array([17.14001206, 0.00004818, 0.0, 0.0]),
		 'OMEGA': array([110.30393684, -0.01183482, 0.0, 0.0]),
		 'PI': array([224.06891629, -0.04062942, 0.0, 0.0])
		}

	def calculateMeeus(self,coeffs,currentJD):
		"""!
		Taken from CU Boulder ASEN 6008 Interplanetary Mission Design
		notes by Kate Davis
		"""
		T = (currentJD - 2451545.0)/36525
		element = coeffs[0] + \
				  coeffs[1]*T + \
				  coeffs[2]*T**2 + \
				  coeffs[3]*T**3 
		return element, T

	def meeusStateUpdate(self, t):
		"""!
		Taken from CU Boulder ASEN 6008 Interplanetary Mission Design
		notes by Kate Davis
		"""
		L,T = self.calculateMeeus(self.meeusCoeffs['L'], t)
		a,T = self.calculateMeeus(self.meeusCoeffs['a'], t)
		a *= au/1000
		e,T = self.calculateMeeus(self.meeusCoeffs['e'], t)
		i,T = self.calculateMeeus(self.meeusCoeffs['i'], t)

		OMEGA,T = self.calculateMeeus(self.meeusCoeffs['OMEGA'], t)
		PI,T = self.calculateMeeus(self.meeusCoeffs['PI'], t)
		omega = PI - OMEGA
		M = L - PI


		Cen = (2*e-e**3/4+5*e**5/96)*sin(M) + \
			  (5*e**2/4-11*e**4/24)*sin(2*M) + \
			  (13*e**3/12-43*e**5/64)*sin(3*M) + \
			  (103*e**4/96)*sin(4*M) + \
			  (1097*e**5/960)*sin(5*M)


		nu = M + Cen

		return coe2rv(a,e,i,OMEGA,omega,nu,mu=1.32712428e11)





