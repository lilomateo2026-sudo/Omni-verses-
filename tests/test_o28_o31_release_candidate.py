import json
from pathlib import Path
from omniverse_design.host_attestation_matrix import build_host_matrix
from omniverse_design.genealogy_reconstruction import reconstruct
from omniverse_design.human_promotion import promotion_request,evaluate_promotion
from omniverse_design.release_manifest import build_release_manifest

def test_o28_o31_locked_chain():
 e=json.loads(Path("evidence/O23_O27_FIRST_RELEASE_SEAL.json").read_text())
 replay=e["independent_replay"]
 matrix=build_host_matrix([replay])
 assert matrix["all_passed"] and matrix["distinct_environment_fingerprints"]==1
 g=reconstruct(e["certificate"]["certificate_hash"],certificate=e["certificate"],attestation=e["attestation"],replay=replay,ledger=e["ledger"],seal=e["release_seal"])
 assert g["passed"]
 req=promotion_request(e["certificate"]["certificate_hash"],e["release_seal"]["constitutional_root"])
 p=evaluate_promotion(req,None)
 assert not p["promoted"] and p["state"]=="AWAITING_AUTHORIZED_HUMAN_SIGNATURE"
 m=build_release_manifest(commit_sha="TEST_HEAD",certificate=e["certificate"],seal=e["release_seal"],host_matrix=matrix,genealogy=g,promotion=p,portal_contract=replay["portal_contract"],ci_runs=["Design Pathology Tribunal","Python package"])
 assert m["release_state"]=="RELEASE_CANDIDATE_NOT_PROMOTED"
