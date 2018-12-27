#!/usr/bin/python
from pyliferisk import *
from pyliferisk.mortalitytables import SPAIN_PASEM2010M
import pandas as pd

mt = MortalityTable(nt=SPAIN_PASEM2010M)

age = 67				
initial_payment = 8000
incr = 0.03				# increment annutie
i = 0.05 				# interest rate

period = list(range(0, mt.w - age))

df = pd.DataFrame(data=period, columns=['t'])

df['date'] = pd.DataFrame(pd.date_range('1/1/2016', periods=len(period), freq='A'))
df['age'] = pd.Series(list(range(age, mt.w)))
df['px'] = df['t'].apply(lambda t: 1 - mt.qx[age+t] / 1000)
df['px_cumprod'] = df['px'].cumprod().round(4)
df['disc_factor'] = df['t'].apply(lambda t: 1 / (1 + i) ** (t + 1))
df['capital'] = df['t'].apply(lambda t: initial_payment * ((1 + incr) ** t)).round(4)
df['payments'] = df['t'].apply(lambda t: initial_payment if t == 0 else df['capital'][t] * df['px_cumprod'][t-1]).round(4)
df['apv_payments'] = df['payments'] * df['disc_factor']
premium = df['apv_payments'].sum().round(2)
print(premium)

writer = pd.ExcelWriter("output.xls")
df.to_excel(writer,'Sheet1')
writer.save()