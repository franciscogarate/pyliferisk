#!/usr/bin/python
from pyliferisk import Actuarial, Axn
from pyliferisk.mortalitytables import GKM95

mt = Actuarial(nt=GKM95, i=0.03)
x = 40 		#age
n = 20 		#horizon
C = 10000 	#capital

print(Axn(mt, x, n) * C)