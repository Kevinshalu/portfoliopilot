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
- [ ] tools/risk.py: `calculate_risk_metrics()` function
- [ ] Beta calculation vs S&P 500
- [ ] Annualized volatility
- [ ] VaR 95% 1-day (parametric)
- [ ] Factor exposures (using value/momentum/quality/low-vol ETF proxies)
- [ ] Concentration metrics (top 5 weight, max position, Herfindahl)
- [ ] Unit tests for risk.py (5 tests minimum)
- [ ] Commit progress

**Notes for Day 3:**
- (fill in at end of Day 2)

---

## Day 3 — June 3, 2026

**Goal:** Tool 3 (scenarios) + Tool 4 (news)

**Completed:**
- [ ] tools/scenarios.py: pre-defined scenarios (rate shock, equity crash, oil shock)
- [ ] tools/news.py: yfinance.news pull + LLM summarization
- [ ] Unit tests for both
- [ ] Commit progress

---

## Day 4 — June 4, 2026

**Goal:** Tool 5 (anomalies) + agent integration

**Completed:**
- [ ] tools/anomalies.py: z-score-based detection
- [ ] agent/portfoliopilot_agent.py: LangGraph ReAct agent
- [ ] System prompt finalized
- [ ] End-to-end test from REPL: 5 sample queries
- [ ] Commit progress

---

## Day 5 — June 5, 2026

**Goal:** FastAPI backend + Streamlit frontend

**Completed:**
- [ ] backend/main.py: /query, /stream, /health endpoints
- [ ] frontend/app.py: 3-panel Streamlit dashboard
- [ ] 5 quick-click sample query buttons
- [ ] Integration tested end-to-end locally
- [ ] Commit progress

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
