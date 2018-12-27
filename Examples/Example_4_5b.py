#!/usr/bin/python
from pyliferisk import *
from pyliferisk.mortalitytables import INM05
import numpy as np
import pandas as pd

rfr = pd.read_excel('EIOPA_RFR_20161231_Term_Structures.xlsx', sheet_name='RFR_spot_no_VA', 
					skiprows=9, usecols='C:C', names=['Euro'])

tariff  = Actuarial(nt=INM05, i=0.05)
reserve = MortalityTable(nt=INM05)
x = 32			# age
Cd = 3000 		# capital death
Premium = Cd * Ax(tariff, 25) / annuity(tariff, 25, 'w', 0) #fixed at age 25

qx_vector = []
px_vector = []
for i in range(x,reserve.w + 1):
	qx = ((reserve.lx[i]-reserve.lx[i+1]) / reserve.lx[x])
	qx_vector.append(qx)
	qx_sum = sum(qx_vector)
	px_vector.append(1 - qx_sum)

def Reserve(i):
	discount_factor = []
	for y in range(0, reserve.w - x + 1):
		if isinstance(i,float):
			discount_factor.append(1 / (1 + i) ** (y + 1))
		elif i == 'rfr':
			discount_factor.append(1 / (1 + rfr['Euro'][y]) ** (y + 1))

	APV_Premium = np.dot(Premium, px_vector)
	APV_Claims = np.dot(Cd, qx_vector)
	return np.dot(discount_factor, np.subtract(APV_Claims, APV_Premium)).round(2)

print(Reserve(0.0191))
print(Reserve(0.0139))
print(Reserve('rfr'))