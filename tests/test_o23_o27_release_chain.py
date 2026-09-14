import base64
import pytest
crypto=pytest.importorskip("cryptography")
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from omniverse_design.book_seed_compiler import compile_book_seed
from omniverse_design.replay_harness import replay_compilation
from omniverse_design.epistemic_gate import evaluate_transition
from omniverse_design.genealogy import build_genealogy
from omniverse_design.self_explanation import build_self_explanation
from omniverse_design.tribunal import run_tribunal
from omniverse_design.tournament import run_tournament
from omniverse_design.constitutional_certificate import issue_certificate
from omniverse_design.signing_interface import build_signing_request,build_attestation_packet,verify_attestation
from omniverse_design.independent_replay import run_independent_replay
from omniverse_design.certificate_ledger import empty_ledger,append_certificate,verify_ledger
from omniverse_design.governance_tribunal import apply_governance_action,certificate_state
from omniverse_design.release_seal import issue_release_seal

def seed(): return {"source_id":"BOOK-001","source_text":"Everything the system becomes remains traceable to its source.","seed_id":"I","concept_seed":"interpretive portal","observer_lens":"architect","epistemic_class":"INTERPRETED"}

def test_locked_o23_o27_chain():
    s=seed(); node=compile_book_seed(s); replay=replay_compilation(s,node); gate=evaluate_transition("INTERPRETED","INTERPRETED",{"reproduced":True,"source_intact":True}); genealogy=build_genealogy(s,node,replay,gate); explanation=build_self_explanation(s,node,gate,replay,genealogy); tribunal=run_tribunal(s,node,replay,gate,genealogy,explanation)
    tournament=run_tournament([{"candidate_id":"a","seed":s},{"candidate_id":"b","seed":{**s,"seed_id":"B","concept_seed":"alternate portal"}}]); portal=next(r for r in tournament["ranking"] if r["candidate_id"]==tournament["winner_candidate_id"])["portal_contract"]
    cert=issue_certificate(node=node,replay=replay,gate=gate,genealogy=genealogy,tribunal=tribunal,tournament=tournament,portal_contract=portal)
    private=Ed25519PrivateKey.generate(); public=private.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw); request=build_signing_request(cert,key_id="CI-EPHEMERAL-O23"); signature=private.sign(base64.b64decode(request["payload_b64"])); packet=build_attestation_packet(request,public_key_b64=base64.b64encode(public).decode(),signature_b64=base64.b64encode(signature).decode()); verified=verify_attestation(packet); assert verified["passed"]
    independent=run_independent_replay(s,node,environment_id="ci-process-isolation"); assert independent["passed"]
    ledger=append_certificate(empty_ledger(),certificate=cert,attestation=packet,independent_replay=independent); assert verify_ledger(ledger)["passed"]
    seal=issue_release_seal(certificate=cert,attestation_verification=verified,independent_replay=independent,ledger=ledger,portal_contract=portal); assert seal["release_state"]=="QUALIFIED_NOT_PROMOTED"
    revoked=apply_governance_action(ledger,target_certificate_hash=cert["certificate_hash"],action="REVOKE",reason="qualification-test"); assert revoked["resulting_state"]["state"]=="REVOKED"; assert len(revoked["ledger"]["entries"])==2; assert certificate_state(revoked["ledger"],cert["certificate_hash"])["state"]=="REVOKED"
    blocked=issue_release_seal(certificate=cert,attestation_verification=verified,independent_replay=independent,ledger=revoked["ledger"],portal_contract=portal); assert blocked["release_state"]=="HOLD"
