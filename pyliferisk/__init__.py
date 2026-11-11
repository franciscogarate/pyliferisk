# -*- coding: utf-8 -*-
#    pyliferisk: A python library for simple actuarial calculations
#    Version: 1.13.0
#    Date: Nov 2026
#    Copyright (C) 2026 Francisco Garate
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numbers
import warnings

__version__ = '1.13.0'

# Mortality table class ----------------

class MortalityTable:
    """Mortality table built from a source table (nt), from lx or from qx.

    Conventions:
    - Probabilities are stored per unit (between 0 and 1): mt.qx[x] is the
      true probability. The source tables (nt) are expressed per mille and
      are converted when loaded; a qx list passed directly must be per unit.
    - Per mille figures are only offered as presentation: view(var='qx').
    - lx starts at 100000 when built from qx.
    - ex is the curtate expectation of life.
    - w (omega) is the last age with lx > 0.
    """
    def __init__(self, lx=None, qx=None, i=None, nt=None, perc=100):
        if i is not None:
            warnings.warn("MortalityTable does not use 'i'; discounting is done by Actuarial",
                          DeprecationWarning, stacklevel=2)
        self.lx = list(lx) if lx is not None else []
        self.qx = list(qx) if qx is not None else []
        if any(not 0 <= q <= 1 for q in self.qx):
            raise ValueError("qx must be expressed per unit (between 0 and 1)")
        self.dx = []
        self.ex = []
        self.w = 0
        self.i = None
        self.perc = perc
        self.nt = nt
        self.Dx = []
        self.Nx = []
        self.Cx = []
        self.Mx = []
        if nt:
            init = nt[0]
            self.qx = [0.0] * init
            for val in nt[1:]:
                q_val = min(val / 1000 * (perc / 100), 1.0)
                self.qx.append(q_val)
                if q_val >= 1.0:
                    break
            if perc != 100 and self.qx[-1] < 1.0:
                self.qx.append(1.0)
        if not self.lx:
            self.lx = [100000.0]
            for val in self.qx:
                self.lx.append(self.lx[-1] * (1 - val))
        if self.lx[-1] != 0.0:
            self.lx.append(0.0)
        if self.w == 0:
            self.w = self.lx.index(0) - 1
        if not self.qx:
            l_x = self.lx[0]
            for l_x1 in self.lx[1:]:
                self.qx.append((l_x - l_x1) / l_x)
                l_x = l_x1
        if not self.dx:
            end_x_lx = self.lx.index(0)
            for age, lx0 in enumerate(self.lx):
                lx1 = min(age + 1, end_x_lx)
                self.dx.append(lx0 - self.lx[lx1])
        if not self.ex:
            for g in range(0, len(self.lx[:-1])):
                lx_g = self.lx[g]
                self.ex.append(sum(self.lx[g + 1:-1]) / lx_g)

    def view(self, start=0, end=10, var='lx'):
        """ Prints the rows from start to end of the variable var.
        Probabilities (qx) are stored per unit and shown here per mille. """
        column = {'qx': self.qx, 'lx': self.lx, 'dx': self.dx, 'ex': self.ex, 'nt': self.nt,
                  'Dx': self.Dx, 'Nx': self.Nx, 'Cx': self.Cx, 'Mx': self.Mx}
        table_str = ''
        index = start
        if var == 'nt':
            subs = 'index'
        else:
            subs = 'x'
        for row in column[var][start:end + 1]:
            if var == 'qx':
                row = round(row * 1000, 9)
            table_str += '[{}={}]  {}={}\n'.format(subs, index, var, row)
            index += 1
        print(table_str + 'Total number of rows for {} = {}'.format(var, len(column[var])))


class Actuarial(MortalityTable):
    """MortalityTable extended with the commutation vectors Dx, Nx, Cx, Mx
    at the effective annual interest rate i."""
    def __init__(self, lx=None, qx=None, nt=None, i=None, perc=100):
        if i is None:
            raise ValueError("Actuarial requires the interest rate 'i'")
        super().__init__(lx=lx, qx=qx, nt=nt, perc=perc)
        self.i = i
        v = 1 / (1 + i)
        for age, lx0 in enumerate(self.lx):
            self.Dx.append((v ** age) * lx0)
        for k in range(0, len(self.Dx)):
            self.Nx.append(sum(self.Dx[k:-1]))
        for age, dx0 in enumerate(self.dx):
            self.Cx.append((v ** (age + 1)) * dx0)
        for k in range(0, len(self.Cx)):
            self.Mx.append(sum(self.Cx[k:-1]))


# Actuarial notation -------------------
def qx(mt, x):
    """ qx: Returns the probability that a life aged x dies before 1 year,
    expressed per unit (between 0 and 1).
    Args:
        mt: the mortality table
        x: the age as integer number.
    """
    if x < len(mt.qx):
        return mt.qx[x]
    else:
        return 0

def lx(mt, x):
    """ lx : Returns the number of survivors at beginning of age x """
    if x < len(mt.lx):
        return mt.lx[x]
    else:
        return 0

def w(mt):
    """ w : omega, the ultimate age (last age with lx > 0) """
    return mt.w

def dx(mt, x):
    """ Returns the number of dying at beginning of age x """
    end_x_val = mt.lx.index(0)
    if x < end_x_val:
        return mt.lx[x] - mt.lx[x + 1]
    else:
        return 0.0

def px(mt, x):
    """ px : Returns the probability of surviving within 1 year,
    expressed per unit (between 0 and 1). """
    return 1 - mt.qx[x]

def tpx(mt, x, t):
    """ tpx : Returns the probability that x will survive within t years,
    expressed per unit (between 0 and 1). """
    return mt.lx[x + t] / mt.lx[x]

def tqx(mt, x, t):
    """ tqx : Returns the probability to die within t years at age x,
    expressed per unit (between 0 and 1). """
    return (mt.lx[x] - mt.lx[x + t]) / mt.lx[x]

def tqxn(mt, x, n, t):
    """ n/tqx : Probability that x survives n years, and then dies in
    the subsequent t years. Expressed per unit (between 0 and 1). """
    return tpx(mt, x, n) * tqx(mt, x + n, t)

def ex(mt, x):
    """ ex : Returns the curtate expectation of life at age x,
    ex = sum(lx[x+1:]) / lx[x]. """
    try:
        return sum(mt.lx[x + 1:-1]) / mt.lx[x]
    except (IndexError, ZeroDivisionError):
        return 0

def mx(mt, x):
    """ mx : Returns the central mortality rate, mx = dx / Lx,
    with Lx approximated as lx - 0.5*dx. Expressed per unit. """
    d = dx(mt, x)
    return d / (mt.lx[x] - 0.5 * d)

# Commutations ------------------

def Dx(mt, x):
    """ Return the Dx """
    return ((1 / (1 + mt.i)) ** x) * mt.lx[x]

def Nx(mt, x):
    """ Return the Nx """
    return sum(mt.Dx[x:-1])

def Sx(mt, x):
    """ Return the Sx """
    return sum(mt.Nx[x:])

def Cx(mt, x):
    """ Return the Cx = v^(x+1) * dx """
    return ((1 / (1 + mt.i)) ** (x + 1)) * mt.dx[x]

def Mx(mt, x):
    """ Return the Mx """
    return sum(mt.Cx[x:-1])

def Rx(mt, x):
    """ Return the Rx """
    return sum(mt.Mx[x:])

# Pure endowment: Deferred capital ---
def nEx(mt, x, n):
    """ nEx : Returns the EPV of a pure endowment (deferred capital).
    Pure endowment benefits are conditional on the survival of the policyholder. (v^n * npx) """
    return mt.Dx[x + n] / mt.Dx[x]

# Actuarial present value

# Whole life insurance ---
def Ax(mt, x):
    """ Ax : Returns the Expected Present Value (EPV) of a whole life insurance (i.e. net single premium).
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value. """
    return mt.Mx[x] / mt.Dx[x]

# Term insurance ---
def Axn(mt, x, n):
    """ (A^1)x:n : Returns the EPV (net single premium) of a term insurance. """
    return (mt.Mx[x] - mt.Mx[x + n]) / mt.Dx[x]

# Endowment insurance ---
def AExn(mt, x, n):
    """ AExn : Returns the EPV of a endowment insurance.
    An endowment insurance provides a combination of a term insurance and a pure endowment
    """
    return (mt.Mx[x] - mt.Mx[x + n]) / mt.Dx[x] + mt.Dx[x + n] / mt.Dx[x]

# Deferred insurance benefits ---
def tAx(mt, x, t):
    """ t/Ax : Returns the EPV (net single premium) of a deferred whole life insurance. """
    return mt.Mx[x + t] / mt.Dx[x]

def tAxn(mt, x, n, t):
    """ t/Axn : Returns the EPV (net single premium) of a deferred term insurance
    (deferred t years, term n years). """
    return (mt.Mx[x + t] - mt.Mx[x + t + n]) / mt.Dx[x]

# IAx  ---
def IAx(mt, x):
    """ This function evaluates the APV of an increasing life insurance. """
    raise NotImplementedError("IAx is not implemented yet")

def IAxn(mt, x, n):
    """ This function evaluates the APV of an increasing life insurance. """
    raise NotImplementedError("IAxn is not implemented yet")

def qAx(mt, x, q):
    """ This function evaluates the APV of a geometrically increasing whole life insurance """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(lx=mt.lx[:], qx=mt.qx[:], i=j)
    return Ax(mtj, x)

def qAxn(mt, x, n, q):
    """ This function evaluates the APV of a geometrically increasing term insurance """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(lx=mt.lx[:], qx=mt.qx[:], i=j)
    return Axn(mtj, x, n)

def qtAx(mt, x, t, q):
    """ This function evaluates the APV of a geometrically increasing deferred whole life insurance """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(lx=mt.lx[:], qx=mt.qx[:], i=j)
    return tAx(mtj, x, t)

def qtAxn(mt, x, t, q):
    raise NotImplementedError("qtAxn is not implemented yet")

# Discrete Life Annuities ------------------

def aaxn(mt, x, n, m=1):
    """ äxn : Return the actuarial present value of a (immediate) temporal (term certain) annuity:
    n-year temporary life annuity-anticipatory. Payable 'm' per year at the beginning of the period
    """
    if m == 1:
        return (mt.Nx[x] - mt.Nx[x + n]) / mt.Dx[x]
    else:
        return (mt.Nx[x] - mt.Nx[x + n]) / mt.Dx[x] - ((float(m - 1) / float(m * 2)) * (1 - nEx(mt, x, n)))

def axn(mt, x, n, m=1):
    """ axn : Return the actuarial present value of a (immediate) temporal (term certain) annuity:
    n-year temporary life annuity-late. Payable 'm' per year at the ends of the period
    """
    if m == 1:
        return (mt.Nx[x + 1] - mt.Nx[x + n + 1]) / mt.Dx[x]
    else:
        return (mt.Nx[x + 1] - mt.Nx[x + n + 1]) / mt.Dx[x] + ((float(m - 1) / float(m * 2)) * (1 - nEx(mt, x, n)))

def aax(mt, x, m=1):
    """ äx : Returns the actuarial present value of an (immediate) annuity of 1 per time period
    (whole life annuity-anticipatory). Payable 'm' per year at the beginning of the period
    """
    return mt.Nx[x] / mt.Dx[x] - (float(m - 1) / float(m * 2))

def ax(mt, x, m=1):
    """ ax : Returns the actuarial present value of an (immediate) annuity of 1 per time period
    (whole life annuity-late). Payable 'm' per year at the ends of the period
    """
    return (mt.Nx[x] / mt.Dx[x] - 1) + (float(m - 1) / float(m * 2))

def taaxn(mt, x, n, t, m=1):
    """ t/äxn : Return the actuarial present value of a deferred temporary annuity
    (deferred t years, term n years), annuity-anticipatory.
    Payable 'm' per year at the beginning of the period
    """
    if m == 1:
        return (mt.Nx[x + t] - mt.Nx[x + t + n]) / mt.Dx[x]
    else:
        return (mt.Nx[x + t] - mt.Nx[x + t + n]) / mt.Dx[x] - \
               ((float(m - 1) / float(m * 2)) * (nEx(mt, x, t) - nEx(mt, x, t + n)))

def taxn(mt, x, n, t, m=1):
    """ t/axn : Return the actuarial present value of a deferred temporary annuity
    (deferred t years, term n years), annuity-late.
    Payable 'm' per year at the ends of the period
    """
    if m == 1:
        return (mt.Nx[x + t + 1] - mt.Nx[x + t + n + 1]) / mt.Dx[x]
    else:
        return (mt.Nx[x + t + 1] - mt.Nx[x + t + n + 1]) / mt.Dx[x] + \
               ((float(m - 1) / float(m * 2)) * (nEx(mt, x, t) - nEx(mt, x, t + n)))

def taax(mt, x, t, m=1):
    """ t/äx : Return the actuarial present value of a deferred annuity (deferred t years):
    t-year deferred whole life annuity-anticipatory. Payable 'm' per year at the beginning of the period
    """
    return mt.Nx[x + t] / mt.Dx[x] - ((float(m - 1) / float(m * 2)) * nEx(mt, x, t))

def tax(mt, x, t, m=1):
    """ t/ax : Return the actuarial present value of a deferred annuity (deferred t years):
    t-year deferred whole life annuity-late. Payable 'm' per year at the ends of the period
    """
    return mt.Nx[x + t + 1] / mt.Dx[x] + ((float(m - 1) / float(m * 2)) * nEx(mt, x, t))


# Arithmetically increasing annuities (unitary) -----------------

def Iaaxn(mt, x, n, *args):
    """ (Iä)x:n : Arithmetically increasing n-year temporary annuity-anticipatory """
    return (Sx(mt, x) - Sx(mt, x + n) - n * Nx(mt, x + n)) / Dx(mt, x)

def Iaxn(mt, x, n, *args):
    """ (Ia)x:n : Arithmetically increasing n-year temporary annuity-late """
    return (Sx(mt, x + 1) - Sx(mt, x + n + 1) - n * Nx(mt, x + n + 1)) / Dx(mt, x)

def Iaax(mt, x, *args):
    """ (Iä)x : Returns the present value of annuity-certain at the beginning of the first year
    and increasing linearly. Arithmetically increasing annuity-anticipatory
    """
    return Sx(mt, x) / Dx(mt, x)

def Iax(mt, x, *args):
    """ (Ia)x : Returns the present value of annuity-certain at the end of the first year
    and increasing linearly. Arithmetically increasing annuity-late
    """
    return Sx(mt, x + 1) / Dx(mt, x)

def Itaax(mt, x, t):
    """ deferred t years, arithmetically increasing annuity-anticipatory """
    return Sx(mt, x + t) / Dx(mt, x)

def Itax(mt, x, t):
    """ deferred t years, arithmetically increasing annuity-late """
    return Sx(mt, x + t + 1) / Dx(mt, x)

# Geometrically increasing annuities ---------------
def qax(mt, x, q, m=1):
    """ Geometrically increasing whole life annuity-late """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(lx=mt.lx[:], qx=mt.qx[:], i=j)
    return ax(mtj, x, m)

def qaax(mt, x, q, m=1):
    """ Geometrically increasing whole life annuity-anticipatory """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(lx=mt.lx[:], qx=mt.qx[:], i=j)
    return aax(mtj, x, m)

def qaxn(mt, x, n, q, m=1):
    """ Geometrically increasing n-year temporary annuity-late """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(lx=mt.lx[:], qx=mt.qx[:], i=j)
    return axn(mtj, x, n, m)

def qaaxn(mt, x, n, q, m=1):
    """ Geometrically increasing n-year temporary annuity-anticipatory """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(lx=mt.lx[:], qx=mt.qx[:], i=j)
    return aaxn(mtj, x, n, m)

def qtax(mt, x, t, q, m=1):
    """ Geometrically increasing deferred whole life annuity-late """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(lx=mt.lx[:], qx=mt.qx[:], i=j)
    return tax(mtj, x, t, m)

def qtaax(mt, x, t, q, m=1):
    """ Geometrically increasing deferred whole life annuity-anticipatory """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(lx=mt.lx[:], qx=mt.qx[:], i=j)
    return taax(mtj, x, t, m)

def qtaaxn(mt, x, n, t, q, m=1):
    """ Geometrically increasing deferred temporary annuity-anticipatory
    (deferred t years, term n years) """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(lx=mt.lx[:], qx=mt.qx[:], i=j)
    return taaxn(mtj, x, n, t, m)

def qtaxn(mt, x, n, t, q, m=1):
    """ Geometrically increasing deferred temporary annuity-late
    (deferred t years, term n years) """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(lx=mt.lx[:], qx=mt.qx[:], i=j)
    return taxn(mtj, x, n, t, m)


# Annuity formula ------------

def annuity(mt, x, n, p, m=1, *args, deferred=0, increase=None):
    """Return the actuarial present value of a life annuity.

    Preferred syntax:
        annuity(mt, x, n, p, m=1, deferred=0, increase=None)
    Args:
        mt = the mortality table (Actuarial instance)
        x = the age as integer number.
        n = An integer number (term of the annuity in years) or 'w' = whole-life.
            (Also, 99 years is defined to be whole-life).
        p = Moment of payment: 0 = beginning of each period (annuity-due),
            1 = end of each period (annuity-immediate).
        m = Payable 'm' per year (fractional payments). Default = 1 (annually)
        deferred = The deferring period in years (keyword argument, default 0).
        increase = None (level annuity), ['g', q] (geometrically increasing at
            rate q) or ['a', q] (arithmetically increasing, unitary).

    Legacy (deprecated) positional syntax is still accepted:
        annuity(mt, x, n, p, m, ['a/g', q], -d)
    where the deferring period is passed as a negative number.
    """
    legacy = list(args)
    if len(legacy) > 2:
        raise TypeError('annuity() takes at most 2 optional positional arguments')
    if isinstance(m, list) or (isinstance(m, numbers.Real) and m < 0):
        legacy.insert(0, m)
        m = 1
    for value in legacy:
        if isinstance(value, list):
            if increase is not None:
                raise ValueError('the increase was given twice')
            increase = value
        else:
            if deferred:
                raise ValueError('the deferring period was given twice')
            deferred = abs(value)
    if legacy:
        warnings.warn("passing the increase and the deferring period positionally is deprecated; "
                      "use annuity(..., deferred=d, increase=['g', q])",
                      DeprecationWarning, stacklevel=2)

    wh_l = isinstance(n, str) or n == 99

    if p == 1:
        post = True
    elif p == 0:
        post = False
    else:
        raise ValueError('payment value (p) must be 0 or 1')

    incr_type = None
    if increase is not None:
        if isinstance(increase, (list, tuple)) and len(increase) == 2 and increase[0] in ('a', 'g'):
            incr_type = increase[0]
            q = increase[1]
        else:
            raise ValueError("increasing value must be ['a', q] or ['g', q]")

    if deferred < 0 or deferred != int(deferred):
        raise ValueError("deferred must be a non-negative integer number of years")
    deferred = int(deferred)
    deff = deferred > 0
    t = deferred

    if incr_type is None:
        if not deff:
            if wh_l:
                return ax(mt, x, m) if post else aax(mt, x, m)
            else:
                return axn(mt, x, n, m) if post else aaxn(mt, x, n, m)
        else:
            if wh_l:
                return tax(mt, x, t, m) if post else taax(mt, x, t, m)
            else:
                return taxn(mt, x, n, t, m) if post else taaxn(mt, x, n, t, m)
    elif incr_type == 'g':
        if not deff:
            if wh_l:
                return qax(mt, x, q, m) if post else qaax(mt, x, q, m)
            else:
                return qaxn(mt, x, n, q, m) if post else qaaxn(mt, x, n, q, m)
        else:
            if wh_l:
                return qtax(mt, x, t, q, m) if post else qtaax(mt, x, t, q, m)
            else:
                return qtaxn(mt, x, n, t, q, m) if post else qtaaxn(mt, x, n, t, q, m)
    else:
        if not deff:
            if wh_l:
                return Iax(mt, x) if post else Iaax(mt, x)
            else:
                return Iaxn(mt, x, n) if post else Iaaxn(mt, x, n)
        else:
            if wh_l:
                return Itax(mt, x, t) if post else Itaax(mt, x, t)
            else:
                raise NotImplementedError('deferred temporary arithmetically increasing '
                                          'annuities are not implemented yet')
