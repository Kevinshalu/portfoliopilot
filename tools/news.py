"""
Tool 4: Holdings News Summarization

For each ticker in the portfolio, pulls recent news headlines via yfinance,
then asks GPT-4o-mini to produce structured summaries: per-ticker sentiment +
key themes + one-line takeaway, plus cross-portfolio themes.

Used by the PortfolioPilot agent for "what's the news on my book?" queries.

Uses OpenAI structured outputs (parse() with a Pydantic schema) for typed,
reliable JSON instead of free-form text.
"""

from __future__ import annotations

import os
from typing import Any, Literal

import yfinance as yf
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

from tools.holdings import get_portfolio_holdings


load_dotenv()
_client = OpenAI()  # reads OPENAI_API_KEY from environment

MODEL = "gpt-4o-mini"
MAX_HEADLINES_PER_TICKER = 5


class TickerNewsSummary(BaseModel):
    ticker: str
    sentiment: Literal["positive", "neutral", "negative", "mixed"]
    key_themes: list[str] = Field(description="2-4 short theme phrases")
    one_line_takeaway: str


class PortfolioNewsResponse(BaseModel):
    per_ticker: list[TickerNewsSummary]
    cross_portfolio_themes: list[str] = Field(
        description="2-4 themes that appear across multiple holdings"
    )


def _fetch_headlines(ticker: str) -> list[dict[str, str]]:
    """Pull recent news for one ticker via yfinance."""
    raw = yf.Ticker(ticker).news or []
    headlines = []
    for item in raw[:MAX_HEADLINES_PER_TICKER]:
        # yfinance changed its news shape across versions: newer versions wrap
        # everything inside a "content" dict, older versions had flat fields.
        content = item.get("content", item)
        title = content.get("title")
        publisher = (
            content.get("provider", {}).get("displayName")
            if isinstance(content.get("provider"), dict)
            else content.get("publisher")
        )
        if not title:
            continue
        headlines.append({
            "title": title,
            "publisher": publisher or "Unknown",
        })
    return headlines


def _summarize_with_llm(headlines_by_ticker: dict[str, list[dict[str, str]]]) -> PortfolioNewsResponse:
    """Send all headlines to GPT-4o-mini in one structured-output call."""
    # Build a compact prompt: one block per ticker, headlines as bullets.
    blocks = []
    for ticker, headlines in headlines_by_ticker.items():
        if not headlines:
            continue
        lines = [f"## {ticker}"]
        for h in headlines:
            lines.append(f"- [{h['publisher']}] {h['title']}")
        blocks.append("\n".join(lines))
    news_text = "\n\n".join(blocks)

    system = (
        "You are an equity research assistant for a portfolio manager. "
        "Given recent news headlines per ticker, produce structured summaries: "
        "for each ticker, infer overall sentiment, identify 2-4 short key themes, "
        "and write a one-line takeaway a PM can read in 3 seconds. "
        "Then list 2-4 cross-portfolio themes that recur across multiple tickers. "
        "Be concise. Do not invent facts not in the headlines."
    )

    response = _client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Recent headlines:\n\n{news_text}"},
        ],
        response_format=PortfolioNewsResponse,
        temperature=0.2,
    )
    return response.choices[0].message.parsed


def summarize_holdings_news(tickers: list[str] | None = None) -> dict[str, Any]:
    """Public entry point: fetch + summarize news for portfolio holdings."""
    portfolio = get_portfolio_holdings()
    holding_tickers = [h["ticker"] for h in portfolio["holdings"]]
    target_tickers = tickers or holding_tickers

    headlines_by_ticker = {t: _fetch_headlines(t) for t in target_tickers}
    tickers_with_news = [t for t, hs in headlines_by_ticker.items() if hs]

    if not tickers_with_news:
        return {
            "per_ticker": [],
            "cross_portfolio_themes": [],
            "summary": "No recent news found for the requested tickers.",
        }

    parsed = _summarize_with_llm(headlines_by_ticker)

    per_ticker = [s.model_dump() for s in parsed.per_ticker]
    cross_themes = parsed.cross_portfolio_themes

    # Headline summary: count of names with news + dominant sentiment
    sentiment_counts: dict[str, int] = {}
    for s in per_ticker:
        sentiment_counts[s["sentiment"]] = sentiment_counts.get(s["sentiment"], 0) + 1
    dominant = max(sentiment_counts.items(), key=lambda kv: kv[1])[0] if sentiment_counts else "neutral"

    summary = (
        f"News across {len(per_ticker)} holdings: {dominant} skew "
        f"({sentiment_counts}). "
        f"Cross-portfolio themes: {'; '.join(cross_themes) if cross_themes else 'none identified'}."
    )

    return {
        "per_ticker": per_ticker,
        "cross_portfolio_themes": cross_themes,
        "summary": summary,
    }


if __name__ == "__main__":
    result = summarize_holdings_news()
    print(result["summary"])
    for s in result["per_ticker"][:3]:
        print(f"\n{s['ticker']} ({s['sentiment']}): {s['one_line_takeaway']}")
        print(f"  Themes: {', '.join(s['key_themes'])}")