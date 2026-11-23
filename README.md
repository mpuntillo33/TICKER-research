# Project 2: Reserve Portfolio Committee App

**AI use:** Built with Claude (Anthropic, Claude Opus 5.5), which helped write the engine, app, tests and first drafts of the docs. Every assumption, check and the final decision are mine (Max Puntillo). The full record is in [docs/validation-and-ai-use.md](docs/validation-and-ai-use.md).
**Education only, not investment advice.**

## The decision

**User:** the investment committee of a $100 million reserve (Lab 13 mandate).
**Action asked:** allocate to, pilot, or reject a constrained four-ETF process (BIL, IEF, LQD, VT) that targets CPI + 4% net of costs over rolling five-year periods.
**Current output (as known on 2026-10-05):** **Pilot.** See [docs/decision-memo.md](docs/decision-memo.md) for the range, triggers and the committee ask, and [output/visible_output.md](output/visible_output.md) for the full executed result. You can read both without running any code.

Project 2 has no Edition A or Edition B (course ruling 2026-10-14), so neither is submitted.

## Run it (Windows PowerShell, Python 3.12)

```powershell
cd ~
git clone -b PROJECT-2 https://github.com/mpuntillo33/TICKER-research.git p2-app
cd p2-app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
streamlit run app.py
```

On the very first run Streamlit asks for an email address: leave it blank and press Enter. The browser then opens the app. Move a driver in the left sidebar and every table, the stress run and the decision update. Nothing needs an internet connection, an account or an API key.

Command-line version of the same result:

```powershell
python engine.py --out output/visible_output.md
python engine.py --tbill-yield 3.69     # example changed input; see --help for every driver
```

Clone into a new folder name (here `p2-app`): if a folder with that name already exists, `git clone` stops and you would end up in an old copy. If `Activate.ps1` is blocked, run `Set-ExecutionPolicy -Scope Process Bypass` first, or use `.\.venv\Scripts\python -m streamlit run app.py`.

## Repository map

| Path | What it is |
|---|---|
| `engine.py` | The only place numbers are calculated: data loading, point-in-time rule, expected returns, mandate checks, optimizer, stress run, range rule, decision rule, report |
| `app.py` | Streamlit committee app; renders engine results only |
| `tests/test_engine.py` | 12 known-answer, directional and failure tests (`pytest.ini` limits pytest to this folder) |
| `data/prices.csv` | Monthly adjusted closes for BIL, IEF, LQD and VT, Oct 2021 to Sep 2026 (Yahoo Finance, downloaded 2026-10-20) |
| `data/rates_as_known.csv` | DGS3MO, DGS10 and BAA values with observation date, vintage date and source (FRED/ALFRED) |
| `output/` | Visible executed output: base run, locked changed-input run, screenshots |
| `docs/` | Decision memo, validation and AI-use record, transcripts, submission manifest |
| `Lab 13` to `Lab 20` | Lab history the app was built from (mandate, baselines, optimizer, provenance gate, data card, readiness check) |

## Data sources

- **Prices:** Yahoo Finance monthly adjusted closes ([BIL](https://finance.yahoo.com/quote/BIL/history/), [IEF](https://finance.yahoo.com/quote/IEF/history/), [LQD](https://finance.yahoo.com/quote/LQD/history/), [VT](https://finance.yahoo.com/quote/VT/history/)). Used for volatility, correlation and worst 12-month loss. Personal, educational use.
- **Point-in-time yields:** FRED/ALFRED [DGS3MO](https://fred.stlouisfed.org/series/DGS3MO) (the signal), [DGS10](https://fred.stlouisfed.org/series/DGS10) and [BAA](https://fred.stlouisfed.org/series/BAA), as known on the decision date (Lab 17 audit).
- **Expense ratios:** issuer pages (BIL 0.1353%, IEF 0.15%, LQD 0.14%, VT 0.06%).

## Known limitations

- The yields are a snapshot as known on 2026-10-05. Re-run with current ALFRED vintages before any real decision.
- 59 monthly returns is a short history and includes the 2022 rate shock, so risk estimates are period-specific.
- The 2.5% CPI figure, the 4% equity premium and the 0.75% LQD credit haircut are planning assumptions, not forecasts. All three are stressed in the app.
- The 5-point weight grid makes the selected mix jump between neighbouring feasible mixes. That instability is a finding, not a bug, and it is why the output is Pilot.
- Taxes, bid-ask spreads and the exact rebalancing schedule are not modeled beyond the cost-drag stress.
