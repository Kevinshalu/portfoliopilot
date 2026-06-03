# PortfolioPilot — Design Decisions

This document captures the architectural and product decisions made during PortfolioPilot's build, with the reasoning behind each. It serves as both project documentation and a reference for the AI PM thinking that drove each choice.

Each decision references concepts from the Morgan Stanley AI PM interview playbook foundation section, demonstrating applied AI PM craft.

---

## 1. LangGraph ReAct vs OpenAI Assistants API

**Decision:** LangGraph with `create_react_agent`.

**Alternatives considered:**
- OpenAI Assistants API (managed by OpenAI)
- LangChain (without LangGraph)
- Custom orchestration with raw OpenAI function calling

**Reasoning:**
- **Cost control:** LangGraph runs locally; OpenAI Assistants charges per "thread" and tool call separately
- **Explicit state management:** LangGraph's StateGraph makes the agent's decision flow inspectable and debuggable
- **Vendor flexibility:** Can swap GPT-4o-mini for Claude or open-source models without rewriting orchestration
- **Production parity:** Mirrors how enterprises (including those building Aladdin-style platforms) actually deploy agents — they need control over routing, retries, and state
- **Consistency with FinRisk Copilot:** Same architectural pattern as my previous production agent (github.com/Kevinshalu/fraud-analyst-agent), demonstrating reusable enterprise patterns

**Reference (MS playbook Section 3.6):** Build vs buy decision — chose to build (LangGraph orchestration) rather than buy (OpenAI Assistants) because the upside on control and cost outweighs the marginal complexity.

---

## 2. GPT-4o-mini vs GPT-4o

**Decision:** GPT-4o-mini for this demo. Document path to GPT-4o for production.

**Cost comparison (June 2026 pricing):**

| Model | Input cost | Output cost | Per query estimate |
|---|---|---|---|
| GPT-4o | $2.50/M tokens | $10.00/M tokens | ~$0.04 per multi-tool query |
| GPT-4o-mini | $0.15/M tokens | $0.60/M tokens | ~$0.002 per multi-tool query |

**Reasoning:**
- **20x cost reduction** with acceptable quality drop for demo-tier accuracy
- **Faster inference** (~2x faster on average), critical for chat-feel UX
- **Production routing path:** For production, dynamically classify query complexity and route simple queries (90%) to mini, complex multi-step queries (10%) to 4o

**Reference (MS playbook Section 3.2):** LLM economics — model selection is a cost/latency/accuracy tradeoff, not a single "best model" choice.

---

## 3. Streamlit vs Next.js / React

**Decision:** Streamlit for demo. Document migration path to Next.js for production.

**Reasoning:**
- **Speed to demo:** Streamlit prototypes in hours; Next.js requires days for equivalent UX
- **Audience fit:** Portfolio managers and analysts are accustomed to internal analytical tools (Streamlit-class). External client-facing tools would need Next.js
- **Streaming support:** Streamlit's `st.write_stream()` handles SSE responses natively
- **Hosting:** Streamlit Community Cloud is free with a public URL; perfect for portfolio demos

**Production migration:** Replace Streamlit with Next.js + React for:
- Better mobile responsiveness
- Custom design system alignment (institutional branding)
- Multi-user state management (each user's portfolio context)
- Advanced charting libraries (D3, ApexCharts)

---

## 4. yfinance vs Bloomberg/Refinitiv

**Decision:** yfinance for all market data.

**Reasoning:**
- **Free and public:** Anyone reviewing the code can reproduce the demo
- **Sufficient quality for demo:** Price data is ~15-min delayed; sufficient for non-real-time analytics
- **Sample portfolio of large-cap names:** Coverage is reliable
- **No API key required:** Lower friction to deploy and demo

**Production implications:** Enterprise asset managers would use Bloomberg BPIPE, Refinitiv Eikon, FactSet, or direct exchange feeds. The data ingestion layer would be entirely different, but the agent orchestration layer (tools, prompts, agent definition) would not change.

---

## 5. Simplified Factor Model vs Production-Grade Multi-Factor

**Decision:** Use Fama-French 5-factor proxies via ETF betas; document limitations explicitly.

**Production-grade reality:** Firms like BlackRock (BARRA), MSCI, Axioma use proprietary 50-100 factor models with daily-updated covariance matrices, optimized for transaction cost analysis, alpha attribution, and risk budgeting.

**Why simplified here:**
- Demonstrates the *concept* of factor decomposition in a working agent context
- The agentic pattern (user asks → tool decomposes → structured output) generalizes regardless of factor model sophistication
- Building a real multi-factor model is months of work and orthogonal to the agentic AI demonstration

**Honest framing in README:** This is explicitly called out as a simplification. AI PM maturity comes from knowing what's prototype-grade vs production-grade — and being transparent about it.

**Reference (MS playbook Section 3.4):** Risk stack — being honest about model simplifications IS risk management at the product level.

---

## 6. Eval-Driven Development (Why Build an Eval Suite at All)

**Decision:** Build a 10-query golden dataset and automated eval framework.

**Why this matters more than the features themselves:**
- Most candidate portfolio AI projects don't have evals
- Evals are the single most important AI PM skill — you can't "QA" a probabilistic system the way you QA deterministic code
- Reviewers (including BlackRock Aladdin AI leaders) recognize eval-driven development as a signal of AI PM maturity

**What the eval suite checks:**
- **Tool selection accuracy:** Did the agent call the right tool(s) for each query?
- **Output structure correctness:** Required fields present in tool outputs?
- **Numerical accuracy:** For deterministic calculations (beta, VaR), are answers within tolerance?
- **Hallucination rate:** Does output reference data that doesn't exist?
- **Multi-step handling:** For complex queries needing 2+ tools, are they sequenced correctly?

**Reference (MS playbook Section 3.3):** Eval-driven development is foundational AI PM craft.

---

## 7. Agent Reasoning Transparency in UI

**Decision:** Show the agent's reasoning trace (tool selection, tool inputs, intermediate steps) in the UI.

**Why:**
- **Trust:** Users (especially in finance) need to understand how an AI reached a conclusion
- **Debugging:** Transparent reasoning makes errors visible
- **Compliance preview:** In a real Aladdin deployment, every AI decision would need an audit trail. Showing reasoning in the demo demonstrates awareness of this requirement.

**Reference (MS playbook Section 3.4 + 3.7):** Risk stack and governance — transparency is the foundation of both.

---

## 8. Why a Portfolio Manager Persona (vs Risk Officer, Trader, etc.)

**Decision:** Target portfolio manager as primary user.

**Why:**
- **Aladdin's primary user base:** Portfolio managers at institutional asset managers are Aladdin's biggest customer segment
- **Workflow richness:** PMs do composition, risk, scenario, research, and pre-market work — perfect for a multi-tool agent demo
- **Story arc:** "I'm building tools my future colleagues will use" is the right framing for BlackRock outreach

**Alternative considered:** Risk officer persona. Rejected because risk-officer workflows are more narrow (mostly Tool 2 + scenarios) — less compelling demo.

---

## 9. Public Demo on Streamlit Cloud vs Local-Only

**Decision:** Deploy publicly on Streamlit Community Cloud.

**Why:**
- Recruiters and BlackRock execs can click a link and see the project work — no setup required on their end
- Lowers friction for the audience by 100x compared to "clone the repo and run locally"
- Free hosting; no infrastructure burden

**Cost:** Need to manage OpenAI API key as a Streamlit secret. Set spending limits in OpenAI dashboard ($10/month cap is sufficient).

---

## 10. Why No Multi-Portfolio Support

**Decision:** Single hardcoded sample portfolio for demo.

**Why:**
- Multi-portfolio adds significant UX complexity (portfolio switcher, state management)
- One well-chosen portfolio shows the patterns; multiple add noise without adding signal
- Production implication noted in `docs/future-work.md`: multi-portfolio support is the obvious Day 8+ extension

---

*This document grows as decisions are made during the build. Each commit that introduces a meaningful design choice should add a section here.*
