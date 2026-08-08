import pytest

from cluster_optics_planner import ClusterProfile, plan_optics


def test_optics_plan_scales_with_gpu_count():
    small = plan_optics(ClusterProfile(512, 800.0, 1.5, 1600.0, 18.0, 2800.0))
    large = plan_optics(ClusterProfile(4096, 800.0, 1.5, 1600.0, 18.0, 2800.0))

    assert large["required_tbps"] > small["required_tbps"]
    assert large["transceiver_count"] > small["transceiver_count"]
    assert large["capex_per_gpu_usd"] > 0


def test_invalid_cluster_rejected():
    with pytest.raises(ValueError):
        plan_optics(ClusterProfile(0, 800.0, 1.5, 1600.0, 18.0, 2800.0))
