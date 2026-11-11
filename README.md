<h1>pyliferisk</h1>
Pyliferisk is a python library for life actuarial calculations, simple, powerful and easy-to-use.

Date: 2026-11-11<br/>
Version: 1.13.0<br/>
Author: Francisco Garate - fgaratesantiago (at) gmail (dot) com<br/>

Documentation
-------------
Documentation: [documentation_1.13.pdf](https://github.com/franciscogarate/pyliferisk/raw/master/documentation_1.13.pdf)

Disclaimer: qx is expressed per unit since version 1.13
-------------------------------------------------------
**Breaking change.** Up to version 1.12, ``mt.qx[x]``, ``qx()`` and ``px()`` were expressed per mille (the true probability was qx/1000). Since version 1.13 they are expressed per unit (between 0 and 1), so ``mt.qx[x]`` is the true probability.

This library is mainly used for academic purposes, and the aim of this change is to align it with the reference bibliography, where qx and px are probabilities between 0 and 1.

Code written for previous versions must be reviewed: any division by 1000 (for instance ``mt.qx[x] / 1000``) must be removed, otherwise the results will be wrong without any error message. The mortality tables included in ``pyliferisk.mortalitytables`` are still stored per mille and they are converted automatically when the table is loaded. See the documentation for the complete list of changes.

Introduction
------------
**Pyliferisk** is an open library written in Python for life and actuarial calculation contracts, based on commonly used methodologies among actuaries (International Actuarial Notation).

This library is able to cover all life contingencies risks (since the actuarial formulas follow the International Actuarial Notation), as well as to support the main insurance products.

This library has no dependencies other than the Python Standard Library, making it amazingly fast. It requires Python 3.8 or higher.

Additionally, the package includes several life mortality tables (``pyliferisk.mortalitytables``), mainly extracted from academic textbooks. Tables are added in list format. ie: SCOT_DLT_00_02_M = [0, 6.205, 0.328, 0.26 ....]
First item indicates the age when table starts; the following items are the qx expressed per mille (they are converted to per unit when the table is loaded).

Quick Start
-----------
The names of the formulas follow the International Actuarial Notation and are easily guessable (qx, lx, px, w, dx, ex, Ax, Axn..), with a few exceptions regarding special characters.

The **reserved variables** (in addition of python language) are the following:

For the mortality assumptions in ``MortalityTable()``:
* ``nt`` = The actuarial table used to perform life contingencies calculations. Syntax: nt=GKM95
* ``perc`` = Optional variable to indicate the percentage of mortality to be applied. Syntax: perc=85
Variable ``perc`` can be omitted, in this case it will be 100 by default.

For discounted (commutation) calculations use ``Actuarial()``, which additionally requires:
* ``i`` = interest rate. The effective rate of interest, namely, the total interest earned in a year. Syntax: i=0.02

All the actuarial formulas must include a minimum of 2 variables: mt (mortality table) and x (age) 
If necessary, additional variables should be included with the following order: 
``n`` (horizon in years),  ``m`` (m-monthly payments), ``t`` (n-years deferred period).

Variable ``m`` can be omitted, in this case it will be 1 (annual payment) by default.

Additionally, there are two smart formulas: annuity() and A(), where the number of variables are not fixed:

``annuity(mt, x, n, p, m=1, deferred=0, increase=None)``
* mt = the mortality table
* x = the age as integer number.   
* n = An integer number (term of insurance in years) or 'w' = whole-life.
* p = Moment of payment. Syntax: 0 = beginning of each period (annuity-due), 1 = end of each period (annuity-immediate),
Optional variables:
* m = Payable 'm' per year (fractional payments). Default = 1 (annually)
* deferred = The deferring period in years. Default = 0
* increase = The increase rate: ['g',q] (geometrical) or ['a',q] (arithmetical). For example, increase=['g',0.03]

The legacy positional syntax ``annuity(mt, x, n, p, m, ['a/g', q], -d)`` (deferring period as a negative number) is still accepted but deprecated.

![Picture](http://garpa.net/assets/images/pyliferisk2.png)

**Example 1:**
Print the omega (limiting age) of the both mortality tables and the qx at 50 years-old:
```python
from pyliferisk import MortalityTable
from pyliferisk.mortalitytables import INE2004, GKM95

tariff = MortalityTable(nt=INE2004)
experience = MortalityTable(nt=GKM95, perc=85)

# Print the omega (limiting age) of the both tables:
print(tariff.w)
print(experience.w)

# Print the qx at 50 years old:
print(tariff.qx[50])
print(experience.qx[50])
```

**Example 2:**
Plotting a surviving graph:
```python
import matplotlib.pyplot as plt
from pyliferisk import *
from pyliferisk.mortalitytables import INE2004, GKM95

tariff = MortalityTable(nt=INE2004)
experience = MortalityTable(nt=GKM95, perc=75)
x = range(0, tariff.w)
y = tariff.lx[:tariff.w]
z = experience.lx[:tariff.w]
plt.plot(x,y, color = 'blue')
plt.plot(x,z, color = 'red')
plt.ylabel('lx')
plt.xlabel('age')
```
![Picture](http://garpa.net/assets/images/pyliferisk3.png)

**Example 3:**:
A Life Temporal insurance for a male, 30 years-old and a horizon for 10 years, fixed annual premium (GKM80, interest 6%):
```python
from pyliferisk import *
from pyliferisk.mortalitytables import GKM80

nt = Actuarial(nt=GKM80, i=0.06)
x = 30
n = 10
C = 1000

print(C * (Axn(nt, x, n) / annuity(nt, x, n, 0)))
```

Installation
------------
Once Python is running, just install this library with ``pip install pyliferisk``

Alternatively, install it from source: ``pip install .`` in the repository root.

Requirements
------------
Python >= 3.8.
Pyliferisk has no dependencies other than the Python Standard Library. That decreases the calculation runtime versus implementations under other libraries (such as Pandas).

License
-------
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. The author does not take any legal responsibility for the accuracy, completeness, or usefulness of the information herein.

Contributions
-------------
Contributions, feedback and suggestions for improvements are greatly appreciated.

Discussions take place on our mailing list.

http://groups.google.com/group/openactuarial (subject: pyliferisk)
