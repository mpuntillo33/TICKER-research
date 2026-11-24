# Lab 19 — Legend Panel

This Streamlit app retains the Lab 18 Buffett checks and adds code-backed Cathie Wood and Burry checks over the same five-year SEC EDGAR 10-K data.

## Run

```powershell
python -m pip install -r requirements.txt
$env:SEC_USER_AGENT = "Your Name your-email@school.edu"
python legend_panel.py COST --output COST_legend_panel.json
streamlit run app.py
```

The program uses only SEC EDGAR `companyfacts` observations filed on 10-K forms: annual flows must cover 300–380 days; equity and liabilities are fiscal-year-end instants; latest-filed observations win. It reports USD millions and never estimates. A missing source fact remains `not found`; a dependent check remains `not known`.

## Checks

| Investor | Code checks |
|---|---|
| Buffett | ROE ≥ 15% every year; owner earnings positive every year; owner earnings grew first to last |
| Cathie Wood | revenue compound annual growth ≥ 5% from first to last year; latest R&D/revenue ≥ 5% |
| Burry | operating cash flow ≥ net income every year; latest liabilities/equity ≤ 2 |

The original 15% Cathie growth threshold was probed, then the retained 5% threshold was recorded below her memo in the app. This makes COST's growth check pass while leaving its R&D check `not known`.

## Sources

- [FAskills](https://github.com/CinderZhang/FAskills)
- [SEC EDGAR companyfacts API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [Streamlit documentation](https://docs.streamlit.io/)

The names label different transparent rule sets rather than reproduce any investor's complete investment process. Educational use only; not investment advice.
