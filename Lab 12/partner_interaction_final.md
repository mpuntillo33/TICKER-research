# Lab 12 — Final Partner Interaction Record

**Participants:** ACI presenter/reviewer and Robinhood (HOOD) presenter/reviewer
**Format:** Final draft of the in-class review notes. Dollar amounts cited in the ACI discussion are USD millions except per-share values.

## ACI presentation — Robinhood partner reviewed

**Partner:** “You started at 0.5% revenue growth even though ACI reported 3.5% FY2025 revenue growth. What makes that a defensible starting point rather than a bearish guess?”

**ACI presenter:** “The reported growth contains a 53rd week, which contributed about $1.36bn of sales. The better operational comparison is identical sales excluding fuel, which was 2.0%. I start below that at 0.5% because the next Q1 showed identical sales down 0.8%, then I only step the forecast up to 2.0% by FY2029–FY2030. The primary check is the FY2025 10-K and the Q1 FY2026 filing cited in the research report.”

**Partner follow-up:** “If the first-quarter decline is your reason for starting low, why do you allow recovery at all?”

**ACI presenter:** “It is a judgment, not guidance. The recovery path reflects ACI's scale and stated ACI Edge productivity effort, but I did not credit a large margin recovery. That is why it stays at 2.0%, not at the headline 3.5% reported FY2025 growth. If future identical sales remain negative, I would revise the later recovery years down instead of treating the path as established fact.”

**Partner:** “Trace the 0.5-point gross-margin sensitivity all the way to the value. I want to know whether it is just a revenue shortcut.”

**ACI presenter:** “It is not a revenue change: FY2030 revenue stays $89,152.5m in all three margin cases. A 0.5-point lower margin reduces gross profit; SG&A remains linked to gross profit at the model's base SG&A/gross-profit ratio, so operating income, tax, net income, and FCFE fall. FY2030 FCFE moves from $781.4m in base to $755.1m in the downside, and equity value moves from $8,401.0m/$16.82 per share to $8,073.1m/$16.16 per share. The upside reaches $8,729.0m/$17.47. The Lab 11 program reruns the balance-sheet and minimum-cash assertions in each case.”

**Partner:** “Your model produces $16.82 per share, but the earlier P/E range tops out at $14.77. Why don't you average them?”

**ACI presenter:** “They do not measure the same thing cleanly enough to average. The P/E result capitalizes FY2025 reported GAAP EPS of $0.40, which includes the opioid charge. The FCFE model values a five-year cash-flow recovery and uses 499.5m shares, while the earlier FCFF DCF uses 547.2m diluted weighted-average shares and a different valuation date. Averaging would hide the disagreement instead of explaining it. The unresolved issue is the extent and timing of opioid cash payments and whether operating results improve without relabeling charges as adjusted.”

**Check performed together:** We opened the ACI FY2025 10-K through the direct link in [Lab 10](../Lab%2010/README.md) and traced FY2025 revenue ($83,172.5m), inventory ($5,173.9m), and the reported opioid charge into the model rationale. We then ran [Lab 11's `proforma.py`](../Lab%2011/proforma.py) and matched the printed base value ($16.82/share) and gross-margin downside ($16.16/share) to the sensitivity table. The check supported the stated model arithmetic and source linkage; it did not prove the recovery assumptions.

**Partner explain-back:** “Your conclusion is watch/defer, not buy, even though the FCFE output exceeds the saved market price. Margin is the largest tested driver because a 0.5-point shift changes FCFE and terminal value more than the chosen 1-point growth shift. The biggest limitation is that the model's recovery and terminal value are assumptions, while the peer P/E denominator is distorted by unusual charges.”

**ACI presenter correction:** “That is accurate. I would add that the margin-versus-growth ranking only applies to the exact ranges tested; it is not a general proof that margin always matters more.”

**Partner feedback:**

- Strength: “The assumptions are connected to reported facts—the 53rd week, identical sales, pharmacy/digital margin pressure, and the opioid charge—rather than copied from headline revenue growth.”
- Improvement: “Add the next-quarter evidence that would make you change each later revenue-growth year, especially identical sales and gross margin, so the recovery path has a more explicit update rule.”

**ACI post-review decision:** Keep the base conclusion and the one-at-a-time sensitivity design. Investigate the next reported identical-sales, gross-margin, SG&A/gross-profit, operating-cash-flow-less-capex, opioid-payment, and debt disclosures. The review does not change the conclusion because it validated the arithmetic and exposed the same unresolved evidence gap already driving the watch/defer view.

## Robinhood presentation — ACI reviewer reviewed

**ACI reviewer:** “Robinhood earns from transaction-based activities, net interest revenue, and other platform services rather than grocery sales. Which of those is your main valuation driver, and what filed metric shows that it can persist without assuming a favorable trading or crypto cycle forever?”

**Robinhood presenter:** “My main driver is diversified platform revenue, but I separate transaction-based revenue from net interest revenue rather than treating total revenue growth as one permanent rate. I use the annual report's revenue disaggregation and operating metrics to identify the starting mix, then test a lower-growth case for the more market-sensitive activity.”

**ACI reviewer follow-up:** “What happens in your model if interest rates fall or customer trading activity normalizes? Show me the line that changes, rather than only saying the risk exists.”

**Robinhood presenter:** “A lower-rate case reduces projected net interest revenue; a lower-activity case reduces transaction-based revenue. Both lower operating income and cash flow, but the effect differs because the revenue streams have different economics. I keep the expense assumptions visible so the valuation does not imply fixed margins regardless of revenue mix.”

**ACI reviewer:** “For your valuation, why are your peer choices comparable to Robinhood rather than simply other companies with high growth? Also, if you use P/E, are the earnings positive and from a period that matches the price date?”

**Robinhood presenter:** “My direct comparisons are with listed financial-platform or brokerage businesses, and I explain differences in customer base, product mix, regulation, balance-sheet interest income, and crypto exposure. I match the price date to the annual reported GAAP earnings period that was public by that date. I do not apply a P/E to a nonpositive earnings measure or blend it mechanically with a DCF.”

**ACI reviewer:** “Does your sensitivity ranking depend on the ranges you picked? For example, a small rate change and a large transaction-volume change might make a ranking look more certain than it is.”

**Robinhood presenter:** “Yes. The ranking is conditional on the disclosed ranges. I present it as a scenario diagnostic, not proof of the permanent most-important driver. The evidence that would change my conclusion is later disclosure of revenue mix, funded customers/assets, trading activity, net interest revenue, and the regulatory or market conditions affecting those lines.”

**Check performed together:** We opened Robinhood's [FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm), filed February 18, 2026, and checked the business description and the revenue/operating-metric disclosures used by the Robinhood presenter. We confirmed that Robinhood is a financial-services platform with brokerage, crypto, advisory, digital-banking, and private-markets offerings. The source supported the business-model description and the need to separate revenue drivers; it did not validate any unshared forecast assumptions or valuation result.

**ACI reviewer explain-back:** “Your conclusion is conditional on the durability of the platform's revenue mix, not merely on high headline growth. Your main uncertainty is sensitivity to market activity and rates, plus the comparability of peers with different product and regulatory exposures. You will revisit the conclusion when reported mix and operating metrics show whether the model's assumptions held.”

**Robinhood presenter correction:** “That is accurate. I would also keep the distinction between a scenario result and management guidance clear.”

**ACI reviewer feedback:**

- Strength: “You separated the economic drivers instead of applying one growth rate to all revenue.”
- Improvement: “Put the held-fixed assumptions beside each sensitivity result and show one fully traced case from revenue driver through expenses, cash flow, and value.”

## Reflection

The question that made me reconsider my ACI work was the request to justify each later recovery year after the weak Q1 comparable-sales result. I now understand more clearly that the model is not improved by calling a recovery conservative; it needs a filing-based update rule. The next-quarter sales, margin, cash-flow, opioid-payment, and debt evidence will determine whether the recovery path remains defensible.
