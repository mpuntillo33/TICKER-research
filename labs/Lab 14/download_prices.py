"""Download five complete years of monthly Yahoo Finance adjusted closes.

Run with: python download_prices.py
The output is prices.csv, with dates in ascending order.
"""

import csv
import datetime as dt
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

TICKERS = ("BIL", "IEF", "LQD", "VT")
START = dt.date(2021, 10, 1)
END = dt.date(2026, 10, 1)  # exclusive: 60 complete months through September 2026
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}"


def unix_time(date):
    """Convert a date to the UTC timestamp expected by Yahoo Finance."""
    return int(dt.datetime.combine(date, dt.time(), tzinfo=dt.timezone.utc).timestamp())


def fetch_monthly_adjusted_closes(ticker):
    """Fetch a ticker's monthly adjusted closes from Yahoo Finance."""
    parameters = urlencode({
        "period1": unix_time(START),
        "period2": unix_time(END),
        "interval": "1mo",
        "events": "history",
    })
    request = Request(
        YAHOO_CHART_URL.format(ticker) + "?" + parameters,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    result = payload["chart"]["result"][0]
    adjusted_closes = result["indicators"]["adjclose"][0]["adjclose"]
    return {
        dt.datetime.fromtimestamp(timestamp, tz=dt.timezone.utc).date().isoformat(): adjusted_close
        for timestamp, adjusted_close in zip(result["timestamp"], adjusted_closes)
        if adjusted_close is not None
    }


def main():
    """Create a date-first CSV covering all selected funds."""
    series = {ticker: fetch_monthly_adjusted_closes(ticker) for ticker in TICKERS}
    dates = sorted(set.intersection(*(set(values) for values in series.values())))
    if len(dates) != 60:
        raise ValueError(f"Expected 60 complete monthly observations; found {len(dates)}.")
    output = Path("prices.csv")
    with output.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(("Date", *TICKERS))
        for date in dates:
            writer.writerow((date, *(f"{series[ticker][date]:.6f}" for ticker in TICKERS)))
    print(f"Wrote {len(dates)} monthly rows to {output}.")


if __name__ == "__main__":
    main()
