"""
Tool 2: Risk Metrics — TO BE IMPLEMENTED ON DAY 2

Calculates risk decomposition for the portfolio:
- Portfolio beta (vs S&P 500)
- Annualized volatility
- Value-at-Risk (95% confidence, 1-day, parametric)
- Factor exposures (simplified — beta to value/growth/momentum ETFs as proxy)
- Concentration metrics (top 5, single max, Herfindahl index)

Data sources:
- Historical returns from yfinance
- Factor proxies: VLUE (value), MTUM (momentum), QUAL (quality), USMV (low-vol)
"""

from __future__ import annotations

from typing import Any


def calculate_risk_metrics(
    tickers: list[str] | None = None,
    time_horizon_days: int = 252,
) -> dict[str, Any]:
    """
    Calculate risk metrics for the portfolio or a subset.

    Args:
        tickers: Optional list of tickers to scope to. If None, uses entire portfolio.
        time_horizon_days: Lookback window for historical analysis (default: 252 trading days = 1 year).

    Returns:
        Dict with portfolio_beta, annualized_volatility, var_95_1day_pct,
        factor_exposures, concentration_risk, and summary.
    """
    # TODO Day 2: implement
    # 1. Load portfolio holdings via tools.holdings.get_portfolio_holdings()
    # 2. Pull historical returns for each ticker + SPY (benchmark) via yfinance
    # 3. Compute weighted portfolio returns
    # 4. Calculate:
    #    - beta = cov(portfolio, SPY) / var(SPY)
    #    - annualized_volatility = std(daily_returns) * sqrt(252)
    #    - var_95_1day = 1.645 * daily_volatility (parametric, normal distribution)
    #    - factor exposures via regression on VLUE, MTUM, QUAL, USMV
    #    - concentration: top_5 weight sum, max single weight, Herfindahl
    # 5. Build natural-language summary
    raise NotImplementedError("Day 2 implementation pending")
