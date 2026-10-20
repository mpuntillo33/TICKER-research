# Assumption-Challenge Record — Project 1 (ACI)

One row per load-bearing driver: **value · basis · challenge · evidence that would change it.** Base values were
proposed by Claude while building the engine and reviewed and accepted by Max in the driver panel on Oct 19, 2026
(see the AI-use register). Partner challenges from the Weeks 5–6 labs are credited to the challenger.

| Driver | Value (base) | Basis | Challenge | Evidence that would change it | One-way value swing (band) |
|---|---|---|---|---|---|
| FY2030 SG&A / gross profit | 94.0% (FY26) → 93.0% (FY30) | FY2025 93.4% ex-opioid charge (10-K); H1 FY2026 adj. EBITDA down 8%; ACI Edge savings unproven | Why assume any improvement when guidance was withdrawn? *(Lab 12 partner: "If the first-quarter decline is your reason for starting low, why do you allow recovery at all?")* | Q3/Q4 FY2026 SG&A rate and adj. EBITDA margin; quantified savings in the Q4 turnaround plan. Flat 94.0% → $12.69 | $2.28–$31.41 |
| WACC | 7.7% (computed 7.68%) | Rf 5.10% (FRED, Oct 15, 2026); grocery unlevered beta 0.85 (Damodaran, Jan 2026) relevered to 1.78; Kd 5.9% pretax; market weights | Raw beta 0.23 would give a far lower cost of equity; the Lab 06 judgment was 8.0% | A bond-market cost of debt above 5.9%, or a credit-rating change | $8.64–$23.29 |
| Terminal growth | 2.0% | Below long-run nominal GDP; mature grocer | Is 2% too high for a chain with negative identical sales? | Identical sales negative through FY2027 → use 1.0–1.5% | $13.11–$20.97 |
| Capex | $2,000m / yr | FY2023–25 $2,156.7m / $1,927.5m / $1,833.6m; FY2026 plan $2.0–2.2bn (10-K) | Turnaround could cut capex, raising FCFF short term but risking store competitiveness | Capex guidance in the Q4 turnaround plan | $14.67–$21.11 |
| FY2026 SG&A / gross profit | 94.0% | H1 FY2026 adj. EBITDA $1,797m vs $1,959m prior year; model FY26 EBITDA within 3.4% of the H1 run-rate | Could be worse given Q2 margin of 4.1% | Q3 FY2026 adj. EBITDA margin below 4.0% | $16.72–$19.99 |
| Gross margin | 26.8% (FY26) → 27.0% (FY30) | 27.8% / 27.7% / 27.2% FY23–25; 26.6% Q1, 26.8% Q2 FY26; pharmacy and digital mix pressure | *(Lab 12 partner: "Trace the 0.5-point gross-margin sensitivity all the way to the value.")* | Gross margin ex-fuel and LIFO trend in Q3/Q4 FY2026 | $17.00–$19.22 (FY30) |
| Revenue growth | −0.5% (FY26), 1.5% (FY28–30) | Identical sales +3.0/+2.0/+2.0% FY23–25, −0.8% Q1 and Q2 FY26; 53rd week removed from base | *(Lab 12 partner: "You started at 0.5% growth even though ACI reported 3.5% FY2025 growth.")* Answer: 3.5% includes the 53rd week; identical sales are the clean measure | Identical sales turning positive for two quarters | FY26 $17.32–$19.32; FY28–30 $16.63–$18.75 |
| Payables | 24.2 days of cost of sales | 10-K accounts payable $4,021.2m on $60,565.8m cost of sales (AI proposal, verified by Max on the 10-K) | Supplier terms could tighten in a turnaround | Payables days in the next 10-Q/10-K | Not a slider (locked) |
| Opioid obligation | $773.8m debt-like | 10-K Note 12: $655.1m + $21.7m + ≈$97.0m, paid over ≈9 years; undiscounted, pre-tax | Undiscounted and pre-tax overstates the claim slightly | Note 12 updates; payments made; participation levels | −$1.59/share vs ignoring it |
| Share count | 488.2m diluted | Q2 FY2026 diluted weighted-average (8-K, Oct 13, 2026); cross-checks 485.3m cover count, 497.0m adjusted diluted | Buybacks continue; RSUs add 8.8m | Q2 10-Q cover-page count | ≈1.8% per-share effect (497.0m) |

## Causal chains for the main drivers (through the statements)

- **SG&A / gross profit ↑** → SG&A ↑ → EBIT ↓ → NOPAT ↓ → FCFF ↓ every year → terminal FCFF ↓ → EV ↓; the bridge
  items are fixed, so equity value falls one-for-one with EV. Revenue, inventory and payables do not move.
- **WACC ↑** → every FCFF and the terminal value are discounted harder, and the Gordon spread (WACC − g) widens →
  EV ↓. No statement line changes.
- **Revenue growth ↑** → revenue ↑ → gross profit and EBIT ↑ at the same ratios; inventory ↑ is now mostly funded by
  payables ↑ (24.2 vs 31.2 days) → small ΔNWC drag → FCFF ↑ → value ↑ modestly.
- **FY2026 gross margin** only changes FY2026 (FY2030 is set by the long-run margin), so it barely moves value;
  this is why the Locked Changed-Input Record showed +$0.01.

## Does the ranking depend on the ranges?

Yes. On historical bands, FY2030 SG&A/GP leads ($29.13 swing), then WACC ($14.65). With narrow,
management-credible bands (SG&A/GP 92.5–93.5%, WACC 7.2–8.2%, g 1.5–2.5%), WACC leads ($6.82) and SG&A/GP falls to
fourth ($5.20). The ranking is therefore reported as conditional on the chosen ranges, not as a probability claim
(`outputs/report.md`).
