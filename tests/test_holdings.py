"""Smoke tests for Tool 1: holdings."""
from tools.holdings import get_portfolio_holdings


def test_returns_holdings():
    result = get_portfolio_holdings()
    assert "holdings" in result
    assert "total_value" in result
    assert result["holdings_count"] == 10


def test_sector_filter():
    result = get_portfolio_holdings(sectors=["Financials"])
    assert all(h["sector"] == "Financials" for h in result["holdings"])
    assert result["holdings_count"] == 2  # JPM + GS


def test_weights_sum_to_100():
    result = get_portfolio_holdings()
    total_weight = sum(h["weight_pct"] for h in result["holdings"])
    assert 99.5 < total_weight < 100.5  # within rounding tolerance
