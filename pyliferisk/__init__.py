#!/usr/bin/python
# -*- coding: utf-8 -*-
#    pyliferisk: A python library for simple actuarial calculations
#    Version: 1.10 - Dec 2018
#    Copyright (C) 2018 Francisco Garate
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
from .mortalitytables import *

# Mortality table class ----------------

class MortalityTable:
    def __init__(self, l_x=[], q_x=[], i=[], nt=None, perc=100):
        self.lx = l_x
        self.qx = q_x
        self.dx = []
        self.ex = []
        self.w = 0
        self.i = i 
        self.q = 0        
        self.perc = perc
        self.nt = nt
        self.Dx = []
        self.Nx = []
        self.Cx = []
        self.Mx = []
        self.nEx = []
        if nt:
            mt = nt
            init = mt[0]
            self.qx = [0.0] * init
            end_val = 0
            for val in mt[1:]:
                if end_val < 1000.0:
                    end_val = val * perc / 100
                    self.qx.append(end_val)
            if perc != 100:
                self.qx.append(1000)
        if self.lx == []:
            self.lx = [100000.0]
            for val in self.qx:
                self.lx.append(self.lx[-1] * (1 - val / 1000))
        if self.lx[-1] != 0.0 : 
            self.lx.append(0.0)
        if self.w == 0 : 
            self.w = self.lx.index(0) - 1
        if self.qx == []:
            #self.qx = []
            l_x = self.lx[0]
            for l_x1 in self.lx[1:]:
                self.qx.append((l_x - l_x1) * 1000 / l_x)
                l_x = l_x1
        if self.dx == []:
            dx_0 = -1
            end_x_lx = self.lx.index(0)
            for lx0 in self.lx:
                dx_0 += 1
                lx1 = min(dx_0 + 1, end_x_lx)
                self.dx.append(lx0 - self.lx[lx1])
        if self.ex == []:
            for g in range(0, len(self.lx[:-1])):
                lx_g = self.lx[g]
                self.ex.append(0.5 + sum(self.lx[g + 1:-1]) / lx_g) #[g+1:-2] according notes from ucm

    def view(self, start=0, end=10, var='lx'):
        column  = {'qx': self.qx, 'lx': self.lx, 'dx': self.dx, 'ex': self.ex, 'nt': self.nt, \
                   'Dx': self.Dx, 'Nx': self.Nx, 'Cx': self.Cx, 'Mx': self.Mx, 'nEx': self.nEx}
        table_str = ''
        index = start
        if var == 'nt':
            subs = 'index'
        else:
            subs = 'x'
        for i in column[var][start:end + 1]:
            table_str += '[{}={}]  {}={}\n'.format(subs, index, var, i)
            index += 1
        print(table_str + 'Total number of rows for {} = {}'.format(var, len(column[var])))

        
class Actuarial:
    def __init__(self, l_x=[], q_x=[], nt=None, i=None, perc=100):
        self.lx = l_x
        self.qx = q_x
        self.dx = []
        self.ex = []
        self.w = 0
        self.i = i 
        self.q = 0        
        self.perc = perc
        self.nt = nt
        self.Dx = []
        self.Nx = []
        self.Cx = []
        self.Mx = []
        self.nEx = []
        if nt:
            mt = nt
            init = mt[0]
            self.qx = [0.0] * init
            end_val = 0
            for val in mt[1:]:
                if end_val < 1000.0:
                    end_val = val * perc / 100
                    self.qx.append(end_val)
            if perc != 100:
                self.qx.append(1000)
        if self.lx == []:
            self.lx = [100000.0]
            for val in self.qx:
                self.lx.append(self.lx[-1] * ( 1 - val / 1000))
        if self.lx[-1] != 0.0 : 
            self.lx.append(0.0)
        if self.w == 0 : 
            self.w = self.lx.index(0) - 1
        if self.qx == []:
            #self.qx = []
            l_x = self.lx[0]
            for l_x1 in self.lx[1:]:
                self.qx.append((l_x - l_x1) * 1000 / l_x)
                l_x = l_x1
        if self.dx == []:
            dx_0 = -1
            end_x_lx = self.lx.index(0)
            for lx0 in self.lx:
                dx_0 += 1
                lx1 = min(dx_0 + 1, end_x_lx)
                self.dx.append(lx0 - self.lx[lx1])
        if self.ex == []:
            for g in range(0, len(self.lx[:-1])):
                lx_g = self.lx[g]
                self.ex.append(0.5 + sum(self.lx[g + 1:-1]) / lx_g) #[g+1:-2] according notes from ucm
        if self.Dx == []:
            #self.Dx = []
            age = -1
            for j in self.lx:
                age+=1
                self.Dx.append(((1 / (1 + i)) ** age) * j)
        if self.Nx == []:
            #self.Nx = []
            for k in range(0, len(self.Dx)):
                self.Nx.append(sum(self.Dx[k:-1])) #[k:-2] according notes from ucm
        if self.Cx == []:
            #self.Cx = []
            age = -1
            for l in self.dx:   #[:-1]
                age += 1
                C_x = ((1 / (1 + i)) ** (age + 1))*l*((1 + i)**0.5)
                self.Cx.append(C_x)
        if self.Mx == []:
            #self.Mx = []
            for m in range(0, len(self.Cx)):
                self.Mx.append(sum(self.Cx[m:-1])) # [m:-2] according notes from ucm

    def view(self, start = 0, end = 10, var = 'lx'):
        column  = {'qx': self.qx, 'lx': self.lx, 'dx': self.dx, 'ex': self.ex, 'nt': self.nt, \
                   'Dx': self.Dx, 'Nx': self.Nx, 'Cx': self.Cx, 'Mx': self.Mx, 'nEx': self.nEx}
        table_str = ''
        index = start
        if var == 'nt':
            subs = 'index'
        else:
            subs = 'x'
        for i in column[var][start:end + 1]:
            table_str += '[{}={}]  {}={}\n'.format(subs, index, var, i)
            index += 1
        print(table_str + 'Total number of rows for {} = {}'.format(var, len(column[var])))

   
# Actuarial notation -------------------
def qx(mt, x):
    """ qx: Returns the probability that a life aged x dies before 1 year
            With the convention: the true probability is qx/1000
    Args:
        mt: the mortality table
        x: the age as integer number.
    """
    if x < len(mt.qx):
        return mt.qx[x]
    else:
        return 0

def lx(mt, x):
    """ lx : Returns the number of survivors at begining of age x """    
    if x < len(mt.lx):
        return mt.lx[x]
    else:
        return 0

def w(mt):
    """ w : ultimate age (lw = 0) """
    return len(mt.lx)

def dx(mt, x):
    """ Returns the number of dying at begining of age x """ 
    end_x_val = mt.lx.index(0)
    if x < end_x_val:  
        return mt.lx[x] - mt.lx[x + 1]
    else:
        return 0.0

def px(mt, x):
    """ px : Returns the probability of surviving within 1 year """
    return 1000 - mt.qx[x]

def tpx(mt, x, t):
    """ tpx : Returns the probability that x will survive within t years """
    """ npx : Returns n years survival probability at age x """
    return mt.lx[x + t] / mt.lx[x]

def tqx(mt, x, t):
    """ nqx : Returns the probability to die within n years at age x """
    return (mt.lx[x] - mt.lx[x + t]) / mt.lx[x]

def tqxn(mt, x, n, t):
    """ n/qx : Probability to die in n years being alive at age x.
    Probability that x survives n year, and then dies in th subsequent t years """
    return tpx(mt, x, t) * qx(mt, x + n)

def ex(mt, x):
    """ ex : Returns the curtate expectation of life. Life expectancy """
    sum1 = 0
    for j in mt.lx[x + 1:-1]:
        sum1 += j
        #print sum1
    try:
        return sum1 / mt.lx[x] + 0.5
    except:
        return 0

def mx(mt, x):
    """ mx : Returns the central mortality rate """
    return dx(mt, x) / mt.lx[x]

# Commutations ------------------

def Dx(mt, x):
    """ Return the Dx """
    return ((1 / (1 + mt.i)) ** x) * mt.lx[x]

def Nx(mt, x):
    """ Return the Nx """ 
    n = len(mt.Dx)
    sum1 = 0
    for j in range(x, n):
        k = mt.Dx[j]
        sum1 += k
    return sum1

def Sx(mt, x):
    """ Return the Sx """    
    n = len(mt.Nx)
    sum1 = 0
    for j in range(x, n):
        k = mt.Nx[j]
        sum1 += k
    return sum1

def Cx(mt, x):
    """ Return the Cx """   
    return ((1 / (1 + mt.i)) ** (x + 1)) * mt.dx[x] * ((1 + mt.i) ** 0.5)

def Mx(mt, x):
    """ Return the Mx """
    n = len(mt.Cx)
    sum1 = 0
    for j in range(x, n):
        k = mt.Cx[j]
        sum1 += k
    return sum1

def Rx(mt, x):
    """ Return the Rx """    
    n = len(mt.Mx)
    sum1 = 0
    for j in range(x, n):
        k = mt.Mx[j]
        sum1 += k
    return sum1

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
    """ n/Ax : Returns the EPV (net single premium) of a deferred whole life insurance. """
    return mt.Mx[x + t] / mt.Dx[x]

def tAxn(mt, x, n, t):
    pass

# IAx  ---
def IAx(mt, x):
    """ This function evaluates the APV of an increasing life insurance. """
    pass

def IAxn(mt, x, n):
    """ This function evaluates the APV of an increasing life insurance. """
    pass

def qAx(mt, x, q):
    """ This function evaluates the APV of a geometrically increasing annual annuity-due """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(nt=mt.nt, i=j)
    return Ax(mtj, x)

def qAxn(nt, x, n, q):
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(nt=mt.nt, i=j)
    return Axn(mtj, x, n)

def qtAx(nt, x, t, q):
    q = float(q)
    j = (mt.i - q) / (1 + q) #j = (i-q)/(1+q)
    mtj = Actuarial(nt=mt.nt, i=j)
    return tAx(mtj, x, t)

def qtAxn(nt, x, t, q):
    pass

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

def taaxn(mt, x, n, m=1):
    pass

def taxn(mt, x, n, m=1):
    pass

def taax(mt, x, t, m=1):
    """ n/äx : Return the actuarial present value of a deferred annuity (deferred n years): 
    n-year deferred whole life annuity-anticipatory. Payable 'm' per year at the beginning of the period 
    """
    return mt.Nx[x + t] / mt.Dx[x] - ((float(m - 1) / float(m * 2)) * (1 - nEx(mt, x, t)))

def tax(mt, x, t, m=1):
    """ n/ax : Return the actuarial present value of a deferred annuity (deferred n years): 
    n-year deferred whole life annuity-late. Payable 'm' per year at the ends of the period 
    """
    return mt.Nx[x + t + 1] / mt.Dx[x] + ((float(m - 1) / float(m * 2)) * (1 - nEx(mt, x, t)))


# Arithmetically increasing annuities (unitary) ----------------- 

def Iaaxn(mt, x, n, *args):
    """ during a term certain, IAn """
    return (Sx(mt, x) - Sx(nt, x + n) - n * Nx(nt, x + n)) / Dx(nt, x)

def Iaxn(mt, x, n, *args):
    """ during a term certain, IAn """
    return (Sx(mt, x + 1) - Sx(mt, x + n + 1) - n * Nx(mt, x + n + 1)) / Dx(mt, x)

def Iaax(mt, x, *args):
    """ (Iä)x : Returns the present value of annuity-certain at the beginning of the first year 
    and increasing linerly. Arithmetically increasing annuity-anticipatory 
    """
    return Sx(mt, x) / Dx(mt, x)

def Iax(mt, x, *args):
    """ (Ia)x : Returns the present value of annuity-certain at the end of the first year 
    and increasing linerly. Arithmetically increasing annuity-late 
    """
    return Sx(mt, x + 1) / Dx(mt, x)

def Iaaxn(mt, x, n):
    pass

def Iaxn(mt, x, n):
    pass

def Itaax(mt, x, t):
    """ deffered t years """
    return (Sx(mt, x) - Sx(mt, x + t)) / Dx(mt, x)

def Itax(mt, x, t):
    """ deffered t years """
    return (Sx(mt, x + 1) - Sx(mt, x + t + 1)) / Dx(mt, x)

# Geometrically increasing annuities ---------------
def qax(mt, x, q, m=1):
    """ geometrica """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(nt=mt.nt, i=j)
    return ax(mtj, x, m)

def qaax(mt, x, q, m=1):
    """ geometrica """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(nt=mt.nt, i=j)
    return aax(mtj, x, m)

def qaxn(mt, x, n, q, m=1):
    """ geometrica """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(nt=mt.nt, i=j)
    return axn(mtj, x, n, m)

def qaaxn(mt, x, n, q, m = 1):
    """ geometrica """
    #i = float(nt[1])
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(nt=mt.nt, i=j)
    return aaxn(mtj, x, n, m)

def qtax(mt, x, t, q, m=1):
    """ geometrica """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(nt=mt.nt, i=j)
    return tax(mtj, x, t) + ((float(m - 1) / float(m * 2)) * (1 - nEx(mt, x, t)))

def qtaax(mt, x, t, q, m=1):
    """ geometrica """
    q = float(q)
    j = (mt.i - q) / (1 + q)
    mtj = Actuarial(nt=mt.nt, i=j)
    return taax(mtj, x, t) - ((float(m - 1) / float(m * 2)) * (1 - nEx(mt, x, t)))


# Annuity formula ------------

def annuity(mt, x, n, p, m=1 , *args):
    """Syntax: annuity(nt, x, n, p, m, ['a/g', q], -d)
    Args:
        mt = the mortality table
        x = the age as integer number.   
        n = A integer number (term of insurance in years) or 'w' = whole-life. 
            (Also, 99 years is defined to be whole-life).
        p = Moment of payment. Syntaxis: 0 = begining of each period (prepaid), 1 = end of each period (postpaid),
    Optional variables:
        m = Payable 'm' per year (frational payments). Default = 1 (annually)
        a or g = a: Arithmetical / g: Geometrical
        q = The increase rate. Syntax: ['g',q] or ['a',q]. For example, ['g',0.03]
    Deferring period:
        -d = The n-years deferring period as negative number. 
    """
    l = len(args)
    post = False
    incr = False
    deff = False
    arit = False
    wh_l = False

    if isinstance(n,str) or n == 99:
        wh_l = True
    else:
        pass

    if isinstance(m,int) and m >=0 and l == 0: 
        pass
    elif l == 0 and isinstance(m,list):  
        args = (m,)
        m = 1
        incr = True
    elif l == 0 and int(m) < 0:
        args = False
        deff = True
        t = int(m) * -1
        m = 1
    elif l == 1:
        if isinstance(args[0], list):
            incr = True
        elif isinstance(args[0], int):
            if isinstance(m, list):
                deff = True
                incr = True
                t = int(args[0]) * -1
                args = (m, )
                m = 1
            else:
                deff = True
                t = int(args[0]) * -1
                args = False
        else:
            pass
    elif l == 2:        
        if isinstance(args[0], list):
            deff = True
            t = int(args[1]) * -1
            incr = True
        elif isinstance(args[0], int):
            deff = True
            t = int(args[0]) * -1
            args = args[1]
        else:
            pass
    else:        
        pass
    
    if p == 1:
        post = True
    elif p == 0:
        pass
    else:
        print('Error: payment value is 0 or 1')

    if incr:
        if 'a' in args[0]:
            arit = True
            incr = False
        elif 'g' in args[0]:
            incr = True
            q = args[0][1]
        else:
            return "Error: increasing value is 'a' or 'g'"

    else:
        pass

    if not incr and not deff and not wh_l and not post:
        return aaxn(mt, x, n, m)
    elif not incr and not deff and not wh_l and post:
        return axn(mt, x, n, m)
    elif not incr and not deff and wh_l and not post:
        return aax(mt, x, m)
    elif not incr and not deff and wh_l and post:
        return ax(mt, x, m)
    elif not incr and deff and not wh_l and not post:
        return taaxn(mt, x, n, t, m)
    elif not incr and deff and not wh_l and post:
        return taxn(mt, x, n, t, m)
    elif not incr and deff and wh_l and not post:
        return taax(mt, x, t, m)
    elif not incr and deff and wh_l and post:
        return tax(mt, x, t, m)
    elif incr and not deff and not wh_l and not post:
        return qaaxn(mt, x, n, q, m)
    elif incr and not deff and not wh_l and post:
        return qaxn(mt, x, n, q, m)
    elif incr and not deff and wh_l and not post:
        return qaax(mt, x, q, m)    
    elif incr and not deff and wh_l and post:
        return qax(mt, x, q, m)
    elif incr and deff and not wh_l and not post:
        return qtaaxn(mt, x, n, t, q, m)
    elif incr and deff and not wh_l and post:
        return qtaxn(mt, x, n, t, q, m)
    elif incr and deff and wh_l and not post:
        return qtaax(mt, x, t, q, m)
    else:
        #elif incr and deff and wh_l and post:
        return Itax(mt, x, t)