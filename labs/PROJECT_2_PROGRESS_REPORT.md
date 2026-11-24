# Project 2 progress report — 2026-11-03

This review checks Labs 13–18 against the published Project 2 requirements. A lab artifact counts as progress, not a final feature, until it is integrated into the final app and documented for a reviewer.

| Lab | Finished evidence | Project 2 value |
|---|---|---|
| 13 | `Lab 13/mandate.py` and notes | Mandate foundation: CPI + 4% objective, 3% reserve minimum, liquidity and issuer-limit checks. |
| 14 | Baseline engine, price data, and notes | BIL/IEF/LQD/VT universe, benchmark and equal-weight baselines, covariance validation. |
| 15 | Streamlit optimizer and stability documentation | Rerunnable allocation engine and an estimate/correlation/window stress. A one-point estimate change moved the allocation 25 points; current call is pilot, not adopt. |
| 16 | Point-in-time provenance gate | Removes duplicate, unavailable, and stale-vintage observations before a signal is calculated. |
| 17 | FRED/ALFRED Streamlit audit and DGS3MO data card | Point-in-time source, vintage audit, revision probe, and an admission rule. |
| 18 | EDGAR Buffett skill and app | Validated security-quality diligence: COST matches the known answer; JPM keeps missing owner-earnings inputs unknown. It is not yet a portfolio-decision input. |

## Current rubric status

| Requirement | Status | Needed next |
|---|---|---|
| One runnable web app | In progress | Combine the Lab 15 allocation engine, baseline comparison, and signal into one final app with a single README/cold run. |
| Mandate | Substantially complete | Put final objective, universe, benchmark, risk measure, and every limit in the final app. |
| Two baselines + constrained portfolio, each with mandate verdict | Partial | Show all three together and label every rule pass/fail. |
| Point-in-time signal + data card | Partial | Connect an as-of signal and decision rule to the allocation process. |
| Stress run + stop condition | Partial | Formalize tested ranges, results, and a measurable pause/reject condition. |
| Locked Changed-Input Record | Not yet evidenced | Commit the AI-off prediction before a final-app changed-input run, then record expected/actual direction and decision effect in `docs/validation-and-ai-use.md`. |
| Recommendation, allocation range, monitoring triggers | Partial | Expand “Pilot, not adopt” into an allocation range and explicit rebalance/pause/reject triggers. |
| Required AI/not-advice statements | Partial | Include both statements at the opening of final README, memo, and each video. |

## Recommended sequence

1. Build the unified final app from the Lab 15 engine.
2. Add the point-in-time signal and data card with a clear decision rule.
3. Add baseline/mandate verdict and stress/stop panels.
4. Create `docs/decision-memo.md` and `docs/validation-and-ai-use.md`, including the Locked Changed-Input Record before its test.
5. Cold-run, then record required videos and transcripts.

## Lab 18 decision

I trust the COST quality-screen verdict as a narrow filing-based check because the five known-answer rows reconciled and all three checks passed. It is not an allocation recommendation because it uses no price, valuation, portfolio mandate, or risk analysis.
