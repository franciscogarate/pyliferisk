#!/usr/bin/python
# -*- coding: utf-8 -*-
#    pyrisk: A python library for simple actuarial calculations
#    Version: 0.0.1 - Feb 2014
#    Copyright (C) 2013 Francisco Garate
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

# Actuarial notation -------------------
def qx(nt,x):
    """ qx: Returns the probability that a life aged x dies before 1 year  
    Args:
        x: the age as integer number.
    Raises:
        TypeError: if n is not a number.
        ValueError: if n is negative.
    """
    mt = nt[0]
    init = mt[0]
    perc = 100
    n = nt[0].index(1000)
    if len(nt) == 3:
        perc = nt[2]     
    if x < init:
        return 0
    elif x < n:
        return mt[x-init+1] * perc/100
    else:
        return 0

def lx(nt,x):
    """ lx : Returns the number of survivors at begining of age x """    
    if x==0:
        i = 100000.0
    else:
        i = lx(nt,x-1)*(1-qx(nt,x-1)/1000)
    return i

def w(nt):
    """ w : ultimate age (lw = 0) """
    pass

def dx(nt,x):
    """ Returns the number of dying at begining of age x """   
    return lx(nt,x)-lx(nt,x+1)

def px(nt,x):
    """ px : Returns the probability of surviving within 1 year """
    return 1000 - qx(nt,x)

def tpx(nt,x,t):
    """ tqx : Returns the probability that x will survive within t years """
    """ npx : Returns n years survival probability at age x """
    return (lx(nt,x+t) / lx(nt,x))

def tqx(nt,x,t):
    """ nqx : Returns the probability to die within n years at age x """
    return (lx(nt,x)-lx(nt,x+t))/lx(nt,x)

def tqxn(nt,x,n,t):
    """ n/qx : Probability to die in n years being alive at age x.
    Probability that x survives n year, and then dies in th subsequent t years """
    return tpx(nt,x,t) * qx(nt,x+n)

def ex(nt,x):
    """ ex : Returns the curtate expectation of life. Life expectancy """ 
    n = nt[0].index(1000)
    sum1 = 0
    for j in range(x+1,n):
        k = lx(nt,j)
        sum1 += k
    try:
        sum1/lx(nt,x)+0.5
    except:
        return 0
    else:
        return sum1/lx(nt,x)+0.5

def mx(nt,x):
    """ mx : Returns the central mortality rate """
    return dx(nt,x) / lx(nt,x)

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

# m, Whole life insurance: the 1/mthly case, Ax(m)
# Actuarial present value

# Whole life insurance ---
def Ax(nt,x):
    """ Ax : Returns the Expected Present Value (EPV) of a whole life insurance (i.e. net single premium).
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value. """
    return Mx(nt,x)/Dx(nt,x)

# Term insurance ---
def AAxn(nt,x,n):
    """ (A^1)x:n : Returns the EPV (net single premium) of a term insurance. """
    return (Mx(nt,x)-Mx(nt,x+n))/Dx(nt,x)

# Endowment insurance ---
def Axn(nt,x,n):
    """ Axn : Returns the EPV of a endowment insurance. 
    An endowment insurance provides a combination of a term insurance and a pure endowment """
    return (Mx(nt,x)-Mx(nt,x+n))/Dx(nt,x) + Dx(nt,x+n)/Dx(nt,x)

# Deferred insurance benefits ---
def tAx(nt,x,t):
    """ n/Ax : Returns the EPV (net single premium) of a deferred whole life insurance. """
    return Mx(nt,x+t)/Dx(nt,x)

def tAxn(nt,x,n,t):
    pass

# IAx ---

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

def ActuarialPresentValue():
    pass

# Life annuities ------------------

def ax(nt,x,m=1):
    """ ax : Returns the actuarial present value of an (immediate) annuity of 1 per time period (whole life immediate annuity). Payable 'm' per year at the ends of the period """
    return (Nx(nt,x)/Dx(nt,x)-1) + (float(m-1)/float(m*2))

def aax(nt,x,m=1):
    """ äx : Returns the actuarial present value of an (immediate) annuity of 1 per time period (whole life immediate annuity). Payable 'm' per year at the beginning of the period """
    return Nx(nt,x)/Dx(nt,x) - (float(m-1)/float(m*2))

def axn(nt,x,n,m=1):
    """ axn : Return the actuarial present value of a (immediate) temporal (term certain) annuity. Term immediate annuity. Payable 'm' per year at the ends of the period """
    if m == 1:
        return (Nx(nt,x+1)-Nx(nt,x+n+1))/Dx(nt,x)
    else:
        return (Nx(nt,x+1)-Nx(nt,x+n+1))/Dx(nt,x) + ((float(m-1)/float(m*2)) * (1 - nEx(nt,x,n)))

def aaxn(nt,x,n,m=1):
    """ äxn : Return the actuarial present value of a (immediate) temporal annuity (term certain). Term immediate annuity. Payable 'm' per year at the beginning of the period """
    if m == 1:
        return (Nx(nt,x)-Nx(nt,x+n))/Dx(nt,x)
    else:
        return (Nx(nt,x)-Nx(nt,x+n))/Dx(nt,x) - ((float(m-1)/float(m*2)) * (1 - nEx(nt,x,n)))
         
def tax(nt,x,t,m=1):
    """ n/ax : Return the actuarial present value of a deferred annuity (deferred n years). Payable 'm' per year at the ends of the period """
    return Nx(nt,x+t+1)/Dx(nt,x) + ((float(m-1)/float(m*2)) * (1 - nEx(nt,x,t)))

def taax(nt,x,t,m=1):
    """ n/äx : Return the actuarial present value of a deferred annuity (deferred n years). Payable 'm' per year at the beginning of the period """
    return Nx(nt,x+t)/Dx(nt,x) - ((float(m-1)/float(m*2)) * (1 - nEx(nt,x,t)))

# Arithmetically increasing annuities (unitary) ----------------- 
def Iaax(nt,x,*args):
    """ (Iä)x : Returns the present value of annuity-certain at the beginning of the first year and increasing linerly """
    return Sx(nt,x)/Dx(nt,x)

def Iax(nt,x,*args):
    """ (Ia)x : Returns the present value of annuity-certain at the end of the first year and increasing linerly """
    return Sx(nt,x+1) / Dx(nt,x)

def Iaaxn(nt,x,n,*args):
    """ during a term certain, IAn """
    return (Sx(nt,x)-Sx(nt,x+n)-n*Nx(nt,x+n)) / Dx(nt,x)

def Iaxn(nt,x,n,*args):
    """ during a term certain, IAn """
    return (Sx(nt,x+1) - Sx(nt,x+n+1) - n * Nx(nt,x+n+1)) / Dx(nt,x)

def Itaax(nt,x,t):
    """ deffered t years """
    return (Sx(nt,x)-Sx(nt,x+t)) / Dx(nt,x)

def Itax(nt,x,t):
    """ deffered t years """
    return (Sx(nt,x+1) - Sx(nt,x+t+1)) / Dx(nt,x)

# Geometrically increasing annuities ---------------

def qaax(nt,x,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    return aax([nt[0],(i-q)/(1+q)],x,m)

def qaax2(nt,x,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    return aax([nt[0],(1+i-q)/q],x,m)

def qax(nt,x,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    return ax([nt[0],(1+i-q)/q],x,m)

def qaaxn(nt,x,n,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    return aaxn([nt[0],(i-q)/(1+q)],x,n,m)

def qaaxn2(nt,x,n,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    return aaxn([nt[0],(1+i-q)/q],x,n,m)

def qaxn(nt,x,n,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    return axn([nt[0],(1+i-q)/q],x,n,m)

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

def qtaax2(nt,x,t,q,m=1):
    """ geometrica """
    i = float(nt[1])
    q = float(q)
    return taax([nt[0],(1+i-q)/q],x,t) - ((float(m-1)/float(m*2)) * (1 - nEx(nt,x,t)))

# Annuity formula ------------

def annuity(nt,x,n,p,m=1,*args):
    """ Payable 'm' per year """
    # ax(nt,x,n,0/1,m=1,*c,a/g,-d)
    l = len(args)
    deff = post = False
    if p == 1:
        post = True
    elif p == 0:
        pass
    else:
        print 'Error: payment value is 0 or 1' 
    if m < 0:
        deff = True
        t = -m
        m = 1
    else:
        pass
    if args:
        if isinstance(args[-1],basestring):
            pass
        else:
            try:
                print args[-1] **(0.5)
            except:
                deff = True
                #m = 1
                t = -args[-1]
            else:
                pass
    else:
        pass

    if deff:
        if post:
            return tax(nt,x,t,m)
        else:
            return taax(nt,x,t,m)
    
    if 'a' in args:
        if l == 2:
            c = args[0]
        else:
            c = m
            m = 1
        print 'arit lineal al' , c, "m es", m
        #Iaaxn(nt,x,n,*args)
        return Iaaxn(nt,x,n,c)  
    elif 'g' in args:
        if l == 2:
            c = args[0]
        else:
            c = m
            m = 1
        #print 'geo al' , c, "m es", m
        if post:
            return qaxn(nt,x,n,c,m)
        else:
            return qaaxn(nt,x,n,c,m)
    else:
        c = 0
        #print 'lineal al' , c, "m es", m
        if post:
            return axn(nt,x,n,m)
        else:
            return aaxn(nt,x,n,m)
