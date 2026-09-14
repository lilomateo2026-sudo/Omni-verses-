"""O16 — deterministic replay harness for Book Seed compilation."""
from __future__ import annotations

import hashlib
from typing import Any, Dict

from .book_seed_compiler import compile_book_seed


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def replay_compilation(seed: Dict[str, Any], prior_output: Dict[str, Any]) -> Dict[str, Any]:
    replay = compile_book_seed(seed)
    source_hash_now = _sha256_text(str(seed["source_text"]))
    checks = {
        "source_hash_matches_prior": source_hash_now == prior_output["source"]["source_hash"],
        "compilation_hash_matches": replay["compilation_hash"] == prior_output["compilation_hash"],
        "node_id_matches": replay["node_id"] == prior_output["node_id"],
        "epistemic_class_matches": replay["epistemic_class"] == prior_output["epistemic_class"],
        "observer_lens_matches": replay["observer_lens"] == prior_output["observer_lens"],
    }
    return {
        "replay_version": "O16.1",
        "passed": all(checks.values()),
        "checks": checks,
        "prior_compilation_hash": prior_output["compilation_hash"],
        "replay_compilation_hash": replay["compilation_hash"],
        "replay_output": replay,
    }
