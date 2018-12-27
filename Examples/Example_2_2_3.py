#!/usr/bin/python
from pyliferisk import MortalityTable
from pyliferisk.mortalitytables import GKM95
import numpy as np

mt = MortalityTable(nt=GKM95)
x = 40 		#age
n = 20 		#horizon
C = 10000 	#capital
i = 0.03	#interest rate

payments = []
for t in range(0, n):
   payments.append((mt.lx[x+t] - mt.lx[x+t+1]) / mt.lx[x] * C)

discount_factor = []
for y in range(0, n):
   discount_factor.append(1 / (1 + i) ** (y + 0.5))

print(np.dot(discount_factor, payments).round(2))