#!/usr/bin/python
from pyliferisk import *
from pyliferisk.mortalitytables import GKM95

nt = Actuarial(nt=GKM95, i=0.03)
x = 40
n = 20
Cm = 100000
Premium = Cm * Axn(nt, x, n) / annuity(nt, x, n, 0)  #fixed premium

def Reserve(t):
   return round(Cm * Axn(nt, x+t, n-t) - Premium * annuity(nt, x+t, n-t, 0),2)

for t in range(0, n+1):
   print(t, Reserve(t))