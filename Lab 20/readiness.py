"""Reproducible Project 2 readiness decision.

Run from the repository root with:
    python "Lab 20/readiness.py"
or change the load-bearing equity-return estimate with:
    python "Lab 20/readiness.py" --equity-return 7.0
"""
from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Lab 15"))
from portfolio import (  # noqa: E402
    CORRELATIONS,
    OBJECTIVE_RETURN,
    RESERVE_ELIGIBLE,
    SLEEVES,
    benchmark_weights,
    covariance_matrix,
    equal_weight_weights,
    expected_return,
    inverse_volatility_weights,
    portfolio_volatility,
    reserve_eligible_weight,
    search_lowest_risk_mix,
)

RESERVE_MINIMUM = 0.03


def verdict(weights, sleeves, covariance):
    earned = expected_return(weights, sleeves)
    reserve = reserve_eligible_weight(weights, RESERVE_ELIGIBLE)
    return {
        "return": earned,
        "volatility": portfolio_volatility(weights, covariance),
        "reserve": reserve,
        "return_pass": earned >= OBJECTIVE_RETURN,
        "reserve_pass": reserve >= RESERVE_MINIMUM,
    }


def describe(name, result):
    weights = ", ".join(f"{asset} {weight:.0%}" for asset, weight in result["weights"].items())
    mandate = "PASS" if result["return_pass"] and result["reserve_pass"] else "FAIL"
    print(f"{name}: {weights}")
    print(f"  expected return {result['return']:.2%} (minimum {OBJECTIVE_RETURN:.2%}): "
          f"{'PASS' if result['return_pass'] else 'FAIL'}")
    print(f"  volatility {result['volatility']:.2%}")
    print(f"  reserve eligible {result['reserve']:.0%} (minimum {RESERVE_MINIMUM:.0%}): "
          f"{'PASS' if result['reserve_pass'] else 'FAIL'}")
    print(f"  mandate verdict: {mandate}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--equity-return", type=float, default=8.0,
                        help="annual equity expected-return estimate in percent (default: 8.0)")
    args = parser.parse_args()
    if not 0 <= args.equity_return <= 100:
        parser.error("--equity-return must be between 0 and 100 percent")

    sleeves = copy.deepcopy(SLEEVES)
    sleeves["equity"]["expected_return"] = args.equity_return / 100
    covariance = covariance_matrix(sleeves, CORRELATIONS)
    print("Project 2 readiness decision — education only, not investment advice")
    print(f"Equity expected-return input: {args.equity_return:.1f}%")
    for name, weights in (
        ("40/60 benchmark", benchmark_weights(sleeves)),
        ("Equal weight", equal_weight_weights(sleeves)),
        ("Inverse volatility", inverse_volatility_weights(sleeves)),
    ):
        describe(name, {"weights": weights, **verdict(weights, sleeves, covariance)})
    selected = search_lowest_risk_mix(sleeves, CORRELATIONS, OBJECTIVE_RETURN,
                                      RESERVE_ELIGIBLE, RESERVE_MINIMUM)
    if selected is None:
        print("Constrained portfolio: no feasible mix — REJECT")
        return
    describe("Constrained lowest-risk mix", {"weights": selected["weights"],
             **verdict(selected["weights"], sleeves, covariance)})
    print("Decision: PILOT, NOT ADOPT. Use the constrained mix only as an education "
          "demonstration; reverse this decision if the planning return, reserve rule, "
          "or point-in-time data rule cannot be defended.")


if __name__ == "__main__":
    main()
