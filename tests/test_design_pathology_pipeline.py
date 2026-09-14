import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from omniverse_design import (
    build_genealogy,
    build_self_explanation,
    compile_book_seed,
    evaluate_transition,
    replay_compilation,
)


def sample_seed():
    return {
        "source_id": "BOOK-OMNIVERSE-001",
        "source_text": "Everything the system becomes must remain traceable to what it observed.",
        "seed_id": "SEED-TRACEABILITY-001",
        "concept_seed": "Preserve source lineage across every descendant.",
        "observer_lens": "architect",
        "epistemic_class": "INTERPRETED",
        "mission": "book_seed_to_universe_node",
        "environment": "isolated_design_sandbox",
    }


def test_locked_order_o13_o14_o16_o15_o17():
    seed = sample_seed()
    original = copy.deepcopy(seed)

    node = compile_book_seed(seed)
    assert seed == original
    assert node["ancestor_mutation_allowed"] is False
    assert node["authority_transfer"] is False

    blocked_gate = evaluate_transition("INTERPRETED", "VERIFIED", {"source_intact": True})
    assert blocked_gate["allowed"] is False

    gate = evaluate_transition(
        "INTERPRETED",
        "VERIFIED",
        {"source_intact": True, "reproduced": True},
    )
    assert gate["allowed"] is True
    assert gate["human_promotion_required"] is True

    replay = replay_compilation(seed, node)
    assert replay["passed"] is True

    genealogy = build_genealogy(seed, node, replay, gate)
    assert genealogy["source_to_descendant_path"][0] == seed["source_id"]
    assert genealogy["source_to_descendant_path"][2] == node["node_id"]

    report = build_self_explanation(seed, node, gate, replay, genealogy)
    assert report["promotion_state"] == "ELIGIBLE_FOR_HUMAN_REVIEW"
    assert "external authority" in report["authority_statement"]


def test_fiction_cannot_auto_promote_to_verified():
    result = evaluate_transition(
        "FICTIONAL", "VERIFIED", {"source_intact": True, "reproduced": True}
    )
    assert result["allowed"] is False
