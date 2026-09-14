"""O23 — external Ed25519 certificate signing / verification interface.

Private keys are intentionally outside this module. The module builds canonical signing
requests and verifies externally produced signatures against public keys.
"""
from __future__ import annotations
import base64, hashlib, json
from typing import Any, Dict

DOMAIN = "OMNIVERSE-DESIGN-PATHOLOGY-O23"
ALG = "Ed25519"

def _digest(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def build_signing_request(certificate: Dict[str, Any], *, key_id: str, signer_scope: str = "EXPERIMENTAL_ATTESTATION") -> Dict[str, Any]:
    certificate_hash = str(certificate.get("certificate_hash", ""))
    if len(certificate_hash) != 64:
        raise ValueError("certificate_hash must be a SHA-256 hex digest")
    payload = f"{DOMAIN}\n{certificate_hash}\n{key_id}\n{signer_scope}".encode("utf-8")
    return {"signing_version":"O23.1","algorithm":ALG,"domain":DOMAIN,"key_id":key_id,"signer_scope":signer_scope,"certificate_hash":certificate_hash,"payload_b64":base64.b64encode(payload).decode("ascii"),"payload_sha256":hashlib.sha256(payload).hexdigest(),"human_promotion_claimed":bool(certificate.get("human_promoted",False))}

def build_attestation_packet(request: Dict[str, Any], *, public_key_b64: str, signature_b64: str) -> Dict[str, Any]:
    if request.get("algorithm") != ALG:
        raise ValueError("unsupported signing algorithm")
    packet={"attestation_version":"O23.1","algorithm":ALG,"key_id":request["key_id"],"signer_scope":request["signer_scope"],"certificate_hash":request["certificate_hash"],"payload_b64":request["payload_b64"],"payload_sha256":request["payload_sha256"],"public_key_b64":public_key_b64,"signature_b64":signature_b64,"human_promotion_claimed":bool(request.get("human_promotion_claimed",False))}
    packet["attestation_hash"]=_digest(packet)
    return packet

def verify_attestation(packet: Dict[str, Any]) -> Dict[str, Any]:
    checks={"algorithm_supported":packet.get("algorithm")==ALG,"payload_hash_matches":False,"signature_valid":False}; error=None
    try:
        payload=base64.b64decode(packet["payload_b64"],validate=True)
        checks["payload_hash_matches"]=hashlib.sha256(payload).hexdigest()==packet.get("payload_sha256")
        pub=base64.b64decode(packet["public_key_b64"],validate=True); sig=base64.b64decode(packet["signature_b64"],validate=True)
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        Ed25519PublicKey.from_public_bytes(pub).verify(sig,payload); checks["signature_valid"]=True
    except Exception as exc:
        error=f"{type(exc).__name__}: {exc}"
    return {"verification_version":"O23.1","passed":all(checks.values()),"checks":checks,"certificate_hash":packet.get("certificate_hash"),"key_id":packet.get("key_id"),"signer_scope":packet.get("signer_scope"),"error":error,"authority_transfer":False}
