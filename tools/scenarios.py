"""
Tool 3: Scenario Analysis — TO BE IMPLEMENTED ON DAY 3

Stress-test portfolio against macro scenarios:
- Rate shock (treasury yields move N bps)
- Equity drawdown (SP500 moves N%)
- Commodity shock (oil moves N%)
- Custom user-defined scenarios

Methodology (simplified):
- Beta-based sensitivity model
- Per-position impact = beta * scenario_market_move * weight
- Document assumptions explicitly in README — this is a demo, not production-grade
"""

from __future__ import annotations

from typing import Any


def run_scenario_analysis(scenario: dict[str, Any]) -> dict[str, Any]:
    """
    Estimate portfolio impact under a macro scenario.

    Args:
        scenario: Dict with scenario_name and shocks dict (e.g.,
            {"scenario_name": "Rate Shock", "shocks": {"10y_treasury_yield_change_bps": 100}})

    Returns:
        Dict with estimated_portfolio_impact_pct, estimated_portfolio_impact_usd,
        most_impacted_positions, least_impacted_positions, and summary.
    """
    # TODO Day 3: implement
    raise NotImplementedError("Day 3 implementation pending")
