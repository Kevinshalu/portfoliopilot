"""
Tool 5: Pre-Market Anomaly Detection

For each ticker in the portfolio, computes z-scores over the last few days
on three signals (daily return, volume, intraday range) against a rolling
baseline. Flags anything beyond a configurable z-threshold.

Used by the PortfolioPilot agent for "what's weird in my book?" queries.

Methodology:
    baseline window: last `baseline_days` excluding the most recent `window_days`
    z = (recent_value - baseline_mean) / baseline_std
    flag if |z| > z_threshold (default 2.0)
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import yfinance as yf

from tools.holdings import get_portfolio_holdings


BASELINE_DAYS = 60
WINDOW_DAYS = 5
Z_THRESHOLD = 2.0


def _fetch_price_volume(ticker: str, total_days: int) -> pd.DataFrame:
    """Pull OHLCV for one ticker, ~total_days of daily bars."""
    # Add ~30 calendar-day buffer to make sure we get enough trading days.
    period = f"{total_days + 30}d"
    df = yf.download(
        ticker,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )
    # yfinance returns a MultiIndex column when given a single ticker in
    # some versions; flatten it so column access is uniform.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df[["Open", "High", "Low", "Close", "Volume"]].dropna()


def _compute_zscores(df: pd.DataFrame, baseline_days: int, window_days: int) -> pd.DataFrame:
    """Return a (window_days × 3) frame of z-scores for return, volume, range."""
    # Build the three signal series from raw OHLCV
    daily_return = df["Close"].pct_change()
    volume = df["Volume"]
    intraday_range = (df["High"] - df["Low"]) / df["Close"]

    signals = pd.DataFrame({
        "return": daily_return,
        "volume": volume,
        "range": intraday_range,
    }).dropna()

    if len(signals) < baseline_days + window_days:
        return pd.DataFrame()  # not enough data; caller will skip

    baseline = signals.iloc[-(baseline_days + window_days):-window_days]
    recent = signals.iloc[-window_days:]

    mean = baseline.mean()
    std = baseline.std(ddof=1).replace(0, np.nan)  # avoid div-by-zero
    zscores = (recent - mean) / std
    return zscores


def flag_anomalies(
    baseline_days: int = BASELINE_DAYS,
    window_days: int = WINDOW_DAYS,
    z_threshold: float = Z_THRESHOLD,
) -> dict[str, Any]:
    """Detect anomalies across the portfolio's holdings."""
    portfolio = get_portfolio_holdings()
    tickers = [h["ticker"] for h in portfolio["holdings"]]

    anomalies: list[dict[str, Any]] = []
    total_days_needed = baseline_days + window_days

    for ticker in tickers:
        df = _fetch_price_volume(ticker, total_days_needed)
        zscores = _compute_zscores(df, baseline_days, window_days)
        if zscores.empty:
            continue

        # Reconstruct the underlying values so the output is interpretable
        recent_returns = df["Close"].pct_change().iloc[-window_days:]
        recent_volume = df["Volume"].iloc[-window_days:]
        recent_range = ((df["High"] - df["Low"]) / df["Close"]).iloc[-window_days:]

        for date, row in zscores.iterrows():
            for signal in ("return", "volume", "range"):
                z = row[signal]
                if pd.isna(z) or abs(z) < z_threshold:
                    continue
                value_lookup = {
                    "return": recent_returns.loc[date],
                    "volume": recent_volume.loc[date],
                    "range": recent_range.loc[date],
                }
                anomalies.append({
                    "ticker": ticker,
                    "date": date.strftime("%Y-%m-%d"),
                    "signal": signal,
                    "z_score": round(float(z), 2),
                    "value": round(float(value_lookup[signal]), 4),
                })

    # Sort by |z| descending — biggest weirdness first
    anomalies.sort(key=lambda a: abs(a["z_score"]), reverse=True)

    summary = (
        f"Scanned {len(tickers)} holdings over last {window_days} days "
        f"(baseline {baseline_days}d, z>{z_threshold}). "
        f"Flagged {len(anomalies)} anomalies."
    )
    if anomalies:
        top = anomalies[0]
        summary += (
            f" Most extreme: {top['ticker']} {top['signal']} z={top['z_score']:+.2f} "
            f"on {top['date']}."
        )

    return {
        "anomalies": anomalies,
        "anomalies_count": len(anomalies),
        "scanned_tickers": tickers,
        "summary": summary,
    }


if __name__ == "__main__":
    result = flag_anomalies()
    print(result["summary"])
    for a in result["anomalies"][:10]:
        print(
            f"  {a['date']}  {a['ticker']:5s}  "
            f"{a['signal']:7s}  z={a['z_score']:+.2f}  value={a['value']:+.4f}"
        )