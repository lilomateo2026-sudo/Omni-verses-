"""O20 — deterministic multi-seed descendant qualification tournament."""
from __future__ import annotations
from copy import deepcopy
from typing import Any, Dict, List
from .book_seed_compiler import compile_book_seed
from .replay_harness import replay_compilation
from .epistemic_gate import evaluate_transition
from .portal_registry import verify_node_contract


def _candidate(candidate: Dict[str, Any]) -> Dict[str, Any]:
    seed = deepcopy(candidate["seed"])
    before = deepcopy(seed)
    node = compile_book_seed(seed)
    replay = replay_compilation(seed, node)
    proposed = str(candidate.get("proposed_class", node["epistemic_class"]))
    gate = evaluate_transition(
        node["epistemic_class"],
        proposed,
        {
            "reproduced": replay["passed"],
            "source_intact": before == seed,
            "direct_observation": bool(candidate.get("direct_observation", False)),
            "independently_confirmed": bool(candidate.get("independently_confirmed", False)),
        },
    )
    contract = verify_node_contract(node)
    checks = {
        "input_immutable": before == seed,
        "replay_passed": replay["passed"],
        "gate_allowed": gate["allowed"],
        "contract_passed": contract["passed"],
        "no_authority_transfer": node["authority_transfer"] is False,
        "no_ancestor_mutation": node["ancestor_mutation_allowed"] is False,
    }
    score = sum(1 for value in checks.values() if value) * 100 // len(checks)
    return {
        "candidate_id": str(candidate["candidate_id"]),
        "score": score,
        "qualified": all(checks.values()),
        "checks": checks,
        "node": node,
        "replay": replay,
        "gate": gate,
        "portal_contract": contract,
    }


def run_tournament(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    if len(candidates) < 2:
        raise ValueError("tournament requires at least two candidates")
    rows = [_candidate(candidate) for candidate in candidates]
    rows.sort(key=lambda row: (-row["score"], row["node"]["compilation_hash"], row["candidate_id"]))
    winner = next((row for row in rows if row["qualified"]), None)
    return {
        "tournament_version": "O20.1",
        "ranking": [{"rank": index + 1, **row} for index, row in enumerate(rows)],
        "winner_candidate_id": winner["candidate_id"] if winner else None,
        "promotion_requires_human": True,
    }
