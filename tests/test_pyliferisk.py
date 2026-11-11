# -*- coding: utf-8 -*-
"""Test suite for pyliferisk 1.13.0.

Each test referencing a number (1.1, 1.4, ...) corresponds to an issue
from the v1.12.0 review (recomendaciones.txt).
"""
import math

import pytest

import pyliferisk as plr
from pyliferisk import (MortalityTable, Actuarial, annuity, qx, lx, w, dx, px,
                        tpx, tqx, tqxn, ex, mx, Cx, Nx, Mx, nEx, Ax, Axn, AExn,
                        tAx, tAxn, aaxn, axn, aax, ax, taaxn, taxn, taax, tax,
                        Iaaxn, Iaxn, Iaax, Iax, Itaax, Itax, qAxn, qtAx,
                        qtaaxn, qtaxn)
from pyliferisk.mortalitytables import GKM80, GKM95


@pytest.fixture
def mt():
    return Actuarial(nt=GKM95, i=0.02)


# 1.1 -- mutable default arguments must not leak state between instances
def test_no_shared_state_between_instances():
    a = MortalityTable(lx=[100, 90, 70, 0])
    b = MortalityTable(lx=[100, 50, 10, 0])
    assert a.qx is not b.qx
    assert a.qx[0] == pytest.approx(0.1)
    assert b.qx[0] == pytest.approx(0.5)


def test_input_lists_not_mutated():
    src = [100, 90, 70, 0]
    MortalityTable(lx=src)
    assert src == [100, 90, 70, 0]


# 1.2 -- Iaaxn / Iaxn must be functional (no empty redefinitions, no NameError)
def test_increasing_temporary_annuities(mt):
    val_due = Iaaxn(mt, 40, 10)
    val_late = Iaxn(mt, 40, 10)
    assert val_due is not None and val_due > 0
    assert val_late is not None and val_late > 0
    assert val_due > val_late  # due is worth more than immediate


# 1.3 -- qAxn / qtAx must not raise NameError
def test_geometric_insurances(mt):
    assert qAxn(mt, 30, 10, 0.02) > 0
    assert qtAx(mt, 30, 10, 0.02) > 0


# 1.4 -- tqxn must be a probability and match its definition
def test_tqxn_is_probability(mt):
    val = tqxn(mt, 30, 10, 5)
    assert 0 <= val <= 1
    assert val == pytest.approx(tpx(mt, 30, 10) * tqx(mt, 40, 5))


# 1.5 -- annuity() deferred branches
def test_annuity_deferred_temporary(mt):
    assert annuity(mt, 30, 10, 0, deferred=5) == pytest.approx(taaxn(mt, 30, 10, 5))
    assert annuity(mt, 30, 10, 1, deferred=5) == pytest.approx(taxn(mt, 30, 10, 5))
    # legacy negative-number syntax still works (with a DeprecationWarning)
    with pytest.warns(DeprecationWarning):
        assert annuity(mt, 30, 10, 0, -5) == pytest.approx(taaxn(mt, 30, 10, 5))


def test_annuity_deferred_geometric(mt):
    expected = qtaaxn(mt, 30, 10, 5, 0.03)
    assert annuity(mt, 30, 10, 0, deferred=5, increase=['g', 0.03]) == pytest.approx(expected)
    with pytest.warns(DeprecationWarning):
        assert annuity(mt, 30, 10, 0, ['g', 0.03], -5) == pytest.approx(expected)
    # deferred geometric whole-life postpaid (former broken else-branch)
    assert annuity(mt, 30, 'w', 1, deferred=5, increase=['g', 0.03]) > 0


def test_deferred_temporary_annuity_identity(mt):
    # t/äx:n = tEx * ä(x+t):n
    assert taaxn(mt, 30, 10, 5) == pytest.approx(nEx(mt, 30, 5) * aaxn(mt, 35, 10))
    assert taxn(mt, 30, 10, 5) == pytest.approx(nEx(mt, 30, 5) * axn(mt, 35, 10))


# 1.6 -- the Cx() function must match the mt.Cx vector
def test_Cx_function_matches_vector(mt):
    for age in (0, 30, 50, 80):
        assert Cx(mt, age) == pytest.approx(mt.Cx[age])


# 1.7 -- single definition of omega
def test_omega_unified(mt):
    assert w(mt) == mt.w
    assert mt.lx[mt.w] > 0
    assert mt.lx[mt.w + 1] == 0


# 1.8 -- Actuarial without interest rate raises a clear error
def test_actuarial_requires_interest_rate():
    with pytest.raises(ValueError):
        Actuarial(nt=GKM95)


# 2.1 -- central mortality rate mx = dx / (lx - 0.5*dx)
def test_central_mortality_rate(mt):
    x = 50
    d = dx(mt, x)
    assert mx(mt, x) == pytest.approx(d / (mt.lx[x] - 0.5 * d))
    assert mx(mt, x) > tqx(mt, x, 1)  # mx is slightly larger than qx


def test_curtate_expectation(mt):
    x = 50
    curtate = sum(mt.lx[x + 1:]) / mt.lx[x]
    assert ex(mt, x) == pytest.approx(curtate)
    assert mt.ex[x] == pytest.approx(curtate)
    assert mt.ex[x] == pytest.approx(27.389458797448576)
    assert ex(mt, 500) == 0
    small = MortalityTable(lx=[100, 50, 0])
    assert small.ex[0] == pytest.approx(0.5)
    assert small.ex[1] == pytest.approx(0.0)


def test_probabilities_per_unit(mt, capsys):
    assert mt.qx[50] == pytest.approx(GKM95[51] / 1000)
    assert 0 <= min(mt.qx) and max(mt.qx) <= 1
    for age in (0, 30, 50, 80):
        assert px(mt, age) == pytest.approx(tpx(mt, age, 1))
        assert qx(mt, age) == pytest.approx(tqx(mt, age, 1))
        assert qx(mt, age) + px(mt, age) == pytest.approx(1)
    from_qx = MortalityTable(qx=[0.1, 0.5, 1.0])
    assert from_qx.lx[:4] == pytest.approx([100000, 90000, 45000, 0])
    mt.view(50, 50, var='qx')
    assert '[x=50]  qx={}'.format(GKM95[51]) in capsys.readouterr().out


def test_lx_unchanged_by_scale(mt):
    assert mt.lx[50] == pytest.approx(93823.1547833275)
    assert Ax(mt, 50) == pytest.approx(0.5832765526571225)
    assert annuity(mt, 30, 10, 0) == pytest.approx(9.1080026405074)


def test_actuarial_inherits_mortalitytable(mt):
    assert isinstance(mt, MortalityTable)
    plain = MortalityTable(nt=GKM95)
    assert plain.lx == mt.lx and plain.qx == mt.qx and plain.ex == mt.ex
    assert plain.Dx == [] and len(mt.Dx) == len(mt.lx)


def test_view_has_no_nEx(mt):
    with pytest.raises(KeyError):
        mt.view(var='nEx')
    assert not hasattr(mt, 'nEx')


# 2.6 -- Nx()/Mx() functions use the same criterion as the class vectors
def test_commutation_functions_match_vectors(mt):
    for age in (0, 30, 50):
        assert Nx(mt, age) == pytest.approx(mt.Nx[age])
        assert Mx(mt, age) == pytest.approx(mt.Mx[age])


# 2.9 -- annuity() input validation
def test_annuity_invalid_inputs(mt):
    with pytest.raises(ValueError):
        annuity(mt, 30, 10, 2)  # p must be 0 or 1
    with pytest.raises(ValueError):
        annuity(mt, 30, 10, 0, increase=['x', 0.03])
    with pytest.raises(ValueError):
        annuity(mt, 30, 10, 0, increase='g')


def test_annuity_named_parameters(mt):
    assert annuity(mt, 30, 'w', 0, deferred=5) == pytest.approx(taax(mt, 30, 5))
    assert annuity(mt, 30, 'w', 1, 12, deferred=5) == pytest.approx(tax(mt, 30, 5, 12))
    assert annuity(mt, 30, 10, 1, increase=['a', 1]) == pytest.approx(Iaxn(mt, 30, 10))
    with pytest.warns(DeprecationWarning):
        assert annuity(mt, 30, 'w', 0, 12, ['g', 0.03], -5) == \
            pytest.approx(annuity(mt, 30, 'w', 0, 12, deferred=5, increase=['g', 0.03]))
    with pytest.warns(DeprecationWarning):
        assert annuity(mt, 30, 'w', 0, ['g', 0.03]) == \
            pytest.approx(annuity(mt, 30, 'w', 0, increase=['g', 0.03]))
    import warnings as _w
    with _w.catch_warnings():
        _w.simplefilter('error')
        annuity(mt, 30, 10, 0, 12, deferred=5, increase=['g', 0.03])


# 2.11 -- perc truncation keeps qx <= 1000 and closes the table once
def test_perc_truncation():
    high = MortalityTable(nt=GKM80, perc=120)
    assert max(high.qx) <= 1.0
    assert high.qx.count(1.0) == 1
    low = MortalityTable(nt=GKM80, perc=50)
    assert low.qx[-1] == 1.0
    assert low.qx.count(1.0) == 1


# 2.12 -- unimplemented functions raise NotImplementedError instead of None
def test_unimplemented_functions_raise(mt):
    for fn, fargs in ((plr.IAx, (mt, 30)), (plr.IAxn, (mt, 30, 10)),
                      (plr.qtAxn, (mt, 30, 10, 0.02))):
        with pytest.raises(NotImplementedError):
            fn(*fargs)


# 2.5 -- MortalityTable warns if 'i' is passed
def test_mortalitytable_warns_on_interest():
    with pytest.warns(DeprecationWarning):
        MortalityTable(nt=GKM95, i=0.02)


# Actuarial identities (sanity of the whole commutation chain) ----------

def test_endowment_identity(mt):
    x, n = 40, 15
    assert AExn(mt, x, n) == pytest.approx(Axn(mt, x, n) + nEx(mt, x, n))


def test_deferred_insurance_identities(mt):
    x, n, t = 40, 15, 5
    assert tAx(mt, x, t) == pytest.approx(Ax(mt, x) - Axn(mt, x, t))
    assert tAxn(mt, x, n, t) == pytest.approx(Axn(mt, x, t + n) - Axn(mt, x, t))


def test_annuity_due_vs_immediate(mt):
    x, n = 40, 15
    assert aax(mt, x) == pytest.approx(ax(mt, x) + 1)
    assert aaxn(mt, x, n) - axn(mt, x, n) == pytest.approx(1 - nEx(mt, x, n))


def test_whole_life_insurance_annuity_identity(mt):
    # Ax = 1 - d * äx  with d = i/(1+i)
    x = 40
    d = mt.i / (1 + mt.i)
    assert Ax(mt, x) == pytest.approx(1 - d * aax(mt, x), rel=1e-6)


def test_deferred_increasing_annuity_brute_force(mt):
    x, t = 30, 5
    v = 1 / (1 + mt.i)
    due = sum((k - t + 1) * v ** k * mt.lx[x + k] / mt.lx[x] for k in range(t, mt.w - x + 1))
    late = sum((k - t) * v ** k * mt.lx[x + k] / mt.lx[x] for k in range(t + 1, mt.w - x + 1))
    assert Itaax(mt, x, t) == pytest.approx(due)
    assert Itax(mt, x, t) == pytest.approx(late)
    assert annuity(mt, x, 'w', 0, deferred=t, increase=['a', 1]) == pytest.approx(due)
    assert annuity(mt, x, 'w', 1, deferred=t, increase=['a', 1]) == pytest.approx(late)
    assert Itaax(mt, x, t) == pytest.approx(nEx(mt, x, t) * Iaax(mt, x + t))
    assert Iaaxn(mt, x, 10) < Iaax(mt, x)
    n = 10
    assert Iaaxn(mt, x, n) == pytest.approx(
        sum((k + 1) * v ** k * mt.lx[x + k] / mt.lx[x] for k in range(n)))
    assert Iaxn(mt, x, n) == pytest.approx(
        sum(k * v ** k * mt.lx[x + k] / mt.lx[x] for k in range(1, n + 1)))


def test_annuity_legacy_combinations(mt):
    np = pytest.importorskip('numpy')
    expected = qtaaxn(mt, 30, 10, 5, 0.03, 12)
    for call_args in ((12, ['g', 0.03], -5), (12, -5, ['g', 0.03])):
        with pytest.warns(DeprecationWarning):
            assert annuity(mt, 30, 10, 0, *call_args) == pytest.approx(expected)
    with pytest.warns(DeprecationWarning):
        assert annuity(mt, 30, 10, 0, -5, ['g', 0.03]) == pytest.approx(qtaaxn(mt, 30, 10, 5, 0.03))
    with pytest.warns(DeprecationWarning):
        assert annuity(mt, 30, 10, 0, np.int64(-5)) == pytest.approx(taaxn(mt, 30, 10, 5))
    assert annuity(mt, 30, 10, 0, deferred=np.int64(5)) == pytest.approx(taaxn(mt, 30, 10, 5))


def test_annuity_errors(mt):
    with pytest.raises(NotImplementedError):
        annuity(mt, 30, 10, 0, deferred=5, increase=['a', 1])
    with pytest.raises(TypeError):
        annuity(mt, 30, 10, 0, 12, ['g', 0.03], -5, 1)
    with pytest.raises(ValueError):
        annuity(mt, 30, 10, 0, deferred=-5)
    with pytest.raises(ValueError):
        annuity(mt, 30, 10, 0, -5, deferred=3)
    with pytest.raises(ValueError):
        annuity(mt, 30, 10, 0, -5, -3)
    with pytest.raises(ValueError):
        annuity(mt, 30, 10, 0, ['g', 0.02], increase=['a', 1])
    with pytest.raises(ValueError):
        annuity(mt, 30, 10, 0, deferred=2.5)


def test_qx_must_be_per_unit():
    with pytest.raises(ValueError):
        MortalityTable(qx=[5, 10, 1000])
    with pytest.raises(ValueError):
        MortalityTable(qx=[0.1, float('nan'), 1])


def test_ex_zero_division_and_other_errors():
    closed = MortalityTable(lx=[100, 50, 0])
    assert ex(closed, 2) == 0
    with pytest.raises(AttributeError):
        ex(None, 0)


def test_constructor_positional_order():
    plain = MortalityTable(None, None, None, GKM95, 85)
    assert plain.perc == 85 and plain.nt is GKM95


def test_readme_example_3():
    # A 10-year term insurance, male aged 30, GKM80 at 6%
    nt = Actuarial(nt=GKM80, i=0.06)
    premium = 1000 * (Axn(nt, 30, 10) / annuity(nt, 30, 10, 0))
    assert premium > 0
    assert math.isfinite(premium)


def test_basic_probabilities(mt):
    x = 50
    assert qx(mt, x) + px(mt, x) == pytest.approx(1)
    assert tpx(mt, x, 1) == pytest.approx(1 - qx(mt, x))
    assert lx(mt, x) > lx(mt, x + 1)
    assert ex(mt, x) > 0


def geometric_tables():
    tables = [(Actuarial(nt=GKM95, i=0.03, perc=perc), 60) for perc in (50, 75, 100)]
    tables.append((Actuarial(lx=[100000., 97000., 90000., 80000., 60000., 30000., 0.], i=.03), 1))
    tables.append((Actuarial(qx=[.03, .07, .12, .2, .4, 1.], i=.03), 1))
    return tables


def test_issue_17_reported_case():
    mt = Actuarial(nt=GKM95, perc=75, i=.03)
    assert plr.qax(mt, 60, 0) == pytest.approx(ax(mt, 60))
    assert ax(mt, 60) == pytest.approx(14.93597449181164)


def test_geometric_zero_growth_matches_level():
    for mt, age in geometric_tables():
        for m in (1, 2, 4, 12):
            assert plr.qax(mt, age, 0., m) == pytest.approx(ax(mt, age, m))
            assert plr.qaax(mt, age, 0., m) == pytest.approx(aax(mt, age, m))
            assert plr.qaxn(mt, age, 2, 0., m) == pytest.approx(axn(mt, age, 2, m))
            assert plr.qaaxn(mt, age, 2, 0., m) == pytest.approx(aaxn(mt, age, 2, m))
            assert qtaxn(mt, age, 2, 1, 0., m) == pytest.approx(taxn(mt, age, 2, 1, m))
            assert qtaaxn(mt, age, 2, 1, 0., m) == pytest.approx(taaxn(mt, age, 2, 1, m))
        assert plr.qAx(mt, age, 0.) == pytest.approx(Ax(mt, age))
        assert qAxn(mt, age, 2, 0.) == pytest.approx(Axn(mt, age, 2))
        assert qtAx(mt, age, 2, 0.) == pytest.approx(tAx(mt, age, 2))
        for n in (2, 'w'):
            for p in (0, 1):
                assert annuity(mt, age, n, p, increase=['g', 0.]) == pytest.approx(annuity(mt, age, n, p))


def test_geometric_annual_cashflows():
    for mt, age in geometric_tables():
        end = len(mt.lx) - age
        for growth in (-.01, 0., .02):
            ratio = (1 + growth) / (1 + mt.i)

            def cash(start, stop):
                return math.fsum(mt.lx[age + k] / mt.lx[age] * ratio ** k for k in range(start, stop))

            def deaths(start, stop):
                return math.fsum((mt.lx[age + k] - mt.lx[age + k + 1]) / mt.lx[age] * ratio ** (k + 1)
                                 for k in range(start, stop))

            assert plr.qax(mt, age, growth) == pytest.approx(cash(1, end))
            assert plr.qaax(mt, age, growth) == pytest.approx(cash(0, end))
            assert plr.qaxn(mt, age, 2, growth) == pytest.approx(cash(1, 3))
            assert plr.qaaxn(mt, age, 2, growth) == pytest.approx(cash(0, 2))
            assert plr.qtax(mt, age, 2, growth) == pytest.approx(cash(3, end))
            assert plr.qtaax(mt, age, 2, growth) == pytest.approx(cash(2, end))
            assert qtaxn(mt, age, 2, 1, growth) == pytest.approx(cash(2, 4))
            assert qtaaxn(mt, age, 2, 1, growth) == pytest.approx(cash(1, 3))
            assert plr.qAx(mt, age, growth) == pytest.approx(deaths(0, end - 1))
            assert qAxn(mt, age, 2, growth) == pytest.approx(deaths(0, 2))
            assert qtAx(mt, age, 2, growth) == pytest.approx(deaths(2, end - 1))


def test_geometric_keeps_caller_table():
    import copy
    for mt, age in geometric_tables():
        before = copy.deepcopy(mt.__dict__)
        plr.qax(mt, age, .02)
        plr.qaaxn(mt, age, 2, -.01)
        plr.qAx(mt, age, 0.)
        assert mt.__dict__ == before


def test_deferred_whole_life_fractional_adjustment(mt):
    for m in (1, 2, 4, 12):
        for x, t in ((30, 5), (50, 10), (60, 1)):
            assert taax(mt, x, t, m) == pytest.approx(nEx(mt, x, t) * aax(mt, x + t, m))
            assert tax(mt, x, t, m) == pytest.approx(nEx(mt, x, t) * ax(mt, x + t, m))
            assert annuity(mt, x, 'w', 0, m, deferred=t) == pytest.approx(nEx(mt, x, t) * aax(mt, x + t, m))
            assert annuity(mt, x, 'w', 1, m, deferred=t) == pytest.approx(nEx(mt, x, t) * ax(mt, x + t, m))
        assert taax(mt, 40, 0, m) == pytest.approx(aax(mt, 40, m))
        assert tax(mt, 40, 0, m) == pytest.approx(ax(mt, 40, m))


def test_geometric_deferred_whole_life_fractional():
    for mt, age in geometric_tables():
        for m in (1, 2, 12):
            assert plr.qtax(mt, age, 2, 0., m) == pytest.approx(tax(mt, age, 2, m))
            assert plr.qtaax(mt, age, 2, 0., m) == pytest.approx(taax(mt, age, 2, m))
            for growth in (-.01, .02):
                j = (mt.i - growth) / (1 + growth)
                mtj = Actuarial(lx=mt.lx, i=j)
                assert plr.qtax(mt, age, 2, growth, m) == pytest.approx(nEx(mtj, age, 2) * ax(mtj, age + 2, m))
                assert plr.qtaax(mt, age, 2, growth, m) == pytest.approx(nEx(mtj, age, 2) * aax(mtj, age + 2, m))
