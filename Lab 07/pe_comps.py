"""Lab 07 P/E comparable-company calculation (standard library only)."""

from dataclasses import dataclass
from statistics import median


# Editable frozen case inputs: USD per share, FY2024 GAAP diluted EPS.
TARGET = ("ABG", "Asbury Automotive", 243.03, 21.50)
PEERS = [
    ("AN", "AutoNation", 169.84, 16.92),
    ("GPI", "Group 1 Automotive", 421.48, 36.81),
]


@dataclass(frozen=True)
class Company:
    ticker: str
    name: str
    price: float | None
    diluted_eps: float | None


def company_from_input(values: tuple[str, str, float | None, float | None]) -> Company:
    """Convert one editable input tuple into a Company."""
    return Company(*values)


def valid_price_and_eps(company: Company) -> bool:
    """P/E is meaningful only when both inputs are present and positive."""
    return (
        company.price is not None
        and company.diluted_eps is not None
        and company.price > 0
        and company.diluted_eps > 0
    )


def pe_multiple(company: Company) -> float | None:
    """Return price / diluted EPS, or None when the multiple is not meaningful."""
    if not valid_price_and_eps(company):
        return None
    return company.price / company.diluted_eps


def deduplicated_peers(target: Company, peer_inputs: list[Company]) -> list[Company]:
    """Keep the first occurrence of each peer ticker and exclude the target."""
    result: list[Company] = []
    seen_tickers = {target.ticker.upper()}
    for peer in peer_inputs:
        ticker = peer.ticker.upper()
        if ticker not in seen_tickers:
            result.append(peer)
            seen_tickers.add(ticker)
    return result


def implied_price(target: Company, multiple: float) -> float | None:
    """Apply a peer P/E to target EPS without a cash/debt bridge."""
    if target.diluted_eps is None or target.diluted_eps <= 0:
        return None
    return multiple * target.diluted_eps


def median_implied_price(target: Company, peers: list[Company]) -> float | None:
    """Return the median-P/E implied price using only peers with valid P/E values."""
    multiples = [multiple for peer in peers if (multiple := pe_multiple(peer)) is not None]
    if not multiples:
        return None
    return implied_price(target, median(multiples))


def dollars(value: float | None) -> str:
    return "not meaningful" if value is None else f"${value:,.2f}"


def main() -> None:
    target = company_from_input(TARGET)
    peers = deduplicated_peers(target, [company_from_input(values) for values in PEERS])
    print("P/E Comparable-Company Analysis")
    print(f"Target: {target.name} ({target.ticker})")
    if valid_price_and_eps(target):
        print(f"Target closing price: {dollars(target.price)}")
        print(f"Target FY2024 GAAP diluted EPS: ${target.diluted_eps:.2f}")
    else:
        print("Target price and/or diluted EPS is missing or nonpositive; implied prices are not meaningful.")
    print("\nPeer P/E multiples")
    valid_peers: list[Company] = []
    valid_multiples: list[float] = []
    for peer in peers:
        multiple = pe_multiple(peer)
        if multiple is None:
            print(f"{peer.ticker}: not meaningful (price and diluted EPS must both be positive)")
        else:
            valid_peers.append(peer)
            valid_multiples.append(multiple)
            print(f"{peer.ticker}: {multiple:.6f}x")
    if not valid_multiples:
        print("\nNo usable peers; no implied estimate.")
    else:
        minimum_multiple, median_multiple, maximum_multiple = min(valid_multiples), median(valid_multiples), max(valid_multiples)
        print(f"\nPeer median P/E: {median_multiple:.6f}x")
        if len(valid_multiples) == 1:
            print("One valid peer: reference estimate, no range.")
            print(f"Target at peer P/E: {dollars(implied_price(target, median_multiple))}")
        else:
            print(f"Target implied-price range: {dollars(implied_price(target, minimum_multiple))} - {dollars(implied_price(target, maximum_multiple))}")
            print(f"Target at peer median P/E: {dollars(implied_price(target, median_multiple))}")
    full_peer_estimate = median_implied_price(target, valid_peers)
    print("\nLeave-one-peer-out analysis")
    if not peers:
        print("No candidate peers to remove.")
    for removed_peer in peers:
        remaining_peers = [peer for peer in peers if peer.ticker.upper() != removed_peer.ticker.upper()]
        remaining_estimate = median_implied_price(target, remaining_peers)
        if remaining_estimate is None or full_peer_estimate is None:
            print(f"Remove {removed_peer.ticker}: no estimate.")
        else:
            change = remaining_estimate - full_peer_estimate
            print(f"Remove {removed_peer.ticker}: remaining median-implied price {dollars(remaining_estimate)}; change from full-peer estimate {change:+.2f}")


if __name__ == "__main__":
    main()
