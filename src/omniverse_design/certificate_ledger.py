"""O25 — append-only, content-addressed constitutional certificate ledger."""
from __future__ import annotations
from copy import deepcopy
import hashlib, json
from typing import Any, Dict
GENESIS="0"*64

def _digest(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def empty_ledger() -> Dict[str, Any]:
    return {"ledger_version":"O25.1","entries":[],"root_hash":GENESIS}

def verify_ledger(ledger: Dict[str, Any]) -> Dict[str, Any]:
    previous=GENESIS; errors=[]
    for index,entry in enumerate(ledger.get("entries",[]),start=1):
        body={k:v for k,v in entry.items() if k not in {"record_hash","root_hash"}}
        expected_record=_digest(body); expected_root=_digest({"previous_root":previous,"record_hash":expected_record})
        if entry.get("sequence")!=index: errors.append(f"sequence mismatch at {index}")
        if entry.get("previous_root")!=previous: errors.append(f"previous_root mismatch at {index}")
        if entry.get("record_hash")!=expected_record: errors.append(f"record_hash mismatch at {index}")
        if entry.get("root_hash")!=expected_root: errors.append(f"root_hash mismatch at {index}")
        previous=expected_root
    if ledger.get("root_hash")!=previous: errors.append("ledger root_hash mismatch")
    return {"verification_version":"O25.1","passed":not errors,"errors":errors,"root_hash":previous,"entry_count":len(ledger.get("entries",[]))}

def append_record(ledger: Dict[str, Any], record_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if not verify_ledger(ledger)["passed"]: raise ValueError("cannot append to invalid ledger")
    out=deepcopy(ledger); previous=out["root_hash"]
    body={"sequence":len(out["entries"])+1,"record_type":record_type,"payload":deepcopy(payload),"payload_hash":_digest(payload),"previous_root":previous}
    record_hash=_digest(body); root_hash=_digest({"previous_root":previous,"record_hash":record_hash})
    out["entries"].append({**body,"record_hash":record_hash,"root_hash":root_hash}); out["root_hash"]=root_hash; return out

def append_certificate(ledger: Dict[str, Any], *, certificate: Dict[str, Any], attestation: Dict[str, Any], independent_replay: Dict[str, Any]) -> Dict[str, Any]:
    payload={"certificate_hash":certificate["certificate_hash"],"subject_node_id":certificate["subject_node_id"],"attestation_hash":attestation["attestation_hash"],"independent_replay_hash":independent_replay["receipt_hash"],"human_promoted":bool(certificate.get("human_promoted",False)),"authority_transfer":False,"status":"ACTIVE"}
    return append_record(ledger,"CERTIFICATE",payload)
