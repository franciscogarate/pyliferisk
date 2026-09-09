import unittest

import pyliferisk as pl
from pyliferisk import Actuarial
from pyliferisk.mortalitytables import GKM95


class DeferredMortalityTest(unittest.TestCase):
    def setUp(self):
        self.mt = Actuarial(nt=GKM95, i=0.06)
        self.x = 40

    def test_zero_deferral_matches_plain_death_probability(self):
        for years in (1, 5, 10, 20):
            with self.subTest(years=years):
                self.assertAlmostEqual(
                    pl.tqxn(self.mt, self.x, 0, years),
                    1000 * pl.tqx(self.mt, self.x, years),
                )

    def test_one_year_deferred_probabilities_telescope(self):
        for years in (1, 5, 10, 20):
            with self.subTest(years=years):
                deferred_sum = sum(
                    pl.tqxn(self.mt, self.x, defer, 1)
                    for defer in range(years)
                )
                self.assertAlmostEqual(
                    deferred_sum,
                    1000 * pl.tqx(self.mt, self.x, years),
                )

    def test_matches_life_table_definition(self):
        for defer, years in ((0, 3), (5, 1), (5, 7), (20, 10)):
            with self.subTest(defer=defer, years=years):
                expected = 1000 * (
                    self.mt.lx[self.x + defer]
                    - self.mt.lx[self.x + defer + years]
                ) / self.mt.lx[self.x]
                self.assertAlmostEqual(
                    pl.tqxn(self.mt, self.x, defer, years),
                    expected,
                )


if __name__ == "__main__":
    unittest.main()
