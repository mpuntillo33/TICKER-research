# Lab 12 — ACI Pro-Forma Sensitivity: Full Analysis and Review

**Company:** Albertsons Companies, Inc. (NYSE: ACI)
**Currency and share basis:** USD millions except per-share amounts; the Lab 10/11 FCFE model uses 499.5m FY2025 issued shares less treasury shares.
**Purpose:** This is the presentation route and final review record for Lab 12. It links to the existing calculations rather than creating a new valuation or a slide deck.

## Current conclusion

My supported conclusion is **watch/defer, not initiate**. The linked FCFE pro-forma values ACI at **$16.82 per share** (value date: the FY2025 opening balance sheet and FY2026E–FY2030E forecast; 499.5m shares). The saved market quote was **$11.95 on September 24, 2026** on the same share-count basis. That gap is a question to investigate, not a buy instruction: the FCFE result depends heavily on an assumed recovery in operating income and on terminal value (73.6% of equity value).

I do not average that result with my earlier valuations. My September 10, 2026 FCFF DCF is **$15.22 per diluted share** using 547.2m diluted weighted-average shares; the separate reported-GAAP P/E comparison is **$5.44–$14.77 per share**, with a $10.11 median. Those methods use different dates, share bases, cash-flow/earnings definitions, and limitations. The peer result is especially charge-sensitive because ACI's FY2025 GAAP EPS includes the opioid-settlement-framework charge.

## Presentation route

### 1. Target selection

I selected ACI because it is a large, publicly reported food-and-drug retailer whose economics can be traced from store sales and gross margin through working capital, capex, debt, and equity cash flow. It has recognizable operating drivers—identical sales, pharmacy/digital mix, shrink/productivity, inventory, and capital spending—but very thin margins. That makes a small assumption change economically meaningful and testable.

My initial view was cautiously interested because of ACI's scale, local banners, pharmacy, digital, loyalty, Own Brands, and operating cash generation. It became more cautious as I found weak current operating evidence: Q1 FY2026 identical sales excluding fuel declined 0.8%, while gross margin and adjusted EBITDA margin also fell. The underlying research and source log are in [the ACI research report](../TICKER-research/ACI_2026-09-03_report.md) and [source log](../TICKER-research/source.md).

### 2. Company and evidence

ACI sells food and drug products through supermarkets, pharmacies, fuel centers, digital pickup/delivery, private brands, and retail media. Its FY2025 10-K reports 2,244 stores under 22 banners. The three annual reporting periods used in the pro-forma are FY2023 (ended February 24, 2024), FY2024 (ended February 22, 2025), and FY2025 (ended February 28, 2026, a 53-week year). Amounts are USD millions.

The facts carrying the forecast are: FY2025 revenue of $83,172.5m; 2.0% identical sales excluding fuel; 27.2% gross margin; $5,173.9m inventory; $9,903.7m net PP&E; and $8,946.6m debt and finance leases. Reported FY2025 growth of 3.5% is not used mechanically because the extra week contributed about $1.36bn of sales. FY2025 GAAP earnings also include a $773.8m pre-tax opioid-settlement-framework charge. The history grid, calculation definitions, and direct 10-K links are documented in [Lab 10](../Lab%2010/README.md).

### 3. Pro-forma

The starting balance sheet is FY2025. Revenue growth is 0.5%, 1.0%, 1.5%, 2.0%, and 2.0% in FY2026E–FY2030E—below recent normalized identical-sales history initially, then recovering gradually. Gross margin starts at 27.0% and rises only to 27.2%, because pharmacy/digital mix and delivery costs have pressured margin. SG&A as a share of gross profit declines from 93.5% to 92.3% after excluding the unusual opioid charge from the starting run rate; this allows limited ACI Edge productivity rather than assuming a major improvement.

Other key assumptions are 31.2 inventory days, depreciation at 19.3% of opening PP&E, flat $2.1bn capex, 25.5% tax, $50m annual debt repayment, $330m annual dividends, a $100m minimum cash floor, and a revolver only if cash would otherwise fall below that floor. The model forecasts the income statement, balance sheet, FCFE, and cash in sequence. It asserts every projected balance sheet balances and that cash remains at or above the floor; no base-case year draws the revolver. The linked [Lab 10 model](../Lab%2010/proforma.py) reproduces the full statements.

The base forecast reaches FY2030 revenue of $89,152.5m, operating income of $1,867.2m, FCFE of $781.4m, and cash of $1,553.1m. These are forecast outputs, not company guidance.

### 4. Valuation

The pro-forma uses an FCFE valuation: forecast FCFE is discounted at a 10.0% cost of equity, then a 2.0% terminal-growth rate is applied after FY2030. It produces $8,401.0m of equity value, $16.82 per share, and a 73.6% terminal-value share. The share basis is 499.5m shares. The saved market quote is $11.95 on September 24, 2026; both are USD per share.

The earlier FCFF DCF used an enterprise-value-to-equity bridge: starting FCFF of $936.75m, 8.0% WACC, 2.5% terminal growth, $198.6m cash, $8,946.6m debt, and 547.2m diluted shares. It produced $15.22 per share on September 10, 2026, with 76.8% of enterprise value from terminal value. At the $11.70 September 10 price, its reverse DCF required a -2.6815 percentage-point uniform shift to the five 2.0% explicit FCFF growth rates, holding all other stated inputs fixed. See [Lab 6](../Lab%2006/lab06_aci_dcf.md) and [DCF code](../Lab%2006/dcf.py).

The peer P/E comparison is not averaged into either DCF. Kroger is the closest operating peer; Sprouts is a qualified, less comparable specialty-grocery endpoint. At the September 10, 2026 close and using annual reported GAAP diluted EPS, the range is $5.44–$14.77 per ACI share (median $10.11). ACI's opioid charge, Kroger's impairment-related charges, and Sprouts' differing business mix limit the comparison. See [Lab 8](../Lab%2008/lab08_aci_pe_comps.md) and [the calculator](../Lab%2008/pe_comps.py).

### 5. Sensitivity and drivers

Lab 11 changes one driver at a time in every forecast year while keeping the rest of the base case fixed. Revenue growth is shifted by ±1.0 percentage point; gross margin is shifted by ±0.5 percentage point. The model reruns the statements, FCFE, liquidity logic, balance-sheet checks, and FCFE valuation in each case.

| Isolated case | FY2030 revenue | FY2030 FCFE | Equity value | Value/share |
|---|---:|---:|---:|---:|
| Revenue growth: -1.0 pp | $84,842.1m | $766.0m | $8,332.7m | $16.68 |
| Revenue growth: base | $89,152.5m | $781.4m | $8,401.0m | $16.82 |
| Revenue growth: +1.0 pp | $93,636.3m | $795.5m | $8,455.3m | $16.93 |
| Gross margin: -0.5 pp | $89,152.5m | $755.1m | $8,073.1m | $16.16 |
| Gross margin: +0.5 pp | $89,152.5m | $807.7m | $8,729.0m | $17.47 |

The causal chain is explicit. A revenue change affects revenue, gross profit at the unchanged margin, inventory, other operating liabilities, and then FCFE. A margin change affects gross profit; SG&A remains tied to gross profit through the base SG&A/gross-profit ratio, so operating income, tax, net income, FCFE, and value change. Over these tested ranges, margin moves value more than revenue growth: the downside/upside margin cases differ from base by -$0.66/+ $0.65 per share, versus -$0.14/+ $0.11 for revenue. That ranking is conditional on the chosen ranges and model mechanics; it does not prove margin is always more important than sales growth. Full assumptions and reproducible output are in [Lab 11](../Lab%2011/README.md) and [its model](../Lab%2011/proforma.py).

### 6. Interpretation and next evidence

My conditional conclusion remains watch/defer. I would upgrade the view only after evidence of positive comparable-sales momentum, stable or improving margin, cash flow after capex and opioid payments that supports debt reduction, and demonstrated—not merely announced—ACI Edge benefits. I would downgrade it if comparable sales, gross margin, or cash generation weaken further, or if debt does not fall despite cash generation.

The question I would investigate next is whether ACI Edge can offset the margin pressure from pharmacy/digital mix. The falsifiable evidence is the next filing's identical-sales result, gross margin, SG&A relative to gross profit, operating cash flow less capex, opioid cash payments, and debt. Since selecting ACI, I have moved from a general interest in its scale and cash generation to a conclusion that evidence of recovery must precede an investment conclusion.

## Review record

The final partner exchange is saved separately in [partner_interaction_final.md](partner_interaction_final.md). It records the specific questions, source/calculation checks, explain-back, feedback, and post-review actions required for both the ACI presenter role and the Robinhood reviewer role.

No new computation was required for Lab 12. To reproduce the referenced results, run `python proforma.py` in [Lab 11](../Lab%2011/) and the linked Lab 6, 8, and 10 programs from their respective folders.
