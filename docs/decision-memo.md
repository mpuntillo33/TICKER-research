# Project 2 decision memo

**AI announcement.** I used OpenAI Codex as a coding and review assistant to organize the project bundle and audit the evidence. I checked the calculations, evidence, and decision myself. **Education only; not investment advice.**

## Decision

**Pilot, not adopt.** The process can be used only as a small, separately approved pilot after the CIO documents the inflation assumption and a rule for resolving the mandate's unspecified trade-offs. It is not a recommendation to buy or sell any security.

## Evidence and condition

The mandate objective is CPI + 4% net of costs over rolling five-year periods, with a 3% reserve minimum. Using the Lab 14 monthly BIL, IEF, LQD, and VT data, the all-history constrained result was 60% BIL / 40% VT, with a 6.61% annualized arithmetic historical estimate, 6.05% estimated volatility, and 60% reserve-eligible weight. The last-36-month result was 85% BIL / 15% VT, 6.75%, 1.79%, and 85%, respectively. Historical estimates are not forecasts.

The riskiest decision claim is stability of the selected allocation. In the documented Meridian stress test, lowering the equity expected-return input from 8.0% to 7.0% changed the selected allocation by 25 percentage points. That is large enough to prevent adoption until the input and trade-off governance are settled.

## Monitoring and reversal

Monitor each decision date for: (1) every mandate verdict, including the 3% reserve minimum; (2) the as-of availability, units, revision, and lag checks for the admitted signal; and (3) maximum allocation change under the approved return, window, correlation, cost, and constraint stresses.

Pause or reject the pilot if a hard mandate rule fails, the signal fails its point-in-time admission rule, or a stress rerun produces an allocation change beyond the committee-approved tolerance. Reverse the pilot recommendation if the final locked changed-input record contradicts the predicted decision effect or if the CIO cannot resolve the missing priority rule.
