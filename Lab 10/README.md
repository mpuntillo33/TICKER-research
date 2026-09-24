# Lab 10 - ACI Pro-Forma

**Question:** What are five years of my company's statements worth, built from assumptions I can defend?

**Company:** Albertsons Companies, Inc. (NYSE: ACI). All dollar figures are USD millions except per-share data.

## Company-specific line

ACI's reported sales can overstate its underlying store growth because pharmacy and digital sales are growing while carrying lower margins, and FY2025 sales also included a 53rd week. I model this by using identical-sales-like revenue growth rather than FY2025's reported 3.5% growth, and by keeping gross margin conservative rather than assuming that higher sales automatically improve it. This replaces ABG's floor-plan row: ACI has no floor-plan financing in this model.

## History grid

The three model years are FY2023 (ended February 24, 2024), FY2024 (ended February 22, 2025), and FY2025 (ended February 28, 2026). I hand-checked FY2025 revenue ($83,172.5m) and FY2025 inventory ($5,173.9m) in the FY2025 10-K.

| Item | FY2023 | FY2024 | FY2025 | Filing source |
|---|---:|---:|---:|---|
| Revenue | 79,237.7 | 80,390.9 | 83,172.5 | FY2024 10-K, p. 55; FY2025 10-K, p. 54 |
| Gross profit | 22,045.7 | 22,255.6 | 22,606.7 | FY2024 10-K, p. 55; FY2025 10-K, p. 54 |
| SG&A | 19,932.9 | 20,613.7 | 21,891.3 | FY2024 10-K, p. 55; FY2025 10-K, p. 54 |
| Net income | 1,296.0 | 958.6 | 217.4 | FY2024 10-K, p. 55; FY2025 10-K, p. 54 |
| Inventory | 4,945.2 | 4,989.0 | 5,173.9 | FY2024 10-K, p. 54; FY2025 10-K, p. 53 |
| PP&E, net | 9,570.3 | 9,811.0 | 9,903.7 | FY2024 10-K, p. 54; FY2025 10-K, p. 53 |
| Stockholders' equity | 2,747.5 | 3,385.9 | 1,836.2 | FY2024 10-K, p. 54; FY2025 10-K, p. 53 |

The FY2023 and FY2024 numbers are also restated in the three-year operations table of the FY2025 filing. Sources: [FY2023 10-K](https://www.sec.gov/Archives/edgar/data/1646972/000164697224000060/aci-20240224.htm), [FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1646972/000164697225000052/aci-20250222.htm), and [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1646972/000164697226000032/aci-20260228.htm).

## Historical ratios

| Ratio / measure | FY2023 | FY2024 | FY2025 | Source and calculation |
|---|---:|---:|---:|---|
| Gross margin | 27.8% | 27.7% | 27.2% | Gross profit / revenue; 10-K operations statements |
| SG&A / gross profit | 90.4% | 92.6% | 96.8% | SG&A / gross profit; 10-K operations statements |
| Inventory days | 31.6 | 31.3 | 31.2 | Inventory / cost of sales x 365; 10-K balance sheets and operations statements |
| D&A / PP&E | 18.6% | 18.5% | 19.3% | D&A / ending PP&E; 10-K cash flows and balance sheets |
| Capital spending | 2,156.7 | 1,927.5 | 1,833.6 | Filing cash-flow/MD&A field; no provider field was used |
| Effective tax rate | 18.4% | 15.1% | 18.8% | Income-tax expense / pretax income; 10-K operations statements |
| Reported revenue growth | 2.0% | 1.5% | 3.5% | 10-K operations statements |
| Identical sales, ex-fuel | 3.0% | 2.0% | 2.0% | FY2025 10-K MD&A reports all three years |

Organic growth means growth from locations already in the comparison base, excluding effects such as acquisitions and new stores. ACI calls it **identical sales, excluding fuel**: stores are compared daily, digital direct-to-consumer sales are included, fuel is excluded, and acquired stores enter after one year. FY2025's reported 3.5% growth included the 53rd week; identical sales were 2.0%. That is why an ABG-style 1.8% forecast growth rate can be below a reported 4.7% rate: the forward assumption is a normalized view of underlying growth, not a mechanical copy of one period's total revenue growth.

## Assumption set

| Assumption | Value | Label | Reason |
|---|---:|---|---|
| Revenue growth | 0.5%, 1.0%, 1.5%, 2.0%, 2.0% | Judgment | I start below ACI's 2.0% identical-sales history because the latest Q1 FY2026 identical sales declined 0.8%; I allow only gradual recovery. |
| Gross margin | 27.0% rising to 27.2% | Judgment | Pharmacy mix and digital delivery costs reduced FY2025 margin to 27.2%, so I do not assume quick margin expansion. |
| SG&A / gross profit | 93.5% falling to 92.3% | Judgment | FY2025's reported ratio includes the $773.8m opioid-settlement charge; I remove that non-recurring charge for the forecast, start near the resulting 93.4%, and allow only modest productivity from ACI Edge. |
| Inventory days | 31.2 days | History | FY2025 inventory days, calculated from the filed balance sheet and cost of sales. |
| D&A / opening PP&E | 19.3% | History | FY2025 D&A divided by FY2025 PP&E. |
| Capital spending | 2,100.0 per year | Guidance | FY2025 10-K gives FY2026 capex guidance of $2.0bn-$2.2bn; I use the midpoint and hold it flat. |
| Tax rate | 25.5% | Judgment | I use a normalized statutory-like rate instead of FY2025's unusual 18.8% effective rate, which followed the opioid charge. |
| Debt repayment | 50.0 per year | Judgment | I think repayment will stall because recent trends show ACI taking on more debt, so an aggressive paydown policy is not realistic. |
| Dividends | 330.0 per year | History | Near FY2025 dividends paid of $322.7m, rounded. |
| Minimum cash | 100.0 | Judgment | This is a conservative liquidity floor below the FY2025 $198.6m cash balance, while the revolver provides backup liquidity. |
| Cost of equity / terminal growth | 10.0% / 2.0% | Judgment | I use a conservative equity discount rate and terminal growth below a long-run nominal-growth assumption because grocery is mature and low margin. |
| Floor plan | None | Company-specific conclusion | ACI is a grocery retailer and its filed debt structure is notes, an ABL facility, and finance leases - not ABG's inventory floor-plan financing. |

FY2025 reported net income was positive, and projected FCFE is positive in every forecast year. If FCFE had been negative, I would write "negative FCFE" for that year and value only positive years: a perpetuity applied to a negative cash flow is not an economic value.

## Opening balance sheet and engine

The opening balance sheet in `proforma.py` is FY2025: inventory 5,173.9; PP&E 9,903.7; other assets 11,489.7; cash 198.6; debt and finance leases 8,946.6; other liabilities 15,983.1; and equity 1,836.2. "Other" lines are explicitly aggregated from the reported balance sheet rather than independently assumed cash plugs.

Run:

```powershell
python proforma.py
```

The model forecasts five years, calculates cash from FCFE, calls `assert_balanced` every year, and refuses a balance-sheet gap or cash below $100m. No projected year draws the revolver because computed cash remains above the floor. I break-tested the refusal without changing the saved model by increasing opening equity $1m in memory; it stopped in FY2026 with `AssertionError: ... assets - liabilities - equity = -1.0`.

## Value and market-price comparison

Using 499.5m FY2025 shares outstanding (issued shares less treasury shares), the model's value per share is **$16.82**. The market quote was **$11.95 on September 24, 2026** (retrieved after the U.S. market close). The model says $16.82, while the market says $11.95 on the same 499.5m-share count; what margin and cash-flow recovery would the market need to believe to close that gap? This is a valuation question, not a recommendation.

## Partner review

**Attack:** "Why is debt repayment only $50m per year when ACI generates operating cash flow above $2bn? Wouldn't a large repayment be more reasonable once the debt refinancing is complete?"

**Answer:** "I chose a small repayment because ACI's FY2025 total debt and finance leases increased by $1.13bn, and it still had $425m outstanding on its ABL facility at year end. I would raise the repayment assumption only after filings show debt falling for more than one period while capex, dividends, and operating cash flow remain covered."

My attack on a partner's model would be: "You label your margin expansion as judgment, but what filed evidence shows the mix or cost change that makes it happen, and what next-quarter result would make you lower it?"

## Reflection

The label I would defend longest is the restrained debt-repayment judgment because it follows the most recent reported debt increase rather than an optimistic use of operating cash flow. The number that surprised me was the $1.36bn estimated sales contribution from the 53rd week, because it makes the reported 3.5% FY2025 growth much less representative of underlying store growth.

