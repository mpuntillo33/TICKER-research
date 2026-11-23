"""Project 2 committee app. Run: streamlit run app.py

All math lives in engine.py; this file only collects inputs and renders results.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

import engine as e

st.set_page_config(page_title="Project 2 - Reserve Portfolio Committee App", layout="wide")

st.info(
    "**AI use:** Built with Claude (Anthropic, Claude Opus 5.5) assisting code, tests and drafting. "
    "The mandate, assumptions, analysis and decision are Max Puntillo's. "
    "**Education only, not investment advice.**"
)
st.title("Reserve portfolio: allocate, pilot or reject?")
st.caption("FIN 43900 Project 2 · Max Puntillo · universe BIL / IEF / LQD / VT")

# ---------------- inputs ----------------
rates = e.load_rates()
dates_known = sorted({r["as_known_on"] for r in rates})
base = e.Inputs()
with st.sidebar:
    st.header("Committee drivers")
    st.caption("Defaults are the base case. Every change re-runs the engine and the stress table.")
    decision_date = st.selectbox("Decision date (as known on)", dates_known,
                                 index=dates_known.index(base.decision_date))
    method = st.radio("Expected-return method", ["point-in-time", "historical"], index=0,
                      help="Point-in-time: yields known on the decision date. Historical: mean past returns.")
    erp = st.slider("Equity risk premium over T-bills (%)", 2.0, 6.0, base.equity_risk_premium * 100, 0.25)
    haircut = st.slider("LQD credit haircut from Baa yield (%)", 0.0, 2.0, base.lqd_credit_haircut * 100, 0.25)
    use_override = st.checkbox("Override the DGS3MO T-bill signal")
    tbill = None
    if use_override:
        tbill = st.number_input("DGS3MO T-bill yield (%)", 0.0, 10.0, 4.19, 0.05) / 100
    window = st.slider("Risk window (months of history)", 24, 59, base.window_months)
    cost = st.slider("Extra cost drag (% per year)", 0.0, 1.0, 0.0, 0.05)
    reserve = st.slider("Reserve minimum (%)", 0.0, 20.0, base.reserve_minimum * 100, 1.0)

inp = e.Inputs(decision_date=decision_date, method=method, window_months=window,
               equity_risk_premium=erp / 100, lqd_credit_haircut=haircut / 100,
               tbill_yield_override=tbill, extra_cost=cost / 100, reserve_minimum=reserve / 100)

try:
    run, cases = e.stress(inp)
except ValueError as err:
    st.error(f"Input rejected by the engine: {err}")
    st.stop()

rng = e.allocation_range(cases)
action, reasons = e.decision(run, cases)
best = run["portfolios"]["Constrained lowest-risk mix"]

# ---------------- decision ----------------
colour = {"ALLOCATE": "success", "PILOT": "warning", "REJECT": "error"}[action]
msg = f"Decision rule output: **{action}**"
if best:
    msg += f" · constrained mix {e.fmt_w(best['weights'])} · expected return {e.pct(best['return'])} · volatility {e.pct(best['volatility'])}"
getattr(st, colour)(msg)
if reasons:
    st.markdown("**Stop conditions that fired:**\n" + "\n".join(f"- {r}" for r in reasons))
else:
    st.markdown("No stop condition fired.")
st.caption("Rule: REJECT if no mix passes the mandate; PILOT if any stress case is infeasible or moves a weight ≥ 25 pts; otherwise ALLOCATE. The analyst owns the final call (see docs/decision-memo.md).")

tab1, tab2, tab3, tab4 = st.tabs(["Portfolios & mandate", "Stress & range", "Inputs & data card", "Export"])

with tab1:
    st.subheader("Mandate")
    st.markdown(
        f"- **Objective:** {e.MANDATE['objective']}; modeled as {e.pct(run['objective'])} nominal "
        f"(2.5% CPI planning assumption + 4%).\n"
        f"- **Universe:** {', '.join(f'{t} ({e.NAMES[t]})' for t in e.TICKERS)}; long-only, 5-point grid.\n"
        f"- **Benchmark:** 40% LQD / 60% VT.\n"
        f"- **Risk measure and limit:** {e.MANDATE['risk_measure']} ≤ benchmark ({e.pct(run['risk_limit'])}); "
        f"worst 12-month loss reported.\n"
        f"- **Limits:** reserve-eligible (BIL + IEF) ≥ {e.pct(inp.reserve_minimum, 0)}; ≥ 90% liquid within 5 days; "
        f"8% single-issuer limit (funds and Treasuries exempt, so it cannot bind here)."
    )
    st.subheader("Two baselines and the constrained portfolio")
    rows = []
    for name, p in run["portfolios"].items():
        if p is None:
            rows.append({"Portfolio": name, "Weights": "no feasible mix", "Verdict": "FAIL"})
            continue
        rows.append({
            "Portfolio": name, "Weights": e.fmt_w(p["weights"]),
            "Expected return": e.pct(p["return"]), "Volatility": e.pct(p["volatility"]),
            "Worst 12 mo": e.pct(p["worst_12m"], 1), "Reserve": e.pct(p["reserve"], 0),
            "Verdict": "PASS" if p["passes"] else "FAIL: " + ", ".join(p["failed"]),
        })
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    with st.expander("Rule-by-rule checks"):
        for name, p in run["portfolios"].items():
            if p is None:
                continue
            st.markdown(f"**{name}**")
            st.dataframe(pd.DataFrame([{"Rule": r[0], "Measured": e.pct(r[1]), "Limit": e.pct(r[2]),
                                        "Result": "PASS" if r[3] else "FAIL"} for r in p["rules"]]),
                         hide_index=True, width="stretch")

with tab2:
    st.subheader("Stress run: estimates, window, costs, constraints")
    st.dataframe(pd.DataFrame([{
        "Case": c["case"],
        "Constrained mix": e.fmt_w(c["weights"]) if c["feasible"] else "NO FEASIBLE MIX",
        "Return": e.pct(c["return"]), "Volatility": e.pct(c["volatility"]),
        "Largest weight move": "" if c["swing"] is None else f"{c['swing']*100:.0f} pts",
        "Stop?": "STOP" if (not c["feasible"] or (c["swing"] or 0) >= e.SWING_LIMIT - 1e-12) else "",
    } for c in cases]), hide_index=True, width="stretch")
    st.subheader("Allocation range")
    st.caption("Rule: for each sleeve, the minimum to maximum weight across every stress case that still passes the mandate.")
    if rng:
        st.dataframe(pd.DataFrame([{"Sleeve": t, "Low": f"{rng[t][0]*100:.0f}%", "High": f"{rng[t][1]*100:.0f}%",
                                    "Base": f"{best['weights'][t]*100:.0f}%" if best else ""} for t in e.TICKERS]),
                     hide_index=True, width="stretch")
    st.subheader("Monitoring triggers")
    st.markdown(
        "- **Re-run:** DGS3MO as known moves ≥ 50 bp from the decision-date value, or each quarter.\n"
        "- **Rebalance:** any sleeve drifts ≥ 5 pts from target.\n"
        "- **Pause:** a re-run shows no feasible mix, or a single input change swings a weight ≥ 25 pts.\n"
        "- **Reject:** the reserve rule or volatility limit is breached at quarter-end, or the point-in-time "
        "audit finds a material revision overlapping the decision date."
    )

with tab3:
    st.subheader("Inputs used")
    st.dataframe(pd.DataFrame([{"Sleeve": f"{t} ({e.NAMES[t]})",
                                "Expected return": e.pct(run["expected_returns"][t]),
                                "Volatility": e.pct(run["volatility"][t]),
                                "Historical mean (reference)": e.pct(run["historical_returns"][t]),
                                "Expense ratio": f"{e.EXPENSE_RATIO_PCT[t]:.4g}%"} for t in e.TICKERS]),
                 hide_index=True, width="stretch")
    st.markdown("**Lineage of each yield**")
    for sid, src, val in run["lineage"]:
        st.markdown(f"- {sid} = {e.pct(val)} — {src}")
    st.subheader("Data card: DGS3MO point-in-time signal")
    st.markdown(
        "| Field | Value |\n|---|---|\n"
        "| Source | Federal Reserve Bank of St. Louis, FRED/ALFRED series DGS3MO |\n"
        "| Measures | Market yield on 3-month constant-maturity Treasuries |\n"
        "| Units | Percent per year, not seasonally adjusted, daily business days |\n"
        "| As-of rule | Use the latest observation published on or before the decision date (ALFRED vintage); carry forward the last business day |\n"
        "| Lag / revisions | Near same-day market rate; Lab 17 audit found no material revisions; quarantine if one overlaps the decision |\n"
        "| How it enters | BIL expected return = DGS3MO − 0.1353% fee; VT expected return = DGS3MO + equity premium − 0.06% fee |\n"
        "| Values checked by hand | 2 Oct 2026 = 4.19%; 5 Oct = 4.22%; 6 Oct = 4.21% (FRED page, checked 29 Oct 2026) |\n"
        "| Licensing | FRED data are public; series used per FRED terms with attribution |"
    )
    st.caption(f"Prices: data/prices.csv, monthly adjusted closes {run['price_months'][0]} to {run['price_months'][1]}, "
               "Yahoo Finance, downloaded 2026-10-20. Adjusted closes already net of fund fees.")

with tab4:
    st.subheader("Visible output")
    text = e.report(inp)
    st.download_button("Download this run as Markdown", text, file_name="visible_output.md")
    if st.button("Save to output/app_run.md"):
        out = Path(__file__).resolve().parent / "output" / "app_run.md"
        out.parent.mkdir(exist_ok=True)
        out.write_text(text, encoding="utf-8")
        st.success(f"Saved {out.name}")
    st.code(text, language="markdown")
