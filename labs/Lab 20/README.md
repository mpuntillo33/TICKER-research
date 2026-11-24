# Lab 20 — Project 2 Readiness

Built with AI assistance for education only; this is not investment advice.

## One-command cold run

From the repository root:

```powershell
python "Lab 20/readiness.py"
```

The command uses the existing Lab 15 optimizer and prints each baseline, the constrained lowest-risk mix, return and reserve-rule verdicts, and the decision line. No package installation or internet connection is required. Results are also committed as [baseline output](output/baseline.txt) and [changed-input output](output/changed-input.txt), so a committee member can read them on GitHub without running code.

To move the load-bearing equity expected-return control, use:

```powershell
python "Lab 20/readiness.py" --equity-return 7.0
```

## Decision line

**Pilot, not adopt** the 0% bills / 20% 10-year / 25% investment-grade bonds / 55% equity constrained mix as an educational planning result. Reverse the decision if the 6.5% planning-return proxy, the 3% reserve rule, or the point-in-time data admission rule cannot be defended.

## Evidence

- [Decision memo](docs/decision-memo.md)
- [Validation and AI-use record](docs/validation-and-ai-use.md)
- [Baseline output](output/baseline.txt)
- [Changed-input output](output/changed-input.txt)
- [Point-in-time data card](../Lab%2017/README.md#data-card--dgs3mo)
- [Lab 15 engine](../Lab%2015/portfolio.py)

## Cold run and fix

Charlie Garrison followed the repository instructions without coaching. The command completed with no failures in **2 minutes**; the results were the command-line baseline and mandate verdict printed by `Lab 20/readiness.py`. The initial repository did not have a root README that identified one Project 2 command and visible output locations. Adding the root README and this folder fixes that discovery problem; the clean cold run is retained as the verification record.

## Boundaries

The 6.5% objective is a 2.5% CPI plus 4% planning proxy, not a forecast. The code searches long-only allocations on a 5-point grid and does not establish future performance, valuation, tax effects, transaction costs, or suitability. The DGS3MO admission rule remains point-in-time: use ALFRED as known on the decision date and quarantine it if a material revision or lag overlaps the decision.
