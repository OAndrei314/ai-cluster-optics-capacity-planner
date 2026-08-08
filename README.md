# ai-cluster-optics-capacity-planner

Maintained by: codex-daily-routine

A deterministic capacity planner for AI-cluster optical networking. It estimates east-west
bandwidth, transceiver count, optical power and rough optics spend from GPU count,
oversubscription and link-rate assumptions.

## Research + Money Thesis

AI training and inference clusters are increasingly constrained by fabric bandwidth,
optical links, power and capex. The money question is where scale-out networking becomes
the bottleneck before another GPU purchase pays off. This project gives a small,
auditable planning model for those tradeoffs.

## Quickstart

```powershell
pip install -r requirements-dev.txt
pip install -e .
python -m pytest -q
python -m cluster_optics_planner
```

## Silicon Valley Interview Hook

The `compare_topologies()` API ranks leaf-spine, rail-optimized and dragonfly-style
assumptions by optical power, capex, latency and cost pressure. That turns the repo into a
tool for the real AI-cluster question: whether the network fabric is the next bottleneck
before another GPU purchase pays off.

## Status

MVP: cluster profile, optical-link plan, power/capex estimates, topology comparison and
tests. Next steps: add topology profiles from measured rail-optimized and dragonfly-style
fabrics.

## License

MIT - see [LICENSE](LICENSE).
