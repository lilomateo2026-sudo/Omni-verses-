"""O21 — versioned portal contract registry."""
from __future__ import annotations
import hashlib
import json
from typing import Any, Dict

REGISTRY_VERSION = "O21.1"
DEFAULT_CONTRACT = {
    "contract_id": "BOOKSEED-PORTAL/1.0.0",
    "compiler_version": "O13.1",
    "source_packet": "BookSeed",
    "target_packet": "UniverseNode",
    "translation": "deterministic_book_seed_compilation",
    "authority_transfer": False,
    "ancestor_mutation_allowed": False,
}


def _digest(obj: Dict[str, Any]) -> str:
    encoded = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def contract_record(contract: Dict[str, Any] | None = None) -> Dict[str, Any]:
    resolved = dict(contract or DEFAULT_CONTRACT)
    return {
        "registry_version": REGISTRY_VERSION,
        "contract": resolved,
        "contract_hash": _digest(resolved),
    }


def resolve_contract(compiler_version: str) -> Dict[str, Any]:
    record = contract_record()
    if record["contract"]["compiler_version"] != compiler_version:
        raise KeyError(f"no portal contract for compiler {compiler_version}")
    return record


def verify_node_contract(node: Dict[str, Any], record: Dict[str, Any] | None = None) -> Dict[str, Any]:
    resolved = record or resolve_contract(str(node["compiler_version"]))
    contract = resolved["contract"]
    checks = {
        "compiler_version": node.get("compiler_version") == contract["compiler_version"],
        "authority_transfer": node.get("authority_transfer") is contract["authority_transfer"],
        "ancestor_mutation_allowed": node.get("ancestor_mutation_allowed") is contract["ancestor_mutation_allowed"],
    }
    return {
        "passed": all(checks.values()),
        "contract_id": contract["contract_id"],
        "contract_hash": resolved["contract_hash"],
        "checks": checks,
    }
