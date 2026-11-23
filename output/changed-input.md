# Project 2 visible output

Built with Claude (Anthropic) assisting code and drafting; the analysis and decision are Max Puntillo's. Education only, not investment advice.

- Decision date (as known on): **2026-10-05**
- Price history: monthly adjusted closes 2021-10-01 to 2026-09-01; risk window 59 months
- Expected-return method: point-in-time; equity premium 4.50%; LQD credit haircut 0.75%; extra costs 0.00%
- Objective: 6.50% nominal (2.5% CPI planning assumption + 4%); reserve minimum 3%; volatility limit = benchmark 12.33%

## Inputs

| Sleeve | Expected return | Volatility |
|---|---:|---:|
| BIL (1-3 month T-bills) | 4.05% | 0.49% |
| IEF (7-10 year Treasuries) | 5.13% | 7.72% |
| LQD (Investment-grade corporates) | 5.58% | 9.87% |
| VT (Global equity) | 8.63% | 14.92% |

Lineage:

- DGS3MO = 4.19% (obs 2026-10-02, known 2026-10-05, FRED/ALFRED DGS3MO; value hand-checked on FRED page in Lab 17 (2026-10-29))
- DGS10 = 5.28% (obs 2026-10-02, known 2026-10-05, ALFRED vintage 2026-10-05; Lab 17 known-answer table)
- BAA = 6.47% (obs 2026-09-01, known 2026-10-05, ALFRED vintage 2026-10-05 (September 2026 monthly); Lab 17 known-answer table)

## Portfolios and mandate verdicts

| Portfolio | Weights | Return | Volatility | Worst 12 mo | Verdict |
|---|---|---:|---:|---:|---|
| Equal weight (baseline 1) | BIL 25% / IEF 25% / LQD 25% / VT 25% | 5.85% | 7.55% | -14.5% | FAIL: Return objective |
| 40/60 LQD/VT benchmark (baseline 2) | BIL 0% / IEF 0% / LQD 40% / VT 60% | 7.41% | 12.33% | -20.6% | FAIL: Reserve-eligible weight |
| Constrained lowest-risk mix | BIL 45% / IEF 0% / LQD 0% / VT 55% | 6.57% | 8.27% | -10.8% | PASS |

## Stress run

| Case | Constrained mix | Return | Volatility | Largest weight move |
|---|---|---:|---:|---:|
| Base case | BIL 45% / IEF 0% / LQD 0% / VT 55% | 6.57% | 8.27% | 0 pts |
| Equity premium -1 pt (3%) | BIL 20% / IEF 0% / LQD 0% / VT 80% | 6.51% | 11.96% | 25 pts |
| Equity premium +1 pt (5%) | BIL 50% / IEF 0% / LQD 0% / VT 50% | 6.59% | 7.53% | 5 pts |
| T-bill signal -50 bp | BIL 35% / IEF 0% / LQD 0% / VT 65% | 6.53% | 9.75% | 10 pts |
| T-bill signal +50 bp | BIL 55% / IEF 0% / LQD 0% / VT 45% | 6.61% | 6.79% | 10 pts |
| Risk window: last 36 months | BIL 45% / IEF 0% / LQD 0% / VT 55% | 6.57% | 6.45% | 0 pts |
| Costs +25 bp per year | BIL 40% / IEF 0% / LQD 0% / VT 60% | 6.55% | 9.01% | 5 pts |
| Costs +50 bp per year | BIL 35% / IEF 0% / LQD 0% / VT 65% | 6.53% | 9.75% | 10 pts |
| Reserve minimum 10% | BIL 45% / IEF 0% / LQD 0% / VT 55% | 6.57% | 8.27% | 0 pts |
| Historical returns, full 59 months | BIL 60% / IEF 0% / LQD 0% / VT 40% | 6.61% | 6.05% | 15 pts |

## Allocation range (rule: min to max across feasible stress cases)

- BIL: 20% to 60%
- IEF: 0% to 0%
- LQD: 0% to 0%
- VT: 40% to 80%

## Decision rule output: **PILOT**

- Equity premium -1 pt (3%): moves a weight 25 pts (stop condition).
