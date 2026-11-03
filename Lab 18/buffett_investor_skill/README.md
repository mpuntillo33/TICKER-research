# Lab 18 — Legend Investor as Skill

AI used: Codex helped build and test this learning demonstration; the student verified the EDGAR source, known-answer reconciliation, and final decision. Education only, not investment advice.

## Run

Install dependencies with `python -m pip install -r requirements.txt`. Set a truthful SEC contact header, then run the EDGAR computation:

```powershell
$env:SEC_USER_AGENT = "Your Name your-email@school.edu"
python edgar_buffett.py COST --output COST_edgar_report.json
streamlit run app.py
```

The script reads keyless SEC EDGAR data, `company_tickers.json` and the padded-CIK companyfacts endpoint. It uses 10-K facts only, values in USD millions, and only the XBRL tags permitted in the Lab 18 handout. It never estimates.

## Skill installation

The installed skill is at `C:\Users\maxpu\.codex\skills\buffett-investor`. This repository copy documents the portable submission. In a fresh Codex chat, ask: “Use the buffett-investor skill on COST.” The skill runs the script first; only then does the model write `COST_buffett_memo.md` using the printed facts.

## What is fixed vs. judgment

Python selects 10-K observations, applies tag precedence, computes ROE and owner earnings, and evaluates the three checks. The AI may only decide **Own the business**, **Watch it**, or **Pass** and write a short rationale. It cannot introduce a fact or fill in a gap.

`not found` is preferable to an estimate: it preserves the boundary between a sourced accounting fact and an assumption. If an input is unavailable, the affected check is `not known`.
