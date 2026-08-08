"""Capacity planning for optical AI-cluster fabrics."""
from __future__ import annotations

import math
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class ClusterProfile:
    gpu_count: int
    bandwidth_per_gpu_gbps: float
    oversubscription: float
    optical_link_rate_gbps: float
    transceiver_power_w: float
    transceiver_cost_usd: float


@dataclass(frozen=True)
class TopologyProfile:
    name: str
    link_multiplier: float
    redundancy_factor: float
    hop_count: int
    latency_per_hop_ns: float


DEFAULT_TOPOLOGIES = (
    TopologyProfile("leaf-spine", 1.0, 1.15, 4, 250.0),
    TopologyProfile("rail-optimized", 0.72, 1.08, 2, 180.0),
    TopologyProfile("dragonfly-plus", 0.86, 1.12, 3, 220.0),
)


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


def plan_topology(profile: ClusterProfile, topology: TopologyProfile) -> dict[str, float | str]:
    if topology.link_multiplier <= 0 or topology.redundancy_factor <= 0:
        raise ValueError("topology multipliers must be positive")
    adjusted = replace(
        profile,
        bandwidth_per_gpu_gbps=profile.bandwidth_per_gpu_gbps * topology.link_multiplier * topology.redundancy_factor,
    )
    plan = plan_optics(adjusted)
    power_per_tbps_kw = float(plan["optical_power_kw"]) / max(float(plan["required_tbps"]), 1e-9)
    cost_pressure = min(1.0, float(plan["capex_per_gpu_usd"]) / 5000.0 + power_per_tbps_kw / 40.0)
    return {
        "topology": topology.name,
        **plan,
        "fabric_latency_ns": round(topology.hop_count * topology.latency_per_hop_ns, 1),
        "power_per_tbps_kw": round(power_per_tbps_kw, 3),
        "cost_pressure_score": round(cost_pressure, 3),
    }


def compare_topologies(
    profile: ClusterProfile,
    topologies: tuple[TopologyProfile, ...] = DEFAULT_TOPOLOGIES,
) -> list[dict[str, float | str]]:
    plans = [plan_topology(profile, topology) for topology in topologies]
    plans.sort(key=lambda item: (float(item["cost_pressure_score"]), float(item["fabric_latency_ns"]), str(item["topology"])))
    return plans


def sample_profile() -> ClusterProfile:
    return ClusterProfile(4096, 800.0, 1.5, 1600.0, 18.0, 2800.0)
