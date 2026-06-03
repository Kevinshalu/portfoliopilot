# PortfolioPilot — Future Work

If PortfolioPilot were a production system (or the next iteration of this prototype), here are the natural extensions in priority order.

This document signals product thinking — the AI PM's job is to articulate not just what you built, but what you'd build next and why.

---

## P0 — Production-readiness foundations

### 1. Multi-portfolio support
Single portfolio limits real-world utility. Production users manage 5-50 portfolios.
- Portfolio switcher in UI
- Cross-portfolio aggregation views
- Per-portfolio user permissions

### 2. Real-time data integration
Replace yfinance with enterprise market data feeds.
- Bloomberg BPIPE or Refinitiv RTH
- Direct exchange feeds for trading-relevant queries
- Corporate actions handling

### 3. Persistent agent memory
Stateless agent = poor UX. Production needs continuity.
- Conversation history per user
- Portfolio preferences (default tickers, scenario sets)
- Cross-session learning of user query patterns

### 4. Production observability
No metrics = no improvement loop.
- Per-query latency and cost tracking
- Tool usage frequency analytics
- User satisfaction signals (thumbs up/down per response)
- Hallucination detection in production

---

## P1 — Compliance and governance

### 5. MNPI screening layer
Compliance-aware filtering of agent outputs.
- Detect and redact MNPI-related information
- Block sensitive tickers based on insider trading policies
- Audit log of every screening decision

### 6. Audit trail with replay
Every query needs immutable logging.
- Per-query session log with full reasoning trace
- Regulator-accessible audit dashboard
- Response replay for compliance review

### 7. Suitability checks
For client-facing variants, verify outputs match user risk profile.
- Integration with KYC/AML systems
- Risk-tolerance-aware response generation
- Disclosure templates for regulated outputs

---

## P2 — Advanced AI capabilities

### 8. Dynamic model routing
Route queries to optimal model based on complexity.
- Lightweight classifier predicts query complexity
- Simple queries → GPT-4o-mini ($0.15/M)
- Complex multi-step → GPT-4o ($2.50/M)
- Domain-specific → Fine-tuned model

### 9. Specialized fine-tuned models
For high-frequency analytical queries, fine-tune on domain data.
- Risk metric explanation model
- Scenario narrative model
- Compliance-aware summarization model

### 10. Agent memory beyond conversation
Long-term agent learning.
- User preference modeling (which sectors/factors the PM cares about)
- Pattern recognition (PM tends to ask risk questions on Mondays, news on Fridays)
- Proactive insights (push notifications when anomalies detected in held positions)

---

## P3 — Product expansion

### 11. Trader-specific tools
PMs are one persona. Traders need different tools.
- Pre-trade impact analysis
- Liquidity scoring
- Best execution analytics
- Trading cost attribution

### 12. Risk officer tools
Risk officers have different workflows than PMs.
- Cross-portfolio risk aggregation
- Limit breach monitoring
- Stress testing across firm
- Counterparty exposure analysis

### 13. Research analyst tools
Buy-side analysts need different agentic flows.
- Earnings transcript analysis
- Peer comparison automation
- Investment thesis validation
- Consensus tracking

### 14. Multi-modal capabilities
Beyond text input.
- Voice query support
- Document upload (research reports, earnings calls)
- Image input (chart interpretation, document OCR)
- Output as formatted PDF reports

---

## P4 — Strategic platform capabilities

### 15. Federation across asset classes
Currently equity-only. Real institutional portfolios span:
- Fixed income (corporate, sovereign, MBS, ABS)
- Derivatives (options, futures, swaps)
- Alternatives (private equity, real estate, infrastructure)

Each requires specialized tools and data integrations.

### 16. Multi-tenant platform architecture
Per-firm isolation, configurable workflows, branded UX.
- Each firm has its own data, models, prompts, compliance rules
- White-label-ready

### 17. Marketplace of agent tools
Extensible architecture where firms can plug in:
- Their proprietary risk models
- Their custom factor definitions
- Their internal data sources
- Their compliance rules

### 18. Cross-firm benchmarking (anonymized)
Anonymized peer comparison — what does my portfolio look like vs other PMs at similar firms?

---

## What I'd build first if I joined Aladdin AI

If hired as an AI PM at BlackRock Aladdin AI, the first 90-day plan informed by PortfolioPilot:

**Days 1-30:** Listen and learn
- Shadow 5-10 PMs at Aladdin client firms to understand actual workflows
- Audit current Aladdin Copilot adoption metrics
- Identify top 3 friction points in PM-to-Aladdin AI interactions

**Days 31-60:** Define and prototype
- Propose 1 high-impact agentic feature for the Aladdin roadmap
- Build a working prototype (PortfolioPilot-style) to validate the feature
- Define KPIs and an eval framework specific to the feature

**Days 61-90:** Ship and measure
- Partner with engineering to ship MVP to internal test users
- Set up adoption + value-realization metrics
- Document learnings and propose next 90-day iteration

---

## Critical AI PM principle

Building PortfolioPilot taught me that agentic AI products live or die on the gap between *demo-grade* and *production-grade*. The 18 items above are the gap.

Closing that gap is the real AI PM job. The prototype is just the entry ticket.

---

*Last updated: June 1, 2026 — Day 1 of build*
