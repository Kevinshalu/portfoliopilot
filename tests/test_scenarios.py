"""Smoke tests for Tool 3: scenarios."""
import pytest

from tools.scenarios import (
    SCENARIOS,
    _apply_scenario_to_holding,
    run_scenario_analysis,
)


def test_apply_to_holding_math():
    """Per-holding P&L = beta * market_move + sector_override, in dollars."""
    holding = {
        "ticker": "X",
        "sector": "Financials",
        "beta": 1.5,
        "market_value": 100_000,
    }
    scenario = {
        "market_move_pct": -10.0,
        "sector_overrides_pct": {"Financials": 2.0},
    }
    # P&L_pct = 1.5 * -10 + 2 = -13.0  → -$13,000
    result = _apply_scenario_to_holding(holding, scenario)
    assert result["pnl_pct"] == -13.0
    assert result["pnl_usd"] == -13_000.0
    assert result["market_value_after"] == 87_000.0


def test_unknown_scenario_raises():
    """Asking for an unknown scenario should raise ValueError with available list."""
    with pytest.raises(ValueError, match="Unknown scenario"):
        run_scenario_analysis("nonexistent_scenario")


def test_equity_crash_dominated_by_beta():
    """Equity crash has no sector overrides → portfolio P&L ≈ portfolio beta * market move."""
    result = run_scenario_analysis("equity_crash_-20%")
    # -20% market × portfolio beta ~1.06 = ~-21.2%; allow generous tolerance for live data drift.
    assert -25.0 < result["total_pnl_pct"] < -18.0
    assert result["total_pnl_usd"] < 0