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

import rigidBodyKinematics as rbk
from numpy import array, array_equal, amax
import pdb

###############################################################################
# 
# absolute(a - b) <= (atol + rtol * absolute(b))
###############################################################################


###############################################################################
#
# test_e3212C() Tests that 3-2-1 euler angles are being converted to DCMs 
# correctly. 
#
# thetaB and thetaF are inputs given in HPS lecture notes volume 2, pages 40-1
# BNTruth, FNTruth, BFTruth, psiTruth, thetaTruth, and phiTruth are the
# outputs as presented in those pages, quoted to as many decimal points as
# HPS does in the notes.
#
# All asserts check that computed values match those given by HPS to within
# rounding error given the number of significant figured he quotes
#
###############################################################################

def test_e3212C():
	thetaB = array([30,-45,60])
	thetaF = array([10, 25,-15])
	
	BN = rbk.e3212C(thetaB)
	BNTruth = array([
		[  0.612372,  0.353553,  0.707107],
		[ -0.780330,  0.126826,  0.612372],
		[  0.126826, -0.926777,  0.353553]
		])

	assert( amax(abs(BN - BNTruth)) < 1e-6)

	FN = rbk.e3212C(thetaF)
	FNTruth = array([
		[  0.892539,  0.157379, -0.422618],
		[ -0.275451,  0.932257, -0.234570],
		[  0.357073,  0.325773,  0.875426]
		])

	assert( amax(abs(FN - FNTruth)) < 1e-6)

	BF = BN.dot(FN.T)
	BFTruth = array([
		[  0.303372, -0.0049418,  0.952859],
		[ -0.935315,  0.1895340,  0.298769],
		[ -0.182075, -0.9818620,  0.052877]
		])

	assert( amax(abs(BF - BFTruth)) < 1e-6)

	angles = rbk.C2e321(BF)
	psi = angles[0]
	theta = angles[1]
	phi = angles[2]
	psiTruth = -0.933242
	thetaTruth = -72.3373	
	phiTruth = 	79.9636

	assert( abs(psi - psiTruth) < 1e-6)
	assert( abs(theta - thetaTruth) < 1e-4)
	assert( abs(phi - phiTruth) < 1e-4)







