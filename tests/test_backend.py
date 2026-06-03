"""Smoke tests for the FastAPI backend."""
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health():
    """Health endpoint should return 200 with status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query_routes_to_agent():
    """POST /query should call run_query and return the expected shape."""
    fake_result = {
        "final_answer": "Your portfolio has 10 holdings totaling $1.9M.",
        "tools_called": ["get_portfolio_holdings"],
    }
    with patch("backend.main.run_query", return_value=fake_result):
        response = client.post("/query", json={"query": "What is in my portfolio?"})
    assert response.status_code == 200
    body = response.json()
    assert body["final_answer"] == fake_result["final_answer"]
    assert body["tools_called"] == ["get_portfolio_holdings"]


def test_query_validation_rejects_empty():
    """Empty query should be rejected by Pydantic validation (422)."""
    response = client.post("/query", json={"query": ""})
    assert response.status_code == 422