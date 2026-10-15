"""Lab 13 -- Portfolio Mandate Defense (standard-library Python only)."""

# Editable inputs: holding, issuer, business days to redeem, reserve-eligible.
HOLDINGS = [
    ("Cash", "none", 0, True),
    ("Treasury bills", "U.S. Treasury", 1, True),
    ("Treasury 10-year note", "U.S. Treasury", 1, True),
    ("Global equity index fund", "diversified fund", 2, False),
    ("Investment-grade bond fund", "diversified fund", 3, False),
    ("Private real estate fund", "diversified fund", 90, False),
    ("Acme Corp bonds", "Acme Corp", 4, False),
    ("Acme Corp stock", "Acme Corp", 1, False),
]

# Editable candidate percentage weights.
CANDIDATES = {
    "A": {"Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
          "Global equity index fund": 60, "Investment-grade bond fund": 26,
          "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0},
    "B": {"Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
          "Global equity index fund": 55, "Investment-grade bond fund": 20,
          "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4},
    "C": {"Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
          "Global equity index fund": 70, "Investment-grade bond fund": 20,
          "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8},
}

RESERVE_SIZE_USD_MILLIONS = 100
QUARTERLY_DISTRIBUTION_USD_MILLIONS = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_BUSINESS_DAYS = 5
MINIMUM_LIQUID_SHARE_PERCENT = 90
ISSUER_LIMIT_PERCENT = 8
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def percent(value):
    return f"{value:.1f}%"


def report_check(label, value, passed, requirement):
    print(f"{label}: {percent(value)} ({requirement}) -- {'PASS' if passed else 'FAIL'}")
    return not passed


def evaluate(candidate_name, weights, reserve_minimum):
    """Calculate all rules; companies are aggregated across their securities."""
    total = sum(weights.get(holding, 0) for holding, *_ in HOLDINGS)
    lowest = min(weights.get(holding, 0) for holding, *_ in HOLDINGS)
    reserve = sum(weights.get(holding, 0) for holding, _, _, eligible in HOLDINGS if eligible)
    liquid = sum(weights.get(holding, 0) for holding, _, days, _ in HOLDINGS
                 if days <= LIQUIDITY_WINDOW_BUSINESS_DAYS)
    issuer_exposure = {}
    for holding, issuer, _, _ in HOLDINGS:
        if issuer not in EXEMPT_ISSUERS:
            issuer_exposure[issuer] = issuer_exposure.get(issuer, 0) + weights.get(holding, 0)
    largest_issuer = max(issuer_exposure.values(), default=0)

    print(f"\nCandidate {candidate_name}")
    failures = 0
    failures += report_check("weights sum", total, total == 100, "must equal 100.0%")
    failures += report_check("lowest weight", lowest, lowest >= 0, "must be at least 0.0%")
    failures += report_check("reserve-eligible weight", reserve, reserve >= reserve_minimum,
                             f"minimum {percent(reserve_minimum)}")
    failures += report_check(f"redeemable within {LIQUIDITY_WINDOW_BUSINESS_DAYS} business days",
                             liquid, liquid >= MINIMUM_LIQUID_SHARE_PERCENT,
                             f"minimum {percent(MINIMUM_LIQUID_SHARE_PERCENT)}")
    failures += report_check("largest single-company exposure", largest_issuer,
                             largest_issuer <= ISSUER_LIMIT_PERCENT,
                             f"maximum {percent(ISSUER_LIMIT_PERCENT)}")
    # The calendar-year loss limit has no implementation-ready definition.
    print("requires CIO clarification")
    print("passes every checkable rule" if failures == 0 else f"fails {failures} rule(s)")


def main():
    reserve_minimum = (QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION_USD_MILLIONS
                       / RESERVE_SIZE_USD_MILLIONS * 100)
    print(f"reserve minimum: {QUARTERS_TO_COVER} * {QUARTERLY_DISTRIBUTION_USD_MILLIONS} "
          f"/ {RESERVE_SIZE_USD_MILLIONS} = {percent(reserve_minimum)}")
    for name, weights in CANDIDATES.items():
        evaluate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
