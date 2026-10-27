# Lab 16 - Provenance Gate

## Run

```powershell
cd "Lab 16"
python asof.py
```

`asof.py` uses only the Python standard library. Its two editable inputs at the top are the training table and `DECISION_DATE`.

## Point-in-time result

The decision date is 2026-03-31. The provenance gate applies these rules in order: quarantine blank tickers, remove exact duplicates, exclude publications after the decision date, then retain the latest publication that was available for each ticker-month.

| Funnel step | Rows removed |
|---|---|
| Quarantined: no ticker | 11 |
| Exact duplicate | 7 |
| Published after 31 March | 3, 8, 10 |
| Older vintage replaced by a revision | 2 |
| As-of panel | 1, 4, 5, 6, 9, 12 |

| Ticker | As-of signal | Naive signal |
|---|---:|---:|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

The as-of signal is the percent change from the prior month to the latest month knowable on the decision date. The naive comparison deliberately ignores publication dates but still takes each ticker-month's latest vintage.

## Later-date check

Changing `DECISION_DATE` to `"2026-04-15"` admits every released observation. The as-of signals then equal the naive signals for AAA, BBB, and CCC. Restoring the date to `"2026-03-31"` reproduces the point-in-time panel above.

## Sanity gate by hand

The provenance gate checks availability, not plausibility. Yield for a one-year zero is `100 / price - 1`.

| Row | Fund | Month | Price | Yield | Breaks |
|---:|---|---|---:|---:|---|
| 1 | AAA | Jan | 101.0 | -0.99% | Negative yield |
| 4 | AAA | Feb | 103.0 | -2.91% | Negative yield |
| 5 | BBB | Jan | 98.0 | +2.04% | Nothing |
| 6 | BBB | Feb | 97.0 | +3.09% | Nothing |
| 9 | CCC | Jan | 110.0 | -9.09% | Negative yield; priced above BBB and AAA |
| 12 | CCC | Feb | 111.0 | -9.91% | Negative yield; priced above BBB and AAA |

A fifth rule could quarantine prices above 100 because a one-year zero returning 100 at maturity must have a negative yield when its price is above 100. In this table that rule would quarantine rows 1, 4, 9, and 12.

## Reflection

Look-ahead bias occurs when a model uses information that was unavailable at the point of a historical decision. Event time is the month a number measures; publication time is the day the number became available. A later revision creates another publication for the same event month. Treating a later publication as if it had been available earlier lets a backtest use the future.

For AAA, on 31 March the latest knowable price was the 103.0 February revision in row 4, following January's 101.0, so the available return was +1.98%. The naive result uses the March 109.0 price that was not published until 10 April and reports +5.83% from February. A backtest using that naive column would overstate what the strategy could have known and could claim performance based on unavailable data. The timing rule removed the most consequential information: rows 3, 8, and 10 were not yet published; within the still-knowable AAA February records, the revision rule correctly replaces row 2 with row 4.
