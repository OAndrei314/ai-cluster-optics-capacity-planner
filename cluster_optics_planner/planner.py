"""Capacity planning for optical AI-cluster fabrics."""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ClusterProfile:
    gpu_count: int
    bandwidth_per_gpu_gbps: float
    oversubscription: float
    optical_link_rate_gbps: float
    transceiver_power_w: float
    transceiver_cost_usd: float


def plan_optics(profile: ClusterProfile) -> dict[str, float]:
    if profile.gpu_count <= 0:
        raise ValueError("gpu_count must be positive")
    if profile.oversubscription <= 0:
        raise ValueError("oversubscription must be positive")
    required_tbps = profile.gpu_count * profile.bandwidth_per_gpu_gbps / profile.oversubscription / 1000.0
    link_count = math.ceil((required_tbps * 1000.0) / profile.optical_link_rate_gbps)
    transceiver_count = link_count * 2
    optical_power_kw = transceiver_count * profile.transceiver_power_w / 1000.0
    optics_capex_usd = transceiver_count * profile.transceiver_cost_usd
    return {
        "required_tbps": round(required_tbps, 3),
        "link_count": float(link_count),
        "transceiver_count": float(transceiver_count),
        "optical_power_kw": round(optical_power_kw, 3),
        "optics_capex_usd": round(optics_capex_usd, 2),
        "capex_per_gpu_usd": round(optics_capex_usd / profile.gpu_count, 2),
    }


def sample_profile() -> ClusterProfile:
    return ClusterProfile(4096, 800.0, 1.5, 1600.0, 18.0, 2800.0)
