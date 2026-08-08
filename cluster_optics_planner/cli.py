"""CLI for AI-cluster optics planning."""
from __future__ import annotations

from .planner import plan_optics, sample_profile


def main(argv: list[str] | None = None) -> int:
    _ = argv
    plan = plan_optics(sample_profile())
    for key, value in plan.items():
        print(f"{key}={value}")
    return 0
