"""
Tool 2: Portfolio Risk Metrics

Computes portfolio-level risk: beta vs S&P 500, annualized volatility,
parametric 1-day 95% VaR, factor exposures (value/momentum/quality/low-vol),
and concentration metrics.

Used by the PortfolioPilot agent for risk-decomposition queries.

Data sources:
- Holdings + weights: tools.holdings.get_portfolio_holdings()
- Historical prices: yfinance (1y daily)
- Factor proxies: VLUE (value), MTUM (momentum), QUAL (quality), USMV (low-vol)
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import yfinance as yf

from tools.holdings import get_portfolio_holdings


SPY = "SPY"
FACTOR_ETFS = {
    "value": "VLUE",
    "momentum": "MTUM",
    "quality": "QUAL",
    "low_volatility": "USMV",
}
TRADING_DAYS = 252
VAR_Z_95 = 1.645  # one-tailed 95% z-score


def _fetch_daily_returns(tickers: list[str], period: str = "1y") -> pd.DataFrame:
    """Download adjusted-close daily returns for the given tickers."""
    prices = yf.download(
        tickers,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )["Close"]

    # yfinance returns a Series for one ticker, a DataFrame for many.
    # Normalize to DataFrame so downstream code is uniform.
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])

    returns = prices.pct_change().dropna(how="all")
    return returns


def _portfolio_beta(holdings: list[dict[str, Any]]) -> float:
    """Weighted average of each holding's beta (vs S&P 500)."""
    total_weight = sum(h["weight_pct"] for h in holdings if h.get("beta") is not None)
    if total_weight == 0:
        return float("nan")
    weighted = sum(
        h["beta"] * h["weight_pct"]
        for h in holdings
        if h.get("beta") is not None
    )
    return round(weighted / total_weight, 3)


def _vol_and_var(
    returns: pd.DataFrame,
    weights: pd.Series,
    total_value: float,
) -> dict[str, float]:
    """Annualized portfolio vol and parametric 1-day 95% VaR (USD)."""
    # Align weights to the columns we actually have returns for
    aligned_weights = weights.reindex(returns.columns).fillna(0)
    aligned_weights = aligned_weights / aligned_weights.sum()  # renormalize

    # Daily portfolio returns = weighted sum of daily stock returns
    port_daily_returns = returns.dot(aligned_weights)

    daily_vol = port_daily_returns.std()
    annual_vol = daily_vol * np.sqrt(TRADING_DAYS)
    var_dollars = VAR_Z_95 * daily_vol * total_value

    return {
        "annualized_volatility_pct": round(100 * annual_vol, 2),
        "var_95_1d_usd": round(var_dollars, 2),
        "var_95_1d_pct": round(100 * VAR_Z_95 * daily_vol, 2),
    }


def _factor_exposures(port_returns: pd.Series) -> dict[str, float]:
    """OLS betas of portfolio returns on each factor ETF's returns."""
    factor_returns = _fetch_daily_returns(list(FACTOR_ETFS.values()))

    # Align dates: keep only days where both portfolio and factors have data
    aligned = factor_returns.join(port_returns.rename("portfolio"), how="inner").dropna()
    y = aligned["portfolio"]
    X = aligned[list(FACTOR_ETFS.values())]

    # OLS: beta = (X'X)^-1 X'y. We run 4 univariate regressions (one per factor)
    # rather than a multivariate regression, because the factor ETFs are highly
    # correlated and multivariate coefficients become unstable / hard to interpret.
    exposures = {}
    for factor_name, etf in FACTOR_ETFS.items():
        cov = np.cov(X[etf], y, ddof=1)[0, 1]
        var = np.var(X[etf], ddof=1)
        beta = cov / var if var > 0 else float("nan")
        exposures[factor_name] = round(beta, 3)
    return exposures


def _concentration(holdings: list[dict[str, Any]]) -> dict[str, float]:
    """Top-5 weight, max position, Herfindahl index."""
    weights = sorted((h["weight_pct"] for h in holdings), reverse=True)
    top_5_weight = sum(weights[:5])
    max_position = weights[0] if weights else 0.0
    # Herfindahl: sum of squared weights (using fractions, not percents).
    # 1/N for an equal-weight portfolio, 1.0 for a single holding.
    herfindahl = sum((w / 100) ** 2 for w in weights)
    return {
        "top_5_weight_pct": round(top_5_weight, 2),
        "max_position_pct": round(max_position, 2),
        "herfindahl_index": round(herfindahl, 4),
        "effective_n_holdings": round(1 / herfindahl, 1) if herfindahl > 0 else 0,
    }


def calculate_risk_metrics() -> dict[str, Any]:
    """
    Compute portfolio-level risk metrics for the current sample portfolio.

    Returns:
        Dict with beta, volatility, var_95_1d, factor_exposures,
        concentration, and a natural-language summary.
    """
    portfolio = get_portfolio_holdings()
    holdings = portfolio["holdings"]
    total_value = portfolio["total_value"]

    tickers = [h["ticker"] for h in holdings]
    weights = pd.Series({h["ticker"]: h["weight_pct"] / 100 for h in holdings})

    returns = _fetch_daily_returns(tickers)
    aligned_weights = weights.reindex(returns.columns).fillna(0)
    aligned_weights = aligned_weights / aligned_weights.sum()
    port_daily_returns = returns.dot(aligned_weights)

    beta = _portfolio_beta(holdings)
    vol_var = _vol_and_var(returns, weights, total_value)
    factors = _factor_exposures(port_daily_returns)
    concentration = _concentration(holdings)

    # Cast numpy scalars to native Python floats so JSON serialization
    # (used when the agent passes this result through the LLM) works cleanly.
    vol_var = {k: float(v) for k, v in vol_var.items()}
    factors = {k: float(v) for k, v in factors.items()}

    top_factor = max(factors.items(), key=lambda kv: kv[1])
    summary = (
        f"Portfolio beta {beta} vs S&P 500. "
        f"Annualized volatility {vol_var['annualized_volatility_pct']}%, "
        f"1-day 95% VaR ${vol_var['var_95_1d_usd']:,.0f} "
        f"({vol_var['var_95_1d_pct']}%). "
        f"Strongest factor tilt: {top_factor[0]} ({top_factor[1]:.2f}). "
        f"Effective holdings: {concentration['effective_n_holdings']} "
        f"(top 5 = {concentration['top_5_weight_pct']}% of book)."
    )

    return {
        "portfolio_beta": beta,
        "volatility_and_var": vol_var,
        "factor_exposures": factors,
        "concentration": concentration,
        "summary": summary,
    }


if __name__ == "__main__":
    result = calculate_risk_metrics()
    print(result["summary"])
    print(f"\nBeta: {result['portfolio_beta']}")
    print(f"Volatility & VaR: {result['volatility_and_var']}")
    print(f"Factor exposures: {result['factor_exposures']}")
    print(f"Concentration: {result['concentration']}")