# PortfolioPilot — Project Context for Claude

## What this project is

PortfolioPilot is an agentic AI prototype for portfolio managers. It demonstrates the kind of natural-language, multi-tool LLM agent pattern that BlackRock Aladdin AI, Bloomberg AI, and Morgan Stanley AI@MS are productizing.

A portfolio manager types questions in natural language. A GPT-4o-mini agent (LangGraph ReAct pattern) autonomously selects and sequences 5 specialized tools to answer:
- Portfolio composition queries
- Risk decomposition (beta, factor exposures, VaR, concentration)
- Scenario analysis (rate shocks, equity drawdowns, commodity shocks)
- News summarization for holdings
- Pre-market anomaly detection

## Why this project exists

**Primary purpose:** Differentiate Kevin's BlackRock Aladdin AI PM Associate application (Job R263783, submitted May 30 2026). The role asks for builders who ship agentic AI in regulated financial services contexts — this project is concrete proof of capability.

**Secondary purpose:** Become the headline portfolio piece for every AI PM application going forward (Morgan Stanley AI PM, Google AI roles, future opportunities).

**Tertiary purpose:** Serve as Kevin's Week 1 "applied case study" for the Morgan Stanley AI PM interview playbook (see related docs). The act of building this project IS the foundational AI PM concept work the playbook requires.

## Who Kevin is (for context)

- NYU MS Management of Technology graduate, May 2026, GPA 3.71
- B.Tech Electrical & Electronics Engineering, GPA 3.98
- 2 years prior at IBM Consulting Bangalore (healthcare insurance analytics + transformation programs)
- Career target: AI Product Manager in financial services / healthcare / fintech
- Already shipped one production agentic AI system: FinRisk Copilot (github.com/Kevinshalu/fraud-analyst-agent) — fraud investigation agent using same LangGraph + GPT-4o + FastAPI + Streamlit pattern
- Daily user of AI-enabled coding agents (Claude Code, Cursor, GitHub Copilot)

## Project tone and quality bar

This is **a portfolio piece going to BlackRock Aladdin AI leadership** via direct LinkedIn outreach. Quality matters more than feature count:
- Code must be clean, well-commented, idiomatic Python
- README must be professional and well-structured
- Architecture diagrams must look polished
- Demo video must be confident and under 90 seconds
- Eval framework must produce real numbers, not vibes

If a feature is buggy or half-finished, ship the project WITHOUT it. Better to ship 3 excellent tools than 5 sloppy ones.

## Tech stack

| Layer | Choice | Rationale |
|---|---|---|
| LLM | GPT-4o-mini | $0.15/M tokens — cost-efficient for demo; can upgrade to GPT-4o for production paths |
| Agent framework | LangGraph (ReAct pattern) | Consistent with FinRisk Copilot; explicit state management; vendor-flexible |
| Backend | FastAPI | Standard for ML-backed APIs; async support |
| Frontend | Streamlit | Fast iteration; suitable for internal analytics tools; sufficient for demo |
| Data | yfinance (free, public) + sample JSON portfolio | Reproducible by anyone reviewing code; no proprietary data |
| Hosting | Streamlit Community Cloud (free) | Public URL for demo; integrates with GitHub |
| Repo | github.com/Kevinshalu/portfoliopilot | Public; main branch protected; clean commit history |

## The 5 agent tools

1. **`get_portfolio_holdings(filters)`** — Returns current holdings with sector/region/weight breakdown
2. **`calculate_risk_metrics(tickers)`** — Beta, factor exposure, VaR, concentration
3. **`run_scenario_analysis(scenario)`** — Stress-test against rate shocks, equity drawdowns, commodity moves
4. **`summarize_holdings_news(tickers)`** — LLM-summarized news per holding with sentiment + themes
5. **`flag_anomalies(window)`** — Z-score-based detection of unusual price/volume/volatility moves

See `docs/design-decisions.md` for the reasoning behind each tool choice.

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
    ├─ Tool 1: holdings.py
    ├─ Tool 2: risk.py
    ├─ Tool 3: scenarios.py
    ├─ Tool 4: news.py
    └─ Tool 5: anomalies.py
         │
         ▼
Data: yfinance + sample_portfolio.json + Fama-French factors
```

## Day-by-day build plan (June 1–7, 2026)

| Day | Date | Goal | Hours |
|---|---|---|---|
| 1 | June 1 (today) | Repo setup, sample data, Tool 1 (holdings) working | 3-4 |
| 2 | June 2 | Tool 2 (risk metrics) + unit tests | 3-4 |
| 3 | June 3 | Tool 3 (scenarios) + Tool 4 (news) | 3-4 |
| 4 | June 4 | Tool 5 (anomalies) + agent integration | 3-4 |
| 5 | June 5 | FastAPI backend + Streamlit frontend | 3-4 |
| 6 | June 6 | Polish, deploy to Streamlit Cloud, write README | 2-3 |
| 7 | June 7 | Record demo video, prep outreach to BlackRock execs | 2 |

**Hard cap: 7 days, ~20 hours total.** If a feature is at risk on Day 5, cut it (anomaly tool first, then scenarios). Ship what works on Day 7.

## Quality gates (do not skip)

- [ ] All tools have unit tests with >80% pass rate
- [ ] Eval framework runs and produces measurable scores (tool selection accuracy, hallucination rate)
- [ ] README explains architecture, design decisions, limitations
- [ ] Demo video walks through 3-4 realistic queries
- [ ] Code passes basic linting (use `ruff` or `black`)
- [ ] No secrets committed to repo (use `.env.example` template; real `.env` is gitignored)
- [ ] Live demo accessible at public Streamlit Cloud URL
- [ ] Architecture diagram exists in repo (use excalidraw.com for free)

## Connection to other Kevin projects

| Project | Path | Relationship |
|---|---|---|
| **career-ops** | `/Users/kevinshalu/Code/career-ops/` | Tracks all Kevin's job applications; PortfolioPilot project plan lives at `career-ops/docs/blackrock/aladdin-portfoliopilot-project-plan.md` |
| **fraud-analyst-agent** | `/Users/kevinshalu/Code/fraud-analyst-agent/` | FinRisk Copilot (same LangGraph + GPT-4o + FastAPI + Streamlit pattern); reference implementation Kevin can copy patterns from |
| Morgan Stanley AI PM playbook | `career-ops/docs/morgan-stanley/morgan-stanley-ai-pm-playbook.md` | Project serves as Week 1 applied case study (Approach 3 hybrid) |

## Honest limitations (document in `docs/limitations.md`)

- Sample portfolio of 10 stocks; production handles 100s-1000s
- Simplified risk model; production uses proprietary 50+ factor models
- yfinance data has 15-min delay; production requires real-time feeds
- No persistent session memory across queries
- No multi-portfolio support
- No compliance-aware filtering (no MNPI screening)
- Demo-grade error handling, not production-grade

These limitations are STRENGTHS, not weaknesses. Documenting them honestly shows AI PM maturity — knowing what's production-grade vs prototype is the core skill.

## Outreach plan

Once the project is live (Day 7), Kevin will:
1. Send 5-8 LinkedIn connection requests to BlackRock Aladdin AI leadership/product/recruiting
2. Send follow-up messages with project + demo links to those who accept
3. Frame as "FYI portfolio piece for your application context" — not as a referral ask

See `career-ops/docs/blackrock/aladdin-portfoliopilot-project-plan.md` Section 10 for the full outreach playbook (target list, messages, timing).

## Critical reminders

- **NEVER use the word "Aladdin"** in project name, branding, README, or descriptions — IP/legal hygiene
- **NEVER use real client data** — only public yfinance + synthetic sample portfolio
- **NEVER claim parity with production systems** — frame as "demonstration of agentic patterns"
- **DO document everything honestly** — limitations, simplifications, future work
- **DO emphasize the eval framework** — most candidates don't build evals; you do
- **DO publish architecture decisions** — the design-decisions.md doc is interview gold

## How to start each new Claude session in this project

Just open Claude in this folder. Claude reads this CLAUDE.md and has full context. Then say:
- *"What day are we on?"* — Claude checks progress vs the 7-day plan
- *"Build the next tool"* — Claude scaffolds the next item
- *"Review my last commit"* — Claude critiques code quality
- *"Update the README"* — Claude integrates latest work into README narrative
- *"Run the eval suite"* — Claude executes evals and helps interpret results
