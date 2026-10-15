# Lab 13 — Portfolio Mandate Defense

## Checker command

```powershell
python mandate.py
```

## S1–S10 sorting table

| Section | Classification | Reason |
|---|---|---|
| S1 | Hard constraint | The reserve requirement sets a measurable minimum that the portfolio must satisfy. |
| S2 | Objective | It states the desired CPI + 4% net-of-costs outcome over rolling five-year periods. |
| S3 | Hard constraint | It imposes a binding liquidity threshold within a stated redemption window. |
| S4 | Preference/benchmark reference rather than an allocation requirement | It identifies a benchmark/reference but does not require a particular allocation or tracking level. |
| S5 | Hard constraint | It limits a measurable portfolio characteristic that must not be exceeded. |
| S6 | Hard constraint | It gives a concrete portfolio restriction that can be checked. |
| S7 | Hard constraint | It gives a concrete portfolio restriction that can be checked. |
| S8 | Hard constraint | It gives a concrete portfolio restriction that can be checked. |
| S9 | Unverifiable promise because no measurement or breach rule is given | Without a metric, test period, or consequence, compliance cannot be determined. |
| S10 | Missing because optimization target/priorities are undefined | No decision rule resolves trade-offs among the mandate's competing goals. |

## Known-answer results and negative-weight probe

The computed reserve minimum is `4 × 0.75 ÷ 100 = 3.0%`.

| Candidate | Checkable result | Key measured values |
|---|---|---|
| A | Passes every checkable rule | Reserve 14.0%; liquidity 100.0%; largest company exposure 0.0%. |
| B | Fails 3 rules | Reserve 1.0%; liquidity 85.0%; Acme Corp exposure 9.0%. |
| C | Fails 1 rule | Reserve 2.0%; liquidity 100.0%; largest company exposure 8.0%. |

For the temporary negative-weight probe, Candidate A was set to Cash = `-2` and Global equity index fund = `64`, with all other weights unchanged. The reserve-eligible weight remained `10.0%`; only the long-only check failed, all other checkable rules passed, and the original inputs were restored.

## Candidate D

Candidate D is 90.0% Cash and 10.0% Global equity index fund. It passes all implemented checks but could be rejected under S2 because it is unlikely to achieve CPI + 4% net of costs over rolling five-year periods.

D is mechanically compliant but not an appropriate long-term mandate portfolio. Under S2, its defensive mix is unlikely to meet the stated real-return objective after costs.

## CIO clarification

How is the calendar-year loss limit measured, do distributions count in that measurement, and what happens after a breach? A binding 10.0% total-return limit would lead to a more defensive design, likely with more liquid high-quality assets and less equity/illiquid risk exposure.

## Investment policy statement context

An investment policy statement (IPS) is the governing document that turns an investor's goals, constraints, governance, and measurement standards into a portfolio mandate. S2 is an objective; S1 and S3 plus S5–S8 are constraints; S4 is a benchmark/reference; S9 is ambiguity because it lacks a test; and S10 identifies missing information needed to prioritize optimization choices.

## Reflection

A mechanically compliant portfolio can still be unsuitable because passing simple thresholds does not prove it serves the return objective, risk tolerance, time horizon, or intended trade-offs. S4 is the most ambiguous classification because a benchmark does not itself impose tracking requirements.

## Complete rundown

Created `Lab 13/mandate.py` using only the Python standard library, with editable holdings, candidate weights, mandate parameters, issuer exemptions, aggregated non-exempt issuer exposure, and computed rule checks. Created this completed notes file, ran `python mandate.py` to verify the known answers, performed the requested temporary negative-weight probe and restored the original inputs, then ran the checker command again to verify the restored baseline output.
