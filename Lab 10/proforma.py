
"""Lab 10: Albertsons Companies (ACI) five-year pro-forma, USD millions."""

from math import isclose

YEARS = (2026, 2027, 2028, 2029, 2030)

# Labelled assumptions and sources are in README.md.
GROWTH = {2026: .005, 2027: .010, 2028: .015, 2029: .020, 2030: .020}
GROSS_MARGIN = {2026: .270, 2027: .2705, 2028: .271, 2029: .2715, 2030: .272}
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
SHARES_OUTSTANDING = 499.542902  # FY2025 issued shares less treasury shares

# FY2025 opening balance sheet (February 28, 2026). Other lines aggregate reported items.
OPENING = {"revenue": 83_172.5, "inventory": 5_173.9, "ppe": 9_903.7,
           "other_assets": 11_489.7, "cash": 198.6, "debt": 8_946.6,
           "revolver": 0.0, "other_liabilities": 15_983.1, "equity": 1_836.2}


def assert_balanced(year: int, gap: float, cash: float) -> None:
    """Refuse an unbalanced statement or cash below its liquidity floor."""
    if not isclose(gap, 0.0, abs_tol=1e-8):
        raise AssertionError(f"FY{year}E is not balanced: assets - liabilities - equity = {gap:.1f}")
    if cash < MINIMUM_CASH - 1e-8:
        raise AssertionError(f"FY{year}E cash is below the minimum: {cash:.1f} < {MINIMUM_CASH:.1f}")


def project() -> dict[int, dict[str, float]]:
    results: dict[int, dict[str, float]] = {}
    opening = OPENING.copy()
    for year in YEARS:
        revenue = opening["revenue"] * (1 + GROWTH[year])
        gross_profit = revenue * GROSS_MARGIN[year]
        sga = gross_profit * SGA_TO_GROSS_PROFIT[year]
        operating_income = gross_profit - sga
        depreciation = opening["ppe"] * DEPRECIATION_TO_OPENING_PPE
        interest = opening["debt"] * INTEREST_RATE + opening["revolver"] * REVOLVER_RATE
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365
        ppe = opening["ppe"] + CAPEX - depreciation
        other_assets = opening["other_assets"]
        other_liabilities_change = OTHER_OPERATING_LIABILITIES_TO_REVENUE_CHANGE * (revenue - opening["revenue"])
        other_liabilities = opening["other_liabilities"] + other_liabilities_change
        debt = opening["debt"] - DEBT_REPAYMENT
        equity = opening["equity"] + net_income - DIVIDENDS

        # Cash is calculated from cash flow; it is not an input or balancing plug.
        fcfe = (net_income + depreciation - CAPEX - (inventory - opening["inventory"])
                - (other_assets - opening["other_assets"]) + other_liabilities_change - DEBT_REPAYMENT)
        preliminary_cash = opening["cash"] + fcfe - DIVIDENDS
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
        liabilities = debt + revolver + other_liabilities
        gap = assets - liabilities - equity
        assert_balanced(year, gap, cash)
        results[year] = {"revenue": revenue, "gross_profit": gross_profit, "sga": sga,
            "depreciation": depreciation, "operating_income": operating_income, "interest": interest,
            "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
            "inventory": inventory, "ppe": ppe, "other_assets": other_assets, "cash": cash,
            "debt": debt, "revolver": revolver, "other_liabilities": other_liabilities, "equity": equity,
            "total_assets": assets, "total_liabilities": liabilities,
            "total_liabilities_and_equity": liabilities + equity, "capex": CAPEX,
            "debt_repayment": DEBT_REPAYMENT, "dividends": DIVIDENDS, "fcfe": fcfe,
            "inventory_change": inventory - opening["inventory"],
            "other_liabilities_change": other_liabilities_change,
            "revolver_change": revolver - opening["revolver"], "cash_change": cash - opening["cash"], "gap": gap}
        opening = {**opening, **results[year]}
    return results


def print_table(title: str, rows: list[tuple[str, str]], results: dict[int, dict[str, float]]) -> None:
    print(f"\n{title}")
    print(f"{'USD millions':<34}" + "".join(f"{year}E".rjust(12) for year in YEARS))
    for label, key in rows:
        print(f"{label:<34}" + "".join(f"{results[year][key]:>12,.1f}" for year in YEARS))


def value_equity(results: dict[int, dict[str, float]]) -> tuple[float, float, float]:
    pv_fcfe = sum(results[y]["fcfe"] / (1 + COST_OF_EQUITY) ** i for i, y in enumerate(YEARS, 1))
    terminal_value = results[2030]["fcfe"] * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    pv_terminal = terminal_value / (1 + COST_OF_EQUITY) ** len(YEARS)
    equity_value = pv_fcfe + pv_terminal
    return equity_value, pv_terminal / equity_value, equity_value / SHARES_OUTSTANDING


def main() -> None:
    results = project()
    print_table("Income Statement", [("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
        ("Operating income", "operating_income"), ("Interest", "interest"), ("Pretax income", "pretax_income"),
        ("Tax", "tax"), ("Net income", "net_income")], results)
    print_table("Balance Sheet", [("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"),
        ("Cash", "cash"), ("Total assets", "total_assets"), ("Debt and finance leases", "debt"),
        ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
        ("Total liabilities", "total_liabilities"), ("Total liabilities and equity", "total_liabilities_and_equity")], results)
    print_table("Cash Flow", [("Net income", "net_income"), ("Depreciation & amortization", "depreciation"),
        ("Capital spending", "capex"), ("Change in inventory", "inventory_change"),
        ("Change in other liabilities", "other_liabilities_change"), ("Debt repayment", "debt_repayment"),
        ("Free cash flow to equity", "fcfe"), ("Dividends", "dividends"), ("Change in revolver", "revolver_change"),
        ("Change in cash", "cash_change")], results)
    print_table("Checks", [("Assets - liabilities - equity", "gap"), ("Cash at / above minimum", "cash")], results)
    equity_value, terminal_share, per_share = value_equity(results)
    print("\nValuation")
    print(f"Equity value: ${equity_value:,.1f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${per_share:,.2f}")


if __name__ == "__main__":
    main()

