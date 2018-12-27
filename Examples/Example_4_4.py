#!/usr/bin/python
import pandas as pd

df = pd.read_excel('EIOPA_RFR_20161231_Term_Structures.xlsx', sheet_name='RFR_spot_no_VA', 
					skiprows=9, usecols='C:C', names=['Euro'])

print(df.head(20))
