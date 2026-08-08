import pytest

from cluster_optics_planner import ClusterProfile, TopologyProfile, compare_topologies, plan_optics, plan_topology


def test_optics_plan_scales_with_gpu_count():
    small = plan_optics(ClusterProfile(512, 800.0, 1.5, 1600.0, 18.0, 2800.0))
    large = plan_optics(ClusterProfile(4096, 800.0, 1.5, 1600.0, 18.0, 2800.0))

    assert large["required_tbps"] > small["required_tbps"]
    assert large["transceiver_count"] > small["transceiver_count"]
    assert large["capex_per_gpu_usd"] > 0


def test_invalid_cluster_rejected():
    with pytest.raises(ValueError):
        plan_optics(ClusterProfile(0, 800.0, 1.5, 1600.0, 18.0, 2800.0))


def test_compare_topologies_returns_ranked_tradeoffs():
    profile = ClusterProfile(4096, 800.0, 1.5, 1600.0, 18.0, 2800.0)
    plans = compare_topologies(profile)

    assert len(plans) >= 3
    assert plans[0]["cost_pressure_score"] <= plans[-1]["cost_pressure_score"]
    assert "fabric_latency_ns" in plans[0]


def test_invalid_topology_rejected():
    profile = ClusterProfile(512, 800.0, 1.5, 1600.0, 18.0, 2800.0)

    with pytest.raises(ValueError):
        plan_topology(profile, TopologyProfile("bad", 0.0, 1.0, 2, 100.0))
