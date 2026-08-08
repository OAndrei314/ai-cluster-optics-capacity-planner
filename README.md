# ai-cluster-optics-capacity-planner

Maintained by: codex-daily-routine

A deterministic capacity planner for AI-cluster optical networking. It estimates east-west
bandwidth, transceiver count, optical power and rough optics spend from GPU count,
oversubscription and link-rate assumptions.

## Quickstart

```powershell
pip install -r requirements-dev.txt
pip install -e .
python -m pytest -q
python -m cluster_optics_planner
```

## Status

MVP: cluster profile, optical-link plan, power/capex estimates, topology comparison and
tests. Next steps: add topology profiles from measured rail-optimized and dragonfly-style
fabrics.

## License

MIT - see [LICENSE](LICENSE).
