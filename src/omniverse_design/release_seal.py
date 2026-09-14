"""O27 — release-grade constitutional seal for a qualified, non-sovereign package."""
from __future__ import annotations
import hashlib, json
from typing import Any, Dict
from .certificate_ledger import verify_ledger
from .governance_tribunal import certificate_state

def _digest(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def issue_release_seal(*, certificate: Dict[str, Any], attestation_verification: Dict[str, Any], independent_replay: Dict[str, Any], ledger: Dict[str, Any], portal_contract: Dict[str, Any]) -> Dict[str, Any]:
    ledger_check=verify_ledger(ledger); state=certificate_state(ledger,certificate["certificate_hash"])
    checks={"certificate_eligible":certificate.get("eligible_for_human_promotion") is True,"attestation_verified":attestation_verification.get("passed") is True,"independent_replay_passed":independent_replay.get("passed") is True,"ledger_valid":ledger_check["passed"],"certificate_active":state.get("state")=="ACTIVE","portal_contract_valid":portal_contract.get("passed") is True,"no_authority_transfer":certificate.get("authority_transfer") is False and attestation_verification.get("authority_transfer") is False}
    root_material={"certificate_hash":certificate["certificate_hash"],"attestation_verification_hash":_digest(attestation_verification),"independent_replay_hash":independent_replay["receipt_hash"],"ledger_root_hash":ledger["root_hash"],"portal_contract_hash":portal_contract["contract_hash"],"governance_state_hash":_digest(state)}
    constitutional_root=_digest(root_material); qualified=all(checks.values()); human_promoted=bool(certificate.get("human_promoted",False))
    seal={"seal_version":"O27.1","subject_node_id":certificate["subject_node_id"],"certificate_hash":certificate["certificate_hash"],"checks":checks,"mechanically_qualified":qualified,"human_promoted":human_promoted,"release_state":"PROMOTED_RELEASE" if qualified and human_promoted else ("QUALIFIED_NOT_PROMOTED" if qualified else "HOLD"),"constitutional_root":constitutional_root,"ledger_root_hash":ledger["root_hash"],"authority_transfer":False,"human_promotion_required":not human_promoted,"scope_statement":"Seal attests recorded software evidence and governance state; it does not establish external physical or metaphysical claims."}
    seal["seal_hash"]=_digest(seal); return seal
