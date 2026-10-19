"""Run one changed input against the base case and print before/after. No AI involved.

Usage (from the repo root):
    python tools/changed_input.py <driver> <new_value>
Example:
    python tools/changed_input.py capex 2200
Drivers: growth_fy2026, growth_long, gross_margin_fy2026, gross_margin_long,
         sga_to_gp_fy2026, sga_to_gp_long, capex, wacc, terminal_growth
"""
import sys
from dataclasses import replace
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analysis as A  # noqa: E402

driver, new = sys.argv[1], float(sys.argv[2])
old = getattr(A.BASE, driver)
before, after = A.run(A.BASE), A.run(replace(A.BASE, **{driver: new}))
print(f"Run at {datetime.now().isoformat(timespec='seconds')} | {driver}: {old} -> {new}")
rows = [("Value per share ($)", lambda r: r["valuation"]["value_per_share"]),
        ("Enterprise value ($m)", lambda r: r["valuation"]["enterprise_value"]),
        ("FY2030 revenue ($m)", lambda r: r["statements"][2030]["revenue"]),
        ("FY2030 EBIT ($m)", lambda r: r["statements"][2030]["ebit"]),
        ("FY2030 FCFF ($m)", lambda r: r["statements"][2030]["fcff"]),
        ("Terminal value share", lambda r: r["valuation"]["terminal_share"])]
print(f"{'Output':<24}{'Before':>12}{'After':>12}{'Change':>12}")
for name, f in rows:
    b, a = f(before), f(after)
    print(f"{name:<24}{b:>12,.3f}{a:>12,.3f}{a - b:>+12,.3f}")
print(f"Market price for reference: ${A.MARKET['price']:.2f} ({A.MARKET['price_date']})")
fails = [n for n, ok, _ in after["checks"] if not ok]
print("Checks after change:", "all pass" if not fails else "FAIL -> " + "; ".join(fails))
