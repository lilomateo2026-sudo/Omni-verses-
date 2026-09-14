"""O24 — process-isolated replay qualification."""
from __future__ import annotations
import hashlib, json, os, subprocess, sys
from typing import Any, Dict
from .portal_registry import verify_node_contract

def _digest(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def run_independent_replay(seed: Dict[str, Any], prior_node: Dict[str, Any], *, environment_id: str="local-process-isolation") -> Dict[str, Any]:
    request={"seed":seed,"prior_node":prior_node}; env=dict(os.environ)
    proc=subprocess.run([sys.executable,"-m","omniverse_design.replay_worker"],input=json.dumps(request,sort_keys=True),text=True,capture_output=True,env=env,check=False)
    if proc.returncode != 0:
        return {"replay_version":"O24.1","passed":False,"environment_id":environment_id,"separation_class":"PROCESS_ISOLATED_SAME_RUNTIME","error":proc.stderr.strip()}
    worker=json.loads(proc.stdout); replay=worker["replay"]; contract=verify_node_contract(replay["replay_output"])
    checks={"worker_replay_passed":replay.get("passed") is True,"node_id_matches":replay["replay_output"]["node_id"]==prior_node["node_id"],"compilation_hash_matches":replay["replay_output"]["compilation_hash"]==prior_node["compilation_hash"],"source_hash_matches":replay["replay_output"]["source"]["source_hash"]==prior_node["source"]["source_hash"],"portal_contract_valid":contract["passed"]}
    body={"replay_version":"O24.1","environment_id":environment_id,"separation_class":"PROCESS_ISOLATED_SAME_RUNTIME","environment":worker["environment"],"checks":checks,"passed":all(checks.values()),"replay_output":replay["replay_output"],"portal_contract":contract}
    body["receipt_hash"]=_digest(body); return body
