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

## Cold run, code explanation, and fix

Charlie Garrison ran the repository instructions independently. The cold run had no failures, took 2 minutes, and reached the command-line baseline and mandate verdict. The partner record was used to fix the repository discovery issue: a root README now supplies one command and names the visible GitHub outputs.

The decision-number block is `search_lowest_risk_mix` in `Lab 15/portfolio.py`: it enumerates long-only 5-point weight combinations, filters out combinations below the return or reserve thresholds, computes full-covariance volatility for the survivors, then retains the smallest value. `Lab 20/readiness.py` supplies the editable equity input, calls that block, and prints the return and reserve verdicts. The unresolved in-person partner code-explanation question is not claimed here.

## AI use

AI was used to help organize the runnable readiness wrapper and documentation. The numerical outputs were independently rerun from the existing Lab 15 engine. AI did not supply market data, override the point-in-time admission rule, or make an investment recommendation.
