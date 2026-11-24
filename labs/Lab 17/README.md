# Lab 17 — Point-in-Time Audit

## Files and run command

`asof_app.py` is a Streamlit FRED-style rates page that downloads each requested series twice: the current FRED CSV and the date-specific ALFRED vintage CSV. No API key or account is used.

```powershell
cd "Lab 17"
streamlit run asof_app.py
```

Install the small dependency set if it is absent:

```powershell
python -m pip install streamlit pandas requests
```

## What I completed

- Built a four-series rates app for BAA, FEDFUNDS, DGS10, and MORTGAGE30US, with all four selected initially.
- Added a typed series-ID field, individual error handling, current-value charts, an as-known-last-observation line, and an audit table.
- Cached the two separate downloads. `download_current` reads FRED's current CSV; `download_as_known_on` sends the same series ID and a `vintage_date` to ALFRED.
- Counted observations that were still unpublished at the selected vintage and observations whose value has changed on the same measurement date.
- Added `DGS3MO` as my Project 2 series and documented the decision below.

## Known-answer check: 5 October 2026

With start date 1 January 2020 and **As known on = 2026-10-05**, the app's `Value as known then` and last measured date should be:

| Series | Last date known | Value |
|---|---|---:|
| BAA | September 2026 | 6.47 |
| FEDFUNDS | September 2026 | 3.75 |
| DGS10 | 2 October 2026 | 5.28 |
| MORTGAGE30US | 1 October 2026 | 7.28 |

These are the required point-in-time answers: the app uses ALFRED for them, not a second read of current FRED data.

## PAYEMS revision probe

Add `PAYEMS`, set **As known on = 2025-01-15**, and inspect the row. The last observation is December 2024 at **159,536** (thousands) as known then. Current FRED's value for the same month is lower, and the `Values revised` count is above zero. This confirms that the app compares a vintage with the current release rather than two current downloads.

## Data card — DGS3MO

| Field | Audit |
|---|---|
| Source and link | Federal Reserve Bank of St. Louis, [DGS3MO FRED page](https://fred.stlouisfed.org/series/DGS3MO) and its downloadable FRED/ALFRED graph CSVs. |
| What it measures | Market yield on the U.S. Treasury's three-month constant-maturity Treasury security. |
| Units | Percent, not seasonally adjusted; daily business-day observations. |
| Publication lag | A market-day rate: it normally appears with very little lag. The app's as-of line shows the last business date actually available at every selected decision date. |
| Revisions | Usually none or very few for ordinary dates, but the audit table tests rather than assumes this by comparing matching dates across the ALFRED vintage and current FRED. |
| Download date | 29 October 2026 (the app reports its own runtime download date in the page caption). |
| Three values checked by hand | Checked against the linked FRED page: 2 Oct 2026 = 4.19%; 5 Oct 2026 = 4.22%; 6 Oct 2026 = 4.21%. |

### Fresh-eyes partner attack

**Partner attack — units:** My partner trusted the units least, because a rate could be mistaken for a decimal return rather than a percentage. The linked FRED page labels DGS3MO “Percent, Not Seasonally Adjusted,” and the app preserves the source values (for example, 4.19 means 4.19%, not 419% or 0.0419%).

### My call

**Admit with an as-of rule:** use DGS3MO only as returned by ALFRED as of each decision date, and carry forward the most recent available business-day observation when a same-day value was not yet released. It may remain admitted while the app continues to show minimal revisions and near-market-day availability; quarantine it if a test vintage reveals material revisions or a lag that overlaps the trading decision.

## Explain the code

`download_as_known_on(series_id, vintage_date)` builds the ALFRED URL with both inputs, requests its CSV, raises an error for a failed download, and calls `read_fred_csv`. The parser selects the observation date and numeric series column, changes FRED's `.` missing marker to a missing value, converts dates and values to usable types, and sorts them. In `audit_series`, the vintage's final valid observation is the last number knowable then; the merge with current FRED on the observation date makes revisions visible without confusing late publications with changed history.

## Reflection

The “as known on” date separates the calendar date a rate measures from the date it became accessible. For DGS3MO, a backtest made from today's FRED history would generally overstate timeliness if it treated each daily rate as known at the beginning of the same trading day; it could also silently use any later corrected value. A data card prevents that leak by identifying source, unit, frequency, release lag, revisions, and download/vintage date. “Cleaned the data” is not a data card because it does not state any of those reproducible facts or the transformations applied.
