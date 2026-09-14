"""O19 — reproducibility and constitutional invariant tribunal."""
from __future__ import annotations
from typing import Any, Dict
from .packet_contracts import validate_many
from .portal_registry import verify_node_contract


def run_tribunal(
    seed: Dict[str, Any],
    node: Dict[str, Any],
    replay: Dict[str, Any],
    gate: Dict[str, Any],
    genealogy: Dict[str, Any],
    explanation: Dict[str, Any],
) -> Dict[str, Any]:
    packets = validate_many((
        ("BookSeed", seed),
        ("UniverseNode", node),
        ("ReplayReceipt", replay),
        ("EpistemicDecision", gate),
        ("GenealogyGraph", genealogy),
        ("SelfExplanation", explanation),
    ))
    contract = verify_node_contract(node)
    invariants = {
        "packets_valid": packets["valid"],
        "replay_passed": replay.get("passed") is True,
        "source_hash_stable": node.get("source", {}).get("source_hash") == replay.get("replay_output", {}).get("source", {}).get("source_hash"),
        "no_authority_transfer": node.get("authority_transfer") is False,
        "no_ancestor_mutation": node.get("ancestor_mutation_allowed") is False,
        "portal_contract_valid": contract["passed"],
    }
    return {
        "tribunal_version": "O19.1",
        "passed": all(invariants.values()),
        "invariants": invariants,
        "packet_validation": packets,
        "portal_contract": contract,
    }
