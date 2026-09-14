from copy import deepcopy

from omniverse_design.book_seed_compiler import compile_book_seed
from omniverse_design.constitutional_certificate import issue_certificate
from omniverse_design.epistemic_gate import evaluate_transition
from omniverse_design.genealogy import build_genealogy
from omniverse_design.packet_contracts import validate_packet
from omniverse_design.portal_registry import resolve_contract, verify_node_contract
from omniverse_design.replay_harness import replay_compilation
from omniverse_design.self_explanation import build_self_explanation
from omniverse_design.tournament import run_tournament
from omniverse_design.tribunal import run_tribunal


def base_seed(seed_id="SEED-A", concept="A book can generate a traceable design descendant"):
    return {
        "source_id": "BOOK-001",
        "source_text": "Everything the system becomes remains traceable to its source.",
        "seed_id": seed_id,
        "concept_seed": concept,
        "observer_lens": "architect",
        "epistemic_class": "INTERPRETED",
    }


def test_locked_o18_o22_chain():
    seed = base_seed()
    before = deepcopy(seed)
    node = compile_book_seed(seed)
    replay = replay_compilation(seed, node)
    gate = evaluate_transition("INTERPRETED", "INTERPRETED", {"reproduced": True, "source_intact": True})
    genealogy = build_genealogy(seed, node, replay, gate)
    explanation = build_self_explanation(seed, node, gate, replay, genealogy)

    assert before == seed
    assert validate_packet("UniverseNode", node)["valid"]

    registry = resolve_contract(node["compiler_version"])
    portal_contract = verify_node_contract(node, registry)
    assert portal_contract["passed"]

    tribunal = run_tribunal(seed, node, replay, gate, genealogy, explanation)
    assert tribunal["passed"]

    interpreted = base_seed("I", "interpretive portal")
    fictional = base_seed("F", "fictional portal")
    fictional["epistemic_class"] = "FICTIONAL"
    tournament = run_tournament([
        {"candidate_id": "fiction", "seed": fictional, "proposed_class": "VERIFIED"},
        {"candidate_id": "interpretation", "seed": interpreted},
    ])

    bad = next(row for row in tournament["ranking"] if row["candidate_id"] == "fiction")
    winner = next(row for row in tournament["ranking"] if row["candidate_id"] == tournament["winner_candidate_id"])
    assert bad["qualified"] is False
    assert tournament["winner_candidate_id"] == "interpretation"

    winner_genealogy = build_genealogy(interpreted, winner["node"], winner["replay"], winner["gate"])
    winner_explanation = build_self_explanation(interpreted, winner["node"], winner["gate"], winner["replay"], winner_genealogy)
    winner_tribunal = run_tribunal(interpreted, winner["node"], winner["replay"], winner["gate"], winner_genealogy, winner_explanation)

    certificate = issue_certificate(
        node=winner["node"],
        replay=winner["replay"],
        gate=winner["gate"],
        genealogy=winner_genealogy,
        tribunal=winner_tribunal,
        tournament=tournament,
        portal_contract=winner["portal_contract"],
    )
    assert certificate["eligible_for_human_promotion"] is True
    assert certificate["human_promoted"] is False
    assert certificate["signature_state"] == "UNSIGNED_HUMAN_PROMOTION_REQUIRED"
    assert len(certificate["certificate_hash"]) == 64
