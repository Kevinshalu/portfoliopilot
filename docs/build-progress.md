# Build Progress Tracker

Update this file at the end of each day to track progress against the 7-day plan.

---

## Day 1 — June 1, 2026

**Goal:** Repo setup, sample data, Tool 1 (holdings) working

**Completed:**
- [x] Project structure created
- [x] requirements.txt, .gitignore, .env.example written
- [x] CLAUDE.md project context written
- [x] README.md, design-decisions.md, limitations.md, future-work.md drafted
- [x] data/sample_portfolio.json created (10 S&P 500 holdings)
- [x] tools/holdings.py implemented
- [x] tests/test_holdings.py with 3 smoke tests
- [x] evals/golden_dataset.json (10-query suite) written
- [x] Initial git commit

**Still pending for Day 1:**
- [ ] Run `pip install -r requirements.txt` in virtualenv
- [ ] Verify `python tools/holdings.py` runs and returns live data
- [ ] Run `pytest tests/test_holdings.py -v` — all 3 should pass
- [ ] Create GitHub repo (Kevinshalu/portfoliopilot)
- [ ] Push to GitHub

**Lessons learned:**
- (fill in after running Tool 1)

**Notes for Day 2:**
- Day 2 focus: implement `tools/risk.py` — portfolio beta, VaR, factor exposures, concentration metrics
- Pull Fama-French 5-factor CSV from Kenneth French data library before Day 2 start
- Reference FinRisk Copilot's similar patterns at `/Users/kevinshalu/Code/fraud-analyst-agent/`

---

## Day 2 — June 2, 2026

**Goal:** Tool 2 (risk metrics) + unit tests

**Completed:**
- [x] tools/risk.py: `calculate_risk_metrics()` function
- [x] Beta calculation vs S&P 500 (weighted average; portfolio beta = 1.06)
- [x] Annualized volatility (14.41% on current sample portfolio)
- [x] VaR 95% 1-day, parametric ($28,921 / 1.49% on $1.93M portfolio)
- [x] Factor exposures via VLUE/MTUM/QUAL/USMV ETF proxies (quality 0.98 dominant)
- [x] Concentration metrics: top-5 weight 78.14%, max position 23.34%, Herfindahl 0.1503, effective N 6.7
- [x] Unit tests for risk.py — 6 tests, all passing (~15s runtime)
- [ ] Commit progress

**Lessons learned:**
- Direct-running a file inside `tools/` requires `python -m tools.risk` (not `python tools/risk.py`) so the project root is on sys.path
- yfinance returns Series for 1 ticker, DataFrame for many — normalize at the boundary
- Used 4 univariate factor regressions instead of one multivariate, because the iShares factor ETFs are highly correlated and multivariate coefficients would be unstable. Documented as a known simplification.
- numpy scalar floats (`np.float64`) don't JSON-serialize cleanly — cast to native `float` at the public-API boundary

**Notes for Day 3:**
- Day 3 focus: Tool 3 (scenarios) + Tool 4 (news)
- Scenarios: pre-defined rate shock / equity crash / oil shock; apply impact via sector or beta sensitivities
- News: yfinance `.news` pull per ticker + GPT-4o-mini summarization with sentiment + themes
- Both should reuse the holdings + risk patterns (function + `__main__` smoke block + ≥5 unit tests)

---

## Day 3 — June 2, 2026 (built early; planned for June 3)

**Goal:** Tool 3 (scenarios) + Tool 4 (news)

**Completed:**
- [x] tools/scenarios.py: 3 pre-defined scenarios (rate_shock_+100bps, equity_crash_-20%, oil_shock_+30%) with per-sector overrides on top of beta-driven market move
- [x] tools/news.py: yfinance.news pull + GPT-4o-mini structured-output summarization (one LLM call, per-ticker sentiment + themes + cross-portfolio themes)
- [x] OpenAI API key wired via python-dotenv + .env (gitignored)
- [x] Unit tests: 3 for scenarios + 3 for news (6 total, ~8s runtime)
- [x] Commit progress

**Lessons learned:**
- yfinance changed its `.news` response shape in 0.2.40+ (everything wrapped in `content` sub-dict). The `content = item.get("content", item)` pattern handles both versions.
- OpenAI's `.beta.chat.completions.parse()` with a Pydantic `response_format` gives typed JSON guarantees — no regex, no json.loads try/except.
- One LLM call across all tickers (vs. per-ticker calls) is cheaper AND unlocks cross-portfolio theme detection that per-ticker loops can't do.
- Live LLM calls in pytest add cost on every test run; mock `_summarize_with_llm` and keep the live LLM check as the `__main__` smoke block.
- Scenarios with no sector_overrides + a market_move act as pure beta stress tests; this is the right primitive to compose more complex scenarios later.

**Notes for Day 4:**
- Day 4 focus: Tool 5 (anomalies) + agent integration
- Anomalies: z-score-based detection on daily returns + volume; window param defaults to 60d for baseline
- Agent: LangGraph ReAct pattern in agent/portfoliopilot_agent.py wrapping all 5 tools
- System prompt should: (1) describe each tool's purpose, (2) anchor the agent to use real tool calls vs. fabricating numbers, (3) name itself "PortfolioPilot"
- Aim to ship Day 4 ahead of plan too — currently ~24h ahead of schedule

---

## Day 4 — June 2, 2026 (built early; planned for June 4)

**Goal:** Tool 5 (anomalies) + agent integration

**Completed:**
- [x] tools/anomalies.py: z-score-based detection on daily return, volume, intraday range; baseline excludes the recent window to avoid self-inflation
- [x] agent/portfoliopilot_agent.py: LangGraph ReAct agent wrapping all 5 tools
- [x] System prompt finalized with 5 explicit rules (#1 = "always call tools, never fabricate")
- [x] End-to-end smoke from __main__: 4 sample queries — composition, risk, scenario, anomalies — agent routes to correct tool every time
- [x] Tests: 3 for anomalies + 2 for agent (5 total; 1 live LLM agent test ~$0.001)
- [x] Commit progress

**Lessons learned:**
- Defensive std=0 → NaN replacement (correct production behavior) broke the first synthetic test (flat baseline). Lesson: synthetic test data needs realistic noise structure, not constant values.
- yfinance returns columns as MultiIndex for single-ticker downloads in 0.2.40+ — flatten with `df.columns.get_level_values(0)` to keep downstream access uniform.
- LangGraph's `create_react_agent` handles the entire reason-act-observe loop; we wrote zero loop code, just @tool wrappers + a system prompt.
- Tool docstrings literally become the LLM's tool descriptions — write them like you're explaining to a colleague who's never seen the codebase.
- Lazy singleton for the agent (`_agent = None` + `_get_agent`) saves ~50ms per query after the first.
- LangGraph v1.0 deprecation warning on `create_react_agent` (moves to `langchain.agents.create_agent` in v2.0). Tracked as known cleanup, not blocking — no v2.0 release date yet.

**Notes for Day 5:**
- Day 5 focus: FastAPI backend + Streamlit frontend
- Backend: /query (POST, sync), /health endpoints — wrap run_query() from the agent module
- Frontend: 3-panel Streamlit (holdings table | chat | output) with 5 quick-click sample query buttons
- Per the plan, no /stream endpoint unless time permits — SSE adds complexity without much demo value

---

## Day 5 — June 2, 2026 (built early; planned for June 5)

**Goal:** FastAPI backend + Streamlit frontend

**Completed:**
- [x] backend/main.py: POST /query and GET /health (Pydantic-validated request/response, CORS for local dev)
- [x] /stream endpoint deferred per "ship what works" rule — SSE adds complexity without much demo value at this scale
- [x] frontend/app.py: 3-panel Streamlit dashboard (holdings | query | answer)
- [x] 5 quick-click sample query buttons + free-text input
- [x] Integration tested end-to-end locally — Streamlit calls FastAPI via httpx, answer + tool trace render correctly
- [x] 3 backend tests using FastAPI TestClient (mocked agent, free, deterministic)
- [x] Commit progress

**Lessons learned:**
- Streamlit can't be invoked with `python -m`, so the sys.path hack at the top of frontend/app.py is required (or PYTHONPATH=.). Project-root sys.path.insert is more robust because it survives any deployment context.
- @st.cache_data(ttl=60) is essential — Streamlit re-runs the entire script on every interaction; without caching we'd hit yfinance dozens of times in a session.
- session_state is needed to make button clicks (sample queries) trigger the agent in a different column. Without it, the local `query` variable disappears on the next rerun.
- httpx default timeout is 5s; agent calls can take 20–40s on multi-tool queries. Bumped to 120s.
- Streamlit auto-reloads on file save (hot reload "out of the box") — significant productivity win vs FastAPI which needs `--reload` flag on uvicorn.
- FastAPI's auto-generated /docs Swagger UI is portfolio gold for interview demos — visual proof of clean API design.

**Notes for Day 6:**
- Day 6 focus: polish, deploy, finalize README, architecture diagram
- Deploy decision: Streamlit Cloud doesn't host FastAPI. Two options: (a) Streamlit-direct calls (skip FastAPI in prod, keep in repo as architectural artifact), (b) deploy FastAPI on Render/Fly.io free tier. Recommend (a) for time-to-ship; document (b) as "production path" in README.
- README: replace placeholder with full architecture diagram, design decisions, quickstart, screenshots
- Architecture diagram: excalidraw.com, 10 minutes
- Bug-fix pass through all 10 golden_dataset queries

---

## Day 6 — June 6, 2026

**Goal:** Polish, deploy to Streamlit Cloud, write README

**Completed:**
- [ ] Bug-fix pass through all 10 golden dataset queries
- [ ] Deploy to Streamlit Community Cloud
- [ ] OpenAI API key set as Streamlit secret
- [ ] Architecture diagram created (excalidraw)
- [ ] README finalized with all sections
- [ ] Final commit + push

---

## Day 7 — June 7, 2026

**Goal:** Demo video + outreach prep

**Completed:**
- [ ] 90-sec Loom walkthrough recorded
- [ ] LinkedIn target list compiled (5-8 BlackRock Aladdin AI contacts)
- [ ] Connection request notes drafted
- [ ] Follow-up message template ready
- [ ] First 3 connection requests sent

---

## Project complete

**Total time invested:** ~ hours
**Final artifacts:**
- GitHub repo: github.com/Kevinshalu/portfoliopilot
- Live demo: [streamlit URL]
- Demo video: [Loom URL]

**Outreach status (post-launch):**
- Connection requests sent: __ / 8
- Connections accepted: __
- Follow-up messages sent: __
- Meaningful conversations: __
