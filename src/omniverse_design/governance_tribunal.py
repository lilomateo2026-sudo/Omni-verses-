"""O26 — revocation / supersession tribunal without historical deletion."""
from __future__ import annotations
import hashlib, json
from typing import Any, Dict
from .certificate_ledger import append_record, verify_ledger
ACTIONS={"REVOKE","SUPERSEDE"}

def _digest(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def certificate_state(ledger: Dict[str, Any], certificate_hash: str) -> Dict[str, Any]:
    if not verify_ledger(ledger)["passed"]: return {"found":False,"state":"LEDGER_INVALID"}
    found=False; state=None; superseded_by=None
    for entry in ledger["entries"]:
        p=entry["payload"]
        if entry["record_type"]=="CERTIFICATE" and p.get("certificate_hash")==certificate_hash: found=True; state="ACTIVE"
        if entry["record_type"]=="GOVERNANCE" and p.get("target_certificate_hash")==certificate_hash:
            if p["action"]=="REVOKE": state="REVOKED"
            elif p["action"]=="SUPERSEDE": state="SUPERSEDED"; superseded_by=p.get("superseding_certificate_hash")
    return {"found":found,"state":state if found else "NOT_FOUND","superseded_by":superseded_by}

def apply_governance_action(ledger: Dict[str, Any], *, target_certificate_hash: str, action: str, reason: str, superseding_certificate_hash: str|None=None) -> Dict[str, Any]:
    action=action.upper()
    if action not in ACTIONS: raise ValueError("unsupported governance action")
    current=certificate_state(ledger,target_certificate_hash)
    if not current["found"]: raise KeyError("target certificate not found")
    if current["state"]!="ACTIVE": raise ValueError(f"target certificate is not ACTIVE: {current['state']}")
    if action=="SUPERSEDE" and not superseding_certificate_hash: raise ValueError("superseding_certificate_hash required")
    event={"governance_version":"O26.1","target_certificate_hash":target_certificate_hash,"action":action,"reason":reason,"superseding_certificate_hash":superseding_certificate_hash,"human_authorization_required":True,"authority_transfer":False}
    event["event_hash"]=_digest(event); updated=append_record(ledger,"GOVERNANCE",event)
    return {"decision_version":"O26.1","action":action,"event":event,"ledger":updated,"resulting_state":certificate_state(updated,target_certificate_hash)}
