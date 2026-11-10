# Validation and AI-use record

**AI announcement.** I used OpenAI Codex as a coding and review assistant to organize this repository and review its cold-run documentation. I checked the calculations, evidence, and decision myself. **Education only; not investment advice.**

## Riskiest claim trace

| Element | Record |
|---|---|
| Claim | The constrained allocation is stable enough to use beyond a pilot. |
| Source | `Lab 15/portfolio.py` (engine), `Lab 15/app.py` (interface), and `Lab 14/prices.csv` (BIL, IEF, LQD, VT monthly adjusted closes). |
| Test | In the documented Meridian run, change the equity expected-return estimate from 8.0% to 7.0%; compare selected weights. |
| Observed outcome | The selected allocation changed by 25 percentage points. |
| Decision supported | The result supports **pilot, not adopt**, rather than an adoption recommendation. |
| Reversal condition | Do not continue the pilot if approved stresses exceed the committee tolerance or if the CIO does not set the missing trade-off rule. |

## Independent-challenge record

An independent challenger could reject this model even if its displayed output looks attractive because:

- the 6.5% planning input is an assumption, not a CPI forecast;
- the selection is materially sensitive to a one-point return-estimate change;
- the mandate has an unresolved optimization-priority gap (Lab 13 S10);
- the point-in-time signal and its admission rule are not yet integrated into the allocation app; and
- baseline verdicts and the constrained portfolio are not yet presented side by side in the final app.

Conceptual soundness is limited by the proxy objective and missing priority rule. Outcome analysis includes mandate known answers, correlation validation, the equity-estimate stress, the 36-month-window comparison, and the ALFRED revision probe. Ongoing monitoring must record input-data availability, revisions, mandate breaches, stress movement, and overrides at every decision date.

## Locked Changed-Input Record

**Status: not yet run — frozen as a must-fix, not represented as completed.**

| Field | Record |
|---|---|
| Input to change | Equity expected-return estimate in `Lab 15/app.py` / the final unified app. |
| AI-off prediction, committed before run | A lower equity estimate will reduce VT weight and increase reserve-eligible weight; the decision should remain pilot/not-adopt unless the sensitivity tolerance is exceeded. |
| Run date and commit | Pending final-app integration. |
| Actual result | Pending. |
| Decision effect | Pending; compare with the prediction before changing the recommendation. |

## AI boundary

AI assisted with repository organization and documentation review. It did not supply unverified market data, substitute for the portfolio engine, or make the investment decision. Source facts, calculations, and the decision remain the student's responsibility.
