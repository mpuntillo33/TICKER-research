# Validation and AI-Use Record

Built with AI assistance for education only; this is not investment advice.

## Baseline checks

`python "Lab 20/readiness.py"` uses the Lab 15 portfolio engine without duplicating its math. It compares three baselines and searches every long-only 5-point mix, retaining only allocations that meet both the 6.5% planning objective and 3% reserve minimum before selecting the lowest-volatility feasible mix. The exact printed result is committed in `../output/baseline.txt`.

The point-in-time data rule and DGS3MO data card are documented in [Lab 17](../../Lab%2017/README.md#data-card--dgs3mo). It admits only the ALFRED vintage knowable on the decision date and quarantines material revision or lag risk.

## Locked changed-input record — prediction (committed before run)

- **Input:** annual equity expected-return estimate.
- **Old value:** 8.0% per year.
- **New value:** 7.0% per year.
- **Prediction:** reducing equity's estimated return should make equity less attractive, lower the selected portfolio's expected return, and could make the 6.5% objective harder to meet. I expect the allocation and possibly the pilot decision to change.
- **Decision expectation:** remain pilot, not adopt, because the test is a sensitivity check rather than evidence of future performance.

## Locked changed-input record — actual result

`python "Lab 20/readiness.py" --equity-return 7.0` produced the committed `../output/changed-input.txt` result. The selected mix changed from 0% bills / 20% 10-year / 25% investment-grade bonds / 55% equity to 0% / 10% / 10% / 80%: the largest weight change was **25 percentage points**. Its expected return was 6.53%, volatility was 12.94%, and reserve-eligible weight was 10%; it still passed both modeled mandate checks.

The allocation direction did **not** match the simple prediction that lower equity return would reduce the equity weight. On a coarse 5-point feasible grid, the lower estimate makes the original mix fall below the 6.5% threshold, so the least-volatile remaining feasible combination is more equity-heavy. The pilot/not-adopt decision did not change, because this unstable boundary result is exactly the sensitivity that prevents adoption.

## Cold run, code explanation, and fix

Charlie Garrison ran the repository instructions independently. The cold run had no failures, took 2 minutes, and reached the command-line baseline and mandate verdict. The partner record was used to fix the repository discovery issue: a root README now supplies one command and names the visible GitHub outputs.

The decision-number block is `search_lowest_risk_mix` in `Lab 15/portfolio.py`: it enumerates long-only 5-point weight combinations, filters out combinations below the return or reserve thresholds, computes full-covariance volatility for the survivors, then retains the smallest value. `Lab 20/readiness.py` supplies the editable equity input, calls that block, and prints the return and reserve verdicts. The unresolved in-person partner code-explanation question is not claimed here.

## AI use

AI was used to help organize the runnable readiness wrapper and documentation. The numerical outputs were independently rerun from the existing Lab 15 engine. AI did not supply market data, override the point-in-time admission rule, or make an investment recommendation.
