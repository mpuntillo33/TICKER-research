"""Project 1 validation tests. Run: python -m pytest -q   (or: python tests/test_engine.py)"""
import subprocess, sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import analysis as A  # noqa: E402


def test_known_answer_lab05_training_case():
    """Course-published training answer: $27.4974 per diluted share (Week 3, Lab 05 starter)."""
    fcff, s = 100.0, {}
    for y, g in zip(A.YEARS, [0.08, 0.06, 0.05, 0.04, 0.03]):
        fcff *= 1 + g
        s[y] = {"fcff": fcff}
    v = A.dcf(s, wacc=0.10, g=0.03, debt=300.0, cash=50.0, shares=50.0, stub=1.0)
    assert round(v["value_per_share"], 4) == 27.4974


def test_known_answer_lab09_abg_proforma():
    """Course-published ABG pro-forma answer reproduced by the Lab 09 engine: $291.75."""
    out = subprocess.run([sys.executable, "proforma.py"], cwd=ROOT / "Lab 09",
                         capture_output=True, text=True, check=True).stdout
    assert "$291.75" in out


def test_base_case_checks_all_pass():
    r = A.run()
    failed = [n for n, ok, _ in r["checks"] + A.base_year_reconciliation() if not ok]
    assert not failed, failed


def test_balance_sheet_and_cash_tie_under_every_band_extreme():
    for k, (_, _, lo, hi, *_rest) in A.BOUNDS.items():
        for x in (lo, hi):
            s = A.project(replace(A.BASE, **{k: x}))
            for y in A.YEARS:
                assert abs(s[y]["bs_gap"]) < 1e-6, (k, x, y)
                assert abs(s[y]["cash_from_cash_flow"] - s[y]["cash"]) < 1e-6, (k, x, y)


def test_dcf_monotonic_in_wacc_and_growth():
    s = A.project(A.BASE)
    vw = [A.dcf(s, w, 0.02)["value_per_share"] for w in (0.07, 0.08, 0.09, 0.10)]
    vg = [A.dcf(s, 0.08, g)["value_per_share"] for g in (0.0, 0.01, 0.02, 0.03)]
    assert all(a > b for a, b in zip(vw, vw[1:])), vw   # higher WACC -> lower value
    assert all(a < b for a, b in zip(vg, vg[1:])), vg   # higher g -> higher value


def test_terminal_growth_at_or_above_wacc_is_refused():
    s = A.project(A.BASE)
    for g in (0.08, 0.09):
        try:
            A.dcf(s, 0.08, g)
        except ValueError:
            continue
        raise AssertionError(f"g={g} was accepted")


def test_bridge_identity():
    v = A.run()["valuation"]
    assert abs(v["enterprise_value"] - v["debt"] + v["cash"] - v["equity_value"]) < 1e-6
    assert abs(v["value_per_share"] * v["shares"] - v["equity_value"]) < 1e-6
    # $100m more debt must cut value by exactly $100m / shares
    v2 = A.dcf(A.project(A.BASE), A.BASE.wacc, A.BASE.terminal_growth, debt=v["debt"] + 100)
    assert abs((v["value_per_share"] - v2["value_per_share"]) - 100 / v["shares"]) < 1e-9


def test_directional_changed_input_written_before_run():
    """Prediction (written before running): a lower long-run gross margin lowers FY2030 EBIT,
    FY2030 FCFF and value per share; revenue is unchanged."""
    lo = replace(A.BASE, gross_margin_long=A.BASE.gross_margin_long - 0.005)
    b, l = A.project(A.BASE), A.project(lo)
    assert l[2030]["revenue"] == b[2030]["revenue"]
    assert l[2030]["ebit"] < b[2030]["ebit"] and l[2030]["fcff"] < b[2030]["fcff"]
    assert A.value(lo) < A.value(A.BASE)


def test_checks_fail_loudly_on_incoherent_input():
    bad = replace(A.BASE, sga_to_gp_fy2026=0.97, sga_to_gp_long=0.97, capex=2_400.0)
    names = {n for n, ok, _ in A.run(bad)["checks"] if not ok}
    assert "Drivers inside historical band" in names


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn(); print("PASS", name)
            except Exception as e:  # noqa: BLE001
                fails += 1; print("FAIL", name, "-", e)
    sys.exit(1 if fails else 0)
