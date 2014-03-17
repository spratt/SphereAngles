#!/usr/bin/env python3.3

MIN_MRD = -180.0
MAX_MRD = 180.0
MIN_PAR = -90
MAX_PAR = 90

ERR_MRD = -1
ERR_PAR = -2

################################################################################
# Arguments

import argparse, sys, math

parser = argparse.ArgumentParser(
    description='Given two meridians and two parallels on a sphere of a '
    +'given radius, calculate the bottom left angle of the triangle')

parser.add_argument('mrd1', type=float,
                    help='The first meridian in degrees ({} to {})'
                    .format(MIN_MRD, MAX_MRD))
parser.add_argument('mrd2', type=float,
                   help='The second meridian in degrees (-180 to 180)')
parser.add_argument('par1', type=float,
                   help='The first parallel in degrees (-90 to 90)')
parser.add_argument('par2', type=float,
                   help='The second parallel in degrees (-90 to 90)')
parser.add_argument('--rad', type=float, default=1.0,
                   help='The radius of the sphere')

def degToRad(angle):
    return angle * math.pi / 180.0

args = parser.parse_args()
mrd1 = degToRad(args.mrd1)
mrd2 = degToRad(args.mrd2)
par1 = degToRad(args.par1)
par2 = degToRad(args.par2)
rad = args.rad

print('mrd1={}, mrd2={}, par1={}, par2={}, rad={}'
      .format(mrd1, mrd2, par1, par2, rad))

if mrd1 < MIN_MRD or mrd1 > MAX_MRD or mrd2 < MIN_MRD or mrd2 > MAX_MRD:
    print("meridians must be between {} and {}".format(MIN_MRD, MAX_MRD))
    sys.exit(ERR_MRD)

if par1 < MIN_PAR or par1 > MAX_PAR or par2 < MIN_PAR or par2 > MAX_PAR:
    print("parallels must be between {} and {}".format(MIN_PAR, MAX_PAR))
    sys.exit(ERR_PAR)

################################################################################
# Determine the spherical coordinates
#
#   mrd1    mrd2
#    |       |
#    |       |
#   -a-------+--par1
#    |\      |
#    | \     |
#    |  \    |
#    |   \   |
#    |    \  |
#    |     \ |
#    |      \|
#   -b-------c---par2
#    |       |
#

#    lat   lon
a = (par1, mrd1)
b = (par2, mrd1)
c = (par2, mrd2)

print('a={}, b={}, c={}'.format(a, b, c))

################################################################################
# Convert the spherical coordinates into cartesian coordinates of three points
#
#    p
#    |\      
#    | \     
#    |  \    
#    |   \   
#    |    \  
#    |     \ 
#    |      \
#    q-------r
#


def sphereToCartesian(point, radius):
    lat, lon = point[0], point[1]
    return (radius * math.cos(lat) * math.cos(lon),
            radius * math.cos(lat) * math.sin(lon),
            radius * math.sin(lat))

p = sphereToCartesian(a, rad)
q = sphereToCartesian(b, rad)
r = sphereToCartesian(c, rad)

print('p={}, q={}, r={}'.format(p, q, r))

################################################################################
# Convert the points into two vectors with the same origin
#
#    u
#    ,      
#   /|\      
#    |      
#    |      
#    |      
#    |      
#    |      
#    o------> v
#

def getVector(p0, p1):
    """ Gives the 3d vector from p0 to p1 """
    return (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])

u = getVector(q, p)
v = getVector(q, r)

print('u={}, v={}'.format(u, v))

################################################################################
# Calculate the angle between the vectors

import numpy as np

rad = np.arccos(np.dot(u,v) / np.linalg.norm(u) / np.linalg.norm(v))

print('rad={}'.format(rad))

################################################################################
# Convert radians to degrees

def radToDeg(angle):
    return angle * 180.0 / math.pi

deg = radToDeg(rad)

print(deg)
