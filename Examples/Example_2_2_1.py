#!/usr/bin/python
from pyliferisk import Actuarial, Ax
from pyliferisk.mortalitytables import GKM95

mt = Actuarial(nt=GKM95, i=0.02)
x = 50 		#age
C = 1000 	#capital

print(Ax(mt, x) * C)