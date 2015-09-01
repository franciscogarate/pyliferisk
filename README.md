<h1>pyliferisk</h1>
Pyliferisk is a python library for life actuarial calculations, simple, powerful and easy-to-use.

Date: 2014-07-01<br/>
Version: 1.2<br/>
Author: Francisco Garate - fgaratesantiago (at) gmail (dot) com<br/>
Site: github.com/franciscogarate/pyliferisk<br/>

![Picture](http://www.garpa.net/github/pyliferisk.png)

<!--
http://en.wikipedia.org/wiki/Markdown
http://tmpvar.com/markdown.html
http://docs.readthedocs.org/en/latest/getting_started.html#write-your-docs
-->

<hr>

<h2>Table of contents</h2>

* [Introduction](#introduction)
* [Quick Start](#quick-start)
* [Examples](#examples)
* [Potential uses](#potential-uses)
* [Other libraries](#other-libraries)
* [Installation](#installation)
* [Links](#links)
* [Books](#books)


#<a name="introduction"></a><h2>Introduction</h2>

**Pyliferisk** is an open library written in python for life and actuarial calculation contracts, based on commonly used methodologies among actuaries (International Actuarial Notation).

This library is able to cover all life contingencies risks (since the actuarial formulas follow the International Actuarial Notation), as well as to support the main insurance products:
* Traditional Business
* Term Assurance
* Annuity
* Unit Linked/Universal Life

Additionally, the library can be easily tailored to any particular or local specifications, since Python is a very intuitive language.

It is ideal not only for academic purposes, but also for professional use by actuaries (implementation of premiums and reserves modules) or by auditors (validation of reserves or capital risk models such as parallel runs).

This library is distributed as a single file module (``lifecontingencies.py``) and has no dependencies other than the Python Standard Library.

While pyliferisk library version 1.1 incorporated some useful basic functions to calculate the present value of cash-flows (it does present value calculations of life payment contingent) using fixed or variable discount rates, it has been discontinued from version 1.2 onwards. I highly recommend to use other mathematical libraries (such as SciPy and NumPy) since they are better for this purposes, moreover other potential uses such as random number generation, interpolation, etc. Please, see the section [Other libraries](#other-libraries) to known how to increase the funcionalities (as import results in MS Excel, ESG, C++ integration, etc...)

Additionally, the package includes several life mortality tables (``mortalitytables.py``), mainly extracted from [academic textbooks](#books).

You can find also an example for individual contract (see examples folder), and a collective contract in the following files:

`` tariff-example1.py ``

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. The author does not take any legal responsibility for the accuracy, completeness, or usefulness of the information herein.

<h3>Why Python?</h3>

Because computing plays an important role in the actuarial profession, but actuaries are not programmers. Python is friendly and easy to learn.

Nowadays, programming is becoming an indispensable skill for actuaries. Python is a clear, readable syntax, powerful and fast language. Easy to learn, especially when you are not used to coding. This language lets you write quickly the code you need, without cumbersome rules or variable predefined tasks. It is clear, forget ending with commas and using curly brackets in functions. 
I highly recommend reading the [official introduction to python](http://www.python.org/about/)

#<a name="quick-start"></a><h2>Quick Start</h2>

The names of the formulas follow the International Actuarial Notation and are easily guessable, with a few exceptions regarding special characters (for example, ``A'x`` is replaced by ``AEx``).

The **reserved variables** (in addition of python languages) are the following:

* ``i`` = interest rate. The effective rate of interest, namely, the total interest earned in a year.
* ``nt`` = The actuarial table used to perform life contingencies calculations. Syntax: nt=[GKM95,2] (Note: GKM95 colum must be in mortalitytables.py)
* ``x`` = The age of the insured.
* ``n`` = The horizon (term of insurance) in years or payment duration
* ``m`` = Number of fractional payments per period. If missing, m is set as 0.
* ``d`` = The deferring period in years. 

All the actuarial formulas must include a minimum of 2 variables: nt (mortality table) and x (age) 
If necessary, additional variables should be included with the following order: 
``n`` (horizon in years),  ``m`` (m-monthly payments), ``t`` (n-years deferred period).

Variable ``m`` can be omitted, in this case it will be 1 (annual payment) by default.

<h3>Smart formulas: annuity() and A()</h3>
Additionally, there are two **smart formulas**: annuity() and A(), where the number of variables are not fixed:

``annuity(nt,x,n,p,m,['a/g',c],-d)``

**Specifications**:
This formula is available for increasing annuities (Arithmetically and Geometrically). Syntaxis: It must be include as ['a',c] or ['g',c'] respectively.
* ``n`` = A integer number (term of insurance in years) or 'w' = whole-life. (Also, 99 years is defined to be whole-life).
* ``p`` = Moment of payment. Syntaxis: 0 = begining of each period, 1 = end of each period,
* ``'a'`` = Arithmetical 
* ``'g'`` = Geometrical
* ``c`` = The increase rate. Syntax: ['g',c] or ['a',c]. For example, ['g',0.03]
* ``-d`` = The n-years deferring period as negative number. 

**Example**:
<pre>
annuity(nt,50,10,12,['g',0.02],-15)
</pre>

![Picture](http://garpa.net/github/pyliferisk2.png)

#<a name="examples"></a><h2>Examples</h2>
<pre>
from pyliferisk import annuity

nt=[INE2004,2]
x = 60 # age
n = 15 # term
d = 5  # 5 years deferred

return annuity(nt,x,n,0,-d)
</pre>

#<a name="potential-uses"></a><h2>Potential uses</h2>

Python is used by several well-known banks companies for asset valuations. The exact search on Google for "financial modelling in Python" shows more than 65.000 results.

![Picture](http://garpa.net/github/financial_modelling_python.jpg)

Python is perfect for risk analysis in big data, since is not limited by database size and is able to access libraries for working with any database is very easy(as DB2, Oracle, MSAccess, SQL..). Moreover, [additional libraries](#other-libraries) (such as SciPy and NumPy) can be included in order to increase the functionality, such as random number generation, interpolation, etc.

This library may be used in tariff processes, in the design phase of new products such as profit testing or estimation of future benefits. Other uses include:
- Auditing purposes tool
- Assumption calibrations, back-testing, etc..
- Replicate the main calculations of the internal model for implementation in pricing, product approval, reserving, etc..
- Perform small reports (output format may be xml, xls, etc...)

If you find something that Python cannot do, or if you need the performance advantage of low-level code, you can write or reuse extension modules in C or C++.

**Solvency II and Actuarial Industrialization**: For European actuaries, Solvency II opens a big opportunity. The new requirements transform into agility, transversality and auditability. The internal model is not only software, it should be an internal process used extensively where all parts must walk hand in hand.

In fact, you can find how Python have been easily used by several advisors in order to implement QIS5 requirements.

Take a look at application domains where Python is used: http://www.python.org/about/apps/

#<a name="other-libraries"></a><h2>Other libraries</h2>

Maths or Statistics libraries:

[http://www.scipy.org/](http://www.scipy.org/)
: Scientific Tools for Python

[http://www.numpy.org/](http://www.numpy.org/)
: NumPy is the fundamental package for scientific computing with Python.

[http://matplotlib.sourceforge.net/](http://matplotlib.sourceforge.net/)
: Data visualization and graphics tools. Matplotlib is a python 2D plotting library which produces publication quality figures

[http://code.google.com/p/pymc/](http://code.google.com/p/pymc/)
: Bayesian Stochastic Modelling in Python, particularly using Markov chain Monte Carlo (MCMC), is an increasingly relevant approach to statistical estimation.

[http://statsmodels.sourceforge.net/](http://statsmodels.sourceforge.net/)
: Statistics in Python. scikits.statsmodels is a Python module that provides classes and functions for the estimation of many different statistical models

[http://pandas.pydata.org/](http://pandas.pydata.org/)
: Python Data Analysis Library (http://pandas.sourceforge.net/)

[http://ipython.org/](http://ipython.org/)
: Productive Interactive Computing

[http://cython.org/](http://cython.org/)
: Cython is a language that makes writing C extensions for the Python language as easy as Python itself.

[http://scikits.appspot.com/](http://scikits.appspot.com/)
: SciKits, short for SciPy Toolkits, toolkits that complement SciPy.

**Others:**
http://www.reportlab.com/software/opensource/: The ReportLab Toolkit is open-source engine for creating PDF (Fast-flexible PDF generation)
http://rpy.sourceforge.net/: A simple and efficient access to R from Python
http://pypi.python.org/pypi: PyPI The Python Package Index, is the official repository of software for the Python programming language.

#<a name="installation"></a><h2>Installation</h2>

<h3>Python 2.7 installation</h3>

Python can be used on 21 different operating systems and environments. There are even versions that run on .NET and the Java virtual machine: 
[www.python.org/downloads](https://www.python.org/downloads/)

The Python implementation is under an open source license that makes it freely usable and distributable, even for commercial use. The [Python license](http://www.python.org/psf/license/) is administered by the Python Software Foundation.

<h3>pyliferisk library installation</h3>

Once pyhon is running, just install this library with ``git clone`` or download the source code at github.

```sh
git clone https://github.com/franciscogarate/pyliferisk.git
```

Then, import this library in projects is automatic as usually:

``import pyliferisk``

or, if only like to use specific functions:

``from pyliferisk import annuity``


<h3>Desktop Software IDE </h3>
For beginners, I highly recommended **Sublime Text 2**: [http://www.sublimetext.com/](http://www.sublimetext.com/). Minimal and non-necessary settings. Ideal for testing. Sublime Text uses a custom UI toolkit, optimized for speed and beauty, and may be downloaded and evaluated for free.

Eclipse is an integrated development environment (IDE) recommended especially for python projects with a lot of files. 
**Aptana Studio 3** (based on Eclipse) was used to write and test this library. Both are open-source and multi-platform. Please check the respective tutorials for installation ([http://www.eclipse.org](http://www.eclipse.org) and [http://www.aptana.org](http://www.aptana.org)).

For professional use, Enthought Inc. develops the Canopy platform ([https://www.enthought.com/products/canopy/](https://www.enthought.com/products/canopy/)): a comprehensive Python analysis environment, with financial case studies: Risk calculation for financial analysis ([https://www.enthought.com/services/consulting/case-studies/VaR](https://www.enthought.com/services/consulting/case-studies/VaR)).

Note: Apart of these programs, Python must be installed in the computer.

#<a name="links"></a><h2>Links</h2>

* http://pandas.pydata.org/talks.html
* http://blog.wesmckinney.com/ (author's panda)
* http://ipython.org/presentation.html
* http://www.amazon.com/Financial-Modelling-Python-Finance-Series/dp/0470987847/

#<a name="books"></a><h2>Books</h2>

The author is checking the library with the examples from the following textbooks:
- Actuarial Mathematics for Life Contingent Risks (David C. M. Dickson, Mary R. Hardy and Howard R. Waters) Cambridge University Press, 2009.
- Actuarial Mathematics (2nd Edition), Bowers et al.  Society of Actuaries, 1997.
- Matemática de los Seguros de Vida, (Gil Fana J.A., Heras Matínez A. and Vilar Zanón J.L.) Fundación Mapfre Estudios, 1999.

It will be documented in the examples folder. Contributions are greatly appreciated. 

