# Lab 05 — FCFF DCF Notes

## Run command

```powershell
python dcf.py
```

Run the command from the folder containing `dcf.py`.

## Coding logic

The model starts with Year 0 FCFF, compounds it once for each of the five stated growth rates, and discounts each resulting end-of-year FCFF by `(1 + WACC)^year`. It calculates terminal value at the end of Year 5 using the Gordon-growth formula, discounts that amount five years to today, adds it to the present value of explicit FCFF to obtain enterprise value, then adds cash, subtracts debt, and divides by diluted shares to reach per-share equity value.

Terminal value is discounted five years, not six, because the Gordon formula produces a value *at the end of Year 5* using Year 6 FCFF. The first terminal cash flow is Year 6 FCFF, but the terminal-value lump sum is located at Year 5 and therefore needs five discount periods.

## WACC prediction and verification

At the training WACC of 10%, the model returns $27.4974 per diluted share. Raising WACC to 11% lowers the value per diluted share to about $23.41 because every future cash flow, especially the terminal value, is discounted more heavily; WACC was then restored to 10%.

## Reversed DCF

A reversed DCF begins with the market price rather than an assumed growth forecast. It converts the market capitalization to enterprise value, subtracts or adds the capital-structure items consistently, then solves backward for the revenue growth, margin, FCFF growth, or terminal assumption that makes the DCF equal to today’s price.

It is useful because it turns a stock price into a testable market expectation. The analyst can then ask whether the implied operating performance is plausible rather than treating a single estimated fair value as certain.

## Scope note

These are Lab 05 training inputs: they are not ACI inputs and no company sourcing is used in this exercise. ACI’s actual filing-based inputs belong in the later company-valuation version of the model.
