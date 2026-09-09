import unittest

import pyliferisk as pl
from pyliferisk import Actuarial
from pyliferisk.mortalitytables import GKM95


class DeferredMonthlyAnnuityTest(unittest.TestCase):
    def setUp(self):
        self.mt = Actuarial(nt=GKM95, i=0.06)
        self.x = 40

    def test_zero_deferral_matches_whole_life_annuity(self):
        for payments_per_year in (1, 2, 4, 12):
            with self.subTest(payments_per_year=payments_per_year):
                self.assertAlmostEqual(
                    pl.taax(self.mt, self.x, 0, payments_per_year),
                    pl.aax(self.mt, self.x, payments_per_year),
                )
                self.assertAlmostEqual(
                    pl.tax(self.mt, self.x, 0, payments_per_year),
                    pl.ax(self.mt, self.x, payments_per_year),
                )

    def test_deferral_discounts_attained_age_annuity(self):
        for defer in (1, 10, 40, 70):
            for payments_per_year in (1, 2, 4, 12):
                with self.subTest(
                    defer=defer,
                    payments_per_year=payments_per_year,
                ):
                    discount = pl.nEx(self.mt, self.x, defer)
                    self.assertAlmostEqual(
                        pl.taax(self.mt, self.x, defer, payments_per_year),
                        discount * pl.aax(
                            self.mt,
                            self.x + defer,
                            payments_per_year,
                        ),
                    )
                    self.assertAlmostEqual(
                        pl.tax(self.mt, self.x, defer, payments_per_year),
                        discount * pl.ax(
                            self.mt,
                            self.x + defer,
                            payments_per_year,
                        ),
                    )

    def test_deferred_annuity_due_is_nonnegative(self):
        for defer in (0, 10, 40, 60, 70, 78):
            with self.subTest(defer=defer):
                self.assertGreaterEqual(pl.taax(self.mt, self.x, defer, 12), 0)

    def test_temporary_and_deferred_parts_reconstruct_whole_life(self):
        for term in (1, 10, 40):
            for payments_per_year in (1, 2, 4, 12):
                with self.subTest(
                    term=term,
                    payments_per_year=payments_per_year,
                ):
                    self.assertAlmostEqual(
                        pl.aax(self.mt, self.x, payments_per_year),
                        pl.aaxn(
                            self.mt,
                            self.x,
                            term,
                            payments_per_year,
                        )
                        + pl.taax(
                            self.mt,
                            self.x,
                            term,
                            payments_per_year,
                        ),
                    )
                    self.assertAlmostEqual(
                        pl.ax(self.mt, self.x, payments_per_year),
                        pl.axn(
                            self.mt,
                            self.x,
                            term,
                            payments_per_year,
                        )
                        + pl.tax(
                            self.mt,
                            self.x,
                            term,
                            payments_per_year,
                        ),
                    )


if __name__ == "__main__":
    unittest.main()
