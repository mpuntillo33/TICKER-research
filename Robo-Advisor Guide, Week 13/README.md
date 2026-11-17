# Robo-Advisor Guide, Week 13

Run with `pip install -r requirements.txt` then `streamlit run robo_app.py`.

## Allocation rule

The suggested allocation is deliberately deterministic and shown in the app: stocks start at `110 − age`, bounded to 20%–90%. A horizon below five years reduces stocks by 30 points; five to nine years reduces 10 points. Near-term need, no emergency fund, a maximum loss of 10% or less, and a sell response each reduce stocks (20, 10, 20, and 10 points respectively); a buy-more response adds 10. The output is rounded to 10% increments. Cash is 20% if money is needed within three years or the emergency fund is absent; bonds receive the remaining balance.

The app retrieves the specified Ken French and FRED files every run, performs the required monthly return calculations, rebalances monthly, and checks historical 12-month losses against the client limit. The bond series is an approximation derived from yields, not a published bond index.

## Validation

The manual override supports the course check: 60/40/0 with $100,000 should yield 432 months from January 1990 through December 2025 and approximately the published metrics (within the French-file revision tolerance).

Education, not investment advice.
