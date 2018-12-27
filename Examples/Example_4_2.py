#!/usr/bin/python
import matplotlib.pyplot as plt
import pyliferisk as life
from pyliferisk.mortalitytables import SPAININE2004, GKM95

tariff = life.MortalityTable(nt=SPAININE2004)
experience = life.MortalityTable(nt=GKM95, perc=75)
x = range(0, tariff.w)
y = tariff.lx[:tariff.w]
z = experience.lx[:tariff.w]
plt.plot(x,y, color = 'blue')
plt.plot(x,z, color = 'red')
plt.ylabel('lx')
plt.xlabel('age')