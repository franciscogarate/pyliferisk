#!/usr/bin/python
# -*- coding: utf-8 -*-
#    pyrisk: A python library for simple actuarial calculations
#    Version: 1.2 - July 2014
#    Copyright (C) 2014 Francisco Garate
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

# Mortality table class ----------------

class MortalityTable:
    def __init__(self, l_x=[], q_x=[], nt=None):
        self.lx = l_x
        self.qx = q_x        
        if nt:
            mt = nt[0]
            init = mt[0]
            perc = 100
            if len(nt) == 3:
                perc = nt[2]
            self.qx = [0.0]*init
            end_val = 0
            for val in mt[1:]:
                if end_val < 1000.0:
                    end_val = val*perc/100
                    self.qx.append(end_val)
        if self.lx == []:
            self.lx = [100000.0]
            for val in self.qx:
                self.lx.append(self.lx[-1]*(1-val/1000))
        if self.lx[-1] != 0.0 : self.lx.append(0.0)
        if self.qx == []:
            self.qx = []
            l_x = self.lx[0]
            for l_x1 in self.lx[1:]:
                self.qx.append((l_x-l_x1)*1000/l_x)
                l_x = l_x1

# Actuarial notation -------------------
def qx(mt,x):
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

def lx(mt,x):
    """ lx : Returns the number of survivors at begining of age x """    
    if x < len(mt.lx):
        return mt.lx[x]
    else:
        return 0

def w(mt):
    """ w : ultimate age (lw = 0) """
    return len(mt.lx)

def dx(mt,x):
    """ Returns the number of dying at begining of age x """   
    return lx(mt,x)-lx(mt,x+1)

def px(mt,x):
    """ px : Returns the probability of surviving within 1 year """
    return 1000 - qx(mt,x)

def tpx(mt,x,t):
    """ tqx : Returns the probability that x will survive within t years """
    """ npx : Returns n years survival probability at age x """
    return lx(mt,x+t) / lx(mt,x)

def tqx(mt,x,t):
    """ nqx : Returns the probability to die within n years at age x """
    return (lx(mt,x)-lx(mt,x+t))/lx(mt,x)

def tqxn(mt,x,n,t):
    """ n/qx : Probability to die in n years being alive at age x.
    Probability that x survives n year, and then dies in th subsequent t years """
    return tpx(mt,x,t) * qx(mt,x+n)

def ex(mt,x):
    """ ex : Returns the curtate expectation of life. Life expectancy """
    sum1 = 0
    for j in mt.lx[x+1:]:
        sum1 += j
    try:
        return sum1/lx(mt,x)+0.5
    except:
        return 0

def mx(mt,x):
    """ mx : Returns the central mortality rate """
    return dx(mt,x) / lx(mt,x)

# Commutations ------------------

def Dx(nt,x):
    """ Return the Dx """
    i = float(nt[1])/100
    return ((1/(1+i))**x)*lx(nt,x)

def Nx(nt,x):
    """ Return the Nx """ 
    n = nt[0].index(1000)
    sum1 = 0
    for j in range(x,n):
        k = Dx(nt,j)
        sum1 += k
    return sum1

def Sx(nt,x):
    """ Return the Sx """    
    n = nt[0].index(1000)
    sum1 = 0
    for j in range(x,n):
        k = Nx(nt,j)
        sum1 += k
    return sum1

def Cx(nt,x):
    """ Return the Cx """
    i = float(nt[1])/100    
    return ((1/(1+i))**(x+1))*dx(nt,x)*((1+i)**0.5)

def Mx(nt,x):
    """ Return the Mx """
    n = nt[0].index(1000)-1
    sum1 = 0
    for j in range(x,n):
        k = Cx(nt,j)
        sum1 += k
    return sum1

def Rx(nt,x):
    """ Return the Rx """    
    n = len(nt[0])
    sum1 = 0
    for j in range(x,n):
        k = Mx(nt,j)
        sum1 += k
    return sum1

# Pure endowment: Deferred capital ---
def nEx(nt,x,n):
    """ nEx : Returns the EPV of a pure endowment (deferred capital). 
    Pure endowment benefits are conditional on the survival of the policyholder. (v^n * npx) """
    return Dx(nt,x+n)/Dx(nt,x)

# Actuarial present value

# Whole life insurance ---
def Ax(nt,x):
    """ Ax : Returns the Expected Present Value (EPV) of a whole life insurance (i.e. net single premium).
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value. """
    return Mx(nt,x)/Dx(nt,x)

# Term insurance ---
def Axn(nt,x,n):
    """ (A^1)x:n : Returns the EPV (net single premium) of a term insurance. """
    return (Mx(nt,x)-Mx(nt,x+n))/Dx(nt,x)

# Endowment insurance ---
def AExn(nt,x,n):
    """ AExn : Returns the EPV of a endowment insurance. 
    An endowment insurance provides a combination of a term insurance and a pure endowment """
    return (Mx(nt,x)-Mx(nt,x+n))/Dx(nt,x) + Dx(nt,x+n)/Dx(nt,x)

# Deferred insurance benefits ---
def tAx(nt,x,t):
    """ n/Ax : Returns the EPV (net single premium) of a deferred whole life insurance. """
    return Mx(nt,x+t)/Dx(nt,x)

def tAxn(nt,x,n,t):
    pass

# IAx  ---

def IAx(nt,x):
    """ This function evaluates the APV of an increasing life insurance. """
    pass

def IAxn(nt,x,n):
    """ This function evaluates the APV of an increasing life insurance. """
    pass

def qAx(nt,x,q):
    i = float(nt[1])
    q = float(q)
    return 1/q * Ax([nt[0],(1+i-q)/q],x)

def qAxn(nt,x,n,q):
    i = float(nt[1])
    q = float(q)
    return 1/q * Axn([nt[0],(1+i-q)/q],x,n)

def qtAx(nt,x,t,q):
    i = float(nt[1])
    q = float(q)
    return 1/(q**(t+1)) * tAx([nt[0],(1+i-q)/q],x,t)

def qtAxn(nt,x,t,q):
    pass


# Discrete Life Annuities ------------------

def aaxn(nt,x,n,m=1):
    """ äxn : Return the actuarial present value of a (immediate) temporal (term certain) annuity: n-year temporary life annuity-anticipatory. Payable 'm' per year at the beginning of the period """
    if m == 1:
        return (Nx(nt,x)-Nx(nt,x+n))/Dx(nt,x)
    else:
        return (Nx(nt,x)-Nx(nt,x+n))/Dx(nt,x) - ((float(m-1)/float(m*2)) * (1 - nEx(nt,x,n)))

def axn(nt,x,n,m=1):
    """ axn : Return the actuarial present value of a (immediate) temporal (term certain) annuity: n-year temporary life annuity-late. Payable 'm' per year at the ends of the period """
    if m == 1:
        return (Nx(nt,x+1)-Nx(nt,x+n+1))/Dx(nt,x)
    else:
        return (Nx(nt,x+1)-Nx(nt,x+n+1))/Dx(nt,x) + ((float(m-1)/float(m*2)) * (1 - nEx(nt,x,n)))
        
def aax(nt,x,m=1):
    """ äx : Returns the actuarial present value of an (immediate) annuity of 1 per time period (whole life annuity-anticipatory). Payable 'm' per year at the beginning of the period """
    return Nx(nt,x)/Dx(nt,x) - (float(m-1)/float(m*2))

def ax(nt,x,m=1):
    """ ax : Returns the actuarial present value of an (immediate) annuity of 1 per time period (whole life annuity-late). Payable 'm' per year at the ends of the period """
    return (Nx(nt,x)/Dx(nt,x)-1) + (float(m-1)/float(m*2))

def taaxn(nt,x,n,m=1):
    pass

def taxn(nt,x,n,m=1):
    pass

def taax(nt,x,t,m=1):
    """ n/äx : Return the actuarial present value of a deferred annuity (deferred n years): n-year deferred whole life annuity-anticipatory. Payable 'm' per year at the beginning of the period """
    return Nx(nt,x+t)/Dx(nt,x) - ((float(m-1)/float(m*2)) * (1 - nEx(nt,x,t)))

def tax(nt,x,t,m=1):
    """ n/ax : Return the actuarial present value of a deferred annuity (deferred n years): n-year deferred whole life annuity-late. Payable 'm' per year at the ends of the period """
    return Nx(nt,x+t+1)/Dx(nt,x) + ((float(m-1)/float(m*2)) * (1 - nEx(nt,x,t)))


# Arithmetically increasing annuities (unitary) ----------------- 

def Iaaxn(nt,x,n,*args):
    """ during a term certain, IAn """
    return (Sx(nt,x)-Sx(nt,x+n)-n*Nx(nt,x+n)) / Dx(nt,x)

def Iaxn(nt,x,n,*args):
    """ during a term certain, IAn """
    return (Sx(nt,x+1) - Sx(nt,x+n+1) - n * Nx(nt,x+n+1)) / Dx(nt,x)

def Iaax(nt,x,*args):
    """ (Iä)x : Returns the present value of annuity-certain at the beginning of the first year and increasing linerly. Arithmetically increasing annuity-anticipatory """
    return Sx(nt,x)/Dx(nt,x)

def Iax(nt,x,*args):
    """ (Ia)x : Returns the present value of annuity-certain at the end of the first year and increasing linerly. Arithmetically increasing annuity-late """
    return Sx(nt,x+1) / Dx(nt,x)

def Iaaxn(nt,x,n):
    pass

def Iaxn(nt,x,n):
    pass

def Itaax(nt,x,t):
    """ deffered t years """
    return (Sx(nt,x)-Sx(nt,x+t)) / Dx(nt,x)

def Itax(nt,x,t):
    """ deffered t years """
    return (Sx(nt,x+1) - Sx(nt,x+t+1)) / Dx(nt,x)

# Geometrically increasing annuities ---------------
def qax(nt,x,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    j = (i-q)/(1+q)
    return ax([nt[0],j],x,m)

def qaax(nt,x,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    j = (i-q)/(1+q)
    return aax([nt[0],j],x,m)

def qaxn(nt,x,n,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    return axn([nt[0],(1+i-q)/q],x,n,m)

def qaaxn(nt,x,n,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    return aaxn([nt[0],(i-q)/(1+q)],x,n,m)

def qtax(nt,x,t,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    return tax([nt[0],(1+i-q)/q],x,t) + ((float(m-1)/float(m*2)) * (1 - nEx(nt,x,t)))

def qtaax(nt,x,t,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    return taax([nt[0],(i-q)/(1+q)],x,t) - ((float(m-1)/float(m*2)) * (1 - nEx(nt,x,t)))


# Annuity formula ------------

def annuity(nt,x,n,p,m=1,*args):
    l = len(args)
    post = False
    incr = False
    deff = False
    arit = False
    wh_l = False

    if isinstance(n,basestring) or n == 99:
        wh_l = True
    else:
        pass

    if isinstance(m,int) and m >=0 and l == 0:
        pass

    elif l == 0 and isinstance(m,list):
        args = m
        m = 1
    elif l == 0 and int(m) < 0:
        args = False
        deff = m
        m = 1
    elif l == 1 and isinstance(args[0],int):
        deff = args[0]
        args = False
    elif l == 2:
        if isinstance(args[0],list):
            deff = args[1]
        elif isinstance(args[0],int):
            deff = int(args[0])
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

    if args:
        if 'a' in args[0][0]:
            incr = True
            arit = True
        elif 'g' in args[0][0]:
            incr = True
        else:
            return "Error: increasing value is 'a' or 'g'"
    else:
        pass

    if incr and not arit:
        incr = False
        i = 0.01
    else:
        pass

    if not incr and not deff and not wh_l and not post:
        return aaxn(nt,x,n,m)
    elif not incr and not deff and not wh_l and post:
        return axn(nt,x,n,m)
    elif not incr and not deff and wh_l and not post:
        return aax(nt,x,m)
    elif not incr and not deff and wh_l and post:
        return ax(nt,x,m)
    elif not incr and deff and not wh_l and not post:
        return taaxn(nt,x,n,t,m)
    elif not incr and deff and not wh_l and post:
        return taxn(nt,x,n,t,m)
    elif not incr and deff and wh_l and not post:
        return taax(nt,x,n,t,m)
    elif not incr and deff and wh_l and post:
        return tax(nt,x,t,m)
    elif incr and not deff and not wh_l and not post:
        return Iaaxn(nt,x,n,i)
    elif incr and not deff and not wh_l and post:
        return Iaxn(nt,x,n,i)
    elif incr and not deff and wh_l and not post:
        return Iaax(nt,x,i)    
    elif incr and not deff and wh_l and post:
        return Iax(nt,x,i)
    elif incr and deff and not wh_l and not post:
        return Itaaxn(nt,x,n,t,i)
    elif incr and deff and not wh_l and post:
        return Itaxn(nt,x,n,t,i)
    elif incr and deff and wh_l and not post:
        return Itaax(nt,x,t,i)
    else:
        #elif incr and deff and wh_l and post:
        return Itax(nt,x,t,i)
