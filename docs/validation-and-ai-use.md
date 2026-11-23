\## Locked Changed-Input Record — prediction (written AI-off, committed before the run)

\- Written by: Max Puntillo, 11/23/2026, 5:04PM

\- Input changed: Equity Risk Premium over T-bills

\- Old value (units): 4.00%

\- New value (units): 4.50%

\- Expected direction (constrained mix, return, volatility) and why: Volatility will increase as the risk premium does, but so will the return, most likely proportionally to the volatility increase. BIL will most likely change as I think they are the most risky, so a decrease in BIL will most likely occur.

\- Expected decision effect (does PILOT change?): PILOT: at least one stress case will not pass or will swing BIL, IEF, LQD, or VT's weight by 25 points or more. Fund small same as 4.00% and go from there.

\- Command I will run: .\\.venv\\Scripts\\python engine.py --equity-premium 4.5 --out output/changed-input.md



\- Revised: 5:17 PM. Changed the new value from 5.00% to 4.50% because 5.00% was already visible in the app's stress table.





\## Locked Changed-Input Record — actual result (written after the run)

\- Run commit: 806ac1f (prediction commit c45dab4)

\- Actual direction (mix, return, volatility): Constrained mix (BIL/IEF/LQD/VT) is now 45 / 0 / 0 / 55, constrained return went up two percentage points, to 6.57%, and volatility actually dropped almost a whole percent, now at 8.27%.

\- Actual decision effect: Decision is still PILOT (unchanged).

\- Prediction vs. actual (which parts matched, which missed): Actual decision effect outcome and return matched the prediction, but mix and volatility actually worked opposite of my prediction (more BIL, not less, and volatility actually dropped a percent).

\- Diagnosis (for each miss: the finance reason, using the rows that moved and the ones that didn't): Volatility dropped because the mix shifted to a less risky mix, fully weighing only BIL and VT, which leads me to believe BIL is actually one of the more secure, less risky bonds, and IEF and LQD are more risky and volatile. To conclude why the mix shifted, it is because the BIL is one of the least volatile bond options, which then explains why the heavier weighing of it in the actual result caused the overall volatility to go down. 

