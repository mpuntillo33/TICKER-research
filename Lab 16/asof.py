"""Lab 16: a point-in-time provenance gate for the supplied training table.

Run: python asof.py
Change DECISION_DATE to test what was knowable on another date.
"""

from datetime import date
from collections import defaultdict


# Editable inputs
DECISION_DATE = "2026-03-31"
TABLE = """row,ticker,month,published_on,price
1,AAA,2026-01,2026-02-10,101.0
2,AAA,2026-02,2026-03-10,104.0
3,AAA,2026-03,2026-04-10,109.0
4,AAA,2026-02,2026-03-25,103.0
5,BBB,2026-01,2026-02-10,98.0
6,BBB,2026-02,2026-03-10,97.0
7,BBB,2026-02,2026-03-10,97.0
8,BBB,2026-03,2026-04-10,92.0
9,CCC,2026-01,2026-02-10,110.0
10,CCC,2026-02,2026-04-05,112.0
11,,2026-02,2026-03-10,99.0
12,CCC,2026-02,2026-03-10,111.0
"""


def parse_table(text):
    """Turn the embedded CSV-style input into typed row dictionaries."""
    lines = [line.strip() for line in text.strip().splitlines()]
    headings = lines[0].split(",")
    rows = []
    for line in lines[1:]:
        values = line.split(",")
        row = dict(zip(headings, values))
        row["row"] = int(row["row"])
        row["published_on"] = date.fromisoformat(row["published_on"])
        row["price"] = float(row["price"])
        rows.append(row)
    return rows


def remove_exact_duplicates(rows):
    """Keep the first occurrence of each complete record."""
    seen = set()
    kept, removed = [], []
    for row in rows:
        fingerprint = (row["ticker"], row["month"], row["published_on"], row["price"])
        if fingerprint in seen:
            removed.append(row)
        else:
            seen.add(fingerprint)
            kept.append(row)
    return kept, removed


def keep_latest_vintage(rows):
    """For each ticker/month pair, keep the row with the latest publication date."""
    latest = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in latest or row["published_on"] > latest[key]["published_on"]:
            latest[key] = row
    kept = [row for row in rows if latest[(row["ticker"], row["month"])] is row]
    removed = [row for row in rows if latest[(row["ticker"], row["month"])] is not row]
    return kept, removed


def provenance_gate(rows, decision_date):
    """Apply the four provenance rules in the assigned order."""
    funnel = []

    kept = [row for row in rows if row["ticker"]]
    funnel.append(("Quarantined: no ticker", [row for row in rows if not row["ticker"]]))

    kept, removed = remove_exact_duplicates(kept)
    funnel.append(("Exact duplicate", removed))

    on_or_before = [row for row in kept if row["published_on"] <= decision_date]
    funnel.append((f"Published after {decision_date.isoformat()}",
                   [row for row in kept if row["published_on"] > decision_date]))

    kept, removed = keep_latest_vintage(on_or_before)
    funnel.append(("Older vintage replaced by a revision", removed))

    return sorted(kept, key=lambda row: row["row"]), funnel


def naive_panel(rows):
    """Use the latest vintage regardless of publication date, for comparison."""
    rows = [row for row in rows if row["ticker"]]
    rows, _ = remove_exact_duplicates(rows)
    rows, _ = keep_latest_vintage(rows)
    return sorted(rows, key=lambda row: row["row"])


def signals(panel):
    """Return each ticker's final month-over-month price return and latest month."""
    by_ticker = defaultdict(list)
    for row in panel:
        by_ticker[row["ticker"]].append(row)

    answer = {}
    for ticker, ticker_rows in by_ticker.items():
        ticker_rows.sort(key=lambda row: row["month"])
        if len(ticker_rows) < 2:
            continue
        previous, latest = ticker_rows[-2:]
        percent_change = (latest["price"] / previous["price"] - 1) * 100
        answer[ticker] = (percent_change, latest["month"])
    return answer


def signed_percent(value):
    return f"{value:+.2f}%"


def print_panel(panel):
    print("Row  Ticker  Month measured  Published on  Price")
    for row in panel:
        print(f"{row['row']:>3}  {row['ticker']:<6}  {row['month']:<14}  "
              f"{row['published_on'].isoformat()}    {row['price']:.1f}")


def main():
    rows = parse_table(TABLE)
    decision_date = date.fromisoformat(DECISION_DATE)
    panel, funnel = provenance_gate(rows, decision_date)

    print(f"Decision date: {decision_date.isoformat()}")
    print("\nRow funnel")
    for label, removed in funnel:
        row_numbers = ", ".join(str(row["row"]) for row in removed) or "none"
        print(f"{label}: {len(removed)} removed (row {row_numbers})")

    print("\nAs-of panel")
    print_panel(panel)

    asof_signals = signals(panel)
    comparison_signals = signals(naive_panel(rows))
    print("\nSignals")
    for ticker in sorted(asof_signals):
        asof_return, asof_month = asof_signals[ticker]
        naive_return, naive_month = comparison_signals[ticker]
        print(f"{ticker}: as-of {signed_percent(asof_return)} ({asof_month}); "
              f"naive {signed_percent(naive_return)} ({naive_month})")


if __name__ == "__main__":
    main()
