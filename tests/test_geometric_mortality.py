"""Geometric revaluation must change interest, not the mortality assumptions."""
import copy
import math
import unittest

import pyliferisk as pl
from pyliferisk.mortalitytables import GKM95


class GeometricMortalityTests(unittest.TestCase):
    def tables(self):
        for perc in (50, 75, 100):
            yield pl.Actuarial(nt=GKM95, i=0.03, perc=perc), 60
        yield pl.Actuarial(lx=[100000., 97000., 90000., 80000., 60000., 30000., 0.], qx=[], i=.03), 1
        yield pl.Actuarial(qx=[30., 70., 120., 200., 400., 1000.], lx=[], i=.03), 1

    def test_zero_growth_matches_level_annuity(self):
        for mt, age in self.tables():
            for m in (1, 2, 4, 12):
                for growing, level, args in ((pl.qax, pl.ax, ()), (pl.qaax, pl.aax, ()),
                                              (pl.qaxn, pl.axn, (2,)), (pl.qaaxn, pl.aaxn, (2,))):
                    with self.subTest(age=age, perc=mt.perc, function=growing.__name__, m=m):
                        self.assertAlmostEqual(growing(mt, age, *args, 0., m), level(mt, age, *args, m), places=11)

    def test_annual_cashflows_and_insurance(self):
        for mt, age in self.tables():
            for growth in (-.01, 0., .02):
                ratio = (1 + growth) / (1 + mt.i)
                def cash(start, stop):
                    return math.fsum(mt.lx[age+k] / mt.lx[age] * ratio**k for k in range(start, stop))
                end = len(mt.lx) - age
                controls = ((pl.qax(mt, age, growth), cash(1, end)),
                            (pl.qaax(mt, age, growth), cash(0, end)),
                            (pl.qaxn(mt, age, 2, growth), cash(1, 3)),
                            (pl.qaaxn(mt, age, 2, growth), cash(0, 2)),
                            (pl.qtax(mt, age, 2, growth), cash(3, end)),
                            (pl.qtaax(mt, age, 2, growth), cash(2, end)),
                            (pl.qAx(mt, age, growth), math.fsum(
                                (mt.lx[age+k] - mt.lx[age+k+1]) / mt.lx[age] * ratio**(k+1)
                                for k in range(end-1))))
                for actual, expected in controls:
                    with self.subTest(age=age, perc=mt.perc, growth=growth, expected=expected):
                        self.assertAlmostEqual(actual, expected, places=11)

    def test_dispatch_preserves_mortality(self):
        for mt, age in self.tables():
            for n in (2, 'w'):
                for payment in (0, 1):
                    with self.subTest(age=age, n=n, payment=payment):
                        self.assertAlmostEqual(pl.annuity(mt, age, n, payment, 1, ['g', 0.]),
                                               pl.annuity(mt, age, n, payment), places=11)

    def test_caller_table_is_unchanged(self):
        for mt, age in self.tables():
            before = copy.deepcopy(mt.__dict__)
            pl.qax(mt, age, .02)
            pl.qaaxn(mt, age, 2, -.01)
            pl.qAx(mt, age, 0.)
            self.assertEqual(mt.__dict__, before)


if __name__ == '__main__':
    unittest.main()
