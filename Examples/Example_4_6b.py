#!/usr/bin/python
import pandas as pd
from pyliferisk import MortalityTable
import matplotlib.pyplot as plt

USLife1979 = pd.read_csv('uslife79.csv')
USLife79lx = USLife1979['lx'].tolist()

mt = MortalityTable(lx=USLife79lx)

fig= plt.figure(figsize=(7.5,3.7))

x = range(0, mt.w)
y = mt.lx[:mt.w]
plt.plot(x, y, linewidth=3, color='0')
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.ylabel('lx')
plt.xlabel('age')
plt.show()