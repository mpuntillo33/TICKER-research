#!/usr/bin/env python3
"""Compute a Buffett-style five-year filing table from SEC EDGAR company facts.

The program deliberately does accounting retrieval and every calculation in Python.
It never estimates a missing fact: a missing source fact stays "not found" and any
check depending on it becomes "not known".
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
MISSING = "not found"
UNKNOWN = "not known"

# Required concept priority from the lab handout. Do not add estimates or substitutes.
METRICS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
    "equity": ["StockholdersEquity"],
}
FLOW_METRICS = {"revenue", "net_income", "operating_cash_flow", "capital_spending"}


def sec_get_json(url: str, user_agent: str) -> dict[str, Any]:
    """Get SEC JSON with the required identifying User-Agent."""
    request = Request(url, headers={"User-Agent": user_agent, "Accept-Encoding": "gzip, deflate"})
    try:
        with urlopen(request, timeout=30) as response:
            payload = response.read()
            if response.headers.get("Content-Encoding", "").lower() == "gzip":
                payload = gzip.decompress(payload)
            return json.loads(payload.decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"SEC EDGAR request failed for {url}: {exc}") from exc


def cik_for_ticker(ticker: str, user_agent: str) -> int:
    records = sec_get_json(TICKERS_URL, user_agent)
    wanted = ticker.upper()
    for record in records.values():
        if record.get("ticker", "").upper() == wanted:
            return int(record["cik_str"])
    raise ValueError(f"Ticker {ticker.upper()} was not found in SEC company_tickers.json")


def _annual_flow(fact: dict[str, Any]) -> bool:
    """True only for a 10-K annual, one-year flow observation."""
    if fact.get("form") != "10-K" or fact.get("fp") != "FY" or not fact.get("start") or not fact.get("end"):
        return False
    try:
        days = (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days
    except ValueError:
        return False
    return 300 <= days <= 380


def _annual_equity(fact: dict[str, Any]) -> bool:
    """True only for a 10-K fiscal-year-end instant balance observation."""
    return fact.get("form") == "10-K" and fact.get("fp") == "FY" and bool(fact.get("end")) and not fact.get("start")


def _facts_for_tag(company_facts: dict[str, Any], tag: str) -> list[dict[str, Any]]:
    """Return USD observations for a US-GAAP tag; an absent tag is not an error."""
    return company_facts.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", [])


def _latest_per_end(observations: Iterable[dict[str, Any]], annual_test) -> dict[str, dict[str, Any]]:
    """Keep the latest-filed 10-K fact for each fiscal-year-end date."""
    selected: dict[str, dict[str, Any]] = {}
    for observation in observations:
        if not annual_test(observation):
            continue
        end = observation["end"]
        current = selected.get(end)
        if current is None or observation.get("filed", "") >= current.get("filed", ""):
            selected[end] = observation
    return selected


def available_fiscal_ends(company_facts: dict[str, Any]) -> list[str]:
    """Use annual net income to define fiscal years that have a valid 10-K flow period."""
    ends = _latest_per_end(_facts_for_tag(company_facts, "NetIncomeLoss"), _annual_flow)
    return sorted(ends)[-5:]


def select_metric(company_facts: dict[str, Any], metric: str, fiscal_end: str) -> dict[str, Any] | None:
    """Select one requested metric for one year, preserving the specified tag priority.

    This is the row-building source selector: it filters to 10-K facts, keeps annual
    one-year flows (or a year-end equity instant), and makes the latest filing win.
    Returning None is the exact code path that becomes 'not found' in a table row.
    """
    annual_test = _annual_flow if metric in FLOW_METRICS else _annual_equity
    for tag in METRICS[metric]:
        candidates = _latest_per_end(_facts_for_tag(company_facts, tag), annual_test)
        fact = candidates.get(fiscal_end)
        if fact is not None:
            return {"value": fact["val"], "tag": tag, "filed": fact.get("filed", "")}
    return None


def display_number(value: float | int | str) -> str:
    if isinstance(value, str):
        return value
    # Values in a row have already been converted from SEC USD to USD millions.
    return f"{value:,.0f}"


def row_for_fiscal_year(company_facts: dict[str, Any], fiscal_end: str) -> dict[str, Any]:
    """Turn EDGAR company facts into exactly one report row for a fiscal year."""
    row: dict[str, Any] = {"fiscal_year_end": fiscal_end}
    selected = {metric: select_metric(company_facts, metric, fiscal_end) for metric in METRICS}
    for metric, fact in selected.items():
        row[metric] = MISSING if fact is None else fact["value"] / 1_000_000
        row[f"{metric}_tag"] = MISSING if fact is None else fact["tag"]

    equity = row["equity"]
    net_income = row["net_income"]
    if isinstance(equity, str) or isinstance(net_income, str) or equity <= 0:
        row["roe"] = UNKNOWN
    else:
        row["roe"] = net_income / equity

    operating_cash_flow = row["operating_cash_flow"]
    capital_spending = row["capital_spending"]
    if isinstance(operating_cash_flow, str) or isinstance(capital_spending, str):
        row["owner_earnings"] = MISSING
    else:
        row["owner_earnings"] = operating_cash_flow - capital_spending
    return row


def compute_checks(rows: list[dict[str, Any]]) -> dict[str, str]:
    def all_known(values: list[Any]) -> bool:
        return len(values) == 5 and all(not isinstance(value, str) for value in values)

    roes = [row["roe"] for row in rows]
    owners = [row["owner_earnings"] for row in rows]
    return {
        "ROE of 15% or more every year": "pass" if all_known(roes) and all(value >= 0.15 for value in roes) else (UNKNOWN if not all_known(roes) else "fail"),
        "Owner earnings positive every year": "pass" if all_known(owners) and all(value > 0 for value in owners) else (UNKNOWN if not all_known(owners) else "fail"),
        "Owner earnings grew, first year to last": "pass" if all_known(owners) and owners[-1] > owners[0] else (UNKNOWN if not all_known(owners) else "fail"),
    }


def build_report(ticker: str, user_agent: str) -> dict[str, Any]:
    ticker = ticker.upper()
    cik = cik_for_ticker(ticker, user_agent)
    facts = sec_get_json(FACTS_URL.format(cik=cik), user_agent)
    ends = available_fiscal_ends(facts)
    rows = [row_for_fiscal_year(facts, end) for end in ends]
    return {
        "ticker": ticker,
        "company": facts.get("entityName", ticker),
        "cik": f"{cik:010d}",
        "source": "SEC EDGAR companyfacts; 10-K only; USD millions",
        "retrieved_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "rows": rows,
        "checks": compute_checks(rows),
    }


def print_report(report: dict[str, Any]) -> None:
    print(f"{report['company']} ({report['ticker']}) | CIK {report['cik']}")
    print("Data from SEC EDGAR; 10-K only; USD millions")
    headers = ["FY end", "Revenue [tag]", "Net income [tag]", "OCF [tag]", "Capex [tag]", "Equity [tag]", "ROE", "Owner earnings"]
    print(" | ".join(headers))
    print(" | ".join(["---"] * len(headers)))
    for row in report["rows"]:
        metric = lambda name: f"{display_number(row[name])} [{row[name + '_tag']}]"
        roe = UNKNOWN if isinstance(row["roe"], str) else f"{row['roe'] * 100:.1f}%"
        print(" | ".join([row["fiscal_year_end"], metric("revenue"), metric("net_income"), metric("operating_cash_flow"), metric("capital_spending"), metric("equity"), roe, display_number(row["owner_earnings"])]))
    print("\nBuffett checks")
    for name, result in report["checks"].items():
        print(f"- {name}: {result}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute Buffett-style facts from SEC EDGAR 10-K company facts.")
    parser.add_argument("ticker", help="US issuer ticker, for example COST")
    parser.add_argument("--output", type=Path, help="Save machine-readable report JSON to this path")
    parser.add_argument("--user-agent", default=os.environ.get("SEC_USER_AGENT", ""), help="Required SEC contact string: 'Name email@example.com'. Set SEC_USER_AGENT to your real name and email.")
    args = parser.parse_args()
    if "@" not in args.user_agent:
        parser.error("SEC User-Agent must include your name and email. Pass --user-agent or set SEC_USER_AGENT.")
    try:
        report = build_report(args.ticker, args.user_agent)
    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print_report(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"\nSaved: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
