# Research Evolution — Project 1 (ACI)

## Edition A — unchanged baseline

**Receipt status (stated plainly):** Edition A was **not submitted** to the Brightspace "Project 1 — Edition A
Checkpoint (AI Closed)" assignment, so no checkpoint receipt exists. Following Dr. Zhang's clarification, the
original file is included unchanged rather than recreated.

**Corroborating evidence:**
- The original file, `Project 1 Edition A - ACI.md`, was last modified **Sept 1, 2026, 5:41:43 PM EDT** and has not
  changed since. SHA-256 `e0d395c77c43c8077ee71dfdee020e887e91be6dd8aba6841905e4d159e232b7`; the repository copy
  (`docs/edition-a/`) matches byte for byte.
- Brightspace records my **Lab 03 checkout** (the supervised, AI-off Edition A lab) as *written Sept 1, 2026,
  4:53 PM – 5:48 PM*, 25/25. It contains my FY2025 10-K analysis from the same session (local file saved 5:47 PM).
  The Edition A file was saved inside that window. Screenshots: `docs/edition-a/lab03-checkout-1..3.png`.

*[The unchanged Edition A text follows on the next page of the PDF, printed from the original file.]*

## Dated correction addendum

None. Edition A's facts (FY2025 revenue $83,172.5m; cash $198.6m; debt incl. finance leases $8,946.6m; net debt
$8,748.0m; 547.2m diluted weighted-average shares; diluted EPS $0.40; 2,244 stores) match the 10-K. Later changes
are updates to newer evidence, recorded in Edition B, not corrections.

## Edition B — after project-specific research and disclosed AI assistance

### Current decision and intended user

The fund's investment committee (no position) should place ACI on **watch/defer**, with a valuation range of
**$13–$19 per share** (base $17.89) against a $13.09 price on Oct 16, 2026, and revisit at Q3 FY2026 results and
the Q4 FY2026 turnaround plan. Initiation requires evidence that SG&A as a share of gross profit is falling.

### A-to-B evidence table

| Item | Edition A (Sept 1) | Edition B (Oct 19) | Primary driver of change | Evidence/test justifying changed or unchanged position |
|---|---|---|---|---|
| Thesis/recommendation | Watch/defer; no valuation yet ("one annual filing and no market-price … work") | **No material change in the call:** watch/defer, now with a $13–$19 range and dated triggers | Mixed: own analysis + new company evidence | Q1 and Q2 FY2026 identical sales −0.8%; guidance withdrawn Oct 13, 2026; reverse DCF implies no cost recovery (FY2030 SG&A/GP 93.9%); flat 94.0% gives $12.69 < $13.09 |
| Data/source choice | FY2025 10-K only; Feb 28, 2026 balance sheet; 547.2m diluted weighted-average shares | 10-K + Q1 10-Q + Q2 8-K; Sept 12, 2026 bridge (debt $9,328.2m, cash $282.0m, opioid obligation $773.8m); 488.2m diluted shares; dated price and WACC inputs | Course instruction (as-of discipline, contamination catalog) + own analysis; AI helped locate the Q2 release and share count | 26.0m shares repurchased in 28 weeks made 547.2m stale (≈12% overstatement); provider "total debt" ($15.92bn) includes operating leases, so the bridge uses filed debt incl. finance leases |
| Assumption/model design | Plan only: DCF + comps, bridge EV − $8,748.0m | Pro-forma-driven FCFF DCF; 52-week normalized base; opioid charge out of SG&A and into the bridge; payables at 24.2 days; WACC 7.7% built from sourced inputs; EV/EBITDA and P/E comps under one definition | Course instruction (Weeks 3–6) + AI (engine build, payables proposal) + own review | Payables proposal checked on the 10-K balance sheet ($4,021.2m) and accepted; 10 tests pass incl. course known answers $27.4974 and $291.75; Locked Changed-Input Record (commits `7ae0841`, `6d9c64e`) |
| Risk/limitation/uncertainty | "Can cash flow service or reduce $8.748bn net debt while reinvesting?" | Main risk moves to the **cost ratio**: value swings ≈$2.60/share per 0.5 pt of SG&A/GP; terminal value 79.7% of EV; no management guidance; debt still rising (Q2 net debt ratio 2.42 vs 2.02) | Own analysis + peer challenge (Lab 12 partner asked why recovery is allowed at all and why the methods are not averaged) | Base-case FCFF stays positive at ≈$0.9–1.15bn a year after $2.0bn capex and cash builds without the revolver, so debt service is not the binding question; one-at-a-time sensitivity and the range-dependence test show SG&A/GP and WACC dominate |

### What changed from Edition A to Edition B, and why?

The **call did not change**: Edition A said watch/defer before any valuation, and Edition B still says watch/defer.
What changed is that the call now rests on tested evidence instead of missing evidence. Three things moved it.
First, new company evidence: two straight quarters of −0.8% identical sales and the Oct 13 guidance withdrawal
mean nothing from management anchors FY2026. Second, my own model: once the FCFF DCF was driven by the pro-forma,
the value turned out to hinge on one ratio, SG&A as a share of gross profit, and the reverse DCF showed the
$13.09 price already assumes no improvement in it. That makes ACI neither clearly cheap nor clearly expensive.
It is a bet on the turnaround. Third, course instruction and a partner challenge pushed me to normalize the base year,
fix the share basis and bridge date, keep the methods separate instead of averaging them, and justify why the model allows any recovery at all.
AI sped up the engine build and proposed the payables change; I accepted that only after checking the 10-K. The
risk Edition A worried about, debt capacity, turned out to be secondary in the base case; the binding risk is
whether costs come down. The evidence that would change the call is named in the memo's triggers.
