"""Smoke tests for the LangGraph agent."""
from agent.portfoliopilot_agent import TOOLS, run_query


def test_tool_inventory():
    """All 5 tools should be registered with their expected names."""
    names = {t.name for t in TOOLS}
    assert names == {
        "get_portfolio_holdings",
        "calculate_risk_metrics",
        "run_scenario_analysis",
        "summarize_holdings_news",
        "flag_anomalies",
    }


def test_agent_routes_holdings_query():
    """A composition question should trigger get_portfolio_holdings (live LLM call)."""
    result = run_query("What are my portfolio holdings?")
    assert "final_answer" in result
    assert isinstance(result["final_answer"], str)
    assert len(result["final_answer"]) > 20
    assert "get_portfolio_holdings" in result["tools_called"]