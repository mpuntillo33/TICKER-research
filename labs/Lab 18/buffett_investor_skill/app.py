"""Streamlit viewer for EDGAR-backed Buffett investor reports."""
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
SCRIPT = HERE / "edgar_buffett.py"
NUMBER = re.compile(r"(?<![\w.])\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?%?|(?<![\w.])\d+(?:\.\d+)?%?")


def report_path(ticker: str) -> Path:
    return HERE / f"{ticker.upper()}_edgar_report.json"


def memo_path(ticker: str) -> Path:
    return HERE / f"{ticker.upper()}_buffett_memo.md"


def allowed_numbers(report: dict) -> set[str]:
    """Build normalized number tokens from facts the script printed."""
    values: set[str] = set()
    # The console also prints the source line, check labels, and fiscal-end dates.
    # Include their number tokens so, for example, an evidence-bound reference to
    # "10-K" is not incorrectly flagged.
    printed_labels = [report["source"], *report["checks"].keys()]
    for label in printed_labels:
        values.update(token.lstrip("$") for token in NUMBER.findall(label))
    for row in report["rows"]:
        values.add(row["fiscal_year_end"])
        for field in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "owner_earnings"):
            value = row[field]
            if not isinstance(value, str):
                values.add(f"{value:,.0f}")
                values.add(f"{value:.0f}")
        if not isinstance(row["roe"], str):
            values.add(f"{row['roe'] * 100:.1f}%")
    return values


def memo_unprinted_numbers(memo: str, report: dict) -> list[str]:
    allowed = allowed_numbers(report)
    flagged: list[str] = []
    for match in NUMBER.findall(memo):
        token = match.lstrip("$")
        # Years appear as the fiscal-year-end date, so permit their individual year component.
        if token in allowed or any(token == date[-4:] for date in (r["fiscal_year_end"] for r in report["rows"])):
            continue
        flagged.append(match)
    return sorted(set(flagged))


st.set_page_config(page_title="Buffett Investor Skill", layout="wide")
st.title("Buffett Investor Skill")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
ticker = st.text_input("Ticker", "COST").strip().upper()
user_agent = st.text_input("SEC User-Agent (your name and email)", value=os.environ.get("SEC_USER_AGENT", ""), type="password", help="SEC requests must identify the requester with a real name and email. This field is used only for the download command.")

left, right = st.columns([1, 2])
with left:
    if st.button("Download 10-K facts", type="primary"):
        result = subprocess.run([sys.executable, str(SCRIPT), ticker, "--output", str(report_path(ticker)), "--user-agent", user_agent], capture_output=True, text=True)
        if result.returncode:
            st.error(result.stderr or result.stdout)
        else:
            st.success("Saved EDGAR report. Use the skill to write the memo from these printed facts.")
            st.code(result.stdout)

path = report_path(ticker)
if not path.exists():
    st.info(f"No report for {ticker}. Click Download 10-K facts or run the skill command first.")
    st.stop()
report = json.loads(path.read_text(encoding="utf-8"))
rows = report["rows"]

chart = pd.DataFrame({"Fiscal year end": [r["fiscal_year_end"] for r in rows], "Owner earnings": [None if isinstance(r["owner_earnings"], str) else r["owner_earnings"] for r in rows], "Net income": [None if isinstance(r["net_income"], str) else r["net_income"] for r in rows]}).set_index("Fiscal year end")
st.subheader(f"{report['company']} ({ticker}) — USD millions")
st.line_chart(chart)

table_rows = []
for row in rows:
    table_rows.append({
        "FY end": row["fiscal_year_end"],
        "Revenue [tag]": f"{row['revenue']:,} [{row['revenue_tag']}]" if not isinstance(row["revenue"], str) else "not found",
        "Net income [tag]": f"{row['net_income']:,} [{row['net_income_tag']}]" if not isinstance(row["net_income"], str) else "not found",
        "OCF [tag]": f"{row['operating_cash_flow']:,} [{row['operating_cash_flow_tag']}]" if not isinstance(row["operating_cash_flow"], str) else "not found",
        "Capex [tag]": f"{row['capital_spending']:,} [{row['capital_spending_tag']}]" if not isinstance(row["capital_spending"], str) else "not found",
        "Equity [tag]": f"{row['equity']:,} [{row['equity_tag']}]" if not isinstance(row["equity"], str) else "not found",
        "ROE": "not known" if isinstance(row["roe"], str) else f"{row['roe'] * 100:.1f}%",
        "Owner earnings": row["owner_earnings"],
    })
st.dataframe(pd.DataFrame(table_rows), width="stretch", hide_index=True)

st.subheader("Buffett checks")
st.dataframe(pd.DataFrame(report["checks"].items(), columns=["Check", "Result"]), width="stretch", hide_index=True)

st.subheader("Buffett memo")
memo_file = memo_path(ticker)
if not memo_file.exists():
    st.warning("No memo yet. Run the skill and save its evidence-bound memo beside this app.")
else:
    memo = memo_file.read_text(encoding="utf-8")
    st.markdown(memo)
    flagged = memo_unprinted_numbers(memo, report)
    if flagged:
        st.error("Numbers in the memo that were not printed by the script: " + ", ".join(flagged))
    else:
        st.success("All numbers in this memo were printed by the EDGAR script.")
