"""
Tool 5: Anomaly Detection — TO BE IMPLEMENTED ON DAY 4

Identifies positions that need attention based on:
- Unusual price moves (z-score > threshold)
- Volume spikes (z-score > threshold)
- Volatility regime changes
- LLM-generated "potential cause" using recent news

Data sources:
- yfinance historical price/volume
- yfinance.news for context
- Statistical analysis: scipy + numpy
"""

from __future__ import annotations

from typing import Any


def flag_anomalies(
    time_window: str = "1d",
    threshold_z_score: float = 2.0,
) -> dict[str, Any]:
    """
    Detect positions with unusual recent activity.

    Args:
        time_window: "1d" for daily anomalies, "1w" for weekly
        threshold_z_score: Standard deviations from mean to flag (default: 2.0)

    Returns:
        Dict with anomalies list (per-position dicts with type, magnitude, z_score,
        potential_cause, recommended_action) and summary.
    """
    # TODO Day 4: implement
    raise NotImplementedError("Day 4 implementation pending")
