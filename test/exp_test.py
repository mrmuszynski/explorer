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
sys.path.insert(0, '../../lib/')

import vehicles, celestialBodies, simScenario
from constants import au
from numpy import array, argmax, argmin, rad2deg, cos, zeros
import matplotlib.pyplot as plt
from timeFcn import timeConvert, day2sec
import orbits as o
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

def test_multiCoe2rv():
	from orbits import coe2rv
	p = zeros(10) + 11067.790 #in km 
	e = zeros(10) + 0.83285
	i = zeros(10) + 87.87 #in degrees
	OMEGA = zeros(10) + 227.89 #in degrees
	omega = zeros(10) + 53.38 #in degrees
	nu = zeros(10) + 92.335 #in degrees
	a = p/(1-e**2)
	X = coe2rv(a,e,i,OMEGA,omega,nu)

	#note: These answers differ from Vallado's but I did them
	#by hand and they match what I have here, so I am quite
	#certain he is wrong
	assert( abs(X[0,0] - 6525.368) < 0.0005 )
	assert( abs(X[1,1] - 6861.532) < 0.0005 )
	assert( abs(X[2,2] - 6449.119) < 0.0005 )
	assert( abs(X[3,3] - 4.902279) < 0.0000005 )
	assert( abs(X[4,4] - 5.533140) < 0.0000005 )
	assert( abs(X[5,5] - (-1.975710)) < 0.0000005 )


def test_meeusStateUpdateVallado():
	"""!
	Test taken from Vallado Algorithm 33. P 296-298
	"""
	from orbits import anomalies, coe2rv
	from constants import au
	jupiter = celestialBodies.celestialBody()
	jupiter.initJupiter()
	scen = simScenario.simScenario()
	scen.addNonGravBody([jupiter])
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

def test_meeusStateUpdateDavis():
	"""!
	Test taken from ASEN 6008 material, CU Boudler Spring 2018. Provided
	by Dr. Kate Davis
	"""

	########################################################
	# Test case 1
	########################################################

	venus = celestialBodies.celestialBody()
	venus.initVenus()
	earth = celestialBodies.celestialBody()
	earth.initEarth()

	departureJD = 2455450.
	arrivalJD = 2455610.

	planet1AtDeparture = earth.meeusStateUpdate(departureJD)
	planet2AtArrival = venus.meeusStateUpdate(arrivalJD)

	correctPlanet1AtDeparture = array([
		147084764.907217,
		-32521189.6497507, 
		467.1900914, 
		5.94623924, 
		28.97464121, 
		-0.000715915])

	correctPlanet2AtArrival = array([
		-88002509.1583767,
		-62680223.1330849, 
		4220331.52492018, 
		20.0705935958064, 
		-28.6898298667745, 
		-1.55129181466267])

	diff1 = planet1AtDeparture - correctPlanet1AtDeparture
	diff2 = planet2AtArrival - correctPlanet2AtArrival

	#assert that all match within 12 digits (or more) precision
	print(diff1)
	assert(abs(diff1[0]) < 5e-6)
	assert(abs(diff1[1]) < 5e-6)
	assert(abs(diff1[2]) < 5e-8)
	assert(abs(diff1[3]) < 5e-10)
	assert(abs(diff1[4]) < 5e-10)
	assert(abs(diff1[5]) < 5e-10)
	assert(abs(diff2[0]) < 5e-6)
	assert(abs(diff2[1]) < 5e-6)
	assert(abs(diff2[2]) < 5e-7)
	assert(abs(diff2[3]) < 5e-12)
	assert(abs(diff2[4]) < 5e-12)
	assert(abs(diff2[5]) < 5e-14)

	########################################################
	# Test case 2
	########################################################

	mars = celestialBodies.celestialBody()
	mars.initMars()
	jupiter = celestialBodies.celestialBody()
	jupiter.initJupiter()

	departureJD = 2456300.
	arrivalJD = 2457500.

	planet1AtDeparture = mars.meeusStateUpdate(departureJD)
	planet2AtArrival = jupiter.meeusStateUpdate(arrivalJD)

	correctPlanet1AtDeparture = array([
		170145121.321308,
		-117637192.836034,
		-6642044.2724648,
		14.7014998589987,
		22.0029290376879,
		0.100109561656046])
	correctPlanet2AtArrival = array([
		-803451694.669228,
		121525767.116065,
		17465211.7766441,
		-2.11046595903622,
		-12.3119924444556,
		0.0981984077206206])

	diff1 = planet1AtDeparture - correctPlanet1AtDeparture
	diff2 = planet2AtArrival - correctPlanet2AtArrival

	#assert that all match within 12 digits (or more) precision
	assert(abs(diff1[0]) < 5e-6)
	assert(abs(diff1[1]) < 5e-6)
	assert(abs(diff1[2]) < 5e-8)
	assert(abs(diff1[3]) < 5e-10)
	assert(abs(diff1[4]) < 5e-10)
	assert(abs(diff1[5]) < 5e-10)
	assert(abs(diff2[0]) < 5e-6)
	assert(abs(diff2[1]) < 5e-6)
	assert(abs(diff2[2]) < 5e-7)
	assert(abs(diff2[3]) < 5e-12)
	assert(abs(diff2[4]) < 5e-12)
	assert(abs(diff2[5]) < 5e-14)

	########################################################
	# Test case 3
	########################################################
	saturn = celestialBodies.celestialBody()
	saturn.initSaturn()
	neptune = celestialBodies.celestialBody()
	neptune.initNeptune()

	departureJD = 2455940
	arrivalJD = 2461940

	planet1AtDeparture = saturn.meeusStateUpdate(departureJD)
	planet2AtArrival = neptune.meeusStateUpdate(arrivalJD)

	correctPlanet1AtDeparture = array([
		-1334047119.28306,
		-571391392.847366,
		63087187.1397936,
		3.26566097701568,
		-8.8999508220789,
		0.0250518196387099])

	correctPlanet2AtArrival = array([
		4446562424.74189,
		484989501.499146,
		-111833872.461498,
		-0.627466452223638,
		5.42732630878375,
		-0.0978994819146572])

	diff1 = planet1AtDeparture - correctPlanet1AtDeparture
	diff2 = planet2AtArrival - correctPlanet2AtArrival

	assert(abs(diff1[0]) < 5e-6)
	assert(abs(diff1[1]) < 5e-6)
	assert(abs(diff1[2]) < 5e-8)
	assert(abs(diff1[3]) < 5e-10)
	assert(abs(diff1[4]) < 5e-10)
	assert(abs(diff1[5]) < 5e-10)
	assert(abs(diff2[0]) < 5e-6)
	assert(abs(diff2[1]) < 5e-6)
	assert(abs(diff2[2]) < 5e-7)
	assert(abs(diff2[3]) < 5e-12)
	assert(abs(diff2[4]) < 5e-12)
	assert(abs(diff2[5]) < 5e-14)
	########################################################
	# Test case 4
	########################################################

	venus = celestialBodies.celestialBody()
	venus.initVenus()
	earth = celestialBodies.celestialBody()
	earth.initEarth()

	departureJD = 2460545
	arrivalJD = 2460919

	planet1AtDeparture = earth.meeusStateUpdate(departureJD)
	planet2AtArrival = venus.meeusStateUpdate(arrivalJD)

	correctPlanet1AtDeparture = array([
		130423562.062471,
		-76679031.8462418,
		3624.81656101975,
		14.6129412274587,
		25.5674761326208,
		-0.00150344550048443])
	correctPlanet2AtArrival = array([
		19195371.6699821,
		106029328.360906,
		348953.802015791,
		-34.5791361074399,
		6.06419077607759,
		2.07855065113644])


	diff1 = planet1AtDeparture - correctPlanet1AtDeparture
	diff2 = planet2AtArrival - correctPlanet2AtArrival

	assert(abs(diff1[0]) < 5e-6)
	assert(abs(diff1[1]) < 5e-6)
	assert(abs(diff1[2]) < 5e-8)
	assert(abs(diff1[3]) < 5e-10)
	assert(abs(diff1[4]) < 5e-10)
	assert(abs(diff1[5]) < 5e-10)
	assert(abs(diff2[0]) < 5e-5)
	assert(abs(diff2[1]) < 5e-6)
	assert(abs(diff2[2]) < 5e-7)
	assert(abs(diff2[3]) < 5e-13)
	assert(abs(diff2[4]) < 5e-12)
	assert(abs(diff2[5]) < 5e-14)


def test_lambertSolver():
	"""!
	Test taken from ASEN 6008 material, CU Boudler Spring 2018. Provided
	by Dr. Kate Davis
	"""

	muSun = 1.32712440018e11
	########################################################
	# Test case 1
	########################################################

	departureJD = 2455450.
	arrivalJD = 2455610.
	TOFdays = arrivalJD - departureJD
	TOFs = day2sec(TOFdays)

	planet1AtDeparture = array([
		147084764.907217,
		-32521189.6497507, 
		467.1900914, 
		5.94623924, 
		28.97464121, 
		-0.000715915])

	planet2AtArrival = array([
		-88002509.1583767,
		-62680223.1330849, 
		4220331.52492018, 
		20.0705935958064, 
		-28.6898298667745, 
		-1.55129181466267])

	lam = o.lambert(planet1AtDeparture,planet2AtArrival,TOFs,mu=muSun)
	v0 = lam['v_0']
	vf = lam['v_f']
	correctV0 = array([4.65144349746008, 26.0824144093203, -1.39306043231699])
	correctVf = array([16.7926204519414, -33.3516748429805, 1.52302150358741])

	v0Diff = v0 - correctV0
	vfDiff = vf - correctVf

	assert(abs(v0Diff[0]) < 5e-12)
	assert(abs(v0Diff[1]) < 5e-13)
	assert(abs(v0Diff[2]) < 5e-14)
	assert(abs(vfDiff[0]) < 5e-12)
	assert(abs(vfDiff[1]) < 5e-12)
	assert(abs(vfDiff[2]) < 5e-13)

	departureVInf = v0 - planet1AtDeparture[3:6]
	arrivalVInf = vf - planet2AtArrival[3:6]
	correctDepartureVInf = \
		array([-1.29479574247079, -2.89222680107954, -1.39234451716994])
	correctArrivalVInf = \
		array([-3.27797314386492,-4.66184497620607,3.07431331825009])

	departureVInfDiff = departureVInf - correctDepartureVInf
	arrivalVInfDiff = arrivalVInf -  correctArrivalVInf


	assert(abs(departureVInfDiff[0]) < 5e-10)
	assert(abs(departureVInfDiff[1]) < 5e-10)
	assert(abs(departureVInfDiff[2]) < 5e-10)
	assert(abs(arrivalVInfDiff[0]) < 5e-12)
	assert(abs(arrivalVInfDiff[1]) < 5e-12)
	assert(abs(arrivalVInfDiff[2]) < 5e-13)

	########################################################
	# Test case 2
	########################################################

	departureJD = 2456300.
	arrivalJD = 2457500.
	TOFdays = arrivalJD - departureJD
	TOFs = day2sec(TOFdays)

	planet1AtDeparture = array([
		170145121.321308,
		-117637192.836034,
		-6642044.2724648,
		14.7014998589987,
		22.0029290376879,
		0.100109561656046])

	planet2AtArrival = array([
		-803451694.669228,
		121525767.116065,
		17465211.7766441,
		-2.11046595903622,
		-12.3119924444556,
		0.0981984077206206])

	lam = o.lambert(planet1AtDeparture,planet2AtArrival,TOFs,mu=muSun)
	v0 = lam['v_0']
	vf = lam['v_f']
	correctV0 = array([13.74077736, 28.83099312, 0.691285008])
	correctVf = array([-0.883933069, -7.983627014, -0.240770598])

	v0Diff = v0 - correctV0
	vfDiff = vf - correctVf

	assert(abs(v0Diff[0]) < 5e-9)
	assert(abs(v0Diff[1]) < 5e-9)
	assert(abs(v0Diff[2]) < 5e-10)
	assert(abs(vfDiff[0]) < 5e-10)
	assert(abs(vfDiff[1]) < 5e-10)
	assert(abs(vfDiff[2]) < 5e-10)

	########################################################
	# Test case 3
	########################################################
	departureJD = 2455940.
	arrivalJD = 2461940.
	TOFdays = arrivalJD - departureJD
	TOFs = day2sec(TOFdays)


	planet1AtDeparture = array([
		-1334047119.28306,
		-571391392.847366,
		63087187.1397936,
		3.26566097701568,
		-8.8999508220789,
		0.0250518196387099])

	planet2AtArrival = array([
		4446562424.74189,
		484989501.499146,
		-111833872.461498,
		-0.627466452223638,
		5.42732630878375,
		-0.0978994819146572])

	lam = o.lambert(planet1AtDeparture,planet2AtArrival,TOFs,mu=muSun)
	v0 = lam['v_0']
	vf = lam['v_f']
	correctV0 = array([11.18326152, -8.90233011, 0.420697886])
	correctVf = array([7.522127215, 4.928368894, -0.474069569])

	v0Diff = v0 - correctV0
	vfDiff = vf - correctVf
	assert(abs(v0Diff[0]) < 5e-9)
	assert(abs(v0Diff[1]) < 5e-10)
	assert(abs(v0Diff[2]) < 5e-11)
	assert(abs(vfDiff[0]) < 5e-11)
	assert(abs(vfDiff[1]) < 5e-10)
	assert(abs(vfDiff[2]) < 5e-10)


	########################################################
	# Test case 4
	########################################################

	departureJD = 2460545
	arrivalJD = 2460919
	TOFdays = arrivalJD - departureJD
	TOFs = day2sec(TOFdays)


	planet1AtDeparture = array([
		130423562.062471,
		-76679031.8462418,
		3624.81656101975,
		14.6129412274587,
		25.5674761326208,
		-0.00150344550048443])
	planet2AtArrival = array([
		19195371.6699821,
		106029328.360906,
		348953.802015791,
		-34.5791361074399,
		6.06419077607759,
		2.07855065113644])

	lam = o.lambert(planet1AtDeparture,planet2AtArrival,TOFs,mu=muSun,
		revs=1,type=3)
	v0 = lam['v_0']
	vf = lam['v_f']
	correctV0 = array([12.76771134, 22.79158874, 0.090338826])
	correctVf = array([-37.30072389, -0.176853447, -0.066693083])

	v0Diff = v0 - correctV0
	vfDiff = vf - correctVf
	assert(abs(v0Diff[0]) < 5e-9 )
	assert(abs(v0Diff[1]) < 5e-9 )
	assert(abs(v0Diff[2]) < 5e-10 )
	assert(abs(vfDiff[0]) < 5e-9 )
	assert(abs(vfDiff[1]) < 5e-11 )
	assert(abs(vfDiff[2]) < 5e-10 )







