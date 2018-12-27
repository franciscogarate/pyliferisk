#!/usr/bin/python
from pyliferisk import *
import numpy as np

mt = Actuarial(nt=FIN, i=0.12/12) #FIN = Financial table

n = 5 * 12
C = 100

print(annuity(mt, 0, n, 1) * C)	#replace age 'x' by 0