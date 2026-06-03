# PortfolioPilot

> Agentic AI assistant for portfolio managers — natural-language interface, multi-tool LLM agent for portfolio composition, risk decomposition, scenario analysis, news synthesis, and pre-market anomaly detection.

Built in a 2-day sprint to demonstrate the agentic-AI patterns that asset managers (BlackRock Aladdin AI, Bloomberg AI, Morgan Stanley AI@MS) are productizing for portfolio managers.

---

## What it does

A PM types natural-language questions in a browser. A GPT-4o-mini agent (LangGraph ReAct pattern) autonomously selects and sequences 5 specialized tools to answer:

| Tool | What it returns |
|---|---|
| `get_portfolio_holdings` | Holdings, weights, sector breakdown, live prices |
| `calculate_risk_metrics` | Beta vs S&P 500, annualized vol, parametric 1-day 95% VaR, factor exposures (value/momentum/quality/low-vol), concentration (top-5, max, Herfindahl, effective N) |
| `run_scenario_analysis` | P&L per holding under pre-defined shocks (rate +100bps, equity −20%, oil +30%) |
| `summarize_holdings_news` | Per-ticker sentiment + themes + one-line takeaway, plus cross-portfolio themes (GPT-4o-mini structured output) |
| `flag_anomalies` | Z-score-based flags on return / volume / intraday range over a configurable window |

**Sample queries the agent handles end-to-end:**
- *"What's my biggest concentration risk?"*
- *"What happens if the Fed hikes rates 100bps?"*
- *"Summarize the news on my holdings"*
- *"Anything weird in my book this week?"*

---

## Eval results

The project ships with a 10-query golden dataset and an automated eval suite. Numbers from the latest run:

| Metric | Score |
|---|---|
| Overall tool-selection accuracy | **90%** (9/10) |
| Single-tool accuracy | **100%** (9/9) |
| Multi-step accuracy | 0% (0/1) — see [limitations §6b](docs/limitations.md) |
| Substance coverage (keyword match) | **0.90** |
| Avg latency per query | 7.0s |
| Avg tools called per query | 1.3 |
| Errors | 0 |

The lone multi-step failure was surfaced **by the eval suite**, not glossed over. On *"Summarize news on my financial holdings and flag any risks,"* the agent correctly chains news + anomalies but misses the implicit "filter to Financials" sub-step. This is documented honestly in [`docs/limitations.md`](docs/limitations.md#6b-multi-step-orchestration-is-fragile-on-implicit-filters) with a v2 fix path.

Re-run with: `python -m evals.eval_suite`

---

## Architecture

```
User (Portfolio Manager)
    │
    ▼
Streamlit Dashboard (3-panel: holdings | query | answer)
    │
    ▼ HTTP (POST /query)
FastAPI Backend (Pydantic-validated; auto-generated /docs)
    │
    ▼
LangGraph ReAct Agent (GPT-4o-mini, temp 0.1)
    │
    ├─ get_portfolio_holdings   → yfinance + sample_portfolio.json
    ├─ calculate_risk_metrics   → yfinance 1y returns + factor ETFs
    ├─ run_scenario_analysis    → beta × market_move + sector overlay
    ├─ summarize_holdings_news  → yfinance.news + GPT-4o-mini parse()
    └─ flag_anomalies           → yfinance OHLCV + z-score
```

A diagram-quality version lives at [`docs/architecture.png`](docs/architecture.png) (built in excalidraw).

---

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| LLM | GPT-4o-mini | $0.15/M input tokens — cost-efficient demo; upgradeable to GPT-4o for production paths |
| Agent framework | LangGraph (ReAct, `create_react_agent`) | Explicit state, vendor-flexible, battle-tested loop |
| Backend | FastAPI + Pydantic | Standard for ML-backed APIs, auto OpenAPI docs |
| Frontend | Streamlit | Fast iteration; suitable for internal analytics tools |
| Data | yfinance (public, ~15min delay) | Reproducible by any reviewer; no proprietary data |
| Tests | pytest (23 tests, ~50s) | Mix of synthetic-math and live-integration |
| Deploy | Streamlit Community Cloud | Free public URL; GitHub integration |

See [`docs/design-decisions.md`](docs/design-decisions.md) for the full reasoning per choice.

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/Kevinshalu/portfoliopilot.git
cd portfoliopilot

# 2. Environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Secrets
cp .env.example .env
# Open .env and paste your OPENAI_API_KEY (sk-proj-...)

# 4. Run tests (proves everything works on your machine)
pytest -v

# 5. Run the eval suite (~2-4 min, ~$0.02)
python -m evals.eval_suite

# 6. Run the full app (two terminals)
# Terminal A
uvicorn backend.main:app --reload --port 8000
# Terminal B
streamlit run frontend/app.py
# → opens http://localhost:8501
```

---

## Repository layout

```
tools/                  # The 5 analytical tools (each runnable with `python -m tools.<name>`)
  holdings.py
  risk.py
  scenarios.py
  news.py
  anomalies.py
agent/
  portfoliopilot_agent.py  # LangGraph agent + @tool wrappers + system prompt
backend/
  main.py               # FastAPI: POST /query, GET /health
frontend/
  app.py                # Streamlit 3-panel dashboard
data/
  sample_portfolio.json # 10 S&P 500 holdings
evals/
  golden_dataset.json   # 10-query benchmark
  eval_suite.py         # Run + score + log
  results/              # Timestamped JSON of every eval run
tests/                  # 23 unit + integration tests
docs/
  design-decisions.md   # Per-layer rationale
  limitations.md        # 18 honest scope boundaries
  future-work.md        # v2 roadmap
  build-progress.md     # Day-by-day build log
  portfoliopilot-logbook.docx  # Full build narrative (each day: what, why, how, what we got)
```

---

## Key design decisions (TL;DR)

| Question | Choice | Rationale |
|---|---|---|
| ReAct framework? | LangGraph `create_react_agent` | Production-tested loop; we write zero loop code, only tool wrappers + system prompt |
| One LLM call for news or one per ticker? | One call across all tickers | Cheaper, and unlocks cross-portfolio theme detection a per-ticker loop can't do |
| Factor model? | 4 univariate OLS regressions on ETF proxies | Univariate avoids unstable multivariate coefficients on highly-correlated factor ETFs; documented simplification |
| VaR method? | Parametric (1.645σ × daily vol) | Honest prototype-grade; production would use historical-simulation or Monte Carlo |
| Streaming responses? | Deferred | SSE adds complexity without visible demo value; documented as future work |
| Live LLM in tests? | Only one (agent-routing) | Cost discipline; structured-output and structured-pipeline tests use mocks |

Full discussion in [`docs/design-decisions.md`](docs/design-decisions.md).

---

## Honest limitations

The full list (18 entries) lives in [`docs/limitations.md`](docs/limitations.md). Highlights:

- **Sample portfolio of 10 stocks** — production handles 100s–1000s
- **Simplified risk model** — production uses proprietary 50+ factor models with daily covariance updates
- **~15-minute delayed market data** via yfinance — production needs Bloomberg / Refinitiv / direct exchange
- **No persistent memory** across sessions
- **No MNPI screening, no audit log** — would block any production deployment in regulated finance
- **One known multi-step orchestration failure** — surfaced by our own eval suite, documented with v2 fix path

Documenting limitations honestly is the AI-PM signal: knowing the gap between prototype and production is the core skill.

---

## About

Built by **[Kevin Shalu](https://linkedin.com/in/kevinshalu)** — NYU MS Management of Technology '26, B.Tech Electrical & Electronics Engineering. Career target: AI Product Manager in financial services. Daily user of AI-enabled coding agents (Claude Code, Cursor, GitHub Copilot).

**Other agentic AI work:**
- [FinRisk Copilot](https://github.com/Kevinshalu/fraud-analyst-agent) — LangGraph + GPT-4o agent for fraud investigation

---

*This is a portfolio piece demonstrating agentic AI patterns applicable to enterprise asset management. Not affiliated with, endorsed by, or representing any financial institution. Sample portfolio and analysis are illustrative only — not investment advice.*
