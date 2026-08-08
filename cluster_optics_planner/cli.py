"""CLI for AI-cluster optics planning."""
from __future__ import annotations

from .planner import compare_topologies, plan_optics, sample_profile


def main(argv: list[str] | None = None) -> int:
    _ = argv
    plan = plan_optics(sample_profile())
    for key, value in plan.items():
        print(f"{key}={value}")
    best = compare_topologies(sample_profile())[0]
    print(f"best_topology={best['topology']}")
    print(f"best_cost_pressure_score={best['cost_pressure_score']}")
    return 0
