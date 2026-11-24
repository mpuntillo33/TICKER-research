"""Streamlit presentation layer for the Lab 19 Legend Panel."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

HERE = Path(__file__).parent
SCRIPT = HERE / "legend_panel.py"
NUMBER = re.compile(r"(?<![\w.])\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?%?|(?<![\w.])\d+(?:\.\d+)?%?")


def path_for(ticker: str) -> Path:
    return HERE / f"{ticker.upper()}_legend_panel.json"


def printed_number_tokens(report: dict) -> set[str]:
    """Tokens produced by legend_panel.py's fact and check printout."""
    tokens = {"10", "5"}  # Source line and threshold label printed by the script.
    for row in report["rows"]:
        tokens.add(row["fiscal_year_end"])
        for field in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "liabilities", "research_and_development", "owner_earnings"):
            value = row[field]
            if not isinstance(value, str): tokens.update({f"{value:,.0f}", f"{value:.0f}"})
        for field in ("roe", "rd_to_revenue"):
            value = row[field]
            if not isinstance(value, str): tokens.add(f"{value * 100:.2f}%")
        value = row["liabilities_to_equity"]
        if not isinstance(value, str): tokens.add(f"{value:.2f}")
    for checks in report["panel"].values():
        for label in checks: tokens.update(x.lstrip("$") for x in NUMBER.findall(label))
    revenues = [row["revenue"] for row in report["rows"]]
    if len(revenues) == 5 and all(not isinstance(value, str) for value in revenues) and revenues[0] > 0:
        tokens.add(f"{((revenues[-1] / revenues[0]) ** .25 - 1) * 100:.2f}%")
    return tokens


def unprinted_numbers(memo: str, report: dict) -> list[str]:
    allowed = printed_number_tokens(report)
    fiscal_years = {row["fiscal_year_end"][-4:] for row in report["rows"]}
    return sorted({match for match in NUMBER.findall(memo) if match.lstrip("$") not in allowed and match not in fiscal_years})


def shown(value: object, pct: bool = False) -> object:
    if isinstance(value, str): return value
    return f"{value * 100:.1f}%" if pct else f"{value:,.0f}"


st.set_page_config(page_title="Lab 19 Legend Panel", layout="wide")
st.title("Lab 19 — Legend Panel")
st.caption("SEC EDGAR 10-K facts only · learning demonstration, not investment advice")
ticker = st.text_input("Ticker", "COST").strip().upper()
user_agent = st.text_input("SEC User-Agent (truthful name and email)", os.environ.get("SEC_USER_AGENT", ""), type="password")

if st.button("Download 10-K facts and run panel", type="primary"):
    run = subprocess.run([sys.executable, str(SCRIPT), ticker, "--output", str(path_for(ticker)), "--user-agent", user_agent], capture_output=True, text=True)
    if run.returncode: st.error(run.stderr or run.stdout)
    else: st.success("Saved panel report."); st.code(run.stdout)

report_file = path_for(ticker)
if not report_file.exists():
    st.info(f"No panel report for {ticker}. Download facts first.")
    st.stop()
report = json.loads(report_file.read_text(encoding="utf-8"))
st.subheader(f"{report['company']} ({report['ticker']})")
st.caption(f"{report['source']} · retrieved {report['retrieved_at_utc']}")

facts = []
for row in report["rows"]:
    facts.append({"FY end": row["fiscal_year_end"], "Revenue": shown(row["revenue"]), "Net income": shown(row["net_income"]), "Operating cash flow": shown(row["operating_cash_flow"]), "Capex": shown(row["capital_spending"]), "Equity": shown(row["equity"]), "Liabilities": shown(row["liabilities"]), "R&D": shown(row["research_and_development"]), "ROE": shown(row["roe"], True), "Owner earnings": shown(row["owner_earnings"]), "R&D ÷ revenue": shown(row["rd_to_revenue"], True), "Liabilities ÷ equity": "not known" if isinstance(row["liabilities_to_equity"], str) else f"{row['liabilities_to_equity']:.2f}"})
st.subheader("Printed 10-K facts — USD millions")
st.dataframe(pd.DataFrame(facts), hide_index=True, width="stretch")

panel_rows = []
for investor, checks in report["panel"].items():
    for check, outcome in checks.items(): panel_rows.append({"Investor": investor, "Check": check, "Result": outcome})
st.subheader("Panel table")
st.dataframe(pd.DataFrame(panel_rows), hide_index=True, width="stretch")

st.subheader("Verdicts and evidence-bound memos")
columns = st.columns(3)
for column, investor in zip(columns, ("Buffett", "Cathie Wood", "Burry")):
    with column:
        st.markdown(f"### {investor}")
        st.write(report["verdicts"][investor])
        memo = report["memos"][investor]
        st.markdown(memo)
        flagged = unprinted_numbers(memo, report)
        if flagged: st.error("Unprinted-number flag: " + ", ".join(flagged))
        else: st.success("Unprinted-number flag: clear")

st.info("Decision: I would use the panel only as a filing-quality screen, conditioned on preserving every not-found/not-known gap and adding valuation, price, and portfolio-risk analysis before an investment decision.")
