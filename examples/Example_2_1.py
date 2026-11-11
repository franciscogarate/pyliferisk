from pyliferisk import MortalityTable
from pyliferisk.mortalitytables import PASEM2020_M_NoRel_1orden, GKM95

tariff = MortalityTable(nt=PASEM2020_M_NoRel_1orden)
experience = MortalityTable(nt=GKM95, perc=85)

# Print the omega (limiting age) of the both tables:
print(tariff.w)
print(experience.w)

# Print the qx at 50 years old:
print(tariff.qx[50])
print(experience.qx[50])