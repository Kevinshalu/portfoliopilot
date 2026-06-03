"""
Tool 4: Holdings News Summarization — TO BE IMPLEMENTED ON DAY 3

Pulls recent news for portfolio holdings and uses GPT-4o-mini to produce
structured summaries with sentiment + key themes.

Data sources:
- yfinance.Ticker(ticker).news (free, 5-10 headlines per ticker)
- LLM: GPT-4o-mini with structured output schema
"""

from __future__ import annotations

from typing import Any


def summarize_holdings_news(
    tickers: list[str],
    days_lookback: int = 7,
    summary_depth: str = "brief",
) -> dict[str, Any]:
    """
    Pull and summarize recent news for given tickers.

    Args:
        tickers: List of tickers to pull news for
        days_lookback: How far back to look (default: 7 days)
        summary_depth: "brief" (1-2 sentences) or "detailed" (paragraph per ticker)

    Returns:
        Dict with summaries (list of per-ticker dicts with sentiment, themes, summary).
    """
    # TODO Day 3: implement
    raise NotImplementedError("Day 3 implementation pending")
