# Decision Memo: Reserve Portfolio Process

**AI use:** I used Claude (Anthropic, Claude Opus 5.5) to help write the engine, app and tests and to draft this memo. The mandate, assumptions, checks and recommendation are mine; I reviewed and edited every line. The full record is in [validation-and-ai-use.md](validation-and-ai-use.md).
**Education only, not investment advice.**

To: Investment committee, $100 million reserve · From: Max Puntillo, portfolio analyst · As of: **2026-10-05** (data as known that day) · Horizon: rolling five-year periods

## Recommendation: PILOT, do not adopt yet

Run the constrained process as a **pilot on 20% of the reserve ($20 million) for two quarters** at the target mix below, and do not move the full reserve to it yet.

| Sleeve | Target | Allocation range (rule below) |
|---|---:|---:|
| BIL, 1–3 month T-bills | 35% | 0% to 60% |
| IEF, 7–10 year Treasuries | 5% | 0% to 45% |
| LQD, investment-grade corporates | 0% | 0% to 10% |
| VT, global equity | 60% | 40% to 80% |

The target mix has a 6.55% expected return, 9.25% volatility, a −12.6% worst 12-month loss in the history, and 40% reserve-eligible weight. It passes every mandate rule.

**Range rule:** each sleeve's range runs from its lowest to its highest weight across the ten stress cases that still pass the mandate. A range this wide is the main finding: the process can land in very different places when one input moves, so it is not ready for the full reserve.

**Committee ask:** approve the $20 million pilot at the target mix, with the triggers below, and a re-run at each quarter-end. Full adoption should come back to the committee only after two quarters with no stop condition firing.

Project 2 has no Edition A or Edition B (course ruling), so this memo is the single written decision.

## Mandate and how each portfolio does

The objective is CPI + 4% net of costs over rolling five-year periods, modeled as **6.5% nominal** (2.5% CPI planning assumption + 4%). Limits: reserve-eligible BIL + IEF ≥ 3% (four quarters × $0.75 million ÷ $100 million); volatility no higher than the 40/60 LQD/VT benchmark (12.33%); at least 90% liquid within 5 days; 8% single-issuer limit (funds and Treasuries are exempt); long-only.

| Portfolio | BIL / IEF / LQD / VT | Return | Volatility | Verdict |
|---|---|---:|---:|---|
| Equal weight (baseline 1) | 25 / 25 / 25 / 25 | 5.72% | 7.55% | Fail: return objective |
| 40/60 LQD/VT benchmark (baseline 2) | 0 / 0 / 40 / 60 | 7.11% | 12.33% | Fail: reserve rule |
| Constrained lowest-risk mix | 35 / 5 / 0 / 60 | 6.55% | 9.25% | Pass |

The constrained process does what neither simple baseline can: it clears the return target while keeping the reserve and staying below benchmark risk.

## Evidence and assumptions

- **Expected returns are point-in-time yields, net of fees.** BIL = 3-month T-bill yield (DGS3MO 4.19%, the signal) − 0.1353% fee. IEF = 10-year yield (5.28%) − 0.15%. LQD = Baa yield (6.47%) − 0.75% credit haircut − 0.14%. VT = T-bill yield + 4% equity premium − 0.06%. Every yield is the value published on or before 2026-10-05 (ALFRED vintage), so nothing from after the decision date leaks in.
- **Risk comes from history.** Volatility, correlations and worst 12-month loss use 59 monthly returns, October 2021 to September 2026 (Yahoo Finance adjusted closes).
- **Assumptions I chose:** the 2.5% CPI figure, the 4% equity premium and the 0.75% LQD haircut. Each is a planning number, not a forecast, and each is stressed below.

## Stress run and stop condition

| Stress | Mix (BIL / IEF / LQD / VT) | Largest move |
|---|---|---:|
| Equity premium 3% / 5% | 20/0/0/80 · 50/0/0/50 | 20 / 15 pts |
| T-bill signal −50 bp / +50 bp | 0/45/0/55 · 50/0/0/50 | **40** / 15 pts |
| Risk window: last 36 months | 30/5/10/55 | 10 pts |
| Costs +25 bp / +50 bp | 30/5/0/65 · 20/10/0/70 | 5 / 15 pts |
| Reserve minimum raised to 10% | 35/5/0/60 | 0 pts |
| Historical average returns | 60/0/0/40 | **25** pts |

**Stop condition:** the process pauses if any single input change leaves no mix that passes the mandate, or swings any sleeve by 25 points or more. It fires twice: a 50 bp lower T-bill yield moves 40 points from bills into IEF, and switching to historical average returns moves 25 points. Those two results are why this is a pilot.

In my locked changed-input test (equity premium 4.0% → 4.5%, prediction committed before the run) the mix moved from 35/5/0/60 to 45/0/0/55, volatility fell from 9.25% to 8.27%, and the decision stayed PILOT. My prediction, the result and my diagnosis are in the validation record.

## Risks and monitoring triggers

| Trigger | Action |
|---|---|
| DGS3MO as known moves 50 bp or more from 4.19%, or quarter-end | Re-run the app on current ALFRED vintages |
| Any sleeve drifts 5 points or more from target | Rebalance to target |
| A re-run finds no feasible mix, or a single input swings a sleeve 25+ points | Pause the pilot and report to the committee |
| Reserve rule or volatility limit breached at quarter-end, or the point-in-time audit finds a material revision overlapping the decision date | Reject and return the pilot to the current policy |

**Principal risks:** the yields are as of October 5 and must be refreshed before money moves; 59 months is a short history that includes the 2022 rate shock; the 5-point weight grid makes the chosen mix jump between neighbours; taxes and bid-ask costs are only covered by the cost-drag stress.

**Reversal:** I would move to ALLOCATE only if a re-run on current data shows every stress case feasible within 25 points for two consecutive quarters, and to REJECT if the base case stops passing the mandate.
