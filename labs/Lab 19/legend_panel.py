#!/usr/bin/env python3
"""EDGAR-backed three-investor legend panel for Lab 19.

Only 10-K companyfacts are used.  A missing fact is printed as ``not found``;
any check needing it is ``not known``.  Memos are generated from this report's
printed numbers, not from invented or estimated inputs.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
MISSING, UNKNOWN = "not found", "not known"
GROWTH_THRESHOLD = 0.05  # Kept after the lab probe: broad screen; R&D remains a required second check.

METRICS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
    "equity": ["StockholdersEquity"],
    "liabilities": ["Liabilities"],
    "research_and_development": ["ResearchAndDevelopmentExpense"],
}
FLOW = {"revenue", "net_income", "operating_cash_flow", "capital_spending", "research_and_development"}


def sec_get_json(url: str, user_agent: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": user_agent, "Accept-Encoding": "gzip, deflate"})
    try:
        with urlopen(request, timeout=30) as response:
            data = response.read()
            if response.headers.get("Content-Encoding", "").lower() == "gzip":
                data = gzip.decompress(data)
            return json.loads(data.decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"SEC EDGAR request failed for {url}: {exc}") from exc


def annual_flow(fact: dict[str, Any]) -> bool:
    if fact.get("form") != "10-K" or fact.get("fp") != "FY" or not fact.get("start") or not fact.get("end"):
        return False
    try:
        return 300 <= (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days <= 380
    except ValueError:
        return False


def annual_instant(fact: dict[str, Any]) -> bool:
    return fact.get("form") == "10-K" and fact.get("fp") == "FY" and bool(fact.get("end")) and not fact.get("start")


def observations(facts: dict[str, Any], tag: str) -> list[dict[str, Any]]:
    return facts.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", [])


def latest_by_end(items: list[dict[str, Any]], predicate: Callable[[dict[str, Any]], bool]) -> dict[str, dict[str, Any]]:
    answer: dict[str, dict[str, Any]] = {}
    for item in items:
        if predicate(item) and (item["end"] not in answer or item.get("filed", "") >= answer[item["end"]].get("filed", "")):
            answer[item["end"]] = item
    return answer


def select_metric(facts: dict[str, Any], metric: str, end: str) -> dict[str, Any] | None:
    predicate = annual_flow if metric in FLOW else annual_instant
    for tag in METRICS[metric]:
        found = latest_by_end(observations(facts, tag), predicate).get(end)
        if found:
            return {"value": found["val"] / 1_000_000, "tag": tag}
    return None


def known(value: Any) -> bool:
    return not isinstance(value, str)


def row_for_year(facts: dict[str, Any], end: str) -> dict[str, Any]:
    row: dict[str, Any] = {"fiscal_year_end": end}
    for metric in METRICS:
        picked = select_metric(facts, metric, end)
        row[metric] = MISSING if picked is None else picked["value"]
        row[f"{metric}_tag"] = MISSING if picked is None else picked["tag"]
    row["roe"] = row["net_income"] / row["equity"] if known(row["net_income"]) and known(row["equity"]) and row["equity"] > 0 else UNKNOWN
    row["owner_earnings"] = row["operating_cash_flow"] - row["capital_spending"] if known(row["operating_cash_flow"]) and known(row["capital_spending"]) else MISSING
    row["rd_to_revenue"] = row["research_and_development"] / row["revenue"] if known(row["research_and_development"]) and known(row["revenue"]) and row["revenue"] != 0 else UNKNOWN
    row["liabilities_to_equity"] = row["liabilities"] / row["equity"] if known(row["liabilities"]) and known(row["equity"]) and row["equity"] != 0 else UNKNOWN
    return row


def all_known(values: list[Any]) -> bool:
    return len(values) == 5 and all(known(value) for value in values)


def result(condition: bool, inputs_known: bool) -> str:
    return "pass" if inputs_known and condition else (UNKNOWN if not inputs_known else "fail")


def buffett_checks(rows: list[dict[str, Any]]) -> dict[str, str]:
    roe, owner = [r["roe"] for r in rows], [r["owner_earnings"] for r in rows]
    return {
        "ROE of 15% or more every year": result(all(v >= .15 for v in roe if known(v)), all_known(roe)),
        "Owner earnings positive every year": result(all(v > 0 for v in owner if known(v)), all_known(owner)),
        "Owner earnings grew, first year to last": result(owner[-1] > owner[0] if all_known(owner) else False, all_known(owner)),
    }


def cathie_wood_checks(rows: list[dict[str, Any]], threshold: float = GROWTH_THRESHOLD) -> dict[str, str]:
    revenue = [r["revenue"] for r in rows]
    growth = (revenue[-1] / revenue[0]) ** .25 - 1 if all_known(revenue) and revenue[0] > 0 else UNKNOWN
    rd = rows[-1]["rd_to_revenue"]
    return {
        f"Revenue grew {threshold * 100:.0f}% or more a year, first year to last": result(growth >= threshold if known(growth) else False, known(growth)),
        "R&D 5% or more of revenue, latest year": result(rd >= .05 if known(rd) else False, known(rd)),
    }


def burry_checks(rows: list[dict[str, Any]]) -> dict[str, str]:
    ocf, net_income = [r["operating_cash_flow"] for r in rows], [r["net_income"] for r in rows]
    coverage_known = all_known(ocf) and all_known(net_income)
    leverage = rows[-1]["liabilities_to_equity"]
    return {
        "Operating cash flow at least net income every year": result(all(a >= b for a, b in zip(ocf, net_income) if known(a) and known(b)), coverage_known),
        "Liabilities no more than twice equity, latest year": result(leverage <= 2 if known(leverage) else False, known(leverage)),
    }


def verdict(checks: dict[str, str]) -> str:
    if "fail" in checks.values(): return "Pass — one or more screen checks fail"
    if UNKNOWN in checks.values(): return "Watch — no failing check, but a required fact is not known"
    return "Own the business — all screen checks pass"


def metric_text(value: Any, suffix: str = "") -> str:
    return value if isinstance(value, str) else f"{value:,.0f}{suffix}"


def percent_text(value: Any) -> str:
    return value if isinstance(value, str) else f"{value * 100:.2f}%"


def ratio_text(value: Any) -> str:
    return value if isinstance(value, str) else f"{value:.2f}"


def make_memos(rows: list[dict[str, Any]], panel: dict[str, dict[str, str]], threshold: float) -> dict[str, str]:
    first, latest = rows[0], rows[-1]
    growth = (latest["revenue"] / first["revenue"]) ** .25 - 1 if all_known([r["revenue"] for r in rows]) and first["revenue"] > 0 else UNKNOWN
    return {
        "Buffett": f"# Buffett memo\n\n**Verdict: {verdict(panel['Buffett'])}**\n\nRevenue moved from {metric_text(first['revenue'])} to {metric_text(latest['revenue'])}; owner earnings moved from {metric_text(first['owner_earnings'])} to {metric_text(latest['owner_earnings'])}. Latest ROE is {percent_text(latest['roe'])}. The printed checks are: " + "; ".join(f"{k}: {v}" for k, v in panel['Buffett'].items()) + ".",
        "Cathie Wood": f"# Cathie Wood memo\n\n**Verdict: {verdict(panel['Cathie Wood'])}**\n\nRevenue moved from {metric_text(first['revenue'])} to {metric_text(latest['revenue'])}; annual growth is {percent_text(growth)}. Latest R&D is {metric_text(latest['research_and_development'])} and latest R&D ÷ revenue is {percent_text(latest['rd_to_revenue'])}. The printed checks are: " + "; ".join(f"{k}: {v}" for k, v in panel['Cathie Wood'].items()) + f".\n\nThreshold used: {threshold * 100:.0f}% annual growth.",
        "Burry": f"# Burry memo\n\n**Verdict: {verdict(panel['Burry'])}**\n\nLatest operating cash flow is {metric_text(latest['operating_cash_flow'])}, versus net income of {metric_text(latest['net_income'])}. Latest liabilities are {metric_text(latest['liabilities'])}, equity is {metric_text(latest['equity'])}, and liabilities ÷ equity is {ratio_text(latest['liabilities_to_equity'])}. The printed checks are: " + "; ".join(f"{k}: {v}" for k, v in panel['Burry'].items()) + ".",
    }


def build_report(ticker: str, user_agent: str, growth_threshold: float = GROWTH_THRESHOLD) -> dict[str, Any]:
    records = sec_get_json(TICKERS_URL, user_agent)
    ticker = ticker.upper()
    cik = next((int(v["cik_str"]) for v in records.values() if v.get("ticker", "").upper() == ticker), None)
    if cik is None: raise ValueError(f"Ticker {ticker} was not found in SEC company_tickers.json")
    facts = sec_get_json(FACTS_URL.format(cik=cik), user_agent)
    ends = sorted(latest_by_end(observations(facts, "NetIncomeLoss"), annual_flow))[-5:]
    rows = [row_for_year(facts, end) for end in ends]
    panel = {"Buffett": buffett_checks(rows), "Cathie Wood": cathie_wood_checks(rows, growth_threshold), "Burry": burry_checks(rows)}
    return {"ticker": ticker, "company": facts.get("entityName", ticker), "cik": f"{cik:010d}", "source": "SEC EDGAR companyfacts; 10-K only; USD millions", "retrieved_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z'), "growth_threshold": growth_threshold, "rows": rows, "panel": panel, "verdicts": {name: verdict(checks) for name, checks in panel.items()}, "memos": make_memos(rows, panel, growth_threshold)}


def print_report(report: dict[str, Any]) -> None:
    print(f"{report['company']} ({report['ticker']}) | CIK {report['cik']}")
    print(report["source"])
    print("FY end | Revenue | Net income | OCF | Capex | Equity | Liabilities | R&D | ROE | Owner earnings | R&D/revenue | Liabilities/equity")
    for r in report["rows"]:
        fields = [r["fiscal_year_end"], *[metric_text(r[k]) for k in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "liabilities", "research_and_development")], percent_text(r["roe"]), metric_text(r["owner_earnings"]), percent_text(r["rd_to_revenue"]), ratio_text(r["liabilities_to_equity"])]
        print(" | ".join(fields))
    print("\nPanel checks")
    for investor, checks in report["panel"].items():
        for name, value in checks.items(): print(f"- {investor} | {name}: {value}")
    revenue = [row["revenue"] for row in report["rows"]]
    if all_known(revenue) and revenue[0] > 0:
        print(f"Revenue growth a year, first to last: {((revenue[-1] / revenue[0]) ** .25 - 1) * 100:.2f}%")
    print("\nMemos")
    for memo in report["memos"].values(): print(memo + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--user-agent", default=os.environ.get("SEC_USER_AGENT", ""))
    parser.add_argument("--growth-threshold", type=float, default=GROWTH_THRESHOLD, help="Cathie annual revenue-growth threshold, e.g. 0.15")
    args = parser.parse_args()
    if "@" not in args.user_agent: parser.error("SEC User-Agent must include a truthful name and email.")
    if not 0 <= args.growth_threshold <= 1: parser.error("--growth-threshold must be between 0 and 1.")
    try: report = build_report(args.ticker, args.user_agent, args.growth_threshold)
    except (RuntimeError, ValueError) as exc: print(f"Error: {exc}", file=sys.stderr); return 1
    print_report(report)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Saved: {args.output}")
    return 0

if __name__ == "__main__": raise SystemExit(main())
