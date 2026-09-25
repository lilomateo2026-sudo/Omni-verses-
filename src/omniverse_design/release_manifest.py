"""O31 — reproducible release-candidate manifest."""
import hashlib,json
def build_release_manifest(*,commit_sha,certificate,seal,host_matrix,genealogy,promotion,portal_contract,ci_runs):
 body={"manifest_version":"O31.1","commit_sha":commit_sha,"certificate_hash":certificate["certificate_hash"],"constitutional_root":seal["constitutional_root"],"seal_hash":seal["seal_hash"],"host_matrix_hash":host_matrix["matrix_hash"],"genealogy_passed":genealogy["passed"],"promotion_state":promotion["state"],"portal_contract_hash":portal_contract["contract_hash"],"ci_runs":ci_runs,"tag_name":"omniverse-design-pathology-o31-rc1","tag_state":"DECLARED_NOT_CREATED_BY_MODULE","release_state":"RELEASE_CANDIDATE_NOT_PROMOTED","authority_transfer":False}
 body["manifest_hash"]=hashlib.sha256(json.dumps(body,sort_keys=True,separators=(",",":")).encode()).hexdigest(); return body
