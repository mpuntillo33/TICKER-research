"""ACI Project 1 engine: five-year three-statement pro-forma driving an FCFF DCF.

All money is USD millions except per-share values. Standard library only.

Layers
------
LOCKED   : filing facts (FILING), normalizations, accounting engine, checks.
EXPOSED  : Drivers (the bounded inputs in the notebook's driver panel).
OUTPUT   : run() returns statements, valuation, bridge and a list of checks.

Nothing in app.ipynb calculates a material number; it only calls this module.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, replace
from math import isclose
from typing import Callable

YEARS = (2026, 2027, 2028, 2029, 2030)

# ---------------------------------------------------------------------------
# LOCKED: filing facts. Every value is traced in docs/validation-and-ai-use.md.
# ---------------------------------------------------------------------------
FILING = {
    # FY2025 Form 10-K, 53 weeks ended Feb 28, 2026 (accession 0001646972-26-000032)
    "fy2025_revenue": 83_172.5,          # statements of operations
    "fy2025_gross_profit": 22_606.7,
    "fy2025_sga": 21_891.3,              # includes the opioid-settlement-framework charge
    "fy2025_net_income": 217.4,
    "fy2025_da": 1_913.7,                # cash-flow statement
    "fy2025_capex": 1_833.6,
    "fy2025_inventory": 5_173.9,         # balance sheet, Feb 28, 2026
    "fy2025_ppe": 9_903.7,
    "fy2025_other_assets": 11_489.7,     # total assets less cash, inventory, PP&E
    "fy2025_cash": 198.6,
    "fy2025_debt": 8_946.6,              # long-term debt and finance leases incl. current maturities
    "fy2025_other_liabilities": 15_983.1,  # all non-debt liabilities, incl. accounts payable
    "fy2025_accounts_payable": 4_021.2,   # balance sheet, Feb 28, 2026
    "fy2025_equity": 1_836.2,
    "opioid_charge_pretax": 773.8,       # one-time; removed from the SG&A run-rate
    "week53_sales": 1_360.0,             # estimated extra-week sales contribution
    "week53_adj_ebitda": 68.0,           # management estimate of extra-week adj. EBITDA
    # Q1 FY2026 10-Q (16 wks to Jun 20, 2026) + Q2 FY2026 earnings release (12 wks to Sep 12, 2026)
    "h1_fy2026_adj_ebitda": 1_013.0 + 784.0,   # 28 weeks
    "h1_fy2025_adj_ebitda": 1_111.0 + 848.4,
    # Q2 FY2026 earnings release, Form 8-K filed Oct 13, 2026 (bridge date Sep 12, 2026)
    "bridge_debt": 9_328.2,              # total debt including finance leases
    "bridge_cash": 282.0,
    "diluted_shares": 488.2,             # diluted weighted-average Class A shares, 12 weeks to Sep 12, 2026
}

# Market and discount-rate inputs (each with source and as-of date; see docs/validation-and-ai-use.md)
MARKET = {
    "price": 13.09,               # ACI close, Oct 16, 2026, 4:00 PM EDT (stockanalysis.com, S&P Global data)
    "price_date": "2026-10-16",
    "shares_outstanding": 485.325683,  # Q1 FY2026 10-Q cover page, as of Jul 24, 2026
}
WACC_INPUTS = {
    "risk_free": 0.0510,          # 10-yr Treasury constant maturity, Oct 15, 2026 (FRED DGS10)
    "erp": 0.0414,                # Damodaran implied ERP used in Lab 06 (Sep 2026)
    "unlevered_beta": 0.85,       # Damodaran Retail (Grocery and Food), cash-corrected, Jan 2026 dataset
    "pretax_cost_of_debt": 0.059, # interest expense / debt incl. finance leases (Q1 FY2026 annualized)
    "tax_rate": 0.255,
    "raw_regression_beta_rejected": 0.23,  # provider "Beta (5Y)"; distorted by 2022-24 merger-arbitrage pricing
}


def wacc_build(price: float | None = None) -> dict[str, float]:
    """Industry unlevered beta relevered at ACI's market D/E (debt incl. finance leases)."""
    w = WACC_INPUTS
    e = (price or MARKET["price"]) * MARKET["shares_outstanding"]
    d = FILING["bridge_debt"]
    levered_beta = w["unlevered_beta"] * (1 + (1 - w["tax_rate"]) * d / e)
    ke = w["risk_free"] + levered_beta * w["erp"]
    kd_after = w["pretax_cost_of_debt"] * (1 - w["tax_rate"])
    wacc = e / (d + e) * ke + d / (d + e) * kd_after
    return {"market_equity": e, "debt": d, "d_to_e": d / e, "levered_beta": levered_beta,
            "cost_of_equity": ke, "after_tax_cost_of_debt": kd_after, "equity_weight": e / (d + e), "wacc": wacc}


# Fiscal 2026 ends Feb 27, 2027; 168 of 364 days remain after the Sep 12, 2026 bridge date.
STUB_FRACTION = 168 / 364

# LOCKED operating conventions (Lab 10 history and judgment, documented in the challenge record)
TAX_RATE = 0.255
DA_TO_OPENING_PPE = FILING["fy2025_da"] / FILING["fy2025_ppe"]
INVENTORY_DAYS = 31.2
COGS_FY2025 = FILING["fy2025_revenue"] - FILING["fy2025_gross_profit"]
PAYABLE_DAYS = FILING["fy2025_accounts_payable"] / COGS_FY2025 * 365   # ~24.2 days of cost of sales
INTEREST_RATE = 0.059
REVOLVER_RATE = 0.065
REVOLVER_LIMIT = 3_562.3
MINIMUM_CASH = 100.0
DEBT_REPAYMENT = 50.0
DIVIDENDS = 330.0          # ~$0.68/share x ~488m shares
COST_OF_EQUITY = 0.10      # FCFE cross-method only

# Normalized FY2025 base (contamination catalog rows N1 and N2)
BASE_REVENUE_52WK = FILING["fy2025_revenue"] - FILING["week53_sales"]
NORMALIZED_SGA_TO_GP = (FILING["fy2025_sga"] - FILING["opioid_charge_pretax"]) / FILING["fy2025_gross_profit"]


# ---------------------------------------------------------------------------
# EXPOSED: drivers with defended bounds (low, high) and historical bands.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Drivers:
    growth_fy2026: float = -0.005    # 52-week revenue growth vs normalized FY2025
    growth_long: float = 0.015       # FY2028-FY2030; FY2027 is the midpoint
    gross_margin_fy2026: float = 0.268
    gross_margin_long: float = 0.270  # reached in FY2030, linear in between
    sga_to_gp_fy2026: float = 0.940
    sga_to_gp_long: float = 0.930
    capex: float = 2_000.0
    wacc: float = 0.077              # wacc_build() = 7.68%, rounded
    terminal_growth: float = 0.020


BASE = Drivers()

# (slider low, slider high, historical/defensible band low, band high, unit, basis)
BOUNDS: dict[str, tuple[float, float, float, float, str, str]] = {
    "growth_fy2026": (-0.03, 0.03, -0.015, 0.02, "%",
        "Identical sales ex-fuel: +3.0% FY23, +2.0% FY24, +2.0% FY25, -0.8% Q1 and Q2 FY26 (10-K MD&A; 10-Q; Q2 release)."),
    "growth_long": (-0.01, 0.03, 0.0, 0.025, "%",
        "Mature grocer; long-run identical sales 2-3% pre-2026; capped below nominal GDP."),
    "gross_margin_fy2026": (0.260, 0.280, 0.264, 0.279, "%",
        "Gross margin 27.8% FY23, 27.7% FY24, 27.2% FY25, 26.6% Q1 FY26, 26.8% Q2 FY26."),
    "gross_margin_long": (0.260, 0.280, 0.264, 0.279, "%",
        "Same band; pharmacy and digital mix pressure margin (FY2025 10-K)."),
    "sga_to_gp_fy2026": (0.900, 0.970, 0.904, 0.960, "%",
        "SG&A / gross profit 90.4% FY23, 92.6% FY24, 93.4% FY25 ex-opioid charge; H1 FY26 adj. EBITDA -8%."),
    "sga_to_gp_long": (0.900, 0.970, 0.904, 0.960, "%",
        "ACI Edge productivity unproven; turnaround plan due by the Q4 FY26 call."),
    "capex": (1_600.0, 2_400.0, 1_800.0, 2_200.0, "$m",
        "Capex $2,156.7m FY23, $1,927.5m FY24, $1,833.6m FY25; FY26 plan $2.0-2.2bn (FY2025 10-K)."),
    "wacc": (0.065, 0.100, 0.070, 0.095, "%",
        "Analyst build: risk-free + beta x ERP, after-tax cost of debt, weights; see docs."),
    "terminal_growth": (0.000, 0.030, 0.010, 0.025, "%",
        "Must stay below long-run nominal GDP and below WACC."),
}


def path(first: float, last: float) -> dict[int, float]:
    """Linear path from FY2026 to FY2030."""
    step = (last - first) / (len(YEARS) - 1)
    return {y: first + step * i for i, y in enumerate(YEARS)}


def growth_path(d: Drivers) -> dict[int, float]:
    return {2026: d.growth_fy2026, 2027: (d.growth_fy2026 + d.growth_long) / 2,
            2028: d.growth_long, 2029: d.growth_long, 2030: d.growth_long}


# ---------------------------------------------------------------------------
# LOCKED: accounting engine
# ---------------------------------------------------------------------------
def project(d: Drivers) -> dict[int, dict[str, float]]:
    """Income statement, balance sheet and cash-flow statement for FY2026E-FY2030E.

    Cash is computed from the cash-flow statement, never plugged. The revolver is drawn
    only to hold minimum cash and is repaid first from excess cash.
    """
    growth = growth_path(d)
    margin = path(d.gross_margin_fy2026, d.gross_margin_long)
    sga_ratio = path(d.sga_to_gp_fy2026, d.sga_to_gp_long)
    o = {"revenue": BASE_REVENUE_52WK, "inventory": FILING["fy2025_inventory"],
         "ppe": FILING["fy2025_ppe"], "other_assets": FILING["fy2025_other_assets"],
         "cash": FILING["fy2025_cash"], "debt": FILING["fy2025_debt"], "revolver": 0.0,
         "other_liabilities": FILING["fy2025_other_liabilities"], "equity": FILING["fy2025_equity"],
         "accounts_payable": FILING["fy2025_accounts_payable"]}
    out: dict[int, dict[str, float]] = {}
    for y in YEARS:
        r: dict[str, float] = {}
        # Income statement
        r["revenue"] = o["revenue"] * (1 + growth[y])
        r["gross_profit"] = r["revenue"] * margin[y]
        r["sga"] = r["gross_profit"] * sga_ratio[y]
        r["ebit"] = r["gross_profit"] - r["sga"]          # D&A sits inside cost of sales and SG&A
        r["da"] = o["ppe"] * DA_TO_OPENING_PPE
        r["ebitda"] = r["ebit"] + r["da"]
        r["interest"] = o["debt"] * INTEREST_RATE + o["revolver"] * REVOLVER_RATE
        r["pretax_income"] = r["ebit"] - r["interest"]
        r["tax"] = max(0.0, r["pretax_income"]) * TAX_RATE
        r["net_income"] = r["pretax_income"] - r["tax"]
        # Working capital and fixed assets
        r["inventory"] = (r["revenue"] - r["gross_profit"]) * INVENTORY_DAYS / 365
        r["capex"] = d.capex
        r["ppe"] = o["ppe"] + d.capex - r["da"]
        r["delta_inventory"] = r["inventory"] - o["inventory"]
        r["accounts_payable"] = (r["revenue"] - r["gross_profit"]) * PAYABLE_DAYS / 365
        r["delta_other_liabilities"] = r["accounts_payable"] - o["accounts_payable"]   # only payables move
        r["other_liabilities"] = o["other_liabilities"] + r["delta_other_liabilities"]
        # Cash-flow statement
        r["cfo"] = r["net_income"] + r["da"] - r["delta_inventory"] + r["delta_other_liabilities"]
        r["cfi"] = -d.capex
        r["debt"] = o["debt"] - DEBT_REPAYMENT
        r["dividends"] = DIVIDENDS
        pre_cash = o["cash"] + r["cfo"] + r["cfi"] - DEBT_REPAYMENT - DIVIDENDS
        revolver = o["revolver"]
        if pre_cash < MINIMUM_CASH:
            revolver += MINIMUM_CASH - pre_cash
        else:
            revolver -= min(revolver, pre_cash - MINIMUM_CASH)
        r["revolver"] = revolver
        r["revolver_change"] = revolver - o["revolver"]
        r["cff"] = -DEBT_REPAYMENT - DIVIDENDS + r["revolver_change"]
        r["net_change_in_cash"] = r["cfo"] + r["cfi"] + r["cff"]
        r["cash_from_cash_flow"] = o["cash"] + r["net_change_in_cash"]
        r["cash"] = max(pre_cash, MINIMUM_CASH) if pre_cash < MINIMUM_CASH else pre_cash - (o["revolver"] - revolver)
        # Balance sheet
        r["other_assets"] = o["other_assets"]
        r["equity"] = o["equity"] + r["net_income"] - DIVIDENDS
        r["total_assets"] = r["inventory"] + r["ppe"] + r["other_assets"] + r["cash"]
        r["total_liabilities"] = r["debt"] + r["revolver"] + r["other_liabilities"]
        r["bs_gap"] = r["total_assets"] - r["total_liabilities"] - r["equity"]
        # Cash flows for valuation
        r["nopat"] = r["ebit"] * (1 - TAX_RATE)
        r["delta_nwc"] = r["delta_inventory"] - r["delta_other_liabilities"]
        r["fcff"] = r["nopat"] + r["da"] - d.capex - r["delta_nwc"]
        r["fcfe"] = r["cfo"] + r["cfi"] - DEBT_REPAYMENT + r["revolver_change"]
        out[y] = r
        o = {**o, **{k: r[k] for k in ("revenue", "inventory", "ppe", "cash", "debt", "revolver",
                                        "other_liabilities", "equity", "accounts_payable")}}
    return out


# ---------------------------------------------------------------------------
# LOCKED: FCFF DCF and enterprise-to-equity bridge (valuation date Sep 12, 2026)
# ---------------------------------------------------------------------------
def dcf(statements: dict[int, dict[str, float]], wacc: float, g: float,
        debt: float = FILING["bridge_debt"], cash: float = FILING["bridge_cash"],
        shares: float = FILING["diluted_shares"], other_debt_like: float = 0.0,
        stub: float = STUB_FRACTION) -> dict[str, float]:
    """FCFF DCF. First forecast year is a stub (fraction of the year left after the bridge date);
    later years are end-of-period. stub=1.0 gives the plain five-year convention used in Lab 05."""
    if g >= wacc:
        raise ValueError(f"Terminal growth {g:.2%} must be below WACC {wacc:.2%}")
    pv_explicit = 0.0
    for i, y in enumerate(YEARS):
        fraction = stub if y == YEARS[0] else 1.0
        t = stub + i  # end-of-period timing after the stub
        pv_explicit += statements[y]["fcff"] * fraction / (1 + wacc) ** t
    last = statements[YEARS[-1]]["fcff"]
    terminal_value = last * (1 + g) / (wacc - g)
    t_last = stub + len(YEARS) - 1
    pv_terminal = terminal_value / (1 + wacc) ** t_last
    ev = pv_explicit + pv_terminal
    equity = ev - debt - other_debt_like + cash
    return {"pv_explicit": pv_explicit, "terminal_value": terminal_value, "pv_terminal": pv_terminal,
            "enterprise_value": ev, "debt": debt, "cash": cash, "other_debt_like": other_debt_like,
            "equity_value": equity, "shares": shares, "value_per_share": equity / shares,
            "terminal_share": pv_terminal / ev}


def fcfe_value(statements: dict[int, dict[str, float]], ke: float = COST_OF_EQUITY,
               g: float = 0.02, shares: float = FILING["diluted_shares"]) -> float:
    """Cross-method only (Lab 10-11 approach): FCFE discounted at cost of equity, FY2025 balance sheet."""
    pv = sum(statements[y]["fcfe"] / (1 + ke) ** i for i, y in enumerate(YEARS, 1))
    tv = statements[YEARS[-1]]["fcfe"] * (1 + g) / (ke - g)
    return (pv + tv / (1 + ke) ** len(YEARS)) / shares


# ---------------------------------------------------------------------------
# LOCKED: checks. Each returns (name, passed, detail). The panel shows red on failure.
# ---------------------------------------------------------------------------
def checks(d: Drivers, s: dict[int, dict[str, float]], v: dict[str, float] | None) -> list[tuple[str, bool, str]]:
    res: list[tuple[str, bool, str]] = []
    worst_gap = max(abs(s[y]["bs_gap"]) for y in YEARS)
    res.append(("Balance sheet balances every year", worst_gap < 1e-6, f"max |gap| = {worst_gap:.6f}"))
    worst_tie = max(abs(s[y]["cash_from_cash_flow"] - s[y]["cash"]) for y in YEARS)
    res.append(("Cash flow ties to balance-sheet cash", worst_tie < 1e-6, f"max |difference| = {worst_tie:.6f}"))
    min_cash = min(s[y]["cash"] for y in YEARS)
    res.append(("Cash stays at or above $100m minimum", min_cash >= MINIMUM_CASH - 1e-6, f"lowest cash = {min_cash:,.1f}"))
    max_rev = max(s[y]["revolver"] for y in YEARS)
    res.append(("Revolver within $3,562m limit", max_rev <= REVOLVER_LIMIT, f"peak revolver = {max_rev:,.1f}"))
    res.append(("Terminal growth below WACC", d.terminal_growth < d.wacc,
                f"g {d.terminal_growth:.2%} vs WACC {d.wacc:.2%}"))
    outside = [k for k, (_, _, lo, hi, _, _) in BOUNDS.items() if not lo - 1e-12 <= getattr(d, k) <= hi + 1e-12]
    res.append(("Drivers inside historical band", not outside, ", ".join(outside) or "all inside"))
    annualized_h1 = FILING["h1_fy2026_adj_ebitda"] * 52 / 28
    gap = s[2026]["ebitda"] / annualized_h1 - 1
    res.append(("FY2026E EBITDA within 15% of H1 FY2026 run-rate", abs(gap) <= 0.15,
                f"model {s[2026]['ebitda']:,.0f} vs run-rate {annualized_h1:,.0f} ({gap:+.1%})"))
    if v is not None:
        bridge = v["enterprise_value"] - v["debt"] - v["other_debt_like"] + v["cash"]
        res.append(("Enterprise-to-equity bridge reconciles",
                    isclose(bridge, v["equity_value"]) and isclose(v["value_per_share"] * v["shares"], v["equity_value"]),
                    f"EV {v['enterprise_value']:,.0f} - debt {v['debt']:,.0f} + cash {v['cash']:,.0f} = {v['equity_value']:,.0f}"))
        res.append(("Terminal value below 85% of EV", v["terminal_share"] < 0.85, f"TV share {v['terminal_share']:.1%}"))
    return res


def base_year_reconciliation() -> list[tuple[str, bool, str]]:
    """Engine opening values must equal the 10-K, and normalizations must be explicit."""
    rows = []
    rows.append(("Normalized revenue = filed revenue - 53rd week",
                 isclose(BASE_REVENUE_52WK + FILING["week53_sales"], FILING["fy2025_revenue"]),
                 f"{BASE_REVENUE_52WK:,.1f} + {FILING['week53_sales']:,.1f} = {FILING['fy2025_revenue']:,.1f}"))
    rows.append(("Normalized SG&A/GP excludes opioid charge",
                 isclose(NORMALIZED_SGA_TO_GP * FILING["fy2025_gross_profit"] + FILING["opioid_charge_pretax"],
                         FILING["fy2025_sga"]), f"{NORMALIZED_SGA_TO_GP:.2%} of gross profit"))
    assets = FILING["fy2025_inventory"] + FILING["fy2025_ppe"] + FILING["fy2025_other_assets"] + FILING["fy2025_cash"]
    liab_eq = FILING["fy2025_debt"] + FILING["fy2025_other_liabilities"] + FILING["fy2025_equity"]
    rows.append(("FY2025 opening balance sheet balances", isclose(assets, liab_eq, abs_tol=0.05),
                 f"assets {assets:,.1f} vs liabilities+equity {liab_eq:,.1f}"))
    return rows


# ---------------------------------------------------------------------------
# Analysis outputs
# ---------------------------------------------------------------------------
def run(d: Drivers = BASE) -> dict:
    s = project(d)
    v = dcf(s, d.wacc, d.terminal_growth) if d.terminal_growth < d.wacc else None
    return {"drivers": asdict(d), "statements": s, "valuation": v, "checks": checks(d, s, v)}


def value(d: Drivers) -> float:
    return dcf(project(d), d.wacc, d.terminal_growth)["value_per_share"]


CASES = {
    "Low: comps stay negative, margin slips": replace(BASE, growth_fy2026=-0.015, growth_long=0.005,
        gross_margin_fy2026=0.265, gross_margin_long=0.265, sga_to_gp_fy2026=0.950, sga_to_gp_long=0.945),
    "Base": BASE,
    "High: turnaround works by FY2028": replace(BASE, growth_fy2026=0.0, growth_long=0.020,
        gross_margin_long=0.273, sga_to_gp_fy2026=0.935, sga_to_gp_long=0.920),
}


def cases() -> dict[str, float]:
    return {name: value(d) for name, d in CASES.items()}


def wacc_growth_grid(waccs=(0.067, 0.072, 0.077, 0.082, 0.087), gs=(0.01, 0.015, 0.02, 0.025)):
    s = project(BASE)
    return {w: {g: dcf(s, w, g)["value_per_share"] for g in gs} for w in waccs}


def tornado(d: Drivers = BASE) -> list[dict]:
    """One-at-a-time: each driver moves to its band low/high, everything else at base."""
    base_s = project(d)
    base_v = dcf(base_s, d.wacc, d.terminal_growth)
    rows = []
    for k, (_, _, lo, hi, unit, basis) in BOUNDS.items():
        r = {"driver": k, "base": getattr(d, k), "low": lo, "high": hi, "unit": unit}
        for side, x in (("at_low", lo), ("at_high", hi)):
            dd = replace(d, **{k: x})
            s = project(dd)
            v = dcf(s, dd.wacc, dd.terminal_growth)
            r[side] = {"value_per_share": v["value_per_share"], "fy2030_ebit": s[2030]["ebit"],
                       "fy2030_fcff": s[2030]["fcff"]}
        r["swing"] = abs(r["at_high"]["value_per_share"] - r["at_low"]["value_per_share"])
        rows.append(r)
    rows.sort(key=lambda r: r["swing"], reverse=True)
    return rows


def reverse_dcf(price: float, driver: str = "sga_to_gp_long", lo: float = 0.85, hi: float = 1.0) -> float:
    """Solve the long-run SG&A/gross-profit ratio that makes value equal the market price."""
    f: Callable[[float], float] = lambda x: value(replace(BASE, **{driver: x})) - price
    a, b = lo, hi
    if f(a) * f(b) > 0:
        raise ValueError("Price is outside the solvable bracket")
    for _ in range(200):
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


def summary(price: float | None = MARKET["price"], price_date: str | None = MARKET["price_date"]) -> dict:
    r = run(BASE)
    out = {
        "as_of": {"bridge_balance_sheet": "2026-09-12", "price_date": price_date,
                  "filings": ["FY2025 10-K (filed 2026-04-27)", "Q1 FY2026 10-Q (filed 2026-07-28)",
                              "Q2 FY2026 earnings release, 8-K (filed 2026-10-13)"]},
        "units": "USD millions except per-share",
        "drivers": r["drivers"],
        "valuation": r["valuation"],
        "cases": cases(),
        "wacc_growth_grid": {f"{w:.1%}": {f"{g:.1%}": round(x, 2) for g, x in row.items()}
                             for w, row in wacc_growth_grid().items()},
        "tornado": [{"driver": t["driver"], "swing": round(t["swing"], 2),
                     "low_value": round(t["at_low"]["value_per_share"], 2),
                     "high_value": round(t["at_high"]["value_per_share"], 2)} for t in tornado()],
        "checks": [{"check": n, "passed": p, "detail": x} for n, p, x in r["checks"] + base_year_reconciliation()],
        "fcfe_cross_method_per_share": fcfe_value(r["statements"]),
        "wacc_build": wacc_build(),
    }
    if price is not None:
        out["market_price"] = price
        out["reverse_dcf_implied_sga_to_gp_long"] = reverse_dcf(price)
    return out


if __name__ == "__main__":
    r = run()
    s, v = r["statements"], r["valuation"]
    print(f"{'USD m':<22}" + "".join(f"FY{y}E".rjust(11) for y in YEARS))
    for lab, k in [("Revenue", "revenue"), ("EBITDA", "ebitda"), ("EBIT", "ebit"), ("Net income", "net_income"),
                   ("FCFF", "fcff"), ("FCFE", "fcfe"), ("Cash", "cash"), ("BS gap", "bs_gap")]:
        print(f"{lab:<22}" + "".join(f"{s[y][k]:>11,.1f}" for y in YEARS))
    print(f"\nEV {v['enterprise_value']:,.0f} | equity {v['equity_value']:,.0f} | "
          f"${v['value_per_share']:.2f}/share | TV share {v['terminal_share']:.1%}")
    for n, p, x in r["checks"] + base_year_reconciliation():
        print(("PASS " if p else "FAIL ") + n + " - " + x)
    print("\nCases:", {k: round(x, 2) for k, x in cases().items()})
    print("FCFE cross-method:", round(fcfe_value(s), 2))
    for t in tornado():
        print(f"{t['driver']:<22} swing ${t['swing']:.2f}  ({t['at_low']['value_per_share']:.2f} to {t['at_high']['value_per_share']:.2f})")
