"""O28 — portable host-attestation matrix."""
import hashlib,json
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def build_host_matrix(receipts):
 rows=[]
 for r in receipts:
  rows.append({"environment_id":r["environment_id"],"environment":r["environment"],"passed":bool(r["passed"]),"receipt_hash":r["receipt_hash"],"separation_class":r["separation_class"]})
 unique=len({(x["environment"].get("python"),x["environment"].get("platform")) for x in rows})
 return {"matrix_version":"O28.1","hosts":rows,"all_passed":bool(rows) and all(x["passed"] for x in rows),"distinct_environment_fingerprints":unique,"matrix_hash":digest(rows),"claim_scope":"Measured replay environments only; no unmeasured host is implied."}
