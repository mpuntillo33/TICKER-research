\## Locked Changed-Input Record — prediction (written AI-off, committed before the run)

\- Written by: Max Puntillo, 11/23/2026, 5:04PM

\- Input changed: Equity Risk Premium over T-bills

\- Old value (units): 4.00%

\- New value (units): 4.50%

\- Expected direction (constrained mix, return, volatility) and why: Volatility will increase as the risk premium does, but so will the return, most likely proportionally to the volatility increase. BIL will most likely change as I think they are the most risky, so a decrease in BIL will most likely occur.

\- Expected decision effect (does PILOT change?): PILOT: at least one stress case will not pass or will swing BIL, IEF, LQD, or VT's weight by 25 points or more. Fund small same as 4.00% and go from there.

\- Command I will run: .\\.venv\\Scripts\\python engine.py --equity-premium 4.5 --out output/changed-input.md



\- Revised: 5:17 PM. Changed the new value from 5.00% to 4.50% because 5.00% was already visible in the app's stress table.





\## Locked Changed-Input Record — actual result (written after the run)

\- Run commit: 806ac1f (prediction commit c45dab4)

\- Actual direction (mix, return, volatility): Constrained mix (BIL/IEF/LQD/VT) is now 45 / 0 / 0 / 55, constrained return went up 0.02 percentage points, to 6.57%, and volatility actually dropped almost a whole percent, now at 8.27%.

\- Actual decision effect: Decision is still PILOT (unchanged).

\- Prediction vs. actual (which parts matched, which missed): Actual decision effect outcome and return matched the prediction, but mix and volatility actually worked opposite of my prediction (more BIL, not less, and volatility actually dropped a percent).

\- Diagnosis (for each miss: the finance reason, using the rows that moved and the ones that didn't): Volatility dropped because the mix shifted to a less risky mix, fully weighing only BIL and VT, which leads me to believe BIL is actually one of the more secure, less risky bonds, and IEF and LQD are more risky and volatile. To conclude why the mix shifted, it is because the BIL is one of the least volatile bond options, which then explains why the heavier weighing of it in the actual result caused the overall volatility to go down. 



---

# Validation and AI-Use Record

**AI use:** Claude (Anthropic, Claude Opus 5.5, used in the Claude app on 2026-11-23) helped write the engine, app, tests and drafts of these docs. The two Locked Changed-Input sections above were written by me with AI off. Every other claim below was checked as described. The analysis and decision are mine.
**Education only, not investment advice.**

## 1. Data ledger

| Input | Source and link | As of / vintage | Units and definition | Transformation | Exclusions, revisions, licensing |
|---|---|---|---|---|---|
| BIL, IEF, LQD, VT prices | Yahoo Finance historical data ([BIL](https://finance.yahoo.com/quote/BIL/history/), [IEF](https://finance.yahoo.com/quote/IEF/history/), [LQD](https://finance.yahoo.com/quote/LQD/history/), [VT](https://finance.yahoo.com/quote/VT/history/)) | Monthly, Oct 2021 to Sep 2026; downloaded 2026-10-20 (Lab 14) | USD adjusted close (dividends reinvested, net of fund fees) | Simple monthly returns; annualized volatility = monthly SD × √12; sample correlations | 60 prices → 59 returns; no rows dropped. Adjusted closes can be restated after later distributions. Personal, educational use under Yahoo terms. |
| DGS3MO (signal) | [FRED/ALFRED DGS3MO](https://fred.stlouisfed.org/series/DGS3MO) | Obs 2026-10-02, as known 2026-10-05 | Percent per year, 3-month constant-maturity Treasury yield | ÷100; minus BIL fee → BIL expected return; plus equity premium minus VT fee → VT expected return | Point-in-time rule: latest value published on or before the decision date. Lab 17 audit: no material revisions. FRED data are public. |
| DGS10 | [FRED/ALFRED DGS10](https://fred.stlouisfed.org/series/DGS10) | Obs 2026-10-02, as known 2026-10-05 | Percent per year | ÷100; minus IEF fee | Same rule; Lab 17 known-answer value. |
| BAA | [FRED/ALFRED BAA](https://fred.stlouisfed.org/series/BAA) | Sep 2026 monthly, as known 2026-10-05 | Percent per year, Moody's Baa corporate yield | ÷100; minus 0.75% credit haircut; minus LQD fee | Same rule. Baa is a lower-rated proxy than LQD's average holding; the haircut covers that and expected losses (assumption, stressed). |
| Expense ratios | Issuer pages: SSGA (BIL 0.1353%), iShares (IEF 0.15%, LQD 0.14%), Vanguard (VT 0.06%) | Checked 2026-11-23 | Percent per year | Subtracted only from yield-based returns | Not subtracted from historical returns, which are already net of fees (avoids double counting). |
| Mandate numbers | Lab 13 mandate | Course case | Reserve $100m, $0.75m quarterly distribution, 4 quarters | Reserve minimum = 4 × 0.75 ÷ 100 = 3.0% | No private data used anywhere in the repo. |

**Timing boundary:** every yield must have been published by 2026-10-05, and the last price month is September 2026, so no input is from after the decision date. The test `test_point_in_time_rule_blocks_later_vintage` enforces the yield rule.

## 2. Conventions (one definition used everywhere)

Weights are fractions, long-only, on a 5-point grid summing to 100%. Returns are annual, nominal, in decimals. Volatility is the annualized standard deviation of monthly returns. "Reserve-eligible" means BIL + IEF. The benchmark is 40% LQD / 60% VT. The constrained portfolio is the lowest-volatility grid mix that passes every rule.

## 3. Validation register

| # | Test | What it protects | Result |
|---|---|---|---|
| 1 | Meridian known answer: engine reproduces Lab 15's 0/20/25/55 mix, 6.51% return, 9.44% volatility | Optimizer logic | Pass |
| 2 | Meridian with 7% equity reproduces Lab 15's 0/10/10/80 | Optimizer response to an input change | Pass |
| 3 | Lab 14 benchmark volatility by hand: √0.010944 = 10.46% | Covariance math, including the correlation term | Pass |
| 4 | Lab 13 reserve minimum = 4 × 0.75 ÷ 100 = 3.0% | Mandate translation | Pass |
| 5 | Own-universe historical case reproduces Lab 15's 60% BIL / 40% VT, 6.61%, 6.05% | Data file and estimator unchanged since Lab 15 | Pass |
| 6 | Point-in-time rule: on 2026-10-05 DGS3MO = 4.19% (obs 2 Oct), not 4.22% (published 6 Oct); a date before any vintage raises an error | No look-ahead in the signal | Pass |
| 7 | Signal bridge: BIL return = 4.19% − 0.1353%; VT = 4.19% + 4% − 0.06% | Units and fee bridge | Pass |
| 8 | Baselines fail for the stated rule only (equal weight: return; benchmark: reserve) | Mandate verdicts | Pass |
| 9 | Directional: a higher equity premium raises VT's expected return | Sign of the driver | Pass |
| 10 | Failure test: a 5% cost drag makes 6.5% unreachable → no feasible mix → REJECT | Highest-risk claim that the process can say no | Pass |
| 11 | Bad price data (a zero price) stops the run with an error | Fails loudly, not silently | Pass |
| 12 | Every grid mix sums to 100% | Weight construction | Pass |

Run with `python -m pytest -q` → `12 passed`.

## 4. Independent checks

- **Signal value:** DGS3MO 4.19% (2 Oct 2026), 4.22% (5 Oct) and 4.21% (6 Oct) were read by hand from the FRED page in Lab 17 (29 Oct 2026). They match `data/rates_as_known.csv`.
- **Fees:** each expense ratio was read from its issuer page, not from Claude.
- **Optimizer:** cross-checked against the Lab 15 engine on two cases (tests 1, 2 and 5). The Project 2 engine is new code, so this confirms it reproduces the earlier, separately written lab results.

## 5. Highest-risk claim and stress results

The highest-risk claim is that the constrained mix is a stable answer. The stress run (app, Stress & range tab; [output/visible_output.md](../output/visible_output.md)) tests estimates (equity premium ±1 pt, T-bill signal ±50 bp), the window (last 36 months), costs (+25 and +50 bp) and constraints (reserve minimum 10%), plus the historical-returns method. Two cases fire the stop condition (T-bill −50 bp: 40-point swing into IEF; historical returns: 25 points). **That limitation drives the action:** the recommendation is a pilot, not adoption.

## 6. Cold run

Both runs by Max on his Windows laptop, 2026-11-23, each recorded as one continuous screen recording (kept as evidence, not submitted), using README commands only, starting from the home folder with a fresh clone and a fresh virtual environment.

| Run | Time | Result |
|---|---|---|
| 1 | about 6:46 PM, 5 min 51 s | **Failed.** An old `C:\Users\maxpu\TICKER-research` folder from an earlier lab already existed, so `git clone` refused to overwrite it and `cd TICKER-research` entered the old copy. Its requirements installed Jupyter, `pytest` was missing and `app.py` did not exist. |
| Fix | commit 13c9ecc | README now clones into a dedicated folder (`p2-app`) and warns that an existing folder with that name makes `git clone` stop. |
| 2 | about 7:07 PM, 6 min | **Passed.** Fresh clone into `p2-app`, fresh venv, `pip install -r requirements.txt`, `python -m pytest -q` showed `12 passed`, and `streamlit run app.py` opened the app with the PILOT banner. |

Lesson: a reproducibility failure can come from the user's machine, not the code, so the README now names its own folder.

## 7. AI-use register

Tool: Claude (Anthropic), model Claude Opus 5.5, in the Claude app, 2026-11-23. Earlier labs also used AI as recorded in their own folders.

| Use | What the AI produced | My check | Disposition |
|---|---|---|---|
| Gap review of the branch | Flagged that the Lab 20 memo reported the Meridian training numbers (0/20/25/55, 6.51%) under my BIL/IEF/LQD/VT names | Compared Lab 20 output with Lab 15's own-universe table: the numbers matched the training case, not my data | **Accepted**; rebuilt the app on my own data |
| Expected-return method | Proposed point-in-time yields instead of 59-month historical means | Historical means gave IEF −1.73% and VT 11–20% (my calculation), which are not credible forward estimates; yields are knowable on the decision date | **Accepted**; kept historical means as a stress case |
| Engine and app code | engine.py, app.py | 12 tests against my lab known answers; ran the app myself | **Accepted after testing** |
| Engine bug | First version defaulted to a 60-month window but the data have 59 returns, so it crashed | The engine raised an error; fixed to 59 | **Corrected** |
| Test setup | pytest also ran my Week 13 robo-advisor test, which needs live data and failed | Saw `1 failed` on my laptop | **Corrected** with `pytest.ini` |
| Fee convention | Suggested subtracting fees only from yield-based returns | Adjusted closes already include fees | **Accepted** |
| Locked changed-input test | Explained form fields only; flagged that my first choice (5.00%) was already visible in the stress table | I changed to 4.50% and noted the revision | Prediction and diagnosis **written by me, AI off** |
| Drafting | First drafts of README, this record, the memo and the three video scripts | I edited every claim and checked each number against the app output | **Qualified**: my edits are final |
