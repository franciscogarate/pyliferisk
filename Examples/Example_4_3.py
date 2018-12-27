#!/usr/bin/python
from pyliferisk import *
from pyliferisk.mortalitytables import SPAININE2004, GKM95
import csv

mt = Actuarial(nt=GKM80, i=0.04)

def single_risk_premium(x, n):
   return nEx(mt, x, n) + Axn(mt, x, n)

def annual_risk_premium(x, n):
   return (single_risk_premium(x, n) / annuity(mt, x, n, 0))

SingleRiskPrem=[]
AnnualRiskPrem=[]

columns = '{0:8} {1:2} {2:9} {3:8} {4:10} {5:10}'
print(columns.format('Contract', 'Age', 'Duration', 'Capital', 'Single Pr', 'Annual Pr'))
print('--' * 26)

with open('colective.csv', 'r') as file:
    colective = csv.DictReader(file, delimiter=';')
    for row in colective:
        age = int(row['age'])
        dur = int(row['duration'])
        capital = int(row['capital'])
        single_premium = round(capital * single_risk_premium(age, dur), 2)
        annual_premium = round(capital * annual_risk_premium(age, dur), 2)
        AnnualRiskPrem.append(annual_premium)
        print(columns.format(row['N_pol'], age, dur, capital, single_premium, annual_premium))

print('--'*26)
print('Total Annual Premium:', sum(AnnualRiskPrem))