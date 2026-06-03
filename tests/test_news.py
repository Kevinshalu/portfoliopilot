"""Smoke tests for Tool 4: news."""
from unittest.mock import patch

from tools.news import (
    PortfolioNewsResponse,
    TickerNewsSummary,
    _fetch_headlines,
    summarize_holdings_news,
)


def test_fetch_headlines_returns_titles():
    """yfinance should return at least one well-shaped headline for a major name."""
    headlines = _fetch_headlines("AAPL")
    assert len(headlines) > 0
    assert all("title" in h and "publisher" in h for h in headlines)
    assert all(isinstance(h["title"], str) and len(h["title"]) > 5 for h in headlines)


def test_summarize_empty_short_circuits():
    """If no holding has news, summarize_holdings_news returns the empty-case payload without calling the LLM."""
    with patch("tools.news._fetch_headlines", return_value=[]):
        result = summarize_holdings_news(tickers=["AAPL"])
    assert result["per_ticker"] == []
    assert result["cross_portfolio_themes"] == []
    assert "No recent news" in result["summary"]


def test_summarize_pipeline_with_mocked_llm():
    """Full pipeline with a stubbed LLM response: shape + summary line should be correct."""
    fake_parsed = PortfolioNewsResponse(
        per_ticker=[
            TickerNewsSummary(
                ticker="AAPL",
                sentiment="positive",
                key_themes=["new product", "AI strategy"],
                one_line_takeaway="Apple launches new AI features.",
            ),
        ],
        cross_portfolio_themes=["AI adoption"],
    )
    with patch("tools.news._summarize_with_llm", return_value=fake_parsed):
        result = summarize_holdings_news(tickers=["AAPL"])
    assert result["per_ticker"][0]["ticker"] == "AAPL"
    assert result["per_ticker"][0]["sentiment"] == "positive"
    assert "AI adoption" in result["cross_portfolio_themes"]
    assert "positive skew" in result["summary"]