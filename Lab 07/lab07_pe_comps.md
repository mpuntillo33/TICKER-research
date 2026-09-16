# Lab 07 - Comparable-Company Policy and Implied Range

## Scope, conventions, and inputs

This is a retrospective P/E comparison for the Asbury Automotive case. Prices are the December 31, 2024 closing prices supplied in the case; earnings are subsequently reported FY2024 total GAAP diluted EPS supplied in the case. The pairing is intentionally retrospective, not information available at the 2024 year-end close. Dollar values are per share.

| Company | Role | December 31, 2024 close | FY2024 total GAAP diluted EPS |
|---|---|---:|---:|
| Asbury Automotive (ABG) | Target | $243.03 | $21.50 |
| AutoNation (AN) | Candidate peer | $169.84 | $16.92 |
| Group 1 Automotive (GPI) | Qualified candidate peer | $421.48 | $36.81 |

The calculation is in `pe_comps.py` and uses only Python's standard library. Run it from this folder with `python pe_comps.py`.

## What P/E means and the question investigated

P/E is price per share divided by earnings per share (EPS). Price per share is the market price of one common share; diluted EPS allocates period earnings across a share count that includes dilution. A 10x P/E prices one share at ten dollars for each dollar of reported annual EPS. EPS permits comparison of differently sized companies because it is an ownership-unit measure.

Applying a peer P/E to ABG's EPS answers: *what would one ABG share be worth if the market assigned it a selected peer earnings multiple?* This complements rather than replaces my DCF: the DCF makes cash-flow, growth, discount-rate, and terminal-value assumptions explicit, while P/E reflects comparable market pricing of reported earnings.

My pre-calculation question was: **does GPI's international footprint and business mix make its higher P/E an appropriate comparison for ABG, or should it be only a qualified peer?**

P/E is useful only when price date, earnings period, accounting basis (here, total GAAP diluted EPS), profitability, and business economics are reasonably comparable. It is not meaningful for nonpositive EPS. It can mislead when earnings include unusual items or when growth, risk, capital structures, accounting, geography, or business mix differ. A lower P/E is not automatically better: it can reflect weaker growth, greater risk, temporary earnings, or a less attractive business. P/E is already an equity per-share multiple, so no cash/debt bridge belongs in this calculation.

Sources: [Investor.gov P/E definition](https://www.investor.gov/introduction-investing/investing-basics/glossary/price-earnings-pe-ratio) and [FINRA explanation of EPS and P/E](https://www.finra.org/investors/investing/investment-products/stocks/evaluating-stocks).

## Peer policy

Franchised vehicle retail and service/parts matter more than a broad industry label because this applies a multiple to earnings. Relevant similarity is dealership operations, franchise relationships, vehicle sales, repair/maintenance, parts, collision work, and finance-and-insurance products.

**AutoNation - use.** ABG is a U.S. franchised retailer of new/used vehicles, parts and service, collision repair, and F&I products. AutoNation's 325 U.S. franchises at 243 stores also sell new/used vehicles and operate parts-and-service businesses. This supports direct-peer use, while its Sunbelt concentration and additional finance, used-vehicle, and collision activities remain qualifications.

**Group 1 - qualify and use in the case range.** Group 1 shares the core model: new/used vehicle retail, financing/service contracts, maintenance/repair, parts, and collision repair. It is directionally comparable, but qualifies because its operations extend across the U.S. and U.K.; ABG operated in 14 U.S. states at year-end 2024. Geography, currencies, franchise portfolio, and growth opportunities can affect P/E. The result belongs in a transparent range, not as proof ABG deserves GPI's multiple.

Business evidence: [ABG FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1144980/000114498025000077/abg-20241231.htm), [AutoNation FY2024 10-K](https://www.sec.gov/Archives/edgar/data/350698/000035069825000029/an-20241231.htm), and [Group 1 FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1031203/000103120325000013/gpi-20241231.htm).

## Reproduced case calculation

Full precision is retained; display values are rounded only at presentation.

| Peer | Calculation | P/E |
|---|---|---:|
| AN | $169.84 / $16.92 | 10.037825x |
| GPI | $421.48 / $36.81 | 11.450149x |
| Median peer P/E | median(10.037825..., 11.450149...) | 10.743987x |

| ABG implied value | Result |
|---|---:|
| Minimum peer P/E | $215.81 |
| Median peer P/E | $231.00 |
| Maximum peer P/E | $246.18 |

The peer-implied range is **$215.81-$246.18** per ABG share. It is not proof ABG is fairly valued: the peer set is small and P/E embeds differing expectations and risks.

## Leave-one-peer-out interpretation

Before reading the output, I predicted removing GPI, the higher-P/E peer, would reduce the median-implied ABG value. It does: removing GPI leaves AN's 10.037825x multiple, producing **$215.81**, a **-$15.18** change from the $231.00 full-peer median estimate (using unrounded values).

Only AN remains after that removal, so it is a **reference estimate, not a range**. A range requires at least two usable peer multiples. This change does not itself justify removing GPI; the qualified-peer decision rests on the business comparison rather than the preferred output.
