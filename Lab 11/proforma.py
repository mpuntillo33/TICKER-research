"""Lab 11: ACI one-at-a-time sensitivity analysis, USD millions."""

from math import isclose

YEARS = (2026, 2027, 2028, 2029, 2030)
BASE_GROWTH = {2026: .005, 2027: .010, 2028: .015, 2029: .020, 2030: .020}
BASE_GROSS_MARGIN = {2026: .270, 2027: .2705, 2028: .271, 2029: .2715, 2030: .272}
SGA_TO_GROSS_PROFIT = {2026: .935, 2027: .932, 2028: .929, 2029: .926, 2030: .923}
INVENTORY_DAYS = 31.2
DEPRECIATION_TO_OPENING_PPE = 1_913.7 / 9_903.7
CAPEX = 2_100.0
TAX_RATE = .255
INTEREST_RATE = .059
OTHER_OPERATING_LIABILITIES_TO_REVENUE_CHANGE = .005
DEBT_REPAYMENT = 50.0
DIVIDENDS = 330.0
MINIMUM_CASH = 100.0
REVOLVER_LIMIT = 3_562.3
REVOLVER_RATE = .065
COST_OF_EQUITY = .10
TERMINAL_GROWTH = .020
SHARES_OUTSTANDING = 499.542902

OPENING = {"revenue": 83_172.5, "inventory": 5_173.9, "ppe": 9_903.7,
           "other_assets": 11_489.7, "cash": 198.6, "debt": 8_946.6,
           "revolver": 0.0, "other_liabilities": 15_983.1, "equity": 1_836.2}


def shifted(path: dict[int, float], change: float) -> dict[int, float]:
    """Apply a percentage-point shift to every forecast year in a path."""
    return {year: value + change for year, value in path.items()}


def assert_balanced(year: int, gap: float, cash: float) -> None:
    if not isclose(gap, 0.0, abs_tol=1e-8):
        raise AssertionError(f"FY{year}E is not balanced: gap = {gap:.1f}")
    if cash < MINIMUM_CASH - 1e-8:
        raise AssertionError(f"FY{year}E cash is below the minimum")


def project(growth: dict[int, float] = BASE_GROWTH,
            gross_margin: dict[int, float] = BASE_GROSS_MARGIN) -> dict[int, dict[str, float]]:
    """Forecast statements. Only the supplied path is changed in a sensitivity."""
    results: dict[int, dict[str, float]] = {}
    opening = OPENING.copy()
    for year in YEARS:
        revenue = opening["revenue"] * (1 + growth[year])
        gross_profit = revenue * gross_margin[year]
        sga = gross_profit * SGA_TO_GROSS_PROFIT[year]
        operating_income = gross_profit - sga
        depreciation = opening["ppe"] * DEPRECIATION_TO_OPENING_PPE
        interest = opening["debt"] * INTEREST_RATE + opening["revolver"] * REVOLVER_RATE
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax
        inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365
        ppe = opening["ppe"] + CAPEX - depreciation
        other_liabilities_change = OTHER_OPERATING_LIABILITIES_TO_REVENUE_CHANGE * (revenue - opening["revenue"])
        other_liabilities = opening["other_liabilities"] + other_liabilities_change
        debt = opening["debt"] - DEBT_REPAYMENT
        equity = opening["equity"] + net_income - DIVIDENDS
        fcfe = (net_income + depreciation - CAPEX - (inventory - opening["inventory"])
                + other_liabilities_change - DEBT_REPAYMENT)
        preliminary_cash = opening["cash"] + fcfe - DIVIDENDS
        revolver = opening["revolver"]
        if preliminary_cash < MINIMUM_CASH:
            draw = MINIMUM_CASH - preliminary_cash
            revolver += draw
            if revolver > REVOLVER_LIMIT:
                raise AssertionError(f"FY{year}E revolver exceeds its limit")
            cash = MINIMUM_CASH
        else:
            repayment = min(revolver, preliminary_cash - MINIMUM_CASH)
            revolver -= repayment
            cash = preliminary_cash - repayment
        assets = inventory + ppe + opening["other_assets"] + cash
        liabilities = debt + revolver + other_liabilities
        gap = assets - liabilities - equity
        assert_balanced(year, gap, cash)
        results[year] = {"revenue": revenue, "gross_profit": gross_profit, "sga": sga,
            "operating_income": operating_income, "interest": interest, "pretax_income": pretax_income,
            "tax": tax, "net_income": net_income, "inventory": inventory, "ppe": ppe,
            "cash": cash, "debt": debt, "revolver": revolver, "other_liabilities": other_liabilities,
            "equity": equity, "total_assets": assets, "total_liabilities": liabilities,
            "total_liabilities_and_equity": liabilities + equity, "capex": CAPEX, "fcfe": fcfe,
            "inventory_change": inventory - opening["inventory"], "cash_change": cash - opening["cash"], "gap": gap}
        opening = {**opening, **results[year], "other_assets": opening["other_assets"]}
    return results


def value_equity(results: dict[int, dict[str, float]]) -> tuple[float, float, float]:
    pv_fcfe = sum(results[y]["fcfe"] / (1 + COST_OF_EQUITY) ** i for i, y in enumerate(YEARS, 1))
    terminal_value = results[2030]["fcfe"] * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    pv_terminal = terminal_value / (1 + COST_OF_EQUITY) ** len(YEARS)
    equity_value = pv_fcfe + pv_terminal
    return equity_value, pv_terminal / equity_value, equity_value / SHARES_OUTSTANDING


def print_base(results: dict[int, dict[str, float]]) -> None:
    print("Base case forecast")
    print(f"{'USD millions':<26}" + "".join(f"FY{y}E".rjust(12) for y in YEARS))
    for label, key in [("Revenue", "revenue"), ("Gross profit", "gross_profit"),
                       ("Operating income", "operating_income"), ("Net income", "net_income"),
                       ("FCFE", "fcfe"), ("Cash", "cash"), ("Balance-sheet gap", "gap")]:
        print(f"{label:<26}" + "".join(f"{results[y][key]:>12,.1f}" for y in YEARS))


def sensitivity_cases() -> list[tuple[str, dict[int, float], dict[int, float]]]:
    return [("Revenue growth: -1.0 pp", shifted(BASE_GROWTH, -.010), BASE_GROSS_MARGIN),
            ("Revenue growth: base", BASE_GROWTH, BASE_GROSS_MARGIN),
            ("Revenue growth: +1.0 pp", shifted(BASE_GROWTH, .010), BASE_GROSS_MARGIN),
            ("Gross margin: -0.5 pp", BASE_GROWTH, shifted(BASE_GROSS_MARGIN, -.005)),
            ("Gross margin: base", BASE_GROWTH, BASE_GROSS_MARGIN),
            ("Gross margin: +0.5 pp", BASE_GROWTH, shifted(BASE_GROSS_MARGIN, .005))]


def print_sensitivity() -> None:
    print("\nOne-at-a-time sensitivity (each shock applies in FY2026-FY2030)")
    print(f"{'Case':<28}{'FY2030 revenue':>16}{'FY2030 FCFE':>15}{'Equity value':>15}{'Value/share':>14}")
    for name, growth, margin in sensitivity_cases():
        result = project(growth, margin)
        equity_value, _, per_share = value_equity(result)
        print(f"{name:<28}{result[2030]['revenue']:>16,.1f}{result[2030]['fcfe']:>15,.1f}"
              f"{equity_value:>15,.1f}{per_share:>14.2f}")


def main() -> None:
    base = project()
    print_base(base)
    value, terminal_share, per_share = value_equity(base)
    print(f"\nBase equity value: ${value:,.1f}m | Value per share: ${per_share:,.2f} | Terminal share: {terminal_share:.1%}")
    print_sensitivity()


if __name__ == "__main__":
    main()
