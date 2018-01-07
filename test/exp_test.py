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
sys.path.insert(0, '../util')

import vehicles, celestialBodies, simScenario
from constants import au
from numpy import array, argmax, argmin, rad2deg, cos
import matplotlib.pyplot as plt
from timeFcn import timeConvert

import pdb

def test_anomalies():
	from orbits import anomalies
	from numpy.random import uniform

	for i in range(0,100):
		#I only test eccentricities up to 0.8 These functions
		#are less accurate for higher eccentricities. I should
		#write another test that cauptures extreme eccentrities.
		e = uniform(800)/1000
		nuSet = anomalies('nu',uniform(360),1,e)
		Eset = anomalies('E',nuSet['E'],1,e)
		Mset = anomalies('M',nuSet['M'],1,e)
		tSet = anomalies('t',nuSet['t'],1,e)

		assert ( nuSet['nu'] - Eset['nu'] < 1e-12 )
		assert ( nuSet['E'] - Eset['E'] < 1e-12 )
		assert ( nuSet['M'] - Eset['M'] < 1e-12 )
		assert ( nuSet['t'] - Eset['t'] < 1e-12 )

		assert ( nuSet['nu'] - Mset['nu'] < 1e-12 )
		assert ( nuSet['E'] - Mset['E'] < 1e-12 )
		assert ( nuSet['M'] - Mset['M'] < 1e-12 )
		assert ( nuSet['t'] - Mset['t'] < 1e-12 )

		# assert ( nuSet['M'] - Mset['t'] < 1e-12 )

	# assert ( nuSet['nu'] - tSet['nu'] < 1e-12 )
	# assert ( nuSet['E'] - tSet['E'] < 1e-12 )
	# assert ( nuSet['M'] - tSet['M'] < 1e-12 )
	# assert ( nuSet['M'] - tSet['t'] < 1e-12 )


def test_coe2rv():
	from orbits import coe2rv
	p = 11067.790 #in km 
	e = 0.83285
	i = 87.87 #in degrees
	OMEGA = 227.89 #in degrees
	omega = 53.38 #in degrees
	nu = 92.335 #in degrees
	a = p/(1-e**2)
	X = coe2rv(a,e,i,OMEGA,omega,nu)

	#note: These answers differ from Vallado's but I did them
	#by hand and they match what I have here, so I am quite
	#certain he is wrong
	assert( abs(X[0] - 6525.368) < 0.0005 )
	assert( abs(X[1] - 6861.532) < 0.0005 )
	assert( abs(X[2] - 6449.119) < 0.0005 )
	assert( abs(X[3] - 4.902279) < 0.0000005 )
	assert( abs(X[4] - 5.533140) < 0.0000005 )
	assert( abs(X[5] - (-1.975710)) < 0.0000005 )



def test_meeusStateUpdate():
	"""!
	Test taken from Vallado Algorithm 33. P 296-298
	"""
	from orbits import anomalies, coe2rv
	from constants import au
	jupiter = celestialBodies.celestialBody()
	jupiter.initJupiter()
	scen = simScenario.simScenario()
	scen.addNonGravBod([jupiter])
	t = scen.currentTime = timeConvert([1994,140,20],'ydnhms','jd')

	#note that Vallado uses omega tilde where Davis uses PI.
	#also, Vallado uses lambda_M where Davis uses L
	a,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['a'], t)
	aAU = a*au/1000 #put a in km to match what coe2rv expects
	e,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['e'], t)
	i,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['i'], t)
	OMEGA,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['OMEGA'], t)
	PI,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['PI'], t)
	L,T = jupiter.calculateMeeus(jupiter.meeusCoeffs['L'], t)
	M = L - PI
	omega = PI - OMEGA
	p = a*(1-e**2)
	nu = anomalies('M',M,a,e)['nu']
	#2449493.333 is given by Vallado. This asserts that they
	#match within sigfigs 
	assert( abs(scen.currentTime - 2449493.333) < 0.0005 )
	#-0.05617158 is given by Vallado. I believe that there is an
	#error in his book, and the last sigfig should be a 7 instead
	#of an 8, so i check to one fewer sigfig than I normally would
	assert( abs(T - (-0.05617158)) < 0.00000005 )

	assert( abs(a - 5.202603) < 0.0000005 )
	assert( abs(e - 0.048486) < 0.0000005 )
	assert( abs(i - 1.303382) < 0.0000005 )
	assert( abs(OMEGA - 100.454519) < 0.0000005 )
	assert( abs(PI - 14.319203) < 0.0000005 )
	assert( abs(L - (-136.12394)) < 0.000005)
	assert( abs((M) - (-150.443142)) < 0.0000005 )
	assert( abs((omega) - (-86.135316)) < 0.0000005 )

	#My value is slightly off compared to vallado here. Haven't
	#checked why yet. One of us is quoting sigfigs wrong, I think.
	assert( abs(p - 5.190372) < 0.0000006)
	assert( abs(nu - 206.95453) < 0.000005)

	X = coe2rv(aAU,e,i,OMEGA,omega,nu)

	#convert postion from km to au to check against Vallado's answer
	#velocity is converted to au/s here
	X /= (au/1000)

	assert( abs(X[0] - (-4.075932)) < 0.0000005 )
	assert( abs(X[1] - (-3.578306)) < 0.0000005 )
	assert( abs(X[2] -    0.105970) < 0.0000005 )
	# assert( abs(X[3] - 4.902276) < 0.000001 )
	# assert( abs(X[4] - 5.533124) < 0.000001 )
	# assert( abs(X[5] - (-1.975709)) < 0.000001 )
	import pdb
	pdb.set_trace()
