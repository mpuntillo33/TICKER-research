"""Project 2 engine: every number in the app and the memo comes from this module.

Education only, not investment advice.

Conventions (one definition used everywhere):
- Weights are fractions of the portfolio, long-only, on a 5-point grid.
- Returns are annual, nominal, in decimals (0.065 = 6.5%).
- Expected returns (base method "point-in-time"): yields as known on the decision
  date, net of each ETF's expense ratio. Equity = T-bill yield + equity risk premium.
- Risk (volatility, correlations, worst 12-month loss) comes from monthly
  adjusted-close history. Adjusted-close returns are already net of fund fees,
  so fees are NOT subtracted again from historical estimates.
"""
from __future__ import annotations

import copy
import csv
import math
from dataclasses import dataclass, field, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRICES_CSV = ROOT / "data" / "prices.csv"
RATES_CSV = ROOT / "data" / "rates_as_known.csv"

TICKERS = ["BIL", "IEF", "LQD", "VT"]
NAMES = {
    "BIL": "1-3 month T-bills",
    "IEF": "7-10 year Treasuries",
    "LQD": "Investment-grade corporates",
    "VT": "Global equity",
}
# Gross expense ratios, % per year (issuer pages, checked 2026-11-23).
EXPENSE_RATIO_PCT = {"BIL": 0.1353, "IEF": 0.15, "LQD": 0.14, "VT": 0.06}

# Mandate (Lab 13), made numeric.
MANDATE = {
    "objective": "CPI + 4% net of costs over rolling five-year periods",
    "cpi_assumption": 0.025,          # planning assumption, not a forecast
    "real_return_target": 0.04,
    "reserve_eligible": {"BIL", "IEF"},
    "reserve_minimum": 0.03,          # 4 quarters x $0.75m / $100m reserve
    "liquid_within_5_days_minimum": 0.90,
    "issuer_limit": 0.08,             # funds and Treasuries are exempt
    "benchmark": {"BIL": 0.0, "IEF": 0.0, "LQD": 0.40, "VT": 0.60},
    "risk_measure": "annualized volatility of monthly returns",
    # Risk limit: no more volatile than the 40/60 benchmark.
}
# Every holding is a daily-traded ETF that settles T+1, a diversified fund or
# Treasury fund, so liquidity is 100% and the issuer limit cannot bind.
DAYS_TO_CASH = {"BIL": 1, "IEF": 1, "LQD": 1, "VT": 1}


@dataclass
class Inputs:
    """Every driver the committee can move. Defaults are the base case."""
    decision_date: str = "2026-10-05"
    method: str = "point-in-time"      # or "historical"
    window_months: int = 59            # all 59 monthly returns; history used for risk (and for returns if historical)
    equity_risk_premium: float = 0.040 # over the T-bill yield
    lqd_credit_haircut: float = 0.0075 # Baa yield -> expected LQD return (losses, rating mix)
    tbill_yield_override: float | None = None  # replace the DGS3MO signal (decimal)
    extra_cost: float = 0.0            # trading/advice drag on every sleeve, per year
    reserve_minimum: float = MANDATE["reserve_minimum"]
    step: float = 0.05
    rates_overrides: dict = field(default_factory=dict)


# ---------- data ----------

def load_prices(path=PRICES_CSV):
    """Monthly adjusted closes, oldest first. Fails loudly on bad data."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("prices.csv has no rows.")
    if list(rows[0])[0] != "Date" or [c for c in rows[0] if c != "Date"] != TICKERS:
        raise ValueError(f"prices.csv must have columns Date,{','.join(TICKERS)}.")
    dates = [r["Date"] for r in rows]
    if dates != sorted(dates) or len(set(dates)) != len(dates):
        raise ValueError("prices.csv dates must be unique and oldest first.")
    prices = {t: [float(r[t]) for r in rows] for t in TICKERS}
    for t, p in prices.items():
        if any(x <= 0 for x in p):
            raise ValueError(f"Non-positive price for {t}.")
    return dates, prices


def monthly_returns(prices):
    return {t: [b / a - 1 for a, b in zip(p, p[1:])] for t, p in prices.items()}


def load_rates(path=RATES_CSV):
    """Rows: series_id, observation_date, value_pct, as_known_on, source."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return rows


def rate_as_known(rows, series_id, decision_date):
    """Latest observation of series_id whose vintage was known on decision_date.

    Point-in-time rule (Lab 16/17): admit only values published on or before the
    decision date; carry forward the most recent available observation.
    """
    eligible = [r for r in rows if r["series_id"] == series_id
                and r["as_known_on"] <= decision_date
                and r["observation_date"] <= decision_date]
    if not eligible:
        raise ValueError(f"No {series_id} value was known on {decision_date}.")
    best = max(eligible, key=lambda r: (r["observation_date"], r["as_known_on"]))
    return float(best["value_pct"]) / 100, best


# ---------- estimates ----------

def risk_estimates(returns, window):
    if window < 12 or window > len(returns[TICKERS[0]]):
        raise ValueError(f"Window must be 12 to {len(returns[TICKERS[0]])} months.")
    r = {t: v[-window:] for t, v in returns.items()}
    mean = {t: sum(v) / window for t, v in r.items()}
    sd = {t: math.sqrt(sum((x - mean[t]) ** 2 for x in v) / (window - 1)) for t, v in r.items()}
    corr = {a: {b: 1.0 if a == b else
                sum((x - mean[a]) * (y - mean[b]) for x, y in zip(r[a], r[b]))
                / ((window - 1) * sd[a] * sd[b]) for b in TICKERS} for a in TICKERS}
    vol = {t: sd[t] * math.sqrt(12) for t in TICKERS}
    hist_return = {t: mean[t] * 12 for t in TICKERS}
    return vol, corr, hist_return


def expected_returns(inp: Inputs, rates, hist_return):
    """Return (expected returns by ticker, lineage rows for the data card)."""
    fee = {t: EXPENSE_RATIO_PCT[t] / 100 for t in TICKERS}
    lineage = []
    if inp.method == "historical":
        er = dict(hist_return)  # adjusted closes are already net of fees
        for t in TICKERS:
            lineage.append((t, f"mean monthly return x 12, last {inp.window_months} months", er[t]))
    elif inp.method == "point-in-time":
        y = {}
        for sid in ("DGS3MO", "DGS10", "BAA"):
            if sid in inp.rates_overrides:
                y[sid] = inp.rates_overrides[sid]
                lineage.append((sid, "override entered in the app", y[sid]))
            else:
                y[sid], row = rate_as_known(rates, sid, inp.decision_date)
                lineage.append((sid, f"obs {row['observation_date']}, known {row['as_known_on']}, {row['source']}", y[sid]))
        if inp.tbill_yield_override is not None:
            y["DGS3MO"] = inp.tbill_yield_override
            lineage.append(("DGS3MO", "locked/changed-input override", y["DGS3MO"]))
        er = {
            "BIL": y["DGS3MO"] - fee["BIL"],
            "IEF": y["DGS10"] - fee["IEF"],
            "LQD": y["BAA"] - inp.lqd_credit_haircut - fee["LQD"],
            "VT": y["DGS3MO"] + inp.equity_risk_premium - fee["VT"],
        }
    else:
        raise ValueError("method must be 'point-in-time' or 'historical'.")
    er = {t: v - inp.extra_cost for t, v in er.items()}
    return er, lineage


# ---------- portfolio math ----------

def port_return(w, er):
    return sum(w[t] * er[t] for t in TICKERS)


def port_vol(w, vol, corr):
    var = sum(w[a] * w[b] * corr[a][b] * vol[a] * vol[b] for a in TICKERS for b in TICKERS)
    return math.sqrt(max(var, 0.0))


def worst_12m(w, returns, window):
    """Worst compounded 12-month return of the fixed-weight mix (monthly rebalanced)."""
    r = [sum(w[t] * returns[t][i] for t in TICKERS) for i in range(len(returns[TICKERS[0]]))][-window:]
    worst = None
    for i in range(len(r) - 11):
        g = 1.0
        for x in r[i:i + 12]:
            g *= 1 + x
        worst = g - 1 if worst is None else min(worst, g - 1)
    return worst


def grid(step):
    units = round(1 / step)
    if not math.isclose(units * step, 1.0):
        raise ValueError("step must divide 100% exactly.")
    for a in range(units + 1):
        for b in range(units + 1 - a):
            for c in range(units + 1 - a - b):
                d = units - a - b - c
                yield {"BIL": a * step, "IEF": b * step, "LQD": c * step, "VT": d * step}


def check_mandate(w, er, vol, corr, inp, objective, risk_limit):
    """Every rule, its measured value, and pass/fail."""
    reserve = sum(w[t] for t in MANDATE["reserve_eligible"])
    liquid = sum(w[t] for t in TICKERS if DAYS_TO_CASH[t] <= 5)
    ret, v = port_return(w, er), port_vol(w, vol, corr)
    rules = [
        ("Return objective", ret, objective, ret + 1e-12 >= objective),
        ("Reserve-eligible weight", reserve, inp.reserve_minimum, reserve + 1e-12 >= inp.reserve_minimum),
        ("Volatility vs benchmark", v, risk_limit, v <= risk_limit + 1e-12),
        ("Liquid within 5 days", liquid, MANDATE["liquid_within_5_days_minimum"], liquid >= MANDATE["liquid_within_5_days_minimum"]),
        ("Long-only, sums to 100%", min(w.values()), 0.0, min(w.values()) >= 0 and math.isclose(sum(w.values()), 1.0)),
    ]
    return rules


def search(er, vol, corr, inp, objective, risk_limit, use_risk_limit=True):
    """Lowest-volatility grid mix that passes every rule; None if none passes."""
    best = None
    for w in grid(inp.step):
        if port_return(w, er) + 1e-12 < objective:
            continue
        if sum(w[t] for t in MANDATE["reserve_eligible"]) + 1e-12 < inp.reserve_minimum:
            continue
        v = port_vol(w, vol, corr)
        if use_risk_limit and v > risk_limit + 1e-12:
            continue
        if best is None or v < best[1] - 1e-12:
            best = (w, v)
    return None if best is None else best[0]


def equal_weight():
    return {t: 0.25 for t in TICKERS}


# ---------- one full run ----------

def run(inp: Inputs | None = None, prices_path=PRICES_CSV, rates_path=RATES_CSV):
    inp = inp or Inputs()
    dates, prices = load_prices(prices_path)
    returns = monthly_returns(prices)
    vol, corr, hist = risk_estimates(returns, inp.window_months)
    er, lineage = expected_returns(inp, load_rates(rates_path), hist)
    objective = MANDATE["cpi_assumption"] + MANDATE["real_return_target"]
    bench = MANDATE["benchmark"]
    risk_limit = port_vol(bench, vol, corr)
    portfolios = {
        "Equal weight (baseline 1)": equal_weight(),
        "40/60 LQD/VT benchmark (baseline 2)": dict(bench),
    }
    best = search(er, vol, corr, inp, objective, risk_limit)
    portfolios["Constrained lowest-risk mix"] = best
    rows = {}
    for name, w in portfolios.items():
        if w is None:
            rows[name] = None
            continue
        rules = check_mandate(w, er, vol, corr, inp, objective, risk_limit)
        rows[name] = {
            "weights": w,
            "return": port_return(w, er),
            "volatility": port_vol(w, vol, corr),
            "worst_12m": worst_12m(w, returns, inp.window_months),
            "reserve": sum(w[t] for t in MANDATE["reserve_eligible"]),
            "rules": rules,
            "passes": all(r[3] for r in rules),
            "failed": [r[0] for r in rules if not r[3]],
        }
    return {
        "inputs": inp, "dates": dates, "price_months": (dates[0], dates[-1]),
        "expected_returns": er, "volatility": vol, "correlations": corr,
        "historical_returns": hist, "lineage": lineage, "objective": objective,
        "risk_limit": risk_limit, "portfolios": rows,
    }


# ---------- stress, range, decision ----------

STRESS_CASES = [
    ("Base case", {}),
    ("Equity premium -1 pt (3%)", {"equity_risk_premium": 0.030}),
    ("Equity premium +1 pt (5%)", {"equity_risk_premium": 0.050}),
    ("T-bill signal -50 bp", {"tbill_shift": -0.005}),
    ("T-bill signal +50 bp", {"tbill_shift": 0.005}),
    ("Risk window: last 36 months", {"window_months": 36}),
    ("Costs +25 bp per year", {"extra_cost": 0.0025}),
    ("Costs +50 bp per year", {"extra_cost": 0.0050}),
    ("Reserve minimum 10%", {"reserve_minimum": 0.10}),
    ("Historical returns, full 59 months", {"method": "historical", "window_months": 59}),
]
SWING_LIMIT = 0.25  # a single-input stress that moves any weight >= 25 pts stops adoption


def _apply(base: Inputs, change: dict):
    inp = replace(base, rates_overrides=copy.deepcopy(base.rates_overrides))
    change = dict(change)
    shift = change.pop("tbill_shift", None)
    for k, v in change.items():
        setattr(inp, k, v)
    if shift is not None:
        base_y = base.tbill_yield_override
        if base_y is None:
            base_y, _ = rate_as_known(load_rates(), "DGS3MO", base.decision_date)
        inp.tbill_yield_override = base_y + shift
    return inp


def max_swing(a, b):
    return max(abs(a[t] - b[t]) for t in TICKERS)


def stress(base: Inputs | None = None):
    base = base or Inputs()
    base_run = run(base)
    base_w = base_run["portfolios"]["Constrained lowest-risk mix"]
    base_w = base_w["weights"] if base_w else None
    out = []
    for label, change in STRESS_CASES:
        r = run(_apply(base, change))
        p = r["portfolios"]["Constrained lowest-risk mix"]
        w = p["weights"] if p else None
        swing = max_swing(w, base_w) if (w and base_w) else None
        out.append({"case": label, "feasible": w is not None, "weights": w,
                    "return": p["return"] if p else None,
                    "volatility": p["volatility"] if p else None,
                    "swing": swing})
    return base_run, out


def allocation_range(cases):
    """Range rule: min-max weight across every stress case that stays feasible."""
    feas = [c["weights"] for c in cases if c["feasible"]]
    if not feas:
        return None
    return {t: (min(w[t] for w in feas), max(w[t] for w in feas)) for t in TICKERS}


def decision(base_run, cases):
    """Decision rule, applied mechanically; the analyst still owns the call.

    REJECT   - the base case has no mix that passes every mandate rule.
    PILOT    - base passes, but a stress case is infeasible or swings a weight >= 25 pts.
    ALLOCATE - base passes and every stress case stays feasible within 25 pts.
    """
    if base_run["portfolios"]["Constrained lowest-risk mix"] is None:
        return "REJECT", ["No mix passes the mandate in the base case."]
    reasons = []
    for c in cases[1:]:
        if not c["feasible"]:
            reasons.append(f"{c['case']}: no feasible mix (stop condition).")
        elif c["swing"] is not None and c["swing"] >= SWING_LIMIT - 1e-12:
            reasons.append(f"{c['case']}: moves a weight {c['swing']*100:.0f} pts (stop condition).")
    return ("PILOT" if reasons else "ALLOCATE"), reasons


# ---------- visible output ----------

def pct(x, d=2):
    return "n/a" if x is None else f"{x*100:.{d}f}%"


def fmt_w(w):
    return " / ".join(f"{t} {w[t]*100:.0f}%" for t in TICKERS)


def report(base: Inputs | None = None):
    base = base or Inputs()
    base_run, cases = stress(base)
    rng = allocation_range(cases)
    action, reasons = decision(base_run, cases)
    i = base_run["inputs"]
    L = [
        "# Project 2 visible output",
        "",
        "Built with Claude (Anthropic) assisting code and drafting; the analysis and decision are Max Puntillo's. Education only, not investment advice.",
        "",
        f"- Decision date (as known on): **{i.decision_date}**",
        f"- Price history: monthly adjusted closes {base_run['price_months'][0]} to {base_run['price_months'][1]}; risk window {i.window_months} months",
        f"- Expected-return method: {i.method}; equity premium {pct(i.equity_risk_premium)}; LQD credit haircut {pct(i.lqd_credit_haircut)}; extra costs {pct(i.extra_cost)}",
        f"- Objective: {pct(base_run['objective'])} nominal (2.5% CPI planning assumption + 4%); reserve minimum {pct(i.reserve_minimum,0)}; volatility limit = benchmark {pct(base_run['risk_limit'])}",
        "",
        "## Inputs",
        "",
        "| Sleeve | Expected return | Volatility |",
        "|---|---:|---:|",
    ]
    for t in TICKERS:
        L.append(f"| {t} ({NAMES[t]}) | {pct(base_run['expected_returns'][t])} | {pct(base_run['volatility'][t])} |")
    L += ["", "Lineage:", ""]
    for sid, src, val in base_run["lineage"]:
        L.append(f"- {sid} = {pct(val)} ({src})")
    L += ["", "## Portfolios and mandate verdicts", "",
          "| Portfolio | Weights | Return | Volatility | Worst 12 mo | Verdict |",
          "|---|---|---:|---:|---:|---|"]
    for name, p in base_run["portfolios"].items():
        if p is None:
            L.append(f"| {name} | none feasible | | | | FAIL |")
            continue
        v = "PASS" if p["passes"] else "FAIL: " + ", ".join(p["failed"])
        L.append(f"| {name} | {fmt_w(p['weights'])} | {pct(p['return'])} | {pct(p['volatility'])} | {pct(p['worst_12m'],1)} | {v} |")
    L += ["", "## Stress run", "", "| Case | Constrained mix | Return | Volatility | Largest weight move |",
          "|---|---|---:|---:|---:|"]
    for c in cases:
        mix = fmt_w(c["weights"]) if c["feasible"] else "NO FEASIBLE MIX"
        sw = "" if c["swing"] is None else f"{c['swing']*100:.0f} pts"
        L.append(f"| {c['case']} | {mix} | {pct(c['return'])} | {pct(c['volatility'])} | {sw} |")
    L += ["", "## Allocation range (rule: min to max across feasible stress cases)", ""]
    if rng:
        for t in TICKERS:
            L.append(f"- {t}: {rng[t][0]*100:.0f}% to {rng[t][1]*100:.0f}%")
    L += ["", f"## Decision rule output: **{action}**", ""]
    L += [f"- {r}" for r in reasons] or ["- No stop condition fired."]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Project 2 engine (education only).")
    ap.add_argument("--tbill-yield", type=float, help="Override DGS3MO, in percent (e.g. 3.69)")
    ap.add_argument("--equity-premium", type=float, help="Equity risk premium, in percent")
    ap.add_argument("--window", type=int, help="Risk window in months")
    ap.add_argument("--lqd-haircut", type=float, help="Baa-to-LQD credit haircut, in percent")
    ap.add_argument("--cost", type=float, help="Extra annual cost drag, in percent")
    ap.add_argument("--reserve-min", type=float, help="Reserve minimum, in percent")
    ap.add_argument("--out", help="Write the report to this Markdown file")
    a = ap.parse_args()
    inp = Inputs()
    if a.tbill_yield is not None:
        inp.tbill_yield_override = a.tbill_yield / 100
    if a.equity_premium is not None:
        inp.equity_risk_premium = a.equity_premium / 100
    if a.window is not None:
        inp.window_months = a.window
    if a.lqd_haircut is not None:
        inp.lqd_credit_haircut = a.lqd_haircut / 100
    if a.cost is not None:
        inp.extra_cost = a.cost / 100
    if a.reserve_min is not None:
        inp.reserve_minimum = a.reserve_min / 100
    text = report(inp)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(text, encoding="utf-8")
    print(text)
