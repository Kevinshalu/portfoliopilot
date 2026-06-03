"""
FastAPI Backend — TO BE IMPLEMENTED ON DAY 5

Exposes the PortfolioPilot agent via REST + SSE streaming endpoints.

Endpoints:
- POST /query    — accept a natural-language query, return agent response (sync)
- POST /stream   — accept a query, stream agent response token-by-token (SSE)
- POST /eval     — run the eval suite, return results
- GET  /health   — health check
"""

from __future__ import annotations

# TODO Day 5: implement
# from fastapi import FastAPI
# from pydantic import BaseModel
#
# from agent.portfoliopilot_agent import build_agent
#
# app = FastAPI(title="PortfolioPilot API", version="0.1.0")
# agent = build_agent()
#
#
# class QueryRequest(BaseModel):
#     query: str
#
#
# @app.get("/health")
# def health():
#     return {"status": "ok"}
#
#
# @app.post("/query")
# async def query(request: QueryRequest):
#     result = await agent.ainvoke({"messages": [("user", request.query)]})
#     return {"response": result["messages"][-1].content}
#
#
# @app.post("/stream")
# async def stream(request: QueryRequest):
#     # TODO: SSE streaming via sse_starlette
#     pass


# Run with: uvicorn backend.main:app --reload --port 8000
