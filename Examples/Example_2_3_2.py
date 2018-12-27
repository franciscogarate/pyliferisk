#!/usr/bin/python
from pyliferisk import *
from pyliferisk.mortalitytables import GKM95

nt = Actuarial(nt=GKM95, i=0.06)
x = 30
n = 10
C = 1000

print(C * (Axn(nt, x, n) / annuity(nt, x, n, 0)))