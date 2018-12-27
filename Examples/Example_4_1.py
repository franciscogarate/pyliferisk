#!/usr/bin/python
import pyliferisk as life
from pyliferisk.mortalitytables import SPAIN_PASEM2010M
import numpy as np

mt = life.MortalityTable(nt=SPAIN_PASEM2010M)

age = 67				
initial_payment = 8000
incr = 0.03				# increment
i = 0.05 				# interest rate

discount_factor = []
for y in range(0, mt.w-age):
	discount_factor.append(1 / (1 + i) ** (y + 1))

payments = [initial_payment]
for x in range(0, mt.w-age-1):
	payments.append(payments[x] * (1 + incr) * (1 - mt.qx[age+x] / 1000))

print('Premium:', np.dot(payments, discount_factor).round(2))