#!/usr/bin/python
from pyliferisk import *
from pyliferisk.mortalitytables import INM05
import numpy as np

tariff  = Actuarial(nt=INM05, i=0.05)
reserve = MortalityTable(nt=INM05)
age = 32			# age
Cd = 3000 			# capital death
Premium = Cd * Ax(tariff, 25) / annuity(tariff, 25, 'w', 0) #fixed at age 25

qx_vector = []
px_vector=[]
for i in range(age, reserve.w + 1):
	qx = ((reserve.lx[i] - reserve.lx[i+1]) / reserve.lx[age])
	qx_vector.append(qx)
	qx_sum = sum(qx_vector)
	px_vector.append(1 - qx_sum)

def Reserve(i):
	discount_factor = []
	for y in range(0, reserve.w-age + 1):
		discount_factor.append(1 / ( 1 + i) ** (y + 1))

	APV_Premium = np.dot(Premium, px_vector)
	APV_Claims = np.dot(Cd, qx_vector)
	# Reserve = APV(Premium) - APV(Claim)
	return np.dot(discount_factor, np.subtract(APV_Claims, APV_Premium)).round(2)

print(Reserve(0.0191))
print(Reserve(0.0139))