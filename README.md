<h1>pyliferisk</h1>
Pyliferisk is a python library for life actuarial calculations, simple, powerful and easy-to-use.

Date: 2017-05-22<br/>
Version: 1.9<br/>
Author: Francisco Garate - fgaratesantiago (at) gmail (dot) com<br/>
Site: github.com/franciscogarate/pyliferisk<br/>
Documentation: [documentation.pdf](https://github.com/franciscogarate/pyliferisk/raw/master/documentation.pdf)

![Picture](http://www.garpa.net/github/pyliferisk.png)

<!--
https://help.github.com/categories/writing-on-github/
-->

<hr>

<h2>Table of contents</h2>

* [Introduction](#introduction)
* [Quick Start](#quick-start)
* [Examples](#examples)
* [Installation](#installation)
* [Books](#books)


<a name="introduction"></a><h2>Introduction</h2>

**Pyliferisk** is an open library written in python for life and actuarial calculation contracts, based on commonly used methodologies among actuaries (International Actuarial Notation).

This library is able to cover all life contingencies risks (since the actuarial formulas follow the International Actuarial Notation), as well as to support the main insurance products.

Additionally, the library can be easily tailored to any particular or local specifications, since Python is a very intuitive language. It is ideal not only for academic purposes, but also for professional use by actuaries (implementation of premiums and reserves modules) or by auditors (validation of reserves or capital risk models such as parallel runs).

This library is distributed as a single file module (``lifecontingencies.py``) and has no dependencies other than the Python Standard Library.

Additionally, the package includes several life mortality tables (``mortalitytables.py``), mainly extracted from [academic textbooks](#books).

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. The author does not take any legal responsibility for the accuracy, completeness, or usefulness of the information herein.

<a name="quick-start"></a><h2>Quick Start</h2>

The names of the formulas follow the International Actuarial Notation and are easily guessable, with a few exceptions regarding special characters (for example, ``A'x`` is replaced by ``AEx``).

The **reserved variables** (in addition of python languages) are the following:

For the mortality table:
* ``nt`` = The actuarial table used to perform life contingencies calculations. Syntax: nt=GKM95 (Note: GKM95 must be included in mortalitytables.py)
* ``i`` = interest rate. The effective rate of interest, namely, the total interest earned in a year. Syntax: i=0.02
* ``perc`` = Optional variable to indicate the percentage of mortality to be applied. Syntax: perc=85
Variable ``perc`` can be omitted, in this case it will be 100 by default.

For actuarial formulas:
* ``x`` = The age of the insured.
* ``n`` = The horizon (term of insurance) in years or payment duration
* ``m`` = Number of fractional payments per period. If missing, m is set as 0.
* ``d`` = The deferring period in years.

The mortality table must be defined with the class ``MortalityTable()``. Example:

```python
import pyliferisk.lifecontingencies as lc
from pyliferisk.mortalitytables import SPAININE2004

tariff=lc.MortalityTable(nt=SPAININE2004)
experience=lc.MortalityTable(nt=SPAININE2004,perc=85)

# Print the omega (limiting age) of the both mortality tables:
print(tariff.w)
print(experience.w)

# Print the qx at 50 years old:
print(tariff.qx[50])
print(experience.qx[50])
```

Example 2:

```python
import matplotlib.pyplot as plt
import pyliferisk.lifecontingencies as lc
from pyliferisk.mortalitytables import SPAININE2004, GKM95
import numpy as np
tarifa=lc.MortalityTable(nt=SPAININE2004)
experiencia=lc.MortalityTable(nt=GKM95,perc=75)
x = np.arange(tarifa.w)
y = tarifa.lx[:tarifa.w]
z = experiencia.lx[:tarifa.w]
plt.plot(x,y, color = 'blue')
plt.plot(x,z, color = 'red')
plt.ylabel('lx')
plt.xlabel('edad')
```
![Picture](http://garpa.net/github/pyliferisk3.png)

Also, 

All the actuarial formulas must include a minimum of 2 variables: mt (mortality table) and x (age) 
If necessary, additional variables should be included with the following order: 
``n`` (horizon in years),  ``m`` (m-monthly payments), ``t`` (n-years deferred period).

Variable ``m`` can be omitted, in this case it will be 1 (annual payment) by default.

<h3>Smart formulas: annuity() and A()</h3>
Additionally, there are two **smart formulas**: annuity() and A(), where the number of variables are not fixed:

``annuity(nt,x,n,p,m,['a/g',c],-d)``

**Specifications**:
This formula is available for increasing annuities (Arithmetically and Geometrically). Syntaxis: It must be include as ['a',c] or ['g',c'] respectively.
* ``n`` = A integer number (term of insurance in years) or 'w' = whole-life. (Also, 99 years is defined to be whole-life).
* ``p`` = Moment of payment. Syntaxis: 0 = begining of each period (prepaid), 1 = end of each period (postpaid),
* ``'a'`` = Arithmetical 
* ``'g'`` = Geometrical
* ``c`` = The increase rate. Syntax: ['g',c] or ['a',c]. For example, ['g',0.03]
* ``-d`` = The n-years deferring period as negative number. 

**Example**:
```python
mt=Actuarial(nt=SPAININE2004,i=0.02)
annuity(mt,50,10,12,['g',0.03],-15)
```

![Picture](http://garpa.net/github/pyliferisk2.png)

<a name="examples"></a><h2>Examples</h2>
```python
mt=lc.Actuarial(nt=SPAININE2004,i=0.02)
x = 60 # age
n = 15 # term
d = 5  # 5 years deferred

return lc.annuity(mt,x,n,0,-d)
```

<h3>Installation</h3>

Once pyhon is running, just install this library with ``pip install pyliferisk`` or download the source code at github (git clone).

```sh
pip install pyliferisk
```

Then, import this library in projects is automatic as usually:

```python
import pyliferisk.lifecontingencies as lc
```

or, if only like to use specific functions:

```python
from pyliferisk.mortalitytables import SPAININE2004
```

<a name="books"></a><h2>Books</h2>

The author is checking the library with the examples from the following textbooks:
- Actuarial Mathematics for Life Contingent Risks (David C. M. Dickson, Mary R. Hardy and Howard R. Waters) Cambridge University Press, 2009.
- Actuarial Mathematics (2nd Edition), Bowers et al.  Society of Actuaries, 1997.
- Matemática de los Seguros de Vida, (Gil Fana J.A., Heras Matínez A. and Vilar Zanón J.L.) Fundación Mapfre Estudios, 1999.

Contributions are greatly appreciated. 
