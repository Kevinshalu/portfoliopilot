"""
PortfolioPilot FastAPI backend.

Thin HTTP wrapper around agent.portfoliopilot_agent.run_query.
Two endpoints: POST /query and GET /health.

Run locally:
    uvicorn backend.main:app --reload --port 8000

Auto-generated OpenAPI docs at http://localhost:8000/docs
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent.portfoliopilot_agent import run_query


app = FastAPI(
    title="PortfolioPilot API",
    description="Agentic AI assistant for portfolio managers.",
    version="0.1.0",
)

# Allow the Streamlit frontend (any localhost port) to call us during dev.
# Tighten this to specific origins before any real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000, description="Natural-language PM question")


class QueryResponse(BaseModel):
    final_answer: str
    tools_called: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest) -> QueryResponse:
    """Run a single PM question through the PortfolioPilot agent."""
    try:
        result = run_query(req.query)
    except Exception as e:
        # Surface the error as a 500 rather than crashing the worker.
        raise HTTPException(status_code=500, detail=f"Agent error: {e}") from e
    return QueryResponse(**result)