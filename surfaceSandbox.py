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
sys.path.insert(0, 'classes')
sys.path.insert(0, 'prop')
sys.path.insert(0, 'fsw')
sys.path.insert(0, 'util')

import vehicles, celestialBodies, simScenario
from constants import au


import PIL 
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from util import rasterize
from util import r1,r2,r3

k = np.deg2rad(0)
l = np.deg2rad(-30)
m = np.deg2rad(20)

rSC = np.array([np.cos(m)*np.cos(l),np.cos(m)*np.sin(l),np.sin(m)])
eSC = rSC/np.linalg.norm(rSC)
rSun = np.array([10,0,0])
eSun = rSun/np.linalg.norm(rSun)

focalLength = 1
detectorWidth = 1
detectorHeight = 1 
resolutionWidth = 100
resolutionHeight = 100

# load bluemarble with PIL
bm = PIL.Image.open('img/lunarSurface.jpg')
# it's big, so I'll rescale it, convert to array, and divide by 256 to get RGB values that matplotlib accept 
bm = np.array(bm)/256.
import pdb
pdb.set_trace()
# coordinates of the image - don't know if this is entirely accurate, but probably close
lons = np.deg2rad(np.linspace(-180, 180, bm.shape[1]))
lats = np.deg2rad(np.linspace(-90, 90, bm.shape[0])[::-1])

n1 = np.outer(np.cos(lons), np.cos(lats)).T.reshape(len(lons)*len(lats))
n2 = np.outer(np.sin(lons), np.cos(lats)).T.reshape(len(lons)*len(lats))
n3 = np.outer(np.ones(np.size(lons)), np.sin(lats)).T.reshape(len(lons)*len(lats))


try:
	bm = bm.reshape(len(lons)*len(lats),3)
except:
	bm = bm.reshape(len(lons)*len(lats))

stack = np.vstack([n1,n2,n3])
sunDotFacet = eSun.dot(stack)

rotate = r1(-k).dot(r2(-m).dot(r3(l)))
rot = rotate.dot(stack)

scDotFacet = eSC.dot(stack)
ind = np.logical_and(scDotFacet >= 0, sunDotFacet >= 0)
stack = stack.T[ind].T
rot = rot.T[ind].T
bm = bm[ind]
sunDotFacet = sunDotFacet[ind]
# plt.plot(n1[ind],n2[ind])
# plt.plot(eSC[0],eSC[1],'X')
# plt.axis('equal')

import pdb
pdb.set_trace()

try:
	rasterRed = \
		rasterize(
			400,400,(-rot[2]+2)*100,(rot[1]+2)*100,bm[:,0]*sunDotFacet,
			avg=1)
	rasterBlue = \
		rasterize(
			400,400,(-rot[2]+2)*100,(rot[1]+2)*100,bm[:,1]*sunDotFacet,
			avg=1)
	rasterGreen = \
		rasterize(
			400,400,(-rot[2]+2)*100,(rot[1]+2)*100,bm[:,2]*sunDotFacet,
			avg=1)
except:
	rasterRed = \
		rasterize(
			400,400,(-rot[2]+2)*100,(rot[1]+2)*100,bm*sunDotFacet*2,
			avg=1)
	rasterBlue = rasterRed
	rasterGreen = rasterRed

plt.imshow(np.hstack([rasterRed,rasterBlue,rasterGreen]).reshape(3,400,400).T)
plt.show()

import pdb
pdb.set_trace()





