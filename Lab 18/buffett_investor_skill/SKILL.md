---
name: buffett-investor
description: Compute a Buffett-style five-year 10-K quality review from SEC EDGAR for a ticker, then write a short evidence-bound investment-quality memo.
---

Use this skill when the user asks whether a company fits a Buffett-style quality screen, wants its five-year ROE or owner earnings from 10-Ks, or asks for a Buffett investor memo.

1. Run `python edgar_buffett.py TICKER --output TICKER_edgar_report.json` from this folder. Use an SEC User-Agent containing the user's real name and email, for example `--user-agent "Max Puntillo name@school.edu"`. Do not use FAskills, paid data services, price data, other filings, or estimates.
2. Treat the script output as the entire factual record. It uses 10-K facts only, selects the latest filing for identical fiscal periods, reports USD millions, and leaves unavailable values as `not found`.
3. Do not recalculate, supplement, round into a new number, or infer missing values. A check marked `not known` remains not known. The model's job is judgment only.
4. Write `TICKER_buffett_memo.md` with this exact shape:
   - Title and a single decision: **Own the business**, **Watch it**, or **Pass**.
   - A short rationale using only values printed by the script, including the three checks.
   - Explicitly say when missing data prevents a judgment, especially owner earnings.
   - State that this is a quality judgment, not a price or investment recommendation.
   - End with one line: `Decision reflection: I [do/do not] trust this verdict because ...`.
5. The memo must not introduce a number absent from the script output. The Streamlit app checks this automatically.

For a handoff, report the script command, report JSON path, memo path, and any missing/unknown fields.
