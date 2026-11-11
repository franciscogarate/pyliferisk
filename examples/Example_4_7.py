from pyliferisk import *
from pyliferisk.mortalitytables import PASEM2020_M_NoRel_1orden
import pandas as pd

mt = MortalityTable(nt=PASEM2020_M_NoRel_1orden)

age = 67				
init_payment = 8000
incr = 0.03		# increment annutie
i = 0.05 		# interest rate

period = len(range(0, mt.w - age))

df = pd.DataFrame(pd.date_range('1/1/2023', periods=period, freq='YE'), columns=['date'])
df['t'] = df.index
df['age'] = pd.Series(list(range(age, mt.w)))
df['px'] = df['t'].apply(lambda t: 1 - mt.qx[age+t])
df['px_cumprod'] = df['px'].cumprod()
df['disc_factor'] = df['t'].apply(lambda t: 1 / (1 + i) ** (t + 1))
df['capital'] = df['t'].apply(lambda t: init_payment * ((1 + incr) ** t))
df['payments'] = df['t'].apply(lambda t: init_payment if t == 0 else
df['capital'][t] * df['px_cumprod'][t-1])
df['apv_payments'] = df['payments'] * df['disc_factor']
premium = df['apv_payments'].sum().round(2)

print(df.head())
print('Premium:', premium)