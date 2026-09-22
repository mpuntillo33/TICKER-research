# Lab 09 - ABG Pro-Forma Build

`proforma.py` is a standard-library-only, five-year (2026E-2030E) three-statement model for Asbury Automotive Group (ABG). All amounts are USD millions except the per-share value.

Run it from this folder:

```powershell
python proforma.py
```

## ABG validation

The model reproduces the supplied known answer, rounded to one decimal:

| Line | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| Free cash flow to equity | 211.4 | 342.3 |
| Cash, year end | 101.8 | 719.8 |
| Assets - liabilities - equity | 0.0 | 0.0 |
| Value per share | $291.75 | - |

The terminal-value share is 79.8% (about 80%). The model calls `assert_balanced` after every projected year and refuses an unbalanced statement or a cash balance below the $25.0 minimum.

To repeat the required break test, replace the FY2026 computed `cash` assignment in `proforma.py` with `cash = opening["cash"]` and run the file. It raises `AssertionError: FY2026E is not balanced ... = -61.4`. Undo that one-line change afterward.

## Model order

Each year computes the income statement first, then all balance-sheet lines except cash, then FCFE and cash. This lets the cash line reflect the combined operating, investing, financing, and buyback effects rather than serving as an independent assumption. The revolver is drawn only to maintain minimum cash and repaid first when excess cash is available.

## Floor plan

Floor-plan financing is inventory borrowing supplied by manufacturers' finance arms or banks. Because the balance rises with inventory, the model projects it as a ratio of inventory. Interest is based on the opening floor-plan balance, and the increase in floor plan is a financing source in FCFE. Removing that financing source would require cash to fund the same inventory build, which is why cash becomes deeply negative in the case demonstration.
