"""O14 — explicit epistemic transition gate."""
from __future__ import annotations

from typing import Any, Dict

CLASSES = {"OBSERVED", "VERIFIED", "INFERRED", "INTERPRETED", "SPECULATIVE", "FICTIONAL"}


def evaluate_transition(
    current_class: str,
    proposed_class: str,
    evidence: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    current = current_class.upper()
    proposed = proposed_class.upper()
    evidence = evidence or {}
    if current not in CLASSES or proposed not in CLASSES:
        raise ValueError("unknown epistemic class")

    reproduced = bool(evidence.get("reproduced"))
    independently_confirmed = bool(evidence.get("independently_confirmed"))
    source_intact = bool(evidence.get("source_intact", True))

    reasons = []
    allowed = True

    if not source_intact:
        allowed = False
        reasons.append("source provenance is not intact")

    if proposed == "VERIFIED" and current != "VERIFIED":
        if not (reproduced or independently_confirmed):
            allowed = False
            reasons.append("VERIFIED requires reproduced or independently confirmed evidence")

    if current == "FICTIONAL" and proposed in {"OBSERVED", "VERIFIED"}:
        allowed = False
        reasons.append("fictional mechanisms cannot auto-promote into observed/verified engineering")

    if current in {"SPECULATIVE", "INTERPRETED", "INFERRED"} and proposed == "OBSERVED":
        if not evidence.get("direct_observation"):
            allowed = False
            reasons.append("OBSERVED requires a direct observation record")

    if not reasons:
        reasons.append("transition satisfies declared evidence gate")

    return {
        "current_class": current,
        "proposed_class": proposed,
        "allowed": allowed,
        "reasons": reasons,
        "evidence": {
            "reproduced": reproduced,
            "independently_confirmed": independently_confirmed,
            "direct_observation": bool(evidence.get("direct_observation")),
            "source_intact": source_intact,
        },
        "human_promotion_required": proposed == "VERIFIED",
    }
