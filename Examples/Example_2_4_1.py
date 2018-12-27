#!/usr/bin/python
from pyliferisk import *
from pyliferisk.mortalitytables import GKM80

C = 1000
x = 60
n = 25
exp = 0.2 / 100 	# expenses over capital
com =  0.10 		# commision over premium

mt = Actuarial(nt=GKM80, i=0.025)

def Premium(mt, x, n):
  return (nEx(mt, x, n) + Axn(mt, x, n)) / annuity(mt, x, n, 0) * C

print((Premium(mt, x, n) + C * exp) / (1 - com))