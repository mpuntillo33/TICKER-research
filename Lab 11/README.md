# Lab 11 - ACI One-at-a-Time Sensitivity Analysis

**Company:** Albertsons Companies, Inc. (NYSE: ACI). Dollar figures are USD millions except per-share values. This lab extends the balanced FY2026-FY2030 pro-forma built in Lab 10; its opening FY2025 balance sheet, operating assumptions, discount rate, and valuation method are unchanged.

## Question and base case

What happens to the ACI equity value when one important operating assumption changes while everything else remains at the Lab 10 base case?

The base revenue-growth path is 0.5%, 1.0%, 1.5%, 2.0%, and 2.0%. The base gross-margin path is 27.00%, 27.05%, 27.10%, 27.15%, and 27.20%. These were intentionally restrained: FY2025 reported growth included a 53rd week, while identical sales excluding fuel were 2.0%, and pharmacy/digital mix can pressure margin. The filing support and historical-ratio calculations are documented in [Lab 10](../Lab%2010/README.md).

## Sensitivity design

This is **one-at-a-time** analysis, not a combined upside/downside matrix. Each shock is applied to every year FY2026-FY2030 and all other assumptions remain fixed.

| Driver | Downside path | Base path | Upside path |
|---|---|---|---|
| Revenue growth | Base minus 1.0 percentage point | 0.5%, 1.0%, 1.5%, 2.0%, 2.0% | Base plus 1.0 percentage point |
| Gross margin | Base minus 0.5 percentage point | 27.00% to 27.20% | Base plus 0.5 percentage point |

For example, FY2026 revenue growth is -0.5% / 0.5% / 1.5%; FY2026 gross margin is 26.50% / 27.00% / 27.50%. A revenue case retains the base gross-margin path, and a margin case retains the base revenue-growth path.

`proforma.py` recomputes the income statement, balance sheet, FCFE, revolver logic, and equity value for every case. It calls a balance-sheet and minimum-cash assertion in every forecast year, so a sensitivity cannot silently break the model.

Run:

```powershell
python proforma.py
```

## Interpretation

The printed table reports FY2030 revenue, FY2030 FCFE, equity value, and value per share for each case. Revenue growth changes sales and working capital; gross margin changes gross profit, SG&A (held at the base SG&A/gross-profit ratio), income, and FCFE. The cases should not be added together: they are isolated views of the sensitivity of the same valuation.

## Partner exchange

**Partner challenge:** “A ±1.0 percentage-point revenue shock is large relative to the 0.5% FY2026 base. Why not combine it with the ±0.5-point margin shock to show a full bear and bull case?”

**My response:** “That would answer a different question. This assignment asks for one-at-a-time sensitivity, so combining the shocks would hide which driver created the value change. The growth range is deliberately wide enough to test a flat-to-recovering identical-sales outcome, while the margin range separately tests mix, shrink, and productivity risk. I would present a combined scenario only as a clearly labeled next step.”

**My challenge to the partner:** “Your margin upside needs a filed or operating mechanism—such as lower shrink, supplier funding, or ACI Edge productivity—and a quarterly KPI that could falsify it. Which one is it?”

**Partner response:** “I would use gross margin and SG&A as a percentage of gross profit in the next quarterly filing; without improvement in at least one, I would remove the margin upside.”

## Conclusion

The sensitivity is a valuation diagnostic, not an investment recommendation. The base case continues to use a 10.0% cost of equity, 2.0% terminal growth, 499.5m shares outstanding, flat $2.1bn annual capex, and the Lab 10 liquidity safeguards. The model output is the auditable numerical result for the six isolated cases.
