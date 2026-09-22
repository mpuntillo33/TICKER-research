"""Lab 09: ABG five-year three-statement pro-forma model (USD millions)."""

from math import isclose


YEARS = (2026, 2027, 2028, 2029, 2030)

# Assumptions
GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_TO_GROSS_PROFIT = {2026: 0.665, 2027: 0.655, 2028: 0.645, 2029: 0.645, 2030: 0.645}
DEPRECIATION_TO_OPENING_PPE = 82.4 / 3_070.4
IMPAIRMENT = 120.0
CAPEX = 250.0
TAX_RATE = 0.255
INVENTORY_DAYS = 2_135.8 / (17_999.0 - 3_071.7) * 365
FLOOR_PLAN_TO_INVENTORY = 2_027.0 / 2_135.8
OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE = 0.008
MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
DEBT_REPAYMENT = 150.0
SHARE_BUYBACK = 150.0
FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349

# FY2025 opening balance sheet
OPENING = {
    "revenue": 17_999.0,
    "inventory": 2_135.8,
    "ppe": 3_070.4,
    "other_assets": 6_371.6,
    "cash": 40.4,
    "floor_plan": 2_027.0,
    "term_debt": 3_572.0,
    "revolver": 0.0,
    "other_liabilities": 2_127.5,
    "equity": 3_891.7,
}


def assert_balanced(year: int, gap: float, cash: float) -> None:
    """Refuse a balance-sheet mismatch or a cash balance under the minimum."""
    if not isclose(gap, 0.0, abs_tol=1e-8):
        raise AssertionError(f"FY{year}E is not balanced: assets - liabilities - equity = {gap:.1f}")
    if cash < MINIMUM_CASH - 1e-8:
        raise AssertionError(
            f"FY{year}E cash is below the minimum: {cash:.1f} < {MINIMUM_CASH:.1f}; "
            f"assets - liabilities - equity = {gap:.1f}"
        )


def project() -> dict[int, dict[str, float]]:
    """Project the income statement, balance sheet, and cash flow in model order."""
    results: dict[int, dict[str, float]] = {}
    opening = OPENING.copy()

    for year in YEARS:
        revenue = opening["revenue"] * (1 + GROWTH)
        gross_profit = revenue * GROSS_MARGIN
        sga = gross_profit * SGA_TO_GROSS_PROFIT[year]
        depreciation = opening["ppe"] * DEPRECIATION_TO_OPENING_PPE
        operating_income = gross_profit - sga - depreciation - IMPAIRMENT
        interest = (
            opening["floor_plan"] * FLOOR_PLAN_RATE
            + opening["term_debt"] * TERM_DEBT_RATE
            + opening["revolver"] * REVOLVER_RATE
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365
        floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
        ppe = opening["ppe"] + CAPEX - depreciation
        revenue_change = revenue - opening["revenue"]
        other_working_capital_change = OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE * revenue_change
        other_assets = opening["other_assets"] + other_working_capital_change - IMPAIRMENT
        term_debt = opening["term_debt"] - DEBT_REPAYMENT
        other_liabilities = opening["other_liabilities"]
        equity = opening["equity"] + net_income - SHARE_BUYBACK

        fcfe = (
            net_income
            + depreciation
            + IMPAIRMENT
            - CAPEX
            - (inventory - opening["inventory"])
            - other_working_capital_change
            + (floor_plan - opening["floor_plan"])
            - DEBT_REPAYMENT
        )
        preliminary_cash = opening["cash"] + fcfe - SHARE_BUYBACK
        revolver = opening["revolver"]
        if preliminary_cash < MINIMUM_CASH:
            draw = MINIMUM_CASH - preliminary_cash
            revolver += draw
            if revolver > REVOLVER_LIMIT:
                raise AssertionError(f"FY{year}E revolver exceeds its {REVOLVER_LIMIT:.1f} limit")
            cash = preliminary_cash + draw
        else:
            repayment = min(revolver, preliminary_cash - MINIMUM_CASH)
            revolver -= repayment
            cash = preliminary_cash - repayment

        assets = inventory + ppe + other_assets + cash
        liabilities = floor_plan + term_debt + revolver + other_liabilities
        gap = assets - liabilities - equity
        assert_balanced(year, gap, cash)

        results[year] = {
            "revenue": revenue, "gross_profit": gross_profit, "sga": sga,
            "depreciation": depreciation, "impairment": IMPAIRMENT,
            "operating_income": operating_income, "interest": interest,
            "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
            "inventory": inventory, "ppe": ppe, "other_assets": other_assets,
            "cash": cash, "floor_plan": floor_plan, "term_debt": term_debt,
            "revolver": revolver, "other_liabilities": other_liabilities,
            "equity": equity, "total_assets": assets, "total_liabilities": liabilities,
            "total_liabilities_and_equity": liabilities + equity,
            "capex": CAPEX, "debt_repayment": DEBT_REPAYMENT,
            "share_buyback": SHARE_BUYBACK, "fcfe": fcfe,
            "inventory_change": inventory - opening["inventory"],
            "other_working_capital_change": other_working_capital_change,
            "floor_plan_change": floor_plan - opening["floor_plan"],
            "revolver_change": revolver - opening["revolver"],
            "cash_change": cash - opening["cash"], "gap": gap,
        }
        opening = {**opening, **results[year]}

    return results


def print_table(title: str, rows: list[tuple[str, str]], results: dict[int, dict[str, float]]) -> None:
    print(f"\n{title}")
    print(f"{'USD millions':<30}" + "".join(f"{year}E".rjust(12) for year in YEARS))
    for label, key in rows:
        print(f"{label:<30}" + "".join(f"{results[year][key]:>12,.1f}" for year in YEARS))


def value_equity(results: dict[int, dict[str, float]]) -> tuple[float, float, float]:
    present_value_fcfe = sum(
        results[year]["fcfe"] / (1 + COST_OF_EQUITY) ** index
        for index, year in enumerate(YEARS, 1)
    )
    terminal_fcfe = results[2030]["fcfe"] + DEBT_REPAYMENT
    terminal_value = terminal_fcfe * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    present_value_terminal = terminal_value / (1 + COST_OF_EQUITY) ** len(YEARS)
    equity_value = present_value_fcfe + present_value_terminal
    return equity_value, present_value_terminal / equity_value, equity_value / SHARES_OUTSTANDING


def main() -> None:
    results = project()
    print_table("Income Statement", [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
        ("Depreciation", "depreciation"), ("Impairment", "impairment"),
        ("Operating income", "operating_income"), ("Interest", "interest"),
        ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income"),
    ], results)
    print_table("Balance Sheet", [
        ("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"),
        ("Cash", "cash"), ("Total assets", "total_assets"),
        ("Floor plan", "floor_plan"), ("Term debt", "term_debt"),
        ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
        ("Total liabilities", "total_liabilities"),
        ("Total liabilities and equity", "total_liabilities_and_equity"),
    ], results)
    print_table("Cash Flow", [
        ("Net income", "net_income"), ("Depreciation", "depreciation"),
        ("Impairment", "impairment"), ("Capital spending", "capex"),
        ("Change in inventory", "inventory_change"),
        ("Change in other working capital", "other_working_capital_change"),
        ("Change in floor plan", "floor_plan_change"),
        ("Debt repayment", "debt_repayment"), ("Free cash flow to equity", "fcfe"),
        ("Share buyback", "share_buyback"), ("Change in revolver", "revolver_change"),
        ("Change in cash", "cash_change"),
    ], results)
    print_table("Checks", [
        ("Assets - liabilities - equity", "gap"),
        ("Cash at / above minimum", "cash"),
    ], results)
    equity_value, terminal_share, value_per_share = value_equity(results)
    print("\nValuation")
    print(f"Equity value: ${equity_value:,.1f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${value_per_share:,.2f}")


if __name__ == "__main__":
    main()
