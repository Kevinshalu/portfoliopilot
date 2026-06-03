# PortfolioPilot — Honest Limitations

This document explicitly catalogs what PortfolioPilot is NOT, alongside what it is. AI PM maturity is knowing the difference between prototype-grade and production-grade — and being transparent about it.

---

## Data limitations

### 1. Sample portfolio is synthetic and small
- 10 holdings (vs production 100-1000s)
- Hand-picked S&P 500 names for sector diversity
- Purchase prices are illustrative, not market-accurate
- No transaction history, dividends, corporate actions

**Production version would need:** Real portfolio data ingestion (FIX, SWIFT messages, custodian feeds), full transaction history with tax lots, corporate actions handling.

### 2. Market data is delayed
- yfinance has ~15-minute delay (acceptable for analytical questions, unacceptable for trading decisions)
- No intraday tick data, no historical depth-of-book
- Coverage limited to widely-tracked names

**Production version would need:** Real-time exchange feeds (Bloomberg BPIPE, Refinitiv RTH, direct exchange data), tick-level history, full corporate actions coverage, OTC/private market data.

### 3. Factor data is simplified
- Uses ETF proxies (VLUE, MTUM, QUAL, USMV) for factor exposures
- Fama-French 5-factor data from public CSV (Kenneth French data library)
- No proprietary factor model

**Production version would need:** Proprietary multi-factor model (50-100 factors), daily covariance matrix updates, custom factor definitions for the firm's investment philosophy.

### 4. News data is shallow
- Uses yfinance.news (5-10 headlines per ticker, sometimes stale)
- No earnings transcripts, analyst reports, regulatory filings
- No sentiment models trained on financial language

**Production version would need:** Bloomberg news, Refinitiv news, Capital IQ, FactSet research, SEC EDGAR filings, structured earnings call transcripts.

---

## Model limitations

### 5. LLM is GPT-4o-mini, not GPT-4o or specialized models
- Demo-tier accuracy
- May hallucinate for complex multi-step reasoning
- No domain-specific fine-tuning

**Production version would need:** Tiered model routing (mini for simple, 4o/Claude for complex), potentially fine-tuned models for domain language, eval-driven model selection.

### 6. No agent memory across sessions
- Each query is stateless
- Agent doesn't learn user preferences over time
- No conversation continuity

**Production version would need:** Persistent memory layer (vector DB or structured), user-specific preferences, conversation context.

---

## Product / UX limitations

### 7. Single-user single-portfolio
- No authentication
- No multi-portfolio support
- No team collaboration features

**Production version would need:** Enterprise SSO (Okta, Azure AD), multi-portfolio management, role-based access controls, team collaboration features.

### 8. No mobile optimization
- Streamlit is desktop-first
- No responsive design for mobile portfolio managers

**Production version would need:** Mobile-first design (probably native iOS for client-facing, web for internal), offline support, push notifications for critical anomalies.

### 9. Limited error handling
- yfinance timeouts handled gracefully but minimally
- Agent errors surface as exceptions in UI
- No retry logic with exponential backoff
- No circuit breakers for upstream data failures

**Production version would need:** Comprehensive error handling, graceful degradation when data sources fail, circuit breakers, queue-based retries, error monitoring (Sentry/DataDog).

---

## Compliance and risk limitations

### 10. No MNPI screening
- Sample data is all public; demo doesn't simulate handling of Material Non-Public Information
- No compliance review of agent outputs

**Production version would need:** MNPI screening layer (flag sensitive holdings, redact outputs), compliance approval workflows for AI outputs, audit logging of every query.

### 11. No regulatory output formatting
- Outputs don't satisfy MiFID II / FINRA / SEC disclosure requirements
- No suitability checks

**Production version would need:** Regulatory output templates, suitability checks for client-facing tools, integration with compliance/legal review workflows.

### 12. No audit trail beyond demo logs
- Each query is logged to console only
- No immutable audit log for regulatory review

**Production version would need:** Tamper-proof audit log, query attribution to specific users, response replay capability, regulator-accessible audit dashboard.

---

## Operational limitations

### 13. No production observability
- No metrics beyond eval suite
- No latency monitoring
- No cost tracking beyond OpenAI dashboard
- No alerting on degradation

**Production version would need:** Full observability stack (Datadog, OpenTelemetry), per-query cost attribution, SLO monitoring, alerting on degraded performance.

### 14. Single-region deployment
- Streamlit Community Cloud runs in one region
- No high-availability setup
- No disaster recovery

**Production version would need:** Multi-region deployment, active-active failover, disaster recovery testing, defined RTO/RPO.

### 15. No A/B testing infrastructure
- No way to compare prompts, models, or tool implementations
- No experimentation framework

**Production version would need:** A/B testing for prompts, models, agent strategies; experiment analysis dashboards.

---

## Scope limitations (by design)

### 16. Not real-time portfolio updates
- Static sample portfolio JSON
- No live position updates from trading systems

### 17. Not trade execution
- Read-only analytics; no order entry or execution
- Wouldn't be appropriate for an AI tool to execute trades without significant human-in-the-loop oversight

### 18. Not financial advice
- Outputs are illustrative analytics, not investment recommendations
- README and UI disclose this explicitly

---

## Why these limitations are STRENGTHS

Documenting limitations honestly signals AI PM maturity. The product manager who can articulate what their AI does NOT do is more trustworthy than one who claims it does everything.

When BlackRock Aladdin AI reviewers see this list, they should think: *"This person understands the gap between prototype and production. They built the prototype to demonstrate the pattern, and they know what production-grade looks like."*

That's the entire value of this project.

---

*Last updated: June 1, 2026 — Day 1 of build*
