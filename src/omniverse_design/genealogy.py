"""O15 — influence genealogy graph."""
from __future__ import annotations

from typing import Any, Dict, List


def build_genealogy(seed: Dict[str, Any], node: Dict[str, Any], replay: Dict[str, Any], gate: Dict[str, Any]) -> Dict[str, Any]:
    source_id = str(seed["source_id"])
    seed_id = str(seed["seed_id"])
    node_id = str(node["node_id"])
    replay_id = f"REPLAY-{node['compilation_hash'][:16].upper()}"
    gate_id = f"GATE-{node['compilation_hash'][16:32].upper()}"

    nodes: List[Dict[str, Any]] = [
        {"id": source_id, "kind": "source", "hash": node["source"]["source_hash"]},
        {"id": seed_id, "kind": "concept_seed", "epistemic_class": node["epistemic_class"]},
        {"id": node_id, "kind": "universe_node", "hash": node["compilation_hash"]},
        {"id": replay_id, "kind": "replay", "passed": replay["passed"]},
        {"id": gate_id, "kind": "epistemic_gate", "allowed": gate["allowed"]},
    ]
    edges = [
        {"from": source_id, "to": seed_id, "relation": "extracts"},
        {"from": seed_id, "to": node_id, "relation": "compiles_to"},
        {"from": node_id, "to": replay_id, "relation": "replayed_as"},
        {"from": replay_id, "to": gate_id, "relation": "evidence_checked_by"},
    ]

    return {
        "graph_version": "O15.1",
        "root_source_id": source_id,
        "nodes": nodes,
        "edges": edges,
        "source_to_descendant_path": [source_id, seed_id, node_id, replay_id, gate_id],
        "cycles_allowed": False,
    }
