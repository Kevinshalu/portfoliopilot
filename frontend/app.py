"""
PortfolioPilot Streamlit dashboard.

Three-panel layout:
  Left   - current portfolio holdings table (live, 60s cached)
  Middle - free-text query input + 5 sample-query buttons
  Right  - agent response + tools called

Run locally (requires backend on :8000):
    streamlit run frontend/app.py
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os

import httpx
import pandas as pd
import streamlit as st


API_URL = os.getenv("PORTFOLIOPILOT_API", "http://localhost:8000")
SAMPLE_QUERIES = [
    "What's in my portfolio?",
    "What's the risk?",
    "What happens if the Fed hikes rates 100bps?",
    "What's the news on my holdings?",
    "Anything weird in my book this week?",
]


# --- Page config ----------------------------------------------------------
st.set_page_config(page_title="PortfolioPilot", layout="wide")
st.title("PortfolioPilot")
st.caption("Agentic AI assistant for portfolio managers — prototype")


# --- Backend client + cached portfolio fetch ------------------------------
def call_agent(query: str) -> dict:
    response = httpx.post(f"{API_URL}/query", json={"query": query}, timeout=120)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=60)
def fetch_holdings() -> dict:
    """Cache holdings for 60s so reruns do not hammer yfinance."""
    from tools.holdings import get_portfolio_holdings
    return get_portfolio_holdings()


# --- Session state --------------------------------------------------------
# active_query stores the query to run on the next render. Set by either
# the Send button or a sample-query button; cleared after the agent runs.
if "active_query" not in st.session_state:
    st.session_state.active_query = ""


# --- Layout ---------------------------------------------------------------
left, middle, right = st.columns([1.2, 1.3, 1.6])

# Left panel: holdings ----------------------------------------------------
with left:
    st.subheader("Holdings")
    portfolio = fetch_holdings()
    df = pd.DataFrame(portfolio["holdings"])[
        ["ticker", "sector", "weight_pct", "market_value"]
    ].rename(columns={
        "ticker": "Ticker",
        "sector": "Sector",
        "weight_pct": "Weight %",
        "market_value": "Market Value",
    })
    st.dataframe(df, use_container_width=True, hide_index=True)
    c1, c2 = st.columns(2)
    c1.metric("Total value", f"${portfolio['total_value']:,.0f}")
    c2.metric("Holdings", portfolio["holdings_count"])

# Middle panel: query input ----------------------------------------------
with middle:
    st.subheader("Ask PortfolioPilot")
    typed = st.text_area(
        "Question",
        placeholder="e.g., 'What's the risk in my portfolio?'",
        height=100,
        label_visibility="collapsed",
    )
    if st.button("Send", type="primary", use_container_width=True):
        st.session_state.active_query = typed.strip()

    st.write("Or try a sample query:")
    for sample in SAMPLE_QUERIES:
        if st.button(sample, key=f"sample_{sample}", use_container_width=True):
            st.session_state.active_query = sample

# Right panel: agent answer ----------------------------------------------
with right:
    st.subheader("Answer")
    if st.session_state.active_query:
        st.markdown(f"**Q:** {st.session_state.active_query}")
        with st.spinner("PortfolioPilot is thinking..."):
            try:
                result = call_agent(st.session_state.active_query)
            except Exception as e:
                st.error(f"Agent error: {e}")
                st.session_state.active_query = ""
            else:
                st.markdown(result["final_answer"])
                tools = result.get("tools_called") or []
                st.caption(f"Tools used: {', '.join(tools) if tools else 'none'}")
                st.session_state.active_query = ""
    else:
        st.info("Submit a question or click a sample query.")