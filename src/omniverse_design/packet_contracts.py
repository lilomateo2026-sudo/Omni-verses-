"""O18 — dependency-free typed packet validation for portal artifacts."""
from __future__ import annotations
from typing import Any, Dict, Iterable

PACKET_REQUIRED = {
    "BookSeed": ("source_id", "source_text", "seed_id", "concept_seed", "observer_lens", "epistemic_class"),
    "UniverseNode": ("compiler_version", "node_id", "source", "observer_lens", "epistemic_class", "compilation_hash", "authority_transfer", "ancestor_mutation_allowed"),
    "ReplayReceipt": ("replay_version", "passed", "checks", "prior_compilation_hash", "replay_compilation_hash"),
    "EpistemicDecision": ("current_class", "proposed_class", "allowed", "reasons", "evidence", "human_promotion_required"),
    "GenealogyGraph": ("graph_version", "root_source_id", "nodes", "edges", "source_to_descendant_path"),
    "SelfExplanation": ("report_version", "identity", "what_created_me", "what_i_changed", "what_i_influenced", "what_is_known", "what_remains_unknown", "promotion_state", "authority_statement"),
}


def validate_packet(packet_type: str, packet: Dict[str, Any]) -> Dict[str, Any]:
    if packet_type not in PACKET_REQUIRED:
        raise ValueError(f"unknown packet type: {packet_type}")
    if not isinstance(packet, dict):
        return {"valid": False, "packet_type": packet_type, "errors": ["packet must be an object"]}
    errors = []
    for key in PACKET_REQUIRED[packet_type]:
        if key not in packet:
            errors.append(f"missing required field: {key}")
    if packet_type == "UniverseNode":
        if packet.get("authority_transfer") is not False:
            errors.append("authority_transfer must be false")
        if packet.get("ancestor_mutation_allowed") is not False:
            errors.append("ancestor_mutation_allowed must be false")
        source = packet.get("source")
        if not isinstance(source, dict) or not all(k in source for k in ("source_id", "source_hash", "seed_id")):
            errors.append("source must include source_id, source_hash, seed_id")
    if packet_type == "ReplayReceipt" and packet.get("passed") is not True:
        errors.append("replay receipt must pass for qualification")
    return {"valid": not errors, "packet_type": packet_type, "errors": errors}


def validate_many(pairs: Iterable[tuple[str, Dict[str, Any]]]) -> Dict[str, Any]:
    results = [validate_packet(packet_type, packet) for packet_type, packet in pairs]
    return {"valid": all(result["valid"] for result in results), "results": results}
