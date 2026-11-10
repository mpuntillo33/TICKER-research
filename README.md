# Project 2 — Portfolio Decision System

**AI announcement.** I used OpenAI Codex as a coding and review assistant to organize this repository and check the cold-run package. I checked the calculations, evidence, and decision myself. **Education only; not investment advice.**

## Committee call

**Pilot, not adopt.** Use no more than a small, separately approved pilot allocation until the CIO supplies a CPI assumption and a rule for resolving the mandate's unspecified trade-offs. The current constrained result is sensitive: a one-percentage-point change in the equity expected-return input moved the selected allocation by 25 percentage points. Pause the process if that sensitivity recurs outside the approved range, if the point-in-time data admission rule fails, or if a mandate limit fails.

## Cold run

From a fresh clone, install the app dependency once:

```powershell
python -m pip install -r requirements.txt
```

Then this is the **one command that produces the result**:

```powershell
python -m streamlit run "Lab 15/app.py"
```

The browser app opens the portfolio result. Leave the uploaded-price field blank to reproduce the documented Meridian training result, or upload `Lab 14/prices.csv` for the Project 2 universe result. The default planning objective is 6.5%, an explicit planning proxy—not a forecast.

Quick non-web checks:

```powershell
python "Lab 13/mandate.py"
python "Lab 15/portfolio.py"
```

## What is here

| Component | Location | Reviewer use |
|---|---|---|
| Mandate and rule checker | [Lab 13](Lab%2013/lab13_notes_and_rundown.md) | Objective, constraints, ambiguous mandate items, and known answers |
| Baselines and price data | [Lab 14](Lab%2014/lab14_notes.md) | Equal weight, benchmark, input provenance, and validation |
| Runnable allocation app and stress evidence | [Lab 15](Lab%2015/README.md) | Constrained search and the 25-point sensitivity finding |
| Point-in-time gate | [Lab 16](Lab%2016/README.md) | Availability and revision logic |
| Data card and FRED/ALFRED audit | [Lab 17](Lab%2017/README.md) | DGS3MO source, units, lag, and revision test |
| Filing-quality checks | [Lab 18](Lab%2018/buffett_investor_skill/README.md) | Narrow EDGAR quality-screen validation only |
| Legend-panel validation | [Lab 19](Lab%2019/README.md) | Transparent investor-rule comparison |
| Committee memo | [Decision memo](docs/decision-memo.md) | Action, conditions, monitor, and reversal |
| Model-risk and AI-use record | [Validation record](docs/validation-and-ai-use.md) | Riskiest claim, test, conceptual limits, and required changed-input record |
| Week 12 studio record | [Studio record](docs/week-12-studio-record.md) | Cold-run protocol, committee challenge, and frozen must-fix list |
| Submission manifest | [Manifest](docs/submission-manifest.md) | Delivery links and video status |

## Scope and current limitation

This repository is ready for a reviewer to run the current allocation app and trace its evidence. It is **not yet a decision-ready adoption system**: the final unified app still needs the side-by-side baseline verdicts, an admitted point-in-time signal, and the formal locked changed-input result. These are deliberately frozen in the Week 12 must-fix list rather than treated as completed analysis.
