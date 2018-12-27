#!/usr/bin/python
from pyliferisk import *
from pyliferisk.mortalitytables import GKM95

tariff = Actuarial(nt=GKM95, i=0.02)

print(tariff.Dx[50])
print(tariff.Nx[50])
print(tariff.Cx[50])
print(tariff.Mx[50])