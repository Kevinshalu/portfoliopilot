"""
PortfolioPilot Agent

LangGraph ReAct agent wrapping the 5 portfolio-analysis tools.
The agent autonomously selects which tools to call based on the user's question.
"""

from __future__ import annotations

from typing import Any

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from tools.anomalies import flag_anomalies as _flag_anomalies
from tools.holdings import get_portfolio_holdings as _get_holdings
from tools.news import summarize_holdings_news as _summarize_news
from tools.risk import calculate_risk_metrics as _calc_risk
from tools.scenarios import run_scenario_analysis as _run_scenario


load_dotenv()
MODEL = "gpt-4o-mini"


# --- Tool wrappers --------------------------------------------------------
# Each @tool wrapper exposes the underlying function to the LLM with a
# clear docstring (becomes the tool description) and type-hinted args
# (auto-converted to JSON schema). Keep wrapper bodies trivial: they
# exist for the LLM-facing surface, not for logic.

@tool
def get_portfolio_holdings(
    sectors: list[str] | None = None,
    min_position_weight_pct: float | None = None,
) -> dict[str, Any]:
    """Return current portfolio holdings with live prices, weights, sector
    breakdown, and per-holding beta and dividend yield. Optionally filter by
    sector list or minimum position weight (%)."""
    return _get_holdings(sectors=sectors, min_position_weight_pct=min_position_weight_pct)


@tool
def calculate_risk_metrics() -> dict[str, Any]:
    """Compute portfolio risk: beta vs S&P 500, annualized volatility,
    parametric 1-day 95% VaR (USD and %), factor exposures (value, momentum,
    quality, low-volatility), and concentration metrics (top-5 weight,
    max position, Herfindahl, effective N)."""
    return _calc_risk()


@tool
def run_scenario_analysis(scenario_name: str) -> dict[str, Any]:
    """Apply a predefined market scenario and return P&L per holding plus
    portfolio total. Available scenario_name values:
    'rate_shock_+100bps', 'equity_crash_-20%', 'oil_shock_+30%'."""
    return _run_scenario(scenario_name)


@tool
def summarize_holdings_news(tickers: list[str] | None = None) -> dict[str, Any]:
    """Summarize recent news for portfolio holdings: per-ticker sentiment,
    key themes, one-line takeaway, plus cross-portfolio themes.
    Pass tickers to restrict; default summarizes all holdings."""
    return _summarize_news(tickers=tickers)


@tool
def flag_anomalies(
    baseline_days: int = 60,
    window_days: int = 5,
    z_threshold: float = 2.0,
) -> dict[str, Any]:
    """Detect unusual moves in portfolio holdings using z-scores on daily
    return, volume, and intraday range over the last `window_days` against
    a `baseline_days` baseline. Flag anything with |z| > z_threshold."""
    return _flag_anomalies(
        baseline_days=baseline_days,
        window_days=window_days,
        z_threshold=z_threshold,
    )


TOOLS = [
    get_portfolio_holdings,
    calculate_risk_metrics,
    run_scenario_analysis,
    summarize_holdings_news,
    flag_anomalies,
]


# --- System prompt --------------------------------------------------------

SYSTEM_PROMPT = """You are PortfolioPilot, an AI assistant for portfolio managers.

You have 5 tools that operate on the user's sample portfolio of 10 US large-cap stocks:
- get_portfolio_holdings: composition, weights, sector breakdown, live prices
- calculate_risk_metrics: beta, vol, VaR, factor exposures, concentration
- run_scenario_analysis: pre-defined stress scenarios
- summarize_holdings_news: recent news per ticker with sentiment + themes
- flag_anomalies: z-score-based detection of unusual price/volume/volatility moves

Rules:
1. Always call tools to get real data. Never fabricate numbers, prices, sentiment, or scenarios.
2. Use multiple tools when a question spans them. Example: "what's risky and why" → calculate_risk_metrics + flag_anomalies + summarize_holdings_news.
3. Be concise. Lead with the headline number, then a one-sentence explanation. PMs scan between meetings.
4. If a user asks for a scenario not in the available list, run the closest match and note the substitution.
5. Acknowledge limitations honestly when relevant: data has a ~15 minute delay, the portfolio is a 10-stock sample, risk methodology is prototype-grade.

Respond in clear plain English. No markdown headers in answers."""


# --- Agent factory + public entry point -----------------------------------

_agent = None


def _get_agent():
    """Lazy singleton — build the agent on first use and reuse it."""
    global _agent
    if _agent is None:
        llm = ChatOpenAI(model=MODEL, temperature=0.1)
        _agent = create_react_agent(llm, TOOLS, prompt=SYSTEM_PROMPT)
    return _agent


def run_query(query: str) -> dict[str, Any]:
    """Run one user question through the agent. Returns the final answer
    plus the list of tools the agent actually called (for evals + debugging)."""
    agent = _get_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    final = result["messages"][-1].content
    tools_called = [
        m.name for m in result["messages"]
        if getattr(m, "type", None) == "tool"
    ]
    return {
        "final_answer": final,
        "tools_called": tools_called,
    }


if __name__ == "__main__":
    queries = [
        "What's in my portfolio?",
        "What's the risk?",
        "What happens if rates spike 100bps?",
        "Anything weird in my book this week?",
    ]
    for q in queries:
        print(f"\n{'=' * 70}\nQ: {q}\n{'=' * 70}")
        result = run_query(q)
        print(result["final_answer"])
        print(f"\n[Tools: {result['tools_called']}]")