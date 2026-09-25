"""O22 — content-addressed constitutional certificate manifest."""
from __future__ import annotations
import hashlib
import json
from typing import Any, Dict


def _digest(obj: Any) -> str:
    encoded = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def issue_certificate(
    *,
    node: Dict[str, Any],
    replay: Dict[str, Any],
    gate: Dict[str, Any],
    genealogy: Dict[str, Any],
    tribunal: Dict[str, Any],
    tournament: Dict[str, Any],
    portal_contract: Dict[str, Any],
    human_promoted: bool = False,
    signature: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    eligible = bool(
        replay.get("passed")
        and tribunal.get("passed")
        and portal_contract.get("passed")
        and tournament.get("winner_candidate_id")
    )
    body = {
        "certificate_version": "O22.1",
        "subject_node_id": node["node_id"],
        "source_hash": node["source"]["source_hash"],
        "compilation_hash": node["compilation_hash"],
        "compiler_version": node["compiler_version"],
        "replay_hash": _digest(replay),
        "epistemic_decision_hash": _digest(gate),
        "genealogy_root_hash": _digest(genealogy),
        "tribunal_hash": _digest(tribunal),
        "tournament_hash": _digest(tournament),
        "portal_contract_hash": portal_contract["contract_hash"],
        "eligible_for_human_promotion": eligible,
        "human_promoted": bool(human_promoted),
        "authority_transfer": False,
    }
    body["certificate_hash"] = _digest(body)
    if signature:
        body["signature"] = signature
        body["signature_state"] = "EXTERNALLY_SUPPLIED_UNVERIFIED_BY_THIS_MODULE"
    else:
        body["signature"] = None
        body["signature_state"] = "UNSIGNED_HUMAN_PROMOTION_REQUIRED"
    return body
