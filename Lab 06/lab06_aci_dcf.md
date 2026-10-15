# Lab 06 — ACI: What Has to Be True

This is a classroom FCFF DCF for Albertsons Companies, Inc. (NYSE: ACI). Dollar amounts are USD millions except per-share figures. The primary filing is ACI’s Form 10-K for the 53 weeks ended February 28, 2026.

## Inputs and sources

| Input | Value used | Unit | As-of date | Source and locator |
|---|---:|---|---|---|
| Starting FCFF | 936.75 | $m | Feb. 28, 2026 | 10-K, Item 8, Cash Flows p. 55: operating cash flow $2,366.7m and capex $1,839.4m. Item 7 p. 36: net interest $504.2m; effective tax rate 18.8%. FCFF = $2,366.7 + $504.2 × (1 − .188) − $1,839.4. |
| FCFF growth, Years 1–5 | 2%, 2%, 2%, 2%, 2% | % | Sep. 10, 2026 | Forecast, not guidance. 10-K Item 7 pp. 35–36: identical sales excluding fuel were 2%, 2%, and 3% in fiscal 2025–2023. The reported 3.5% fiscal-2025 sales growth included an estimated $1.4bn extra-week effect. |
| WACC | 8.0% | % | Sep. 10, 2026 | Analyst estimate, not copied from training. Cross-checks: 10-year Treasury yield 4.844%, Damodaran implied ERP 4.14%, and ACI 10-K debt and interest expense. |
| Terminal growth | 2.5% | % | Sep. 10, 2026 | Long-run economic assumption, not company-specific growth; below WACC. |
| Cash | 198.6 | $m | Feb. 28, 2026 | 10-K, Item 8, Balance Sheet p. 53. |
| Debt | 8,946.6 | $m | Feb. 28, 2026 | 10-K, Note 5 p. 68, Total debt; includes finance leases. |
| Diluted shares | 547.2 | million | FY2025 | 10-K, Note 13, diluted weighted-average Class A shares. |
| Reverse-DCF target price | 11.70 | $/share | Sep. 10, 2026, 4:30 p.m. EDT | Time-stamped ACI market quote. |

Sources: [ACI 2026 10-K](https://www.sec.gov/Archives/edgar/data/1646972/000164697226000032/aci-20260228.htm), [Treasury yield](https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data), [Damodaran ERP](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm), and [ACI quote](https://finance.yahoo.com/quote/ACI/).

## Results

`python dcf.py` gives enterprise value of $17,076.57m, equity value of $8,328.57m, and **$15.22 per diluted share**. Present-value terminal value is 76.82% of enterprise value.

The $15.22 value is 1.30× the $11.70 price (price/value = 76.9%), within the 0.5×–2.0× reasonableness range. I distrust the single-year starting FCFF most because working-capital and legal-settlement effects may make it unrepresentative of sustainable grocery cash generation.

| WACC \ terminal growth | 2.0% | 3.0% | 4.0% |
|---:|---:|---:|---:|
| 9.0% | $8.96 | $12.15 | $16.61 |
| 10.0% | $5.84 | $8.15 | $11.22 |
| 11.0% | $3.41 | $5.14 | $7.37 |

The low corner is $3.41 (11% WACC, 2% terminal growth); the high corner is $16.61 (9%, 4%).

## Reverse DCF and call

At $11.70, bisection within the required −5.0% to +10.0% bracket solves a **−2.6815 percentage-point uniform shift** to all five explicit FCFF growth rates: the five 2.0% rates become approximately −0.68%. Held fixed: starting FCFF, WACC, terminal growth, cash, debt, diluted shares, and the five-year forecast structure. This is a model-implied assumption, not proof of mispricing.

**Initiate if** ACI remains at or below $12.18 (a 20% margin below the $15.22 value) **and** next annual operating-cash-flow-less-capex remains at or above $936.75m; **otherwise, defer.** Monitor operating cash flow less capex and total debt.
