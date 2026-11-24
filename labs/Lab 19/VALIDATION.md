# Validation and reflection

## COST known answer: initial 15% Cathie Wood growth screen

`COST_baseline_15pct.json` is a live SEC EDGAR run, not a typed table. Its five fiscal-year ends are 2022-08-28 through 2026-08-30.

| Investor | Result |
|---|---|
| Buffett | 3 of 3 pass |
| Cathie Wood | Revenue growth **fail: 7.51%** versus 15%; R&D/revenue **not known** because R&D is `not found` |
| Burry | 2 of 2 pass; latest liabilities/equity **1.49** |

The year-by-year liabilities/equity values are 2.11, 1.75, 1.96, 1.64, and 1.49. All come from the report's printed `Liabilities` and `Equity` facts.

## Threshold probe and retained setting

Running the exact same COST facts with `--growth-threshold 0.05` makes Cathie Wood's revenue-growth check pass at 7.51%; her R&D check remains `not known`. I kept **5%** as the retained exploratory screen because it separates steady growth from the original high-growth hurdle while keeping the independent R&D requirement and its source gap visible. The app's saved COST panel and its default download use that retained threshold; the 15% baseline is retained as the reproducible known-answer evidence.

## Project 2 company: NVDA

The existing Project 2 universe contains VT, its global-equity index fund. I used **NVDA** as the largest-company assumption for that fund; if the fund's holdings file used in class identifies a different top holding, rerun the same command with that ticker and retain this gap note.

The 5% panel results are Buffett 3 of 3 pass, Cathie Wood 2 of 2 pass, and Burry 1 pass / 1 fail. Burry's operating-cash-flow check fails because the printed latest OCF is 102,718 while net income is 120,067; his latest liabilities/equity check passes at 0.31.

Bull case: Buffett's three quality checks and Cathie Wood's growth and R&D checks all pass on the same printed facts. Bear case: Burry identifies that cash conversion fails his every-year OCF-at-least-net-income test, despite low latest balance-sheet leverage.

Decision: **Only with a condition** - I would use this panel as a filing-quality screen only if each `not found`/`not known` remains visible and valuation, market price, and portfolio-risk analysis are added before a Project 2 decision.

## What the panel teaches

The three personas disagree because they apply different transparent rules to the same facts: durable returns and owner earnings, growth plus R&D intensity, and cash conversion plus balance-sheet constraint. The COST threshold probe shows that a screen verdict is partly a design choice, so it must always display its threshold and not be treated as an investment recommendation.
