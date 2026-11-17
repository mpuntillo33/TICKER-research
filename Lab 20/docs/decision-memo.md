# Project 2 Decision Memo

Built with AI assistance for education only; this is not investment advice.

## Committee decision

**Pilot, not adopt** the constrained 0% bills / 20% 10-year Treasury / 25% investment-grade bonds / 55% equity mix as an educational planning result. It has a 6.51% expected return, 9.44% volatility, and 20% reserve-eligible weight on the current 5-point-grid inputs. Reverse the decision if the 6.5% planning proxy (CPI + 4%), the 3% reserve minimum, or the point-in-time data admission rule cannot be defended.

## Mandate and comparison

The objective is CPI + 4% net of costs over rolling five-year periods. The runnable model uses a disclosed 6.5% nominal planning proxy (2.5% CPI + 4%) because the optimizer requires a numeric threshold. BIL and IEF/10-year Treasury are reserve eligible; their combined weight must be at least 3%. The universe is BIL, IEF, LQD, and VT, with long-only 5-point weights.

| Portfolio | Expected return | Volatility | Reserve eligible | Mandate verdict |
|---|---:|---:|---:|---|
| 40/60 IG-bond/equity benchmark | 6.80% | 10.46% | 0% | Fail — reserve |
| Equal weight | 5.20% | 5.21% | 50% | Fail — return |
| Inverse volatility | 3.77% | 1.05% | 90.3% | Fail — return |
| Constrained lowest-risk mix | 6.51% | 9.44% | 20% | Pass |

The changed-input stress is deliberately not an approval test: reducing the equity estimate from 8.0% to 7.0% shifts the selected mix to 0% / 10% / 10% / 80%, a 25-point largest allocation change, and raises volatility to 12.94%. That sensitivity supports a pilot rather than adoption.

## Monitoring and limitations

Re-run before each decision date with the current point-in-time-approved inputs. Pause or reject the pilot if no mix clears the return and reserve rules, if an input change causes a 25-point-or-larger allocation change without committee review, or if the DGS3MO vintage audit reveals a material revision or lag overlapping the decision. This evidence does not validate future returns or replace a CIO decision.
