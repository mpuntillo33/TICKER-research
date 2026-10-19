"""Comparable-company check for ACI: one enterprise-value multiple (EV/EBITDA) and one equity
multiple (P/E, carried from Lab 08). USD millions except per share. Standard library only.

Peer policy (written in Lab 08 before peers were selected, unchanged): admit U.S.-listed conventional
food-and-drug supermarket operators with positive annual GAAP EPS; qualify (not exclude) peers with
materially different format/growth. Kroger = use; Sprouts = qualified endpoint.

ONE definition applied to all three companies (multiple-definition consistency):
  EV       = market cap + (provider total debt - all lease liabilities) - cash & equivalents
  EBITDA   = provider EBITDA, trailing twelve months
Source for every field: stockanalysis.com (S&P Global Market Intelligence data), retrieved Oct 19, 2026.
Leases are excluded from debt for every company because provider EBITDA is after operating-lease rent;
including lease liabilities in EV while EBITDA is after rent would mismatch numerator and denominator.
"""
from __future__ import annotations

from statistics import median

COMPANIES = {
    # ticker: market cap, debt excl. leases, cash, EBITDA TTM, balance-sheet date, price note
    "ACI": {"market_cap": 6_353.0, "debt_ex_leases": 746.1 + 8_009.0, "cash": 293.4, "ebitda_ttm": 3_440.0,
            "bs_date": "2026-06-20", "price": "13.09 close 2026-10-16", "role": "target"},
    "KR":  {"market_cap": 37_170.0, "debt_ex_leases": 1_452.0 + 13_915.0, "cash": 1_676.0, "ebitda_ttm": 8_040.0,
            "bs_date": "2026-08-15", "price": "62.93 intraday 2026-10-19", "role": "use"},
    "SFM": {"market_cap": 5_980.0, "debt_ex_leases": 99.18, "cash": 223.93, "ebitda_ttm": 842.36,
            "bs_date": "2026-06-28", "price": "64.17 intraday 2026-10-19", "role": "qualified"},
}
ACI_SHARES = 488.2  # same diluted basis as the DCF
OPIOID_OBLIGATION = 773.8  # same debt-like claim as the DCF bridge (FY2025 10-K Note 12)


def ev(c: dict) -> float:
    return c["market_cap"] + c["debt_ex_leases"] - c["cash"]


def ev_ebitda(t: str) -> float:
    c = COMPANIES[t]
    if c["ebitda_ttm"] <= 0:
        raise ValueError(f"{t}: EV/EBITDA not meaningful for nonpositive EBITDA")
    return ev(c) / c["ebitda_ttm"]


def implied_aci_value(multiple: float) -> float:
    a = COMPANIES["ACI"]
    equity = multiple * a["ebitda_ttm"] - (a["debt_ex_leases"] - a["cash"]) - OPIOID_OBLIGATION
    return equity / ACI_SHARES


def results() -> dict:
    peers = [t for t, c in COMPANIES.items() if c["role"] != "target"]
    mult = {t: ev_ebitda(t) for t in COMPANIES}
    peer_mults = [mult[t] for t in peers]
    return {
        "multiples": mult,
        "aci_own_multiple": mult["ACI"],
        "implied_low": implied_aci_value(min(peer_mults)),
        "implied_median": implied_aci_value(median(peer_mults)),
        "implied_high": implied_aci_value(max(peer_mults)),
        "pe_lab08": {"low": 5.44, "median": 10.11, "high": 14.77, "as_of": "2026-09-10"},
    }


def consistency_checks() -> list[tuple[str, bool, str]]:
    out = []
    for t, c in COMPANIES.items():
        rebuilt = c["market_cap"] + c["debt_ex_leases"] - c["cash"]
        out.append((f"{t}: EV uses the shared definition", abs(rebuilt - ev(c)) < 1e-9, f"EV {rebuilt:,.0f}"))
    a = COMPANIES["ACI"]
    out.append(("ACI implied value at its own multiple round-trips the bridge",
                abs(implied_aci_value(ev_ebitda("ACI")) * ACI_SHARES + OPIOID_OBLIGATION - a["market_cap"]) < 1e-6,
                "market cap = implied equity + opioid claim"))
    return out


if __name__ == "__main__":
    r = results()
    for t, m in r["multiples"].items():
        c = COMPANIES[t]
        print(f"{t:<4} {c['role']:<9} EV {ev(c):>9,.0f}  EBITDA {c['ebitda_ttm']:>7,.0f}  EV/EBITDA {m:5.2f}x  (BS {c['bs_date']})")
    print(f"ACI implied from peers: ${r['implied_low']:.2f} - ${r['implied_high']:.2f} (median ${r['implied_median']:.2f})")
    for n, ok, x in consistency_checks():
        print(("PASS " if ok else "FAIL ") + n + " - " + x)
