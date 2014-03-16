#!/usr/bin/env python3.2

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
#   par1    par2
#    |       |
#    |       |
#   -a-------+--mrd1
#    |\      |
#    | \     |
#    |  \    |
#    |   \   |
#    |    \  |
#    |     \ |
#    |      \|
#   -b-------c---mrd2
#    |       |
#

#    lat   lon
a = (mrd1, par1)
b = (mrd2, par1)
c = (mrd2, par2)

print('a={}, b={}, c={}'.format(a, b, c))

################################################################################
# Translate the spherical coordinates into cartesian coordinates

def sphereToCartesian(point, radius):
    lat, lon = point[0], point[1]
    return (radius * math.sin(lat) * math.cos(lon),
            radius * math.sin(lat) * math.sin(lat),
            radius * math.cos(lat))

p = sphereToCartesian(a, rad)
q = sphereToCartesian(b, rad)
r = sphereToCartesian(c, rad)

print('p={}, q={}, r={}'.format(p, q, r))
