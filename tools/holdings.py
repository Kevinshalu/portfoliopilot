"""
Tool 1: Portfolio Holdings

Returns current portfolio holdings with sector breakdown, live prices, weights,
and basic risk metrics (beta, dividend yield).

Used by the PortfolioPilot agent when a user asks portfolio composition questions.

Data sources:
- Sample portfolio definition: data/sample_portfolio.json (synthetic)
- Live prices and beta: yfinance (public, free, ~15-min delay)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yfinance as yf


PORTFOLIO_PATH = Path(__file__).parent.parent / "data" / "sample_portfolio.json"


def _load_portfolio_definition() -> dict[str, Any]:
    """Load the static portfolio definition from JSON."""
    with PORTFOLIO_PATH.open("r") as f:
        return json.load(f)


def _enrich_with_market_data(ticker: str) -> dict[str, Any]:
    """Fetch live market data for a single ticker via yfinance."""
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "beta": info.get("beta"),
        "dividend_yield": info.get("dividendYield"),
        "market_cap": info.get("marketCap"),
        "industry": info.get("industry"),
    }


def get_portfolio_holdings(
    sectors: list[str] | None = None,
    min_position_weight_pct: float | None = None,
) -> dict[str, Any]:
    """
    Return current portfolio holdings, enriched with live market data.

    Args:
        sectors: Optional list of sector names to filter to (e.g., ["Financials"]).
        min_position_weight_pct: Optional minimum position weight (%) to include.

    Returns:
        Dict with:
            - holdings: list of position dicts (ticker, name, sector, shares,
              current_price, market_value, weight_pct, beta, dividend_yield, etc.)
            - total_value: total portfolio market value in USD
            - holdings_count: number of holdings returned (after filtering)
            - summary: 1-2 sentence natural language summary
    """
    portfolio = _load_portfolio_definition()
    enriched_holdings = []

    # First pass: enrich each holding with live data and compute market value
    for h in portfolio["holdings"]:
        market_data = _enrich_with_market_data(h["ticker"])
        current_price = market_data["current_price"]
        if current_price is None:
            # Skip holdings we can't price (shouldn't happen for S&P 500 names)
            continue
        enriched_holdings.append(
            {
                "ticker": h["ticker"],
                "name": h["name"],
                "sector": h["sector"],
                "shares": h["shares"],
                "purchase_price": h["purchase_price"],
                "current_price": round(current_price, 2),
                "market_value": round(current_price * h["shares"], 2),
                "beta": market_data["beta"],
                "dividend_yield": market_data["dividend_yield"],
                "market_cap": market_data["market_cap"],
                "industry": market_data["industry"],
            }
        )

    # Compute portfolio total and weights
    total_value = sum(h["market_value"] for h in enriched_holdings)
    for h in enriched_holdings:
        h["weight_pct"] = round(100 * h["market_value"] / total_value, 2)

    # Apply filters
    if sectors is not None:
        enriched_holdings = [h for h in enriched_holdings if h["sector"] in sectors]
    if min_position_weight_pct is not None:
        enriched_holdings = [
            h for h in enriched_holdings if h["weight_pct"] >= min_position_weight_pct
        ]

    # Sort by weight descending
    enriched_holdings.sort(key=lambda h: h["weight_pct"], reverse=True)

    # Build natural-language summary
    sector_breakdown: dict[str, float] = {}
    for h in enriched_holdings:
        sector_breakdown[h["sector"]] = sector_breakdown.get(h["sector"], 0) + h["weight_pct"]
    top_sector = max(sector_breakdown.items(), key=lambda kv: kv[1])
    summary = (
        f"Portfolio has {len(enriched_holdings)} holdings totaling "
        f"${total_value:,.0f}. Largest sector: {top_sector[0]} "
        f"({top_sector[1]:.1f}% of portfolio)."
    )

    return {
        "holdings": enriched_holdings,
        "total_value": round(total_value, 2),
        "holdings_count": len(enriched_holdings),
        "sector_breakdown": {k: round(v, 2) for k, v in sector_breakdown.items()},
        "summary": summary,
    }


if __name__ == "__main__":
    # Smoke test: run this file directly to verify the tool works
    result = get_portfolio_holdings()
    print(f"Total portfolio value: ${result['total_value']:,.2f}")
    print(f"Number of holdings: {result['holdings_count']}")
    print(f"\nSector breakdown:")
    for sector, weight in result["sector_breakdown"].items():
        print(f"  {sector}: {weight}%")
    print(f"\nTop 3 holdings by weight:")
    for h in result["holdings"][:3]:
        print(f"  {h['ticker']} ({h['name']}): {h['weight_pct']}% — ${h['market_value']:,.0f}")
