"""
PortfolioPilot Eval Suite.

Runs the golden_dataset.json queries through the agent and computes:
- Tool selection accuracy (% of queries where expected tools were called)
- Multi-step handling (subset of accuracy, restricted to multi-step cases)
- Coverage (% of answers mentioning expected substance keywords)
- Average tools called per query

Results dumped to evals/results/run_<timestamp>.json + printed to stdout.

Run with:
    python -m evals.eval_suite
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

from agent.portfoliopilot_agent import run_query


GOLDEN_PATH = Path(__file__).parent / "golden_dataset.json"
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def _tool_selection_score(expected: list[str], actual: list[str]) -> bool:
    """Lenient: every expected tool must appear in actual; extras allowed."""
    return set(expected).issubset(set(actual))


def _coverage_score(answer: str, keywords: list[str]) -> float:
    """Fraction of expected substance keywords that appear in the answer (case-insensitive, lenient stem match)."""
    if not keywords:
        return 1.0
    answer_lower = answer.lower()
    # Strip pluralization / suffix for lenient matching ("holdings" → "holding")
    hits = sum(1 for k in keywords if k.lower().rstrip("s") in answer_lower)
    return hits / len(keywords)


def run_evals() -> dict:
    with GOLDEN_PATH.open("r") as f:
        golden = json.load(f)

    results = []
    total_start = time.time()

    for case in golden:
        print(f"[{case['id']:2d}/{len(golden)}] {case['query'][:60]}...")
        t0 = time.time()
        try:
            response = run_query(case["query"])
            elapsed = time.time() - t0
            actual_tools = response["tools_called"]
            answer = response["final_answer"]
            error = None
        except Exception as e:
            elapsed = time.time() - t0
            actual_tools = []
            answer = ""
            error = str(e)

        result = {
            "id": case["id"],
            "query": case["query"],
            "complexity": case["complexity"],
            "expected_tools": case["expected_tools"],
            "actual_tools": actual_tools,
            "tool_selection_correct": _tool_selection_score(case["expected_tools"], actual_tools),
            "coverage_score": _coverage_score(answer, case.get("expected_output_contains", [])),
            "answer_preview": answer[:200],
            "elapsed_sec": round(elapsed, 2),
            "error": error,
        }
        results.append(result)
        status = "OK " if result["tool_selection_correct"] else "MISS"
        print(f"     {status}  expected={case['expected_tools']}  actual={actual_tools}  ({elapsed:.1f}s)")

    total_elapsed = time.time() - total_start

    # Aggregate
    total = len(results)
    single = [r for r in results if r["complexity"] == "single-tool"]
    multi = [r for r in results if r["complexity"] == "multi-step"]
    summary = {
        "total_cases": total,
        "overall_tool_accuracy_pct": round(100 * sum(r["tool_selection_correct"] for r in results) / total, 1),
        "single_tool_accuracy_pct": round(100 * sum(r["tool_selection_correct"] for r in single) / len(single), 1) if single else None,
        "multi_step_accuracy_pct": round(100 * sum(r["tool_selection_correct"] for r in multi) / len(multi), 1) if multi else None,
        "avg_coverage_score": round(sum(r["coverage_score"] for r in results) / total, 2),
        "avg_tools_per_query": round(sum(len(r["actual_tools"]) for r in results) / total, 2),
        "avg_seconds_per_query": round(sum(r["elapsed_sec"] for r in results) / total, 2),
        "total_seconds": round(total_elapsed, 2),
        "errors": sum(1 for r in results if r["error"]),
    }

    # Persist
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = RESULTS_DIR / f"run_{timestamp}.json"
    with output_path.open("w") as f:
        json.dump({"summary": summary, "details": results}, f, indent=2)

    # Pretty-print summary
    print()
    print("=" * 60)
    print("EVAL SUMMARY")
    print("=" * 60)
    for k, v in summary.items():
        print(f"  {k:30s}  {v}")
    print(f"\n  Results saved to {output_path}")
    return summary


if __name__ == "__main__":
    run_evals()