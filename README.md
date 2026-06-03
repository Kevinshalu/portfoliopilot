# PortfolioPilot

> Agentic AI prototype for portfolio managers — natural-language interface, multi-tool LLM agent for risk decomposition, scenario analysis, news synthesis, and pre-market intelligence.

🚧 **Status: In active development (Day 1 of 7-day build, June 1 2026)** 🚧

---

## What it is

A working prototype demonstrating the agentic AI patterns enterprise asset managers are productizing for portfolio managers. A user types natural-language questions; a GPT-4o-mini agent (LangGraph ReAct pattern) autonomously selects and sequences 5 specialized analytical tools to answer.

**Example queries:**
- *"What's my biggest concentration risk and how do I reduce it?"*
- *"Run a rate shock scenario — what if 10-year yields rise 100bps?"*
- *"Summarize the latest news on my top 5 holdings"*
- *"Which positions need my attention before market open?"*

## Tech stack

- **LLM:** GPT-4o-mini (OpenAI)
- **Agent framework:** LangGraph (ReAct pattern)
- **Backend:** FastAPI with SSE streaming
- **Frontend:** Streamlit
- **Data:** yfinance (public market data) + sample portfolio JSON

## The 5 agent tools

| # | Tool | Status |
|---|---|---|
| 1 | `get_portfolio_holdings()` — Returns holdings with sector/weight breakdown | ✅ Day 1 (live) |
| 2 | `calculate_risk_metrics()` — Beta, factor exposure, VaR, concentration | ⏳ Day 2 |
| 3 | `run_scenario_analysis()` — Rate/equity/commodity shock stress tests | ⏳ Day 3 |
| 4 | `summarize_holdings_news()` — LLM-summarized news per holding | ⏳ Day 3 |
| 5 | `flag_anomalies()` — Z-score-based price/volume anomaly detection | ⏳ Day 4 |

## Architecture

```
User (Portfolio Manager)
    │
    ▼
Streamlit Dashboard (3-panel: holdings, chat, output)
    │
    ▼ HTTP / SSE
FastAPI Backend
    │
    ▼
LangGraph ReAct Agent (GPT-4o-mini)
    │
    ├─ Tool 1: get_portfolio_holdings
    ├─ Tool 2: calculate_risk_metrics
    ├─ Tool 3: run_scenario_analysis
    ├─ Tool 4: summarize_holdings_news
    └─ Tool 5: flag_anomalies
         │
         ▼
Data: yfinance (live prices/news) + sample_portfolio.json + Fama-French factors
```

## Quick start

```bash
# Clone
git clone https://github.com/Kevinshalu/portfoliopilot.git
cd portfoliopilot

# Set up environment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure secrets
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Smoke test Tool 1
python tools/holdings.py

# Run backend (once Days 4-5 complete)
uvicorn backend.main:app --reload --port 8000

# Run frontend (once Day 5 complete)
streamlit run frontend/app.py
```

## Key design decisions

See `docs/design-decisions.md` for the full reasoning behind:
- Why LangGraph ReAct vs OpenAI Assistants API
- Why GPT-4o-mini vs GPT-4o for the demo
- Why Streamlit vs Next.js/React
- Why yfinance vs Bloomberg/Refinitiv
- Why a simplified factor model vs production-grade

## Eval framework

PortfolioPilot ships with a 10-query golden dataset and automated evals checking:
- Tool selection accuracy
- Numerical output accuracy
- Output structure correctness
- Hallucination rate

Run evals: `python evals/eval_suite.py`

Results auto-logged to `evals/results/`.

## Limitations (honest disclosure)

This is a portfolio demonstration, not a production system. See `docs/limitations.md` for the full discussion. Highlights:
- Sample portfolio of 10 stocks; production handles 100s-1000s
- Simplified risk model; production uses proprietary 50+ factor models
- 15-min delayed market data via yfinance
- No persistent session memory across queries
- No compliance-aware filtering (no MNPI screening)

## About

Built by **Kevin Shalu**, NYU MS Management of Technology '26 + B.Tech Electrical & Electronics Engineering. Daily user of AI-enabled coding agents (Claude Code, Cursor, GitHub Copilot).

**Other production AI projects:**
- [FinRisk Copilot](https://github.com/Kevinshalu/fraud-analyst-agent) — GenAI agent for fraud investigation

**LinkedIn:** [linkedin.com/in/kevinshalu](https://linkedin.com/in/kevinshalu)

---

*This is a portfolio piece demonstrating agentic AI patterns applicable to enterprise asset management. Not affiliated with, endorsed by, or representing any financial institution. Sample portfolio and analysis are illustrative only — not investment advice.*
