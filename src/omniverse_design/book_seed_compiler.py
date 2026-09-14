"""O13 — deterministic Book Seed -> Universe Node compiler."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Dict

EPISTEMIC_CLASSES = {
    "OBSERVED", "VERIFIED", "INFERRED", "INTERPRETED", "SPECULATIVE", "FICTIONAL"
}


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _stable_digest(payload: Dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def compile_book_seed(seed: Dict[str, Any]) -> Dict[str, Any]:
    """Compile a provenance-addressed book seed into an isolated Universe Node config.

    Required inputs are intentionally small and declarative. The compiler does not execute
    source text, shell commands, Python, or network actions.
    """
    required = ("source_id", "source_text", "seed_id", "concept_seed", "observer_lens", "epistemic_class")
    missing = [key for key in required if not seed.get(key)]
    if missing:
        raise ValueError(f"missing required seed fields: {', '.join(missing)}")

    epistemic_class = str(seed["epistemic_class"]).upper()
    if epistemic_class not in EPISTEMIC_CLASSES:
        raise ValueError(f"unsupported epistemic class: {epistemic_class}")

    source_hash = _sha256_text(str(seed["source_text"]))
    normalized = {
        "source_id": str(seed["source_id"]),
        "source_hash": source_hash,
        "seed_id": str(seed["seed_id"]),
        "concept_seed": str(seed["concept_seed"]).strip(),
        "observer_lens": str(seed["observer_lens"]).strip(),
        "epistemic_class": epistemic_class,
        "contradiction": seed.get("contradiction"),
        "mission": seed.get("mission", "translate_book_seed"),
        "environment": seed.get("environment", "isolated_design_sandbox"),
    }
    compilation_hash = _stable_digest(normalized)
    node_id = f"UNIVERSE-{compilation_hash[:16].upper()}"

    return {
        "compiler_version": "O13.1",
        "node_id": node_id,
        "node_type": "software_sandbox",
        "mission": normalized["mission"],
        "environment": normalized["environment"],
        "source": {
            "source_id": normalized["source_id"],
            "source_hash": source_hash,
            "seed_id": normalized["seed_id"],
        },
        "observer_lens": normalized["observer_lens"],
        "epistemic_class": epistemic_class,
        "concept_seed": normalized["concept_seed"],
        "contradiction": normalized["contradiction"],
        "authority_transfer": False,
        "ancestor_mutation_allowed": False,
        "execution_policy": "declarative_only",
        "compilation_hash": compilation_hash,
    }
