"""Known-answer and failure tests. Run: python -m pytest -q"""
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import engine as e  # noqa: E402

# Lab 15 Meridian training case, mapped onto the four tickers.
MERIDIAN_ER = {"BIL": 0.035, "IEF": 0.043, "LQD": 0.050, "VT": 0.080}
MERIDIAN_VOL = {"BIL": 0.005, "IEF": 0.070, "LQD": 0.060, "VT": 0.160}
MERIDIAN_CORR = {
    "BIL": {"BIL": 1.00, "IEF": 0.10, "LQD": 0.05, "VT": 0.00},
    "IEF": {"BIL": 0.10, "IEF": 1.00, "LQD": 0.80, "VT": -0.10},
    "LQD": {"BIL": 0.05, "IEF": 0.80, "LQD": 1.00, "VT": 0.25},
    "VT": {"BIL": 0.00, "IEF": -0.10, "LQD": 0.25, "VT": 1.00},
}


def _w(b, i, l, v):
    return {"BIL": b, "IEF": i, "LQD": l, "VT": v}


def _same(a, b):
    return all(math.isclose(a[t], b[t], abs_tol=1e-9) for t in e.TICKERS)


def test_meridian_known_answer():
    w = e.search(MERIDIAN_ER, MERIDIAN_VOL, MERIDIAN_CORR, e.Inputs(), 0.065, 1.0, use_risk_limit=False)
    assert _same(w, _w(0, .20, .25, .55))
    assert round(e.port_return(w, MERIDIAN_ER), 4) == 0.0651
    assert round(e.port_vol(w, MERIDIAN_VOL, MERIDIAN_CORR), 4) == 0.0944


def test_meridian_equity_7pct_known_answer():
    er = dict(MERIDIAN_ER, VT=0.07)
    w = e.search(er, MERIDIAN_VOL, MERIDIAN_CORR, e.Inputs(), 0.065, 1.0, use_risk_limit=False)
    assert _same(w, _w(0, .10, .10, .80))


def test_lab14_benchmark_volatility_by_hand():
    # 0.40^2*0.06^2 + 0.60^2*0.16^2 + 2*0.40*0.60*0.25*0.06*0.16 = 0.010944
    v = e.port_vol(_w(0, 0, .40, .60), MERIDIAN_VOL, MERIDIAN_CORR)
    assert math.isclose(v, math.sqrt(0.010944), abs_tol=1e-12)


def test_lab13_reserve_minimum():
    assert math.isclose(4 * 0.75 / 100, e.MANDATE["reserve_minimum"])


def test_lab15_own_universe_historical_known_answer():
    r = e.run(e.Inputs(method="historical", window_months=59))
    p = r["portfolios"]["Constrained lowest-risk mix"]
    assert _same(p["weights"], _w(.60, 0, 0, .40))
    assert round(p["return"], 4) == 0.0661 and round(p["volatility"], 4) == 0.0605


def test_point_in_time_rule_blocks_later_vintage():
    rows = e.load_rates()
    v, row = e.rate_as_known(rows, "DGS3MO", "2026-10-05")
    assert v == pytest.approx(0.0419) and row["observation_date"] == "2026-10-02"
    v2, _ = e.rate_as_known(rows, "DGS3MO", "2026-10-06")
    assert v2 == pytest.approx(0.0422)
    with pytest.raises(ValueError):
        e.rate_as_known(rows, "DGS3MO", "2026-09-30")


def test_signal_bridge_net_of_fee():
    r = e.run()
    assert r["expected_returns"]["BIL"] == pytest.approx(0.0419 - 0.001353)
    assert r["expected_returns"]["VT"] == pytest.approx(0.0419 + 0.04 - 0.0006)


def test_base_constrained_passes_every_rule_and_baselines_fail():
    r = e.run()
    assert r["portfolios"]["Constrained lowest-risk mix"]["passes"]
    assert r["portfolios"]["Equal weight (baseline 1)"]["failed"] == ["Return objective"]
    assert r["portfolios"]["40/60 LQD/VT benchmark (baseline 2)"]["failed"] == ["Reserve-eligible weight"]


def test_directional_higher_equity_premium_not_less_return():
    lo = e.run(e.Inputs(equity_risk_premium=0.03))["expected_returns"]["VT"]
    hi = e.run(e.Inputs(equity_risk_premium=0.05))["expected_returns"]["VT"]
    assert hi > lo


def test_impossible_objective_is_infeasible_and_rejects():
    inp = e.Inputs(extra_cost=0.05)  # 5% drag makes 6.5% unreachable
    r = e.run(inp)
    assert r["portfolios"]["Constrained lowest-risk mix"] is None
    assert e.decision(r, [])[0] == "REJECT"


def test_bad_prices_fail_loudly(tmp_path):
    bad = tmp_path / "p.csv"
    bad.write_text("Date,BIL,IEF,LQD,VT\n2026-01-01,1,1,1,0\n2026-02-01,1,1,1,1\n")
    with pytest.raises(ValueError):
        e.load_prices(bad)


def test_weights_sum_to_one_on_grid():
    assert all(math.isclose(sum(w.values()), 1.0) for w in e.grid(0.05))
