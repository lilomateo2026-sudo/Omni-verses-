"""O29 — human promotion request/verification boundary."""
def promotion_request(certificate_hash, constitutional_root):
 return {"promotion_version":"O29.1","certificate_hash":certificate_hash,"constitutional_root":constitutional_root,"required_signer_scope":"AUTHORIZED_HUMAN_PROMOTION","state":"AWAITING_AUTHORIZED_HUMAN_SIGNATURE","authority_transfer":False}
def evaluate_promotion(request, verification):
 ok=bool(verification and verification.get("passed") and verification.get("signer_scope")=="AUTHORIZED_HUMAN_PROMOTION" and verification.get("certificate_hash")==request["certificate_hash"])
 return {"promotion_version":"O29.1","promoted":ok,"state":"HUMAN_PROMOTED" if ok else "AWAITING_AUTHORIZED_HUMAN_SIGNATURE","authority_transfer":False}
