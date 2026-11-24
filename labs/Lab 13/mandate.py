"""Lab 13 -- Portfolio Mandate Defense.

All inputs in the two sections below are deliberately editable.
"""

# Supplied holdings table: holding, issuer, business days to redeem,
# reserve-eligible.  The final Boolean is the reserve-eligibility flag.
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

# Candidate percentage weights, keyed by the holding names above.
CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5,
        "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0,
        "Acme Corp stock": 8,
    },
    # Lab 14 benchmark: 40% investment-grade bonds and 60% global equity.
    "E": {
        "Cash": 0, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 60, "Investment-grade bond fund": 40,
        "Private real estate fund": 0, "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
}

RESERVE_SIZE_USD_MILLIONS = 100
QUARTERLY_DISTRIBUTION_USD_MILLIONS = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_BUSINESS_DAYS = 5
MINIMUM_LIQUID_SHARE_PERCENT = 90
ISSUER_LIMIT_PERCENT = 8

# Cash, U.S. Treasury, and diversified funds do not count toward issuer limit.
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def percent(value):
    """Format a percentage with the lab's required one decimal place."""
    return f"{value:.1f}%"


def check(label, measured, passes, requirement=""):
    suffix = f" ({requirement})" if requirement else ""
    outcome = "PASS" if passes else "FAIL"
    print(f"{label}: {percent(measured)}{suffix} — {outcome}")
    return not passes


def evaluate_candidate(name, weights, reserve_minimum_percent):
    """Calculate every rule from the editable table and weights."""
    metadata = {holding: (issuer, days, reserve_eligible)
                for holding, issuer, days, reserve_eligible in HOLDINGS}
    total_weight = sum(weights.get(holding, 0) for holding in metadata)
    lowest_weight = min(weights.get(holding, 0) for holding in metadata)
    reserve_weight = sum(
        weights.get(holding, 0)
        for holding, (_, _, reserve_eligible) in metadata.items()
        if reserve_eligible
    )
    liquid_weight = sum(
        weights.get(holding, 0)
        for holding, (_, days, _) in metadata.items()
        if days <= LIQUIDITY_WINDOW_BUSINESS_DAYS
    )

    company_exposures = {}
    for holding, (issuer, _, _) in metadata.items():
        if issuer not in EXEMPT_ISSUERS:
            company_exposures[issuer] = company_exposures.get(issuer, 0) + weights.get(holding, 0)
    largest_company_exposure = max(company_exposures.values(), default=0)

    print(f"\nCandidate {name}")
    failures = 0
    failures += check("weights sum", total_weight, total_weight == 100,
                      "must equal 100.0%")
    failures += check("lowest weight", lowest_weight, lowest_weight >= 0,
                      "must be at least 0.0%")
    failures += check("reserve-eligible weight", reserve_weight,
                      reserve_weight >= reserve_minimum_percent,
                      f"minimum {percent(reserve_minimum_percent)}")
    failures += check(f"redeemable within {LIQUIDITY_WINDOW_BUSINESS_DAYS} business days",
                      liquid_weight, liquid_weight >= MINIMUM_LIQUID_SHARE_PERCENT,
                      f"minimum {percent(MINIMUM_LIQUID_SHARE_PERCENT)}")
    failures += check("largest single-company exposure", largest_company_exposure,
                      largest_company_exposure <= ISSUER_LIMIT_PERCENT,
                      f"maximum {percent(ISSUER_LIMIT_PERCENT)}")

    # The mandate does not define this test, so it is intentionally never tested.
    print("requires CIO clarification")
    if failures:
        print(f"fails {failures} rule(s)")
    else:
        print("passes every checkable rule")


def main():
    reserve_minimum_percent = (
        QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION_USD_MILLIONS
        / RESERVE_SIZE_USD_MILLIONS * 100
    )
    print("reserve minimum: "
          f"{QUARTERS_TO_COVER} × {QUARTERLY_DISTRIBUTION_USD_MILLIONS} "
          f"÷ {RESERVE_SIZE_USD_MILLIONS} = {percent(reserve_minimum_percent)}")
    for name, weights in CANDIDATES.items():
        evaluate_candidate(name, weights, reserve_minimum_percent)


if __name__ == "__main__":
    main()
