"""
Tool 3: Scenario Analysis

Applies pre-defined hypothetical market shocks to the portfolio and reports
expected P&L per holding and at the portfolio level.

Used by the PortfolioPilot agent for "what-if" risk queries.

Methodology (simplified, prototype-grade):
    P&L_pct per holding = beta * market_move_pct + sector_override_pct
    P&L_usd = market_value * P&L_pct / 100

Real risk systems use full revaluation against shocked factor curves;
this is a directional approximation suitable for demos.
"""

from __future__ import annotations

from typing import Any

from tools.holdings import get_portfolio_holdings


SCENARIOS: dict[str, dict[str, Any]] = {
    "rate_shock_+100bps": {
        "description": "Fed surprise +100bps rate hike",
        "market_move_pct": -3.0,
        "sector_overrides_pct": {
            "Financials": 1.5,
            "Information Technology": -2.0,
            "Communication Services": -1.5,
            "Consumer Discretionary": -1.0,
        },
    },
    "equity_crash_-20%": {
        "description": "Broad equity drawdown of 20%",
        "market_move_pct": -20.0,
        "sector_overrides_pct": {},
    },
    "oil_shock_+30%": {
        "description": "Oil price spike of +30%",
        "market_move_pct": -1.0,
        "sector_overrides_pct": {
            "Energy": 10.0,
            "Consumer Discretionary": -3.0,
            "Industrials": -2.0,
        },
    },
}


def _apply_scenario_to_holding(holding: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    """Compute P&L for a single holding under one scenario."""
    beta = holding.get("beta") or 1.0  # missing beta → assume market-neutral 1.0
    sector_override = scenario["sector_overrides_pct"].get(holding["sector"], 0.0)
    pnl_pct = beta * scenario["market_move_pct"] + sector_override
    pnl_usd = holding["market_value"] * pnl_pct / 100
    return {
        "ticker": holding["ticker"],
        "sector": holding["sector"],
        "market_value_before": holding["market_value"],
        "pnl_pct": round(pnl_pct, 2),
        "pnl_usd": round(pnl_usd, 2),
        "market_value_after": round(holding["market_value"] + pnl_usd, 2),
    }


def run_scenario_analysis(scenario_name: str) -> dict[str, Any]:
    """Apply a named scenario to the current portfolio and return per-holding + total P&L."""
    if scenario_name not in SCENARIOS:
        raise ValueError(
            f"Unknown scenario '{scenario_name}'. "
            f"Available: {list(SCENARIOS.keys())}"
        )
    scenario = SCENARIOS[scenario_name]
    portfolio = get_portfolio_holdings()
    holdings = portfolio["holdings"]

    impacts = [_apply_scenario_to_holding(h, scenario) for h in holdings]
    impacts.sort(key=lambda i: i["pnl_usd"])  # losers first — what a PM looks at

    total_value_before = portfolio["total_value"]
    total_pnl_usd = sum(i["pnl_usd"] for i in impacts)
    total_pnl_pct = 100 * total_pnl_usd / total_value_before

    worst = impacts[0]
    best = impacts[-1]
    summary = (
        f"Scenario '{scenario_name}': {scenario['description']}. "
        f"Portfolio P&L: ${total_pnl_usd:,.0f} ({total_pnl_pct:+.2f}%). "
        f"Worst hit: {worst['ticker']} ${worst['pnl_usd']:,.0f} ({worst['pnl_pct']:+.2f}%). "
        f"Best: {best['ticker']} ${best['pnl_usd']:,.0f} ({best['pnl_pct']:+.2f}%)."
    )

    return {
        "scenario_name": scenario_name,
        "scenario_description": scenario["description"],
        "total_value_before": total_value_before,
        "total_value_after": round(total_value_before + total_pnl_usd, 2),
        "total_pnl_usd": round(total_pnl_usd, 2),
        "total_pnl_pct": round(total_pnl_pct, 2),
        "holding_impacts": impacts,
        "summary": summary,
    }


if __name__ == "__main__":
    for name in SCENARIOS:
        result = run_scenario_analysis(name)
        print(result["summary"])