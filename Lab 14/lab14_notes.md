# Lab 14 — Portfolio Baselines

## Results

`python portfolio.py` prices the three course baselines from the editable return, volatility, and correlation inputs.

| Portfolio | Bills / 10-year / IG / equity (%) | Return | Volatility | Reserve eligible | Meets 6.5%? |
|---|---:|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

The benchmark earns enough for the 6.5% objective but fails the Lab 13 reserve rule: it has 0.0% in reserve-eligible bills or the 10-year note, below the 3.0% minimum. Candidate E in `mandate.py` records and tests that conclusion.

## Validation performed

- Changing both IG bond/equity correlations from 0.25 to 0.50 raises benchmark volatility to 11.00%; the input file remains at 0.25 after the test.
- Setting the IG bond/equity correlation to 1.30 makes the engine stop with a clear `ValueError` that correlations must be between -1 and 1.
- The correlation validator also stops if a correlation table is not symmetric.

## Diversification explanation

Diversification means combining investments whose returns do not move in perfect lockstep. When correlation is below +1, losses in one sleeve are not always matched by proportional losses in the other, so the covariance term reduces the combined variance.

For the 40% IG bond / 60% equity benchmark, the variance is:

`0.40² × 0.06² + 0.60² × 0.16² + 2 × 0.40 × 0.60 × 0.25 × 0.06 × 0.16 = 0.010944`

The volatility is `sqrt(0.010944) = 0.1046`, or **10.46%**. The correlation term is essential; leaving it out would give the incorrect 9.90% result.

Inverse volatility heavily weights bills because their 0.5% volatility gives them the largest `1 / volatility` value. I would show the CIO the benchmark first: it is the only baseline that achieves the 6.5% objective, while clearly flagging the reserve-rule breach that must be fixed before it can meet the mandate.

## Fund universe and price source

| Ticker | Fund | Role |
|---|---|---|
| BIL | SPDR Bloomberg 1-3 Month T-Bill ETF | Cash and reserve |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds / reserve eligible |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Investment-grade fixed income |
| VT | Vanguard Total World Stock ETF | Broad global equity |

`prices.csv` contains each fund's monthly **Adj Close** from Yahoo Finance, with the date first and the oldest observation first. It covers 60 complete calendar months, October 2021 through September 2026, rather than including the partial October 2026 month. Download date: **2026-10-20**. Source: Yahoo Finance Historical Data / chart endpoint for [BIL](https://finance.yahoo.com/quote/BIL/history/), [IEF](https://finance.yahoo.com/quote/IEF/history/), [LQD](https://finance.yahoo.com/quote/LQD/history/), and [VT](https://finance.yahoo.com/quote/VT/history/).

To refresh the data, run `python download_prices.py`.
