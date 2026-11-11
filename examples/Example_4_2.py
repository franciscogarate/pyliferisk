import matplotlib.pyplot as plt
import pyliferisk as life
from pyliferisk.mortalitytables import PASEM2020_M_NoRel_1orden, GKM95

tariff = life.MortalityTable(nt=PASEM2020_M_NoRel_1orden)
experience = life.MortalityTable(nt=GKM95, perc=75)
x = range(0, tariff.w)
y = tariff.lx[:tariff.w]
z = experience.lx[:tariff.w]
plt.plot(x,y, color = 'blue')
plt.plot(x,z, color = 'red')
plt.ylabel('lx')
plt.xlabel('age')