#!/usr/bin/python
import pandas as pd
from pyliferisk import MortalityTable

USLife1979 = pd.read_csv('uslife79.csv')
USLife79lx = USLife1979['lx'].tolist()

mt = MortalityTable(lx=USLife79lx)

print('Live to 100:', mt.lx[100]/mt.lx[20])
print('Die before 70:', 1 - mt.lx[70]/mt.lx[20])
print('Die in the tenth decade of life:', (mt.lx[90]-mt.lx[100])/mt.lx[20])


print('Probability of death between 50 and 51:', 
	(mt.lx[50] - mt.lx[51]) / mt.lx[50])
print('Likewise with qx:', mt.qx[50] / 1000)
print('Ultimate age:', mt.w)