# Validation and AI Use — Project 1 (ACI)

*Working source for `Validation-and-AI-Use.pdf`. Draft in progress; sections are filled as evidence is produced.*

## Decision, version, and as-of boundary

- Decision/user: initiate, watch/defer, or do not initiate ACI — fund investment committee, no current position.
- Bridge balance sheet: Sept 12, 2026 (Q2 FY2026). Market price: $13.09 close, Oct 16, 2026.
- Source cutoff: filings and data available through Oct 19, 2026.
- Repository commit/tag: _to fill at freeze (`p1-final`)_.

## Data and convention ledger

| Material input | Source | As-of/availability | Definition/units | Transformation/exclusion | Risk |
|---|---|---|---|---|---|
| Accounts payable $4,021.2m | FY2025 Form 10-K, consolidated balance sheet | Feb 28, 2026; filed Apr 27, 2026 | USD millions | Converted to 24.2 days of FY2025 cost of sales ($60,565.8m) to project payables | Payable days may drift with supplier terms; held constant |
| _(more rows to come)_ | | | | | |

## Validation register

| Claim/output | Failure mode | Test and expected result/direction | Actual result | Disposition | Evidence location |
|---|---|---|---|---|---|
| _(to fill)_ | | | | | |

## Locked Changed-Input Record — human prediction first; AI closed during execution

_To be completed by Max, AI-off._

## Named AI-use register

| Tool/model surface and exposed version | Interaction date | Material task | Output/claim used or considered | Independent check | Accept/modify/qualify/reject | Effect on decision |
|---|---|---|---|---|---|---|
| Claude (Anthropic) in the Claude app; configured model `claude-opus-5-5` | Oct 19, 2026 | Review the Lab 10/11 pro-forma working-capital design while building the Project 1 engine | Claude flagged that Lab 10/11 grew "other liabilities" at only 0.5% of the revenue change, so inventory growth was almost unfunded and higher revenue growth *lowered* value. It proposed projecting accounts payable at days of cost of sales, using FY2025 accounts payable of $4,021.2m (≈24.2 days). | Max opened the FY2025 Form 10-K (local copy of accession 0001646972-26-000032) in a browser, found the consolidated balance sheet, and confirmed accounts payable of $4,021.2m at Feb 28, 2026 ($4,092.7m at Feb 22, 2025), in USD millions. Total assets of $26,765.9m on the same page also match the engine's opening balance sheet. Screenshot: `docs/evidence/ap-10k-check.png`. | **Accept** — the figure matches the filing and the mechanism is economically sound for a grocer whose suppliers fund much of its inventory. | Revenue growth now raises value instead of lowering it; base value moved from $16.05 to $17.55 per share (at 8.0% WACC) before the WACC rebuild. |

## Limitations, monitoring, and kill/escalation rules

_(to fill)_
