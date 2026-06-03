"""
PortfolioPilot Eval Suite — TO BE IMPLEMENTED ON DAY 6

Runs the golden_dataset.json queries through the agent and computes:
- Tool selection accuracy (% of queries where expected tools were called)
- Output structure correctness (% with all expected fields)
- Numerical accuracy (% within tolerance for deterministic answers)
- Hallucination rate (% of outputs referencing non-existent data)
- Multi-step handling (% of multi-step queries with correct tool sequencing)

Logs results to evals/results/run_<timestamp>.json
"""

from __future__ import annotations

# TODO Day 6: implement
# import json
# from datetime import datetime
# from pathlib import Path
#
# from agent.portfoliopilot_agent import build_agent
#
# GOLDEN_PATH = Path(__file__).parent / "golden_dataset.json"
# RESULTS_DIR = Path(__file__).parent / "results"
#
#
# def run_evals():
#     with GOLDEN_PATH.open("r") as f:
#         golden = json.load(f)
#
#     agent = build_agent()
#     results = []
#
#     for case in golden:
#         response = agent.invoke({"messages": [("user", case["query"])]})
#         tools_called = extract_tools_called(response)
#         result = {
#             "id": case["id"],
#             "query": case["query"],
#             "expected_tools": case["expected_tools"],
#             "actual_tools": tools_called,
#             "tool_selection_correct": set(case["expected_tools"]).issubset(set(tools_called)),
#             # ... other checks
#         }
#         results.append(result)
#
#     summary = compute_summary(results)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     output_path = RESULTS_DIR / f"run_{timestamp}.json"
#     with output_path.open("w") as f:
#         json.dump({"summary": summary, "details": results}, f, indent=2)
#
#     print_summary(summary)
#
#
# if __name__ == "__main__":
#     run_evals()
