import json
from pathlib import Path


EVIDENCE = Path("evidence/GITHUB_APP_INTEGRATION_O21_2.json")


def load_evidence():
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def test_o21_2_write_probe_is_qualified():
    evidence = load_evidence()
    probe = evidence["probe"]

    assert evidence["status"] == "PASS"
    assert evidence["authorization"]["installed_repository_visible"] is True
    assert evidence["authorization"]["permissions"]["pull"] is True
    assert evidence["authorization"]["permissions"]["push"] is True
    assert probe["readback_exact_match"] is True
    assert probe["net_tree_change_after_cleanup"] is False
    assert probe["main_modified_by_probe"] is False
    assert probe["base_tree_sha"] == probe["cleanup_tree_sha"]


def test_o21_2_invariants_are_all_true():
    evidence = load_evidence()
    assert evidence["invariants"]
    assert all(evidence["invariants"].values())


def test_o21_3_is_the_only_declared_next_stage():
    evidence = load_evidence()
    assert evidence["next_stage"] == "O21.3_REPO_READY_INTEGRATION_PATCH"
