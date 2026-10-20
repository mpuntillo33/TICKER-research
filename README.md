# ACI Pro-Forma Workbench — FIN 43900 Project 1

> AI-assisted coursework for FIN 43900 (Purdue). Education, not investment advice. All AI use is named in
> [`docs/validation-and-ai-use.md`](docs/validation-and-ai-use.md).

## Finance decision and intended user

Should the fund **initiate a position, place Albertsons Companies, Inc. (NYSE: ACI) on watch/defer, or not
initiate**? The user is the fund's investment committee, which holds no position. Decision horizon: through
ACI's Q4 FY2026 call (turnaround plan due) and its spring 2027 investor day.

- **Valuation (bridge) date:** Sept 12, 2026 (Q2 FY2026 balance sheet). **Market price:** $13.09, close Oct 16, 2026.
- **Currency/units:** USD millions except per-share values.
- **Share basis:** 488.2m diluted weighted-average Class A shares (Q2 FY2026 earnings release, Form 8-K filed Oct 13, 2026).
- **Exclusions:** no control premium; the 2022 Kroger merger price ($34.10, blocked Dec 2024) is excluded as stale control-and-synergy evidence.

## Visible result (no need to run anything)

- [`outputs/report.md`](outputs/report.md): every material input, the bridge, statements, WACC build, sensitivity, comps, method comparison and checks.
- [`outputs/visible_output.json`](outputs/visible_output.json): the same results as a frozen machine-readable file.
- [`app.ipynb`](app.ipynb): the executed driver-panel notebook, saved with its output.

| Case | Value per share |
|---|---:|
| Low: identical sales stay negative, margin slips | $7.92 |
| Base | $17.89 |
| High: turnaround works by FY2028 | $24.74 |

## Setup and run (Windows; macOS/Linux use `python3` and `.venv/bin/python`)

```
git clone --branch PROJECT-1 https://github.com/mpuntillo33/ticker-research.git
cd ticker-research
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python tests\test_engine.py      # 10 validation tests, all should PASS
.venv\Scripts\python analysis.py               # base statements, valuation, checks
.venv\Scripts\python comps.py                  # EV/EBITDA comps and consistency checks
.venv\Scripts\python tools\make_report.py      # regenerates outputs/report.md and visible_output.json
.venv\Scripts\python -m jupyter lab app.ipynb  # driver panel: Run All, then move the sliders
```

No API keys or credentials are needed; there is no `.env`.

## Repository map

| Path | What it is |
|---|---|
| `analysis.py` | Locked engine: filing facts, normalizations, three-statement pro-forma, FCFF DCF, bridge, checks, cases, sensitivity, reverse DCF, WACC build |
| `comps.py` | Peer EV/EBITDA under one shared definition; P/E range carried from Lab 08 |
| `app.ipynb` | Driver panel: nine bounded sliders, reset to base, live checks that turn red |
| `tests/test_engine.py` | Known answers, articulation, monotonicity, bridge, changed-input and comps-consistency tests |
| `tools/changed_input.py` | Runs one changed input against base (used for the Locked Changed-Input Record) |
| `tools/make_report.py` | Writes the frozen visible output |
| `docs/` | Edition A (original, unchanged) and evidence, Locked Changed-Input Record, validation and AI-use record, memo and research-evolution sources |
| `Lab 05` – `Lab 12` | The course labs this project builds on, unchanged except two typo/link fixes |

**Data flow:** filing facts and sourced market inputs (`analysis.FILING`, `MARKET`, `WACC_INPUTS`) → pro-forma
statements → FCFF → DCF and bridge → checks → `tools/make_report.py` → `outputs/` → `app.ipynb` displays.
The notebook never computes a material number itself.

## Data sources and point-in-time boundary

ACI FY2025 Form 10-K (accession 0001646972-26-000032, filed Apr 27, 2026); Q1 FY2026 Form 10-Q (filed Jul 28, 2026);
Q2 FY2026 earnings release, Form 8-K (filed Oct 13, 2026); FRED DGS10 (Oct 15, 2026); Damodaran industry betas
(Jan 2026); stockanalysis.com / S&P Global market data (retrieved Oct 19, 2026). Nothing after Oct 19, 2026 is used.
Full ledger in `docs/validation-and-ai-use.md`.

## Financial conventions and assumptions

- FY2025 base normalized: 53rd-week sales (≈$1,360m) removed; $773.8m opioid-settlement charge removed from SG&A.
- The opioid obligation ($773.8m, 10-K Note 12) is deducted in the bridge as a debt-like claim.
- Debt in the bridge includes finance leases, excludes operating leases (FCFF is after rent).
- WACC 7.7% from sourced inputs (computed 7.68%); terminal growth 2.0%; FY2026 is a stub from Sept 12, 2026.
- Driver values, bounds and the evidence behind each are in `analysis.BOUNDS` and the assumption-challenge record.

## Validation and changed-input tests

See `tests/test_engine.py`, `outputs/report.md` (checks table) and `docs/locked-changed-input-record.md`.

## Known limitations, monitoring and reversal triggers

- Value is dominated by FY2030 SG&A / gross profit and WACC; terminal value is ≈80% of EV.
- Peer EBITDA is a provider field applied identically to all companies; its exact definition is not published on the page.
- ACI guidance was withdrawn Oct 13, 2026, so no management forecast anchors FY2026.
- Monitor: Q3 and Q4 FY2026 identical sales and SG&A / gross profit; the turnaround plan at the Q4 call; debt and opioid payments.
