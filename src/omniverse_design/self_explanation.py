"""O17 — recursive self-explanation report."""
from __future__ import annotations

from typing import Any, Dict


def build_self_explanation(
    seed: Dict[str, Any],
    node: Dict[str, Any],
    gate: Dict[str, Any],
    replay: Dict[str, Any],
    genealogy: Dict[str, Any],
) -> Dict[str, Any]:
    known = [
        f"source {seed['source_id']} is preserved by SHA-256 {node['source']['source_hash']}",
        f"seed {seed['seed_id']} compiled deterministically to {node['node_id']}",
        f"replay {'passed' if replay['passed'] else 'failed'}",
        f"epistemic transition gate {'allowed' if gate['allowed'] else 'blocked'} the proposed transition",
    ]
    unknown = []
    if node["epistemic_class"] not in {"OBSERVED", "VERIFIED"}:
        unknown.append("the concept seed is not established as verified external fact")
    if not gate["allowed"]:
        unknown.extend(gate["reasons"])

    return {
        "report_version": "O17.1",
        "identity": node["node_id"],
        "what_created_me": {
            "source_id": seed["source_id"],
            "seed_id": seed["seed_id"],
            "observer_lens": node["observer_lens"],
        },
        "what_i_changed": [
            "translated prose seed into a declarative isolated Universe Node configuration"
        ],
        "what_i_influenced": [edge["to"] for edge in genealogy["edges"] if edge["from"] == node["node_id"]],
        "what_is_known": known,
        "what_remains_unknown": unknown,
        "promotion_state": "ELIGIBLE_FOR_HUMAN_REVIEW" if replay["passed"] and gate["allowed"] else "HOLD",
        "authority_statement": "This report explains recorded transformations; it does not grant the model external authority.",
    }
