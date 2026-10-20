# Validation and AI Use — Project 1 (ACI)

*Content-equivalent working source for `Validation-and-AI-Use.pdf`.*

## Decision, version, and as-of boundary

- **Decision/user:** initiate, watch/defer, or do not initiate Albertsons Companies, Inc. (NYSE: ACI); fund
  investment committee with no position. **Recommendation:** watch/defer, $13–$19 per share.
- **Repository:** github.com/mpuntillo33/ticker-research, branch `PROJECT-1`, frozen at tag `p1-final` (commit recorded in the manifest).
- **Bridge date:** Sept 12, 2026. **Price:** $13.09, close Oct 16, 2026. **Source cutoff:** information available by Oct 19, 2026.
- **Environment:** Windows 11, Python 3.12.10, packages in `requirements.txt`; engine uses the standard library only.

## Data and convention ledger

| Material input | Source | As-of/availability | Definition/units | Transformation/exclusion | Risk |
|---|---|---|---|---|---|
| FY2025 revenue $83,172.5m; gross profit $22,606.7m; SG&A $21,891.3m | FY2025 Form 10-K (acc. 0001646972-26-000032), statement of operations | 53 wks to Feb 28, 2026; filed Apr 27, 2026 | USD m | Revenue less $1,360m 53rd week; SG&A less $773.8m opioid charge (93.4% of GP) | Extra-week estimate is management's |
| Balance sheet: inventory $5,173.9m, PP&E $9,903.7m, cash $198.6m, debt incl. finance leases $8,946.6m, equity $1,836.2m | 10-K balance sheet | Feb 28, 2026 | USD m | Opening balance sheet; "other" lines aggregated; balances to $26,765.9m | Aggregation hides line detail |
| Accounts payable $4,021.2m | 10-K balance sheet (screenshot `docs/evidence/ap-10k-check.png`) | Feb 28, 2026 | USD m | 24.2 days of FY2025 cost of sales | Days held constant |
| Opioid Settlement Framework $773.8m | 10-K Note 12: $655.1m + $21.7m + ≈$97.0m | Filed Apr 27, 2026 | USD m, undiscounted, pre-tax | Debt-like bridge item | Overstates slightly (undiscounted) |
| Q1 FY2026: identical sales −0.8%, adj. EBITDA $1,013.0m; cover shares 485,325,683 (Jul 24, 2026) | Q1 FY2026 Form 10-Q | 16 wks to Jun 20, 2026; filed Jul 28, 2026 | % / USD m / shares | EBITDA run-rate check; market-cap shares | — |
| Q2 FY2026: identical sales −0.8%, adj. EBITDA $784.0m (4.1%), debt incl. finance leases $9,328.2m, cash $282.0m, diluted shares 488.2m; guidance withdrawn | Q2 FY2026 earnings release, Form 8-K Ex. 99.1 | 12 wks to Sept 12, 2026; filed Oct 13, 2026 | USD m / m shares | Bridge and share basis | Q2 10-Q not yet filed (checked EDGAR Oct 19) |
| ACI price $13.09 | stockanalysis.com (S&P Global data) | Close Oct 16, 2026, 4:00 PM EDT | USD | Market cap, reverse DCF | Single provider; Digrin showed $13.18 undated |
| 10-yr Treasury 5.10% | FRED DGS10 | Oct 15, 2026 | % | Risk-free rate | — |
| Unlevered beta 0.85 | Damodaran, Retail (Grocery and Food), cash-corrected | Jan 2026 dataset | — | Relevered at D/E 1.47 → 1.78 | Industry, not company, beta |
| ERP 4.14% | Damodaran implied ERP (as used in Lab 06) | Sep 2026 | % | CAPM | — |
| Peer market cap, debt, leases, cash, EBITDA TTM (ACI, KR, SFM) | stockanalysis.com statistics and quarterly balance sheets | Retrieved Oct 19, 2026; balance sheets Jun 20 / Aug 15 / Jun 28, 2026 | USD m | EV = mkt cap + debt excl. all leases − cash | Provider EBITDA definition not published on page |

## Validation register

| Claim/output | Failure mode | Test and expected result/direction | Actual result | Disposition | Evidence location |
|---|---|---|---|---|---|
| DCF engine is correct | Discounting/terminal error | **Known answer:** Lab 05 training case → $27.4974 | $27.4974 | Pass | `tests/test_engine.py` |
| Pro-forma method is correct | Statement linkage error | **Known answer:** Lab 09 ABG case → $291.75 | $291.75 | Pass | `tests/test_engine.py` |
| Statements articulate | Plugged cash, imbalance | BS balances and CF ties to cash every year, at every driver band extreme | Max gap 0.000000 | Pass | `tests/test_engine.py`; report checks |
| Base year reconciles to filing | Silent normalization | Normalized revenue + $1,360m = $83,172.5m; SG&A/GP + charge = filed SG&A; opening BS balances | All reconcile | Pass | `analysis.base_year_reconciliation()` |
| DCF boundary/monotonicity | Wrong sign or invalid TV | WACC↑ → value↓; g↑ → value↑; g ≥ WACC refused | As expected; ValueError raised | Pass | `tests/test_engine.py` |
| Bridge | Double count or omission | EV − debt − opioid + cash = equity; +$100m debt → −$100m/488.2m per share | Exact | Pass | `tests/test_engine.py` |
| **Independent source/definition check** | Provider label ≠ filing definition | Provider "Total debt" for ACI vs bridge debt | Provider $15.92bn includes operating-lease liabilities; filing $9,328.2m = debt incl. finance leases. Bridge keeps the filing figure because FCFF is after rent | Pass (label reconciled) | stockanalysis.com ACI statistics, Oct 19, 2026; Q2 release |
| **Directional changed-input test (written before run)** | Margin not flowing to value | Lower FY2030 gross margin −0.5 pt → FY2030 EBIT↓, FCFF↓, value↓, revenue unchanged | As predicted | Pass | `tests/test_engine.py` |
| Peer policy and multiple definition | Mixed definitions | Same EV definition, same provider, leases excluded for all; ACI round-trip | Consistent | Pass | `comps.py`; Lab 08 policy (written before selection) |
| FY2026 forecast plausible | Forecast detached from current run-rate | Model FY2026 EBITDA within ±15% of annualized H1 FY2026 adj. EBITDA | −3.4% | Pass | report checks |
| **Highest-risk claim:** base value above price | Value depends on unproven cost recovery | Hold FY2030 SG&A/GP at FY2026's 94.0% | $12.69 < $13.09 price: the upside disappears | **Claim qualified:** recommendation set to watch/defer, initiation tied to SG&A/GP evidence | `tools/changed_input.py sga_to_gp_long 0.94`; Video 2 |
| Checks fail loudly | Silent nonsense | SG&A/GP 97%, capex $2,400m → "Drivers inside historical band" FAILS | Fails (red in panel) | Pass | `tests/test_engine.py`; Video 3 |
| Sensitivity ranking | Ranking presented as fact | Re-rank with narrow bands for the top three drivers | Leader changes from SG&A/GP to WACC | Ranking reported as range-conditional | `outputs/report.md` |
| **Cold run** | README insufficient | Fresh clone + new venv following README | First failure: `cd $HOME\Desktop` (OneDrive path); README steps then ran: 10/10 tests, $17.89 | Pass with logged failure | `docs/cold-run-log.md`; recordings |

## Locked Changed-Input Record — human prediction first; AI closed during execution

Full record: `docs/locked-changed-input-record.md`.

### Precommit before the run and before AI assistance on the prediction

| Precommit timestamp | Repository commit | Material input | Old → new value/units | Expected output direction | Expected decision effect |
|---|---|---|---|---|---|
| Oct 19, 2026, 7:40 PM EDT (pushed 8:00 PM) | `7ae0841` | FY2026 gross margin | 26.80% → 27.30% | Value up ≈ +$1.40/share; FY2030 EBIT and FCFF up | Likely to change watch/defer |

### Preserved execution result

| Before/after output | Actual decision effect | Prediction reconciliation | Failure diagnosis or why action did not change | Evidence path |
|---|---|---|---|---|
| $19.474 → $19.483 (+$0.01); FY2030 EBIT unchanged; FY2030 FCFF −$2.0m (run 8:07:55 PM) | None | Missed (direction right, size far off) | In Max's words: see the record. Engine note: run on the engine at `7ae0841`, before the opioid obligation was added; that item shifts both values by a constant −$1.59/share | `docs/locked-changed-input-record.md`, commits `7ae0841` → `6d9c64e` |

Max asked Claude only what the form fields meant while writing the prediction; Claude declined to review or suggest answers.

## Named AI-use register

| Tool/model surface and exposed version | Interaction date | Material task | Output/claim used or considered | Independent check | Accept/modify/qualify/reject | Effect on decision |
|---|---|---|---|---|---|---|
| Claude (Anthropic), Claude app; configured model `claude-opus-5-5` | Oct 19, 2026 | Review Lab 10/11 working-capital design | Proposed projecting accounts payable at days of cost of sales ($4,021.2m, ≈24.2 days) because growth was destroying value | Max opened the 10-K balance sheet and confirmed $4,021.2m and total assets $26,765.9m (`docs/evidence/ap-10k-check.png`) | **Accept** | Growth now adds value; base moved $16.05 → $17.55 at 8.0% WACC before the WACC rebuild |
| Same | Oct 19, 2026 | WACC inputs | Proposed rejecting the provider's raw beta (0.23) and relevering Damodaran's grocery beta (0.85) | Damodaran Jan 2026 table; Kroger–Albertsons deal pricing (announced 2022 at $34.10, blocked Dec 2024) explains the low raw beta; computed WACC 7.68% vs Lab 06's 8.0% judgment | **Qualify**: used, with industry-beta limitation stated | WACC 7.7% |
| Same | Oct 19, 2026 | Build `analysis.py`, `comps.py`, `app.ipynb`, tests, report tool | Engine code, driver base values and bounds, cases | 10 tests incl. course known answers; Max reviewed every driver in the panel and accepted the base values (7:29 PM) | **Accept** after tests and review | All model outputs |
| Same | Oct 19, 2026 | Locate newest share count and filings | 488.2m diluted shares (Q2 release); Q2 10-Q not yet filed | EDGAR full-text search, Oct 19, 2026 | **Accept** | Replaced 547.2m and 499.5m |
| Same | Oct 19, 2026 | Draft memo, Edition B, this record; Video 2 script; video talking points | Draft text | Max reviewed and edited; figures trace to `outputs/report.md`; videos delivered in Max's voice | **Modify** | Communication only |
| ChatGPT / Codex (OpenAI) | Sept 3 – Oct 1, 2026 | Labs 05–12 assistance and the Sept 3 report draft (disclosed in each lab) | Lab code and drafts | Lab known answers and partner reviews | As recorded in each lab | Lab inputs reused here |

**Pre-Edition-A note:** a `/Finance` agent session record dated Aug 27, 2026 (Week 1, the disclosed AI-assisted
screening period) exists in my course folder; it records no project output. Edition A itself was written in the
supervised AI-off Lab 03 on Sept 1, 2026.

## Limitations, monitoring, and kill/escalation rules

- Terminal value is 79.7% of EV; value is dominated by FY2030 SG&A/GP and WACC.
- No management guidance after Oct 13, 2026; FY2026 is anchored to the H1 run-rate instead.
- Peer EBITDA is a provider field applied identically to all companies; its exact definition is not published.
- The opioid obligation is undiscounted and pre-tax.
- **Kill/escalation:** if the bridge stops reconciling, any articulation check fails, or a new filing changes debt,
  shares or the opioid obligation, re-run `tools/make_report.py` before any committee use. Monitoring triggers are in the memo.
