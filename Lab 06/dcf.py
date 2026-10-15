"""Five-year FCFF DCF model (USD millions, except per-share value)."""
import sys

# Editable inputs
STARTING_FCFF = 936.75
YEARLY_GROWTH_RATES = [0.02, 0.02, 0.02, 0.02, 0.02]
WACC = 0.08
TERMINAL_GROWTH = 0.025
NON_OPERATING_CASH = 198.6
DEBT = 8946.6
DILUTED_SHARES = 547.2

# Lab 06 sensitivity and reverse-DCF inputs
SENSITIVITY_WACCS = [0.09, 0.10, 0.11]
SENSITIVITY_TERMINAL_GROWTHS = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 11.70
REVERSE_SHIFT_LOWER_BOUND = -0.05
REVERSE_SHIFT_UPPER_BOUND = 0.10
BISECTION_TOLERANCE = 0.000001
MAX_BISECTION_ITERATIONS = 200


def value_per_share(yearly_growth_rates, wacc, terminal_growth):
    """Return DCF value per diluted share, or None for an invalid WACC/g pair."""
    if terminal_growth >= wacc:
        return None
    fcff = STARTING_FCFF
    fcff_by_year = []
    for growth_rate in yearly_growth_rates:
        fcff *= 1.0 + growth_rate
        fcff_by_year.append(fcff)
    explicit_pv = sum(
        fcff / (1.0 + wacc) ** year
        for year, fcff in enumerate(fcff_by_year, start=1)
    )
    terminal_value = fcff_by_year[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)
    terminal_pv = terminal_value / (1.0 + wacc) ** 5
    equity_value = explicit_pv + terminal_pv + NON_OPERATING_CASH - DEBT
    return equity_value / DILUTED_SHARES


def print_sensitivity_grid():
    print("\nSensitivity grid: value per diluted share")
    header = "WACC \\ terminal growth".ljust(24)
    print(header + "".join(f"{growth:>12.1%}" for growth in SENSITIVITY_TERMINAL_GROWTHS))
    for sensitivity_wacc in SENSITIVITY_WACCS:
        row = f"{sensitivity_wacc:.1%}".ljust(24)
        for sensitivity_growth in SENSITIVITY_TERMINAL_GROWTHS:
            result = value_per_share(YEARLY_GROWTH_RATES, sensitivity_wacc, sensitivity_growth)
            cell = "invalid" if result is None else f"${result:,.2f}"
            row += f"{cell:>12}"
        print(row)


def reverse_dcf_uniform_growth_shift():
    """Solve the uniform explicit-growth shift by bisection, if bracketed."""
    if any(growth + bound <= -1.0 for growth in YEARLY_GROWTH_RATES
           for bound in (REVERSE_SHIFT_LOWER_BOUND, REVERSE_SHIFT_UPPER_BOUND)):
        return None
    def difference(shift):
        result = value_per_share([growth + shift for growth in YEARLY_GROWTH_RATES], WACC, TERMINAL_GROWTH)
        if result is None:
            raise ValueError("Base WACC and terminal growth create an invalid valuation.")
        return result - TARGET_SHARE_PRICE
    lower, upper = REVERSE_SHIFT_LOWER_BOUND, REVERSE_SHIFT_UPPER_BOUND
    lower_difference, upper_difference = difference(lower), difference(upper)
    if lower_difference == 0:
        return lower
    if upper_difference == 0:
        return upper
    if lower_difference * upper_difference > 0:
        return None
    for _ in range(MAX_BISECTION_ITERATIONS):
        midpoint = (lower + upper) / 2.0
        midpoint_difference = difference(midpoint)
        if abs(midpoint_difference) <= BISECTION_TOLERANCE:
            return midpoint
        if lower_difference * midpoint_difference < 0:
            upper = midpoint
        else:
            lower, lower_difference = midpoint, midpoint_difference
    return None


def print_reverse_dcf():
    print("\nReverse DCF: uniform shift to all five explicit growth rates")
    print(f"Target share price: ${TARGET_SHARE_PRICE:,.2f}")
    print("Held fixed: "
          f"starting FCFF ${STARTING_FCFF:,.2f}m; WACC {WACC:.1%}; "
          f"terminal growth {TERMINAL_GROWTH:.1%}; cash ${NON_OPERATING_CASH:,.1f}m; "
          f"debt ${DEBT:,.1f}m; diluted shares {DILUTED_SHARES:,.1f}m.")
    print("Base explicit growth rates held in the shift: " + ", ".join(f"{rate:.1%}" for rate in YEARLY_GROWTH_RATES))
    print(f"Bisection bracket: {REVERSE_SHIFT_LOWER_BOUND:+.1%} to {REVERSE_SHIFT_UPPER_BOUND:+.1%}.")
    solved_shift = reverse_dcf_uniform_growth_shift()
    print("No solution in this bracket." if solved_shift is None else f"Solved uniform growth shift: {solved_shift:+.4%}")


def main():
    if TERMINAL_GROWTH >= WACC:
        sys.exit("Error: terminal growth must be less than WACC.")
    if len(YEARLY_GROWTH_RATES) != 5:
        sys.exit("Error: provide exactly five yearly growth rates.")
    if DILUTED_SHARES <= 0:
        sys.exit("Error: diluted shares must be greater than zero.")
    fcff, fcff_by_year = STARTING_FCFF, []
    for growth_rate in YEARLY_GROWTH_RATES:
        fcff *= 1.0 + growth_rate
        fcff_by_year.append(fcff)
    present_value_explicit_fcff = sum(fcff / (1.0 + WACC) ** year for year, fcff in enumerate(fcff_by_year, start=1))
    terminal_value_year_5 = fcff_by_year[-1] * (1.0 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    present_value_terminal_value = terminal_value_year_5 / (1.0 + WACC) ** 5
    enterprise_value = present_value_explicit_fcff + present_value_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value = equity_value / DILUTED_SHARES
    terminal_share = present_value_terminal_value / enterprise_value
    # Keep these twelve base-case lines unchanged from Lab 05.
    for year, fcff in enumerate(fcff_by_year, start=1):
        print(f"FCFF Year {year}: {fcff:.4f}")
    print(f"Present value of the explicit FCFF: {present_value_explicit_fcff:.4f}")
    print(f"Terminal value at Year 5: {terminal_value_year_5:.4f}")
    print(f"Present value of the terminal value: {present_value_terminal_value:.4f}")
    print(f"Enterprise value: {enterprise_value:.4f}")
    print(f"Equity value: {equity_value:.4f}")
    print(f"Value per diluted share: {value:.4f}")
    print("Present value of the terminal value as a share of enterprise value: " f"{terminal_share:.4f}")
    print_sensitivity_grid()
    print_reverse_dcf()


if __name__ == "__main__":
    main()
