"""Lab 15 -- Portfolio stability decision engine.

Run with: python portfolio.py
The original Lab 14 output below is intentionally unchanged.
"""

import csv
import io
import math


SLEEVES = {
    "bills": {"expected_return": 0.035, "volatility": 0.005},
    "10-year": {"expected_return": 0.043, "volatility": 0.070},
    "IG bonds": {"expected_return": 0.050, "volatility": 0.060},
    "equity": {"expected_return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "bills": {"bills": 1.00, "10-year": 0.10, "IG bonds": 0.05, "equity": 0.00},
    "10-year": {"bills": 0.10, "10-year": 1.00, "IG bonds": 0.80, "equity": -0.10},
    "IG bonds": {"bills": 0.05, "10-year": 0.80, "IG bonds": 1.00, "equity": 0.25},
    "equity": {"bills": 0.00, "10-year": -0.10, "IG bonds": 0.25, "equity": 1.00},
}

OBJECTIVE_RETURN = 0.065
RESERVE_ELIGIBLE = {"bills", "10-year"}


def validate_correlation_table(correlations, sleeves):
    """Reject missing, out-of-range, or non-symmetric correlation entries."""
    names = list(sleeves)
    if set(correlations) != set(names):
        raise ValueError("Correlation table rows must match the sleeve names.")
    for left in names:
        if set(correlations[left]) != set(names):
            raise ValueError(f"Correlation row for {left} must contain every sleeve.")
        for right in names:
            value = correlations[left][right]
            if not -1 <= value <= 1:
                raise ValueError(
                    f"Correlation for {left} and {right} is {value}; it must be between -1 and 1."
                )
            if not math.isclose(value, correlations[right][left], abs_tol=1e-12):
                raise ValueError(
                    f"Correlation table is not symmetric: {left}/{right} does not equal {right}/{left}."
                )


def covariance_matrix(sleeves, correlations):
    """Return covariance[i][j] = correlation[i][j] * vol[i] * vol[j]."""
    return {
        left: {
            right: correlations[left][right]
            * sleeves[left]["volatility"]
            * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def benchmark_weights(sleeves):
    """Return the 40% IG-bond / 60% equity benchmark weights."""
    return {name: 0.40 if name == "IG bonds" else 0.60 if name == "equity" else 0.0
            for name in sleeves}


def equal_weight_weights(sleeves):
    """Return equal weights across all sleeves."""
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility_weights(sleeves):
    """Return weights proportional to one divided by each sleeve's volatility."""
    inverse_volatilities = {
        name: 1 / values["volatility"] for name, values in sleeves.items()
    }
    total = sum(inverse_volatilities.values())
    return {name: value / total for name, value in inverse_volatilities.items()}


def expected_return(weights, sleeves):
    """Calculate the weighted expected return."""
    return sum(weights[name] * sleeves[name]["expected_return"] for name in sleeves)


def portfolio_variance(weights, covariance):
    """Calculate w-transpose times covariance times w using the full matrix."""
    return sum(
        weights[left] * covariance[left][right] * weights[right]
        for left in weights
        for right in weights
    )


def portfolio_volatility(weights, covariance):
    """Calculate portfolio volatility as the square root of portfolio variance."""
    return portfolio_variance(weights, covariance) ** 0.5


def reserve_eligible_weight(weights, reserve_eligible):
    """Sum the weights of sleeves that can serve as the reserve."""
    return sum(weights[name] for name in reserve_eligible)


def format_weights(weights, sleeves):
    """Format sleeve weights in the requested display order."""
    return " / ".join(f"{weights[name] * 100:.1f}" for name in sleeves)


def print_portfolio(name, weights, sleeves, covariance, objective_return, reserve_eligible):
    """Print one portfolio's calculated lab outputs."""
    earned = expected_return(weights, sleeves)
    risk = portfolio_volatility(weights, covariance)
    reserve = reserve_eligible_weight(weights, reserve_eligible)
    meets_objective = "yes" if earned >= objective_return else "no"
    print(f"{name}\n"
          f"  Weights (bills / 10-year / IG / equity): {format_weights(weights, sleeves)}\n"
          f"  Expected return: {earned * 100:.2f}%\n"
          f"  Volatility: {risk * 100:.2f}%\n"
          f"  Reserve-eligible weight: {reserve * 100:.1f}%\n"
          f"  Meets {objective_return * 100:.1f}% objective? {meets_objective}")


def _weight_combinations(asset_count, units):
    """Yield every non-negative integer vector adding to units."""
    if asset_count == 1:
        yield (units,)
        return
    for first in range(units + 1):
        for remainder in _weight_combinations(asset_count - 1, units - first):
            yield (first,) + remainder


def search_lowest_risk_mix(sleeves, correlations, objective_return, reserve_eligible,
                           reserve_minimum, step=0.05):
    """Return the lowest-volatility feasible long-only mix on a fixed weight grid.

    Returns None when no mix meets both the return objective and reserve rule.
    """
    if not 0 < step <= 1 or not math.isclose(1 / step, round(1 / step)):
        raise ValueError("step must divide 100% exactly.")
    validate_correlation_table(correlations, sleeves)
    names = list(sleeves)
    if not set(reserve_eligible).issubset(sleeves):
        raise ValueError("Reserve-eligible assets must be in sleeves.")
    covariance = covariance_matrix(sleeves, correlations)
    units = round(1 / step)
    best = None
    for combination in _weight_combinations(len(names), units):
        weights = {name: unit * step for name, unit in zip(names, combination)}
        earned = expected_return(weights, sleeves)
        reserve = reserve_eligible_weight(weights, reserve_eligible)
        if earned + 1e-12 < objective_return or reserve + 1e-12 < reserve_minimum:
            continue
        volatility = portfolio_volatility(weights, covariance)
        if best is None or volatility < best["volatility"] - 1e-12:
            best = {"weights": weights, "expected_return": earned,
                    "volatility": volatility, "reserve_weight": reserve}
    return best


def estimate_from_prices_csv(source, last_36_months=False):
    """Estimate annualized returns, volatility, and correlations from monthly prices.

    The input has date first, oldest first, and one price column per ticker.
    With last_36_months=True, estimates use the latest 36 monthly returns.
    """
    if hasattr(source, "read"):
        raw = source.read()
    else:
        with open(source, "rb") as price_file:
            raw = price_file.read()
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(raw)))
    if not rows or not rows[0]:
        raise ValueError("The prices CSV has no data rows.")
    fields = list(rows[0])
    if len(fields) < 3 or fields[0].strip().lower() != "date":
        raise ValueError("CSV must have Date first and at least two ticker columns.")
    names = fields[1:]
    prices = {name: [] for name in names}
    for row in rows:
        for name in names:
            try:
                price = float(row[name])
            except (TypeError, ValueError) as error:
                raise ValueError(f"Invalid price for {name}.") from error
            if price <= 0:
                raise ValueError(f"Prices for {name} must be positive.")
            prices[name].append(price)
    returns = {name: [later / earlier - 1 for earlier, later in zip(values, values[1:])]
               for name, values in prices.items()}
    if last_36_months:
        returns = {name: values[-36:] for name, values in returns.items()}
    observations = len(next(iter(returns.values())))
    if observations < 2:
        raise ValueError("At least three monthly prices are required.")
    means = {name: sum(values) / observations for name, values in returns.items()}
    monthly_volatility = {
        name: math.sqrt(sum((value - means[name]) ** 2 for value in values)
                        / (observations - 1))
        for name, values in returns.items()
    }
    if any(value == 0 for value in monthly_volatility.values()):
        raise ValueError("Cannot calculate correlation when a ticker has zero volatility.")
    correlations = {
        left: {
            right: 1.0 if left == right else sum(
                (x - means[left]) * (y - means[right])
                for x, y in zip(returns[left], returns[right])
            ) / ((observations - 1) * monthly_volatility[left] * monthly_volatility[right])
            for right in names
        }
        for left in names
    }
    sleeves = {
        name: {"expected_return": means[name] * 12,
               "volatility": monthly_volatility[name] * math.sqrt(12)}
        for name in names
    }
    return sleeves, correlations


def main():
    """Validate inputs, construct covariance, and price all baseline portfolios."""
    validate_correlation_table(CORRELATIONS, SLEEVES)
    covariance = covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": benchmark_weights(SLEEVES),
        "Equal weight": equal_weight_weights(SLEEVES),
        "Inverse volatility": inverse_volatility_weights(SLEEVES),
    }
    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariance, OBJECTIVE_RETURN, RESERVE_ELIGIBLE)


if __name__ == "__main__":
    main()
