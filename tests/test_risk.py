"""Smoke tests for Tool 2: risk metrics."""
import pandas as pd

from tools.risk import (
    _concentration,
    _factor_exposures,
    _fetch_daily_returns,
    _portfolio_beta,
    _vol_and_var,
    calculate_risk_metrics,
)


def test_fetch_returns_shape():
    """Returns dataframe should have ~1y of daily rows and one col per ticker."""
    returns = _fetch_daily_returns(["AAPL", "MSFT", "SPY"])
    assert returns.shape[0] > 200  # at least 200 trading days
    assert set(returns.columns) == {"AAPL", "MSFT", "SPY"}
    assert returns.abs().max().max() < 0.5  # no single-day move > 50% (sanity)


def test_portfolio_beta_weighted_correctly():
    """Weighted average of betas should equal hand-computed value."""
    holdings = [
        {"ticker": "A", "beta": 1.5, "weight_pct": 60.0},
        {"ticker": "B", "beta": 0.5, "weight_pct": 40.0},
    ]
    # 0.6*1.5 + 0.4*0.5 = 1.1
    assert _portfolio_beta(holdings) == 1.1


def test_portfolio_beta_skips_missing():
    """Holdings with None beta should be excluded and weights renormalized."""
    holdings = [
        {"ticker": "A", "beta": 1.0, "weight_pct": 50.0},
        {"ticker": "B", "beta": None, "weight_pct": 50.0},
    ]
    # Only A counts; weighted average over included = 1.0
    assert _portfolio_beta(holdings) == 1.0


def test_concentration_math():
    """Top-5, max position, Herfindahl, and effective N should all be correct."""
    holdings = [{"ticker": f"T{i}", "weight_pct": 10.0} for i in range(10)]
    result = _concentration(holdings)
    assert result["top_5_weight_pct"] == 50.0
    assert result["max_position_pct"] == 10.0
    # Equal-weight 10 stocks: H = 10 * 0.1^2 = 0.10, effective N = 10
    assert result["herfindahl_index"] == 0.10
    assert result["effective_n_holdings"] == 10.0


def test_vol_and_var_signs():
    """Vol and VaR must be non-negative; pct values bounded sensibly."""
    returns = _fetch_daily_returns(["SPY"])
    weights = pd.Series({"SPY": 1.0})
    result = _vol_and_var(returns, weights, total_value=1_000_000)
    assert result["annualized_volatility_pct"] > 0
    assert result["var_95_1d_usd"] > 0
    assert 0 < result["var_95_1d_pct"] < 10  # SPY VaR shouldn't exceed 10%


def test_calculate_risk_metrics_end_to_end():
    """Top-level function returns the expected shape and a non-empty summary."""
    result = calculate_risk_metrics()
    assert "portfolio_beta" in result
    assert "volatility_and_var" in result
    assert "factor_exposures" in result
    assert "concentration" in result
    assert isinstance(result["summary"], str) and len(result["summary"]) > 50
    # Factor exposures dict should have all 4 named factors
    assert set(result["factor_exposures"].keys()) == {
        "value", "momentum", "quality", "low_volatility",
    }