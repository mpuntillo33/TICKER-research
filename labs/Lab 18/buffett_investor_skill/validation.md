# Lab 18 validation record

AI used: Codex helped implement and test the SEC EDGAR retrieval, skill, app, and memo workflow. The student remains responsible for the factual source check and decision. Education only, not investment advice.

## Known-answer reconciliation — COST

Run: `python edgar_buffett.py COST --output COST_edgar_report.json` on 2026-11-03 using SEC EDGAR company facts and 10-K observations only.

The five rows matched the Lab 18 known answer exactly in USD millions:

| Fiscal year end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE | Owner earnings |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2022-08-28 | 226,954 | 5,844 | 7,392 | 3,891 | 20,642 | 28.3% | 3,501 |
| 2023-09-03 | 242,290 | 6,292 | 11,068 | 4,323 | 25,058 | 25.1% | 6,745 |
| 2024-09-01 | 254,453 | 7,367 | 11,339 | 4,710 | 23,622 | 31.2% | 6,629 |
| 2025-08-31 | 275,235 | 8,099 | 13,335 | 5,498 | 29,164 | 27.8% | 7,837 |
| 2026-08-30 | 303,154 | 9,226 | 15,817 | 6,435 | 35,803 | 25.8% | 9,382 |

All three checks passed.

## Probe — JPM

Run: `python edgar_buffett.py JPM --output JPM_edgar_report.json`.

The permitted capital-spending tags were absent, so capital spending and owner earnings print `not found`. The two owner-earnings checks print `not known`. The JPM memo explicitly says owner earnings cannot be judged.

## Memo-number guard

The Streamlit app compares numbers it finds in a memo against the values printed by the EDGAR report. Adding `40.0%` to the COST memo makes the guard flag `40.0%`; the unaltered COST memo passes the guard.

## Explain the row builder

`row_for_fiscal_year` calls `select_metric` for every required metric. `select_metric` tries only the handout's tags in their specified order, filters each candidate to a 10-K annual fact, keeps the latest filed fact for the same end date, and returns one fact or `None`. Back in the row builder, `None` becomes `not found`. ROE is `not known` if net income/equity is absent or equity is nonpositive; owner earnings is `not found` if operating cash flow or capital spending is absent. The checks then turn any missing dependency into `not known`.
