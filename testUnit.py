#!/usr/bin/python
# -*- coding: utf-8 -*-
#    pyrisk: A python library for simple actuarial calculations
#    Version: 2.0 - December 2016
#    Copyright (C) 2016 Francisco Garate, Florian Pons
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


import unittest
import lifecontingencies as lc
import mortalitytables



class TestActuarialMethods(unittest.TestCase):
    
    def setUp(self):
        self.H_gen_1961_mt = mortalitytables.get_TGHF05('H')['1961']
        self.F_gen_1963_mt = mortalitytables.get_TGHF05('F')['1963']
        self.pers_H_1961 = lc.Pers(self.H_gen_1961_mt)
        self.pers_F_1963 = lc.Pers(self.F_gen_1963_mt)
        self.pers_H_F = lc.Pers([self.H_gen_1961_mt,self.F_gen_1963_mt], [-1961,-1963])
        
        self.Act_H_1961 = lc.Actuarial(0.05, self.pers_H_1961)
        self.Act_F_1963 = lc.Actuarial(0.05, self.pers_F_1963)
        self.Act_H_F = lc.Actuarial(0.05, self.pers_H_F)
    
    def test_ax(self):
        ax = self.Act_H_1961.ax(61,m=4)
        self.assertEqual(ax, 14.88478298)
    
    def test_axy(self):
        axy = self.Act_H_F.ax(61,m=4)
        self.assertEqual(axy, 14.40246915)

if __name__ == '__main__':
    unittest.main()
